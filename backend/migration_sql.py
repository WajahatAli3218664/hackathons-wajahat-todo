"""
Simple migration script to add advanced features to existing database.
This will be run through the existing backend API.
"""

# For now, let's update the models and let SQLModel handle the schema changes
# We'll create the migration SQL and apply it manually if needed

MIGRATION_SQL = """
-- Add advanced features to tasks table
ALTER TABLE task ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurring_pattern VARCHAR(10);
ALTER TABLE task ADD COLUMN IF NOT EXISTS recurring_interval INTEGER;
ALTER TABLE task ADD COLUMN IF NOT EXISTS next_due_date TIMESTAMP WITH TIME ZONE;
ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_minutes INTEGER;

-- Create tags table
CREATE TABLE IF NOT EXISTS tag (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#3B82F6',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create task_tags junction table
CREATE TABLE IF NOT EXISTS tasktag (
    task_id UUID REFERENCES task(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_task_user_priority ON task(user_id, priority);
CREATE INDEX IF NOT EXISTS idx_tag_user ON tag(user_id);
"""

print("Migration SQL ready:")
print(MIGRATION_SQL)
print("\nApply this SQL to your database manually or through your database admin tool.")