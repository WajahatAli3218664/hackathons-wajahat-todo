"""
Event system using Kafka for Phase V event-driven architecture.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio

logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Will be updated for real deployment
KAFKA_TOPICS = {
    "task_events": "task-events",
    "reminders": "reminders", 
    "task_updates": "task-updates"
}

class EventPublisher:
    """Kafka event publisher for task events."""
    
    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        
    async def start(self):
        """Start the Kafka producer."""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
            )
            await self.producer.start()
            logger.info("Kafka producer started")
        except Exception as e:
            logger.warning(f"Kafka producer failed to start: {e}")
            self.producer = None
    
    async def stop(self):
        """Stop the Kafka producer."""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")
    
    async def publish_task_event(self, event_type: str, task_data: Dict[str, Any], user_id: UUID):
        """Publish a task event to Kafka."""
        if not self.producer:
            logger.warning("Kafka producer not available, skipping event")
            return
            
        event = {
            "event_type": event_type,
            "task_id": task_data.get("id"),
            "task_data": task_data,
            "user_id": str(user_id),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            await self.producer.send(KAFKA_TOPICS["task_events"], event)
            logger.info(f"Published task event: {event_type} for task {task_data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to publish task event: {e}")
    
    async def publish_reminder_event(self, task_data: Dict[str, Any], user_id: UUID):
        """Publish a reminder event to Kafka."""
        if not self.producer or not task_data.get("due_date"):
            return
            
        event = {
            "task_id": task_data.get("id"),
            "title": task_data.get("title"),
            "due_at": task_data.get("due_date"),
            "remind_at": task_data.get("due_date"),  # For now, same as due date
            "user_id": str(user_id),
            "notification_type": "email"
        }
        
        try:
            await self.producer.send(KAFKA_TOPICS["reminders"], event)
            logger.info(f"Published reminder event for task {task_data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to publish reminder event: {e}")

# Global event publisher instance
event_publisher = EventPublisher()

async def startup_events():
    """Startup event handler for FastAPI."""
    await event_publisher.start()

async def shutdown_events():
    """Shutdown event handler for FastAPI."""
    await event_publisher.stop()