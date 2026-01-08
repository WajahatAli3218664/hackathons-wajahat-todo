"""
Database migration for Phase V advanced features.

Adds:
- priority, due_date, recurring fields to tasks
- tags table
- task_tags junction table
"""

from sqlalchemy import text
from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/todoapp?sslmode=require")

def migrate_database():
    """Run migration to add advanced features."""
    # Convert asyncpg URL to sync for migration
    sync_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url)
    
    with engine.connect() as conn:
        # Add new columns to tasks table
        migrations = [
            # Add priority column
            """
            ALTER TABLE task 
            ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium' NOT NULL
            """,
            
            # Add due_date column
            """
            ALTER TABLE task 
            ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE
            """,
            
            # Add recurring columns
            """
            ALTER TABLE task 
            ADD COLUMN IF NOT EXISTS recurring_pattern VARCHAR(10)
            """,
            
            """
            ALTER TABLE task 
            ADD COLUMN IF NOT EXISTS recurring_interval INTEGER
            """,
            
            """
            ALTER TABLE task 
            ADD COLUMN IF NOT EXISTS next_due_date TIMESTAMP WITH TIME ZONE
            """,
            
            # Add reminder column
            """
            ALTER TABLE task 
            ADD COLUMN IF NOT EXISTS reminder_minutes INTEGER
            """,
            
            # Create tags table
            """
            CREATE TABLE IF NOT EXISTS tag (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL,
                name VARCHAR(50) NOT NULL,
                color VARCHAR(7) DEFAULT '#3B82F6',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """,
            
            # Create task_tags junction table
            """
            CREATE TABLE IF NOT EXISTS tasktag (
                task_id UUID REFERENCES task(id) ON DELETE CASCADE,
                tag_id UUID REFERENCES tag(id) ON DELETE CASCADE,
                PRIMARY KEY (task_id, tag_id)
            )
            """,
            
            # Add indexes for performance
            """
            CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority)
            """,
            
            """
            CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date)
            """,
            
            """
            CREATE INDEX IF NOT EXISTS idx_task_user_priority ON task(user_id, priority)
            """,
            
            """
            CREATE INDEX IF NOT EXISTS idx_tag_user ON tag(user_id)
            """,
        ]
        
        for migration in migrations:
            try:
                conn.execute(text(migration))
                print(f"✅ Executed: {migration.strip()[:50]}...")
            except Exception as e:
                print(f"❌ Failed: {migration.strip()[:50]}... - {e}")
        
        conn.commit()
        print("🚀 Migration completed!")

if __name__ == "__main__":
    migrate_database()