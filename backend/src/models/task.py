"""
SQLModel database models and Pydantic schemas for Task entities.

This module defines:
- Task: SQLModel table for storing todo items
- TaskCreate: Schema for creating new tasks
- TaskUpdate: Schema for updating existing tasks
- TaskResponse: Schema for task API responses
- TaskListResponse: Schema for task list responses
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from pydantic import Field
from sqlmodel import Field as SQLField, SQLModel, Relationship


class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecurringPattern(str, Enum):
    """Recurring task patterns."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Tag(SQLModel, table=True):
    """Tag model for task categorization."""
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    user_id: UUID = SQLField(nullable=False)
    name: str = SQLField(max_length=50, nullable=False)
    color: str = SQLField(max_length=7, default="#3B82F6")  # Hex color
    created_at: datetime = SQLField(default_factory=datetime.utcnow)


class TaskTag(SQLModel, table=True):
    """Many-to-many relationship between tasks and tags."""
    task_id: UUID = SQLField(foreign_key="task.id", primary_key=True)
    tag_id: UUID = SQLField(foreign_key="tag.id", primary_key=True)


class Task(SQLModel, table=True):
    """
    SQLModel table representing a todo task owned by a user.

    Attributes:
        id: Unique identifier (UUID primary key)
        user_id: Foreign key to the owning user (managed by Better Auth)
        title: Task title (required, 1-500 characters)
        description: Optional task details (max 5000 characters)
        completed: Completion status (default False)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified

    Relationships:
        user: Many-to-one relationship with User (for FK reference)

    Note:
        - The User table is managed by Better Auth on the frontend
        - user_id is a required foreign key for data isolation
        - All queries must filter by user_id for user-specific data
    """

    id: UUID = SQLField(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique task identifier",
    )

    user_id: UUID = SQLField(
        nullable=False,
        description="Foreign key to the owning user",
    )

    title: str = SQLField(
        min_length=1,
        max_length=500,
        nullable=False,
        description="Task title (required, 1-500 characters)",
    )

    description: Optional[str] = SQLField(
        default=None,
        max_length=5000,
        nullable=True,
        description="Optional task details (max 5000 characters)",
    )

    completed: bool = SQLField(
        default=False,
        nullable=False,
        description="Completion status",
    )

    created_at: datetime = SQLField(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp",
    )

    updated_at: datetime = SQLField(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last modification timestamp",
    )

    # Advanced features
    priority: Priority = SQLField(
        default=Priority.MEDIUM,
        nullable=False,
        description="Task priority level",
    )

    due_date: Optional[datetime] = SQLField(
        default=None,
        nullable=True,
        description="Task due date with timezone",
    )

    recurring_pattern: Optional[RecurringPattern] = SQLField(
        default=None,
        nullable=True,
        description="Recurring pattern if task repeats",
    )

    recurring_interval: Optional[int] = SQLField(
        default=None,
        nullable=True,
        description="Interval for recurring pattern (e.g., every 2 weeks)",
    )

    next_due_date: Optional[datetime] = SQLField(
        default=None,
        nullable=True,
        description="Next occurrence for recurring tasks",
    )

    reminder_minutes: Optional[int] = SQLField(
        default=None,
        nullable=True,
        description="Minutes before due date to send reminder",
    )

    # Relationships (commented out for now - will add after migration)
    # tags: List[Tag] = Relationship(
    #     back_populates="tasks",
    #     link_model=TaskTag,
    # )

    class Config:
        from_attributes = True


class TaskCreate(SQLModel):
    """
    Pydantic schema for creating a new task.

    Attributes:
        title: Task title (required, 1-500 characters)
        description: Optional task details (max 5000 characters)
        priority: Task priority level
        due_date: Optional due date
        recurring_pattern: Optional recurring pattern
        recurring_interval: Interval for recurring tasks
        reminder_minutes: Minutes before due date for reminder
        tag_ids: List of tag IDs to associate with task
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title (required, 1-500 characters)",
        examples=["Buy groceries"],
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional task details",
        examples=["Milk, eggs, bread"],
    )

    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Task priority level",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Task due date",
    )

    recurring_pattern: Optional[RecurringPattern] = Field(
        default=None,
        description="Recurring pattern",
    )

    recurring_interval: Optional[int] = Field(
        default=1,
        ge=1,
        description="Interval for recurring pattern",
    )

    reminder_minutes: Optional[int] = Field(
        default=None,
        ge=0,
        description="Minutes before due date for reminder",
    )

    tag_ids: List[UUID] = Field(
        default_factory=list,
        description="List of tag IDs",
    )


class TaskUpdate(SQLModel):
    """
    Pydantic schema for updating an existing task.

    All fields are optional - only provided fields will be updated.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Task title",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task details",
    )

    completed: Optional[bool] = Field(
        default=None,
        description="Completion status",
    )

    priority: Optional[Priority] = Field(
        default=None,
        description="Task priority",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Task due date",
    )

    recurring_pattern: Optional[RecurringPattern] = Field(
        default=None,
        description="Recurring pattern",
    )

    recurring_interval: Optional[int] = Field(
        default=None,
        ge=1,
        description="Recurring interval",
    )

    reminder_minutes: Optional[int] = Field(
        default=None,
        ge=0,
        description="Reminder minutes",
    )

    tag_ids: Optional[List[UUID]] = Field(
        default=None,
        description="Tag IDs",
    )


class TaskResponse(SQLModel):
    """
    Pydantic schema for task API responses.

    This schema is used for serializing Task data in API responses.
    All datetime fields are converted to ISO 8601 string format.
    """

    id: str = Field(..., description="Task UUID")
    user_id: str = Field(..., description="Owning user UUID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(default=None, description="Task details")
    completed: bool = Field(..., description="Completion status")
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: str = Field(..., description="Modification timestamp (ISO 8601)")
    
    # Advanced fields
    priority: str = Field(..., description="Task priority")
    due_date: Optional[str] = Field(default=None, description="Due date (ISO 8601)")
    recurring_pattern: Optional[str] = Field(default=None, description="Recurring pattern")
    recurring_interval: Optional[int] = Field(default=None, description="Recurring interval")
    next_due_date: Optional[str] = Field(default=None, description="Next due date (ISO 8601)")
    reminder_minutes: Optional[int] = Field(default=None, description="Reminder minutes")

    @classmethod
    def from_orm(cls, task: Task) -> "TaskResponse":
        """
        Convert a Task SQLModel instance to TaskResponse.

        Args:
            task: SQLModel Task instance

        Returns:
            TaskResponse instance with string UUIDs and formatted timestamps
        """
        return cls(
            id=str(task.id),
            user_id=str(task.user_id),
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            priority=task.priority.value,
            due_date=task.due_date.isoformat() if task.due_date else None,
            recurring_pattern=task.recurring_pattern.value if task.recurring_pattern else None,
            recurring_interval=task.recurring_interval,
            next_due_date=task.next_due_date.isoformat() if task.next_due_date else None,
            reminder_minutes=task.reminder_minutes,
        )


class TaskListResponse(SQLModel):
    """
    Pydantic schema for the task list API response.

    Attributes:
        tasks: List of TaskResponse objects
        total: Total number of tasks in the list
    """

    tasks: list[TaskResponse] = Field(default_factory=list, description="List of tasks")
    total: int = Field(..., description="Total number of tasks")