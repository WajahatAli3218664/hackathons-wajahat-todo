"""
Recurring Task Service - Microservice for handling recurring task creation.
Consumes task completion events and creates next occurrences.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Recurring Task Service", version="1.0.0")

class RecurringTaskService:
    """Service for handling recurring task logic."""
    
    def __init__(self):
        self.consumer = None
        self.running = False
    
    async def start(self):
        """Start the recurring task service."""
        try:
            self.consumer = AIOKafkaConsumer(
                'task-events',
                bootstrap_servers='localhost:9092',
                group_id='recurring-service',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            await self.consumer.start()
            self.running = True
            logger.info("Recurring task service started")
            
            asyncio.create_task(self.consume_messages())
            
        except Exception as e:
            logger.error(f"Failed to start recurring service: {e}")
    
    async def stop(self):
        """Stop the recurring task service."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
        logger.info("Recurring task service stopped")
    
    async def consume_messages(self):
        """Consume task events from Kafka."""
        try:
            async for message in self.consumer:
                await self.process_task_event(message.value)
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
    
    async def process_task_event(self, event_data: Dict[str, Any]):
        """Process a task event."""
        try:
            event_type = event_data.get('event_type')
            task_data = event_data.get('task_data', {})
            
            if event_type == 'completed' and task_data.get('recurring_pattern'):
                await self.create_next_occurrence(task_data)
                
        except Exception as e:
            logger.error(f"Error processing task event: {e}")
    
    async def create_next_occurrence(self, task_data: Dict[str, Any]):
        """Create next occurrence of a recurring task."""
        try:
            pattern = task_data.get('recurring_pattern')
            interval = task_data.get('recurring_interval', 1)
            
            logger.info(f"Creating next occurrence for recurring task: {task_data.get('title')}")
            logger.info(f"Pattern: {pattern}, Interval: {interval}")
            
            # Calculate next due date
            next_due = self.calculate_next_due_date(pattern, interval)
            
            # In real implementation, would create new task via API call
            logger.info(f"📅 RECURRING: Next occurrence due at {next_due}")
            
        except Exception as e:
            logger.error(f"Error creating next occurrence: {e}")
    
    def calculate_next_due_date(self, pattern: str, interval: int) -> datetime:
        """Calculate next due date based on pattern."""
        now = datetime.utcnow()
        
        if pattern == 'daily':
            return now + timedelta(days=interval)
        elif pattern == 'weekly':
            return now + timedelta(weeks=interval)
        elif pattern == 'monthly':
            return now + timedelta(days=30 * interval)
        else:
            return now + timedelta(days=1)

# Global service instance
recurring_service = RecurringTaskService()

@app.on_event("startup")
async def startup():
    await recurring_service.start()

@app.on_event("shutdown")
async def shutdown():
    await recurring_service.stop()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "recurring"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)