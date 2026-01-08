"""
Notification Service - Microservice for handling task reminders and notifications.
Consumes events from Kafka and sends notifications.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="1.0.0")

class NotificationService:
    """Service for handling notifications and reminders."""
    
    def __init__(self):
        self.consumer = None
        self.running = False
    
    async def start(self):
        """Start the notification service."""
        try:
            self.consumer = AIOKafkaConsumer(
                'reminders',
                bootstrap_servers='localhost:9092',
                group_id='notification-service',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            await self.consumer.start()
            self.running = True
            logger.info("Notification service started")
            
            # Start consuming messages
            asyncio.create_task(self.consume_messages())
            
        except Exception as e:
            logger.error(f"Failed to start notification service: {e}")
    
    async def stop(self):
        """Stop the notification service."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
        logger.info("Notification service stopped")
    
    async def consume_messages(self):
        """Consume reminder messages from Kafka."""
        try:
            async for message in self.consumer:
                await self.process_reminder(message.value)
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
    
    async def process_reminder(self, reminder_data: Dict[str, Any]):
        """Process a reminder event."""
        try:
            task_id = reminder_data.get('task_id')
            title = reminder_data.get('title')
            user_id = reminder_data.get('user_id')
            due_at = reminder_data.get('due_at')
            
            logger.info(f"Processing reminder for task {task_id}: {title}")
            
            await self.send_notification(user_id, title, due_at)
            
        except Exception as e:
            logger.error(f"Error processing reminder: {e}")
    
    async def send_notification(self, user_id: str, title: str, due_at: str):
        """Send notification to user."""
        logger.info(f"📧 NOTIFICATION: User {user_id} - Task '{title}' is due at {due_at}")

# Global service instance
notification_service = NotificationService()

@app.on_event("startup")
async def startup():
    await notification_service.start()

@app.on_event("shutdown") 
async def shutdown():
    await notification_service.stop()

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "notification"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)