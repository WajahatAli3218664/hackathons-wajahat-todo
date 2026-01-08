import os
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Environment setup
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if DATABASE_URL.startswith("sqlite://"):
    DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Models
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    user_id: UUID = SQLField(nullable=False)
    title: str = SQLField(min_length=1, max_length=500, nullable=False)
    description: Optional[str] = SQLField(default=None, max_length=5000)
    completed: bool = SQLField(default=False)
    priority: Priority = SQLField(default=Priority.MEDIUM)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)
    priority: Priority = Field(default=Priority.MEDIUM)

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    created_at: str
    updated_at: str

    @classmethod
    def from_orm(cls, task: Task):
        return cls(
            id=str(task.id),
            user_id=str(task.user_id),
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority.value,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
        )

# Database dependency
async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Auth dependency (simplified)
async def get_current_user() -> UUID:
    # For demo purposes, return a fixed user ID
    return UUID("9a6a3993-91a6-41fe-9644-6e7089c0928c")

# FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Routes
@app.get("/")
def read_root():
    return {"message": "Todo API is running on Vercel!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/health")
def api_health():
    return {"status": "ok", "service": "todo-api"}

@app.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks(
    current_user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).where(Task.user_id == current_user_id))
    tasks = result.scalars().all()
    return [TaskResponse.from_orm(task) for task in tasks]

@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )
    
    task = Task(
        user_id=current_user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        priority=task_data.priority,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskResponse.from_orm(task)

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    return TaskResponse.from_orm(task)

@app.patch("/api/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: UUID,
    request: Request,
    current_user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    body = await request.json()
    completed = body.get("completed")
    
    if completed is None or not isinstance(completed, bool):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'completed' field is required and must be a boolean"
        )
    
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    task.completed = completed
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return TaskResponse.from_orm(task)

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    await db.delete(task)
    await db.commit()