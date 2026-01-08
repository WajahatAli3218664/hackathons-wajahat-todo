"""
Tag models and schemas for task categorization.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field
from sqlmodel import Field as SQLField, SQLModel


class TagCreate(SQLModel):
    """Schema for creating a new tag."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Tag name",
    )
    
    color: str = Field(
        default="#3B82F6",
        regex=r"^#[0-9A-Fa-f]{6}$",
        description="Hex color code",
    )


class TagUpdate(SQLModel):
    """Schema for updating a tag."""
    
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Tag name",
    )
    
    color: Optional[str] = Field(
        default=None,
        regex=r"^#[0-9A-Fa-f]{6}$",
        description="Hex color code",
    )


class TagResponse(SQLModel):
    """Schema for tag API responses."""
    
    id: str = Field(..., description="Tag UUID")
    user_id: str = Field(..., description="Owner UUID")
    name: str = Field(..., description="Tag name")
    color: str = Field(..., description="Hex color")
    created_at: str = Field(..., description="Creation timestamp")
    
    @classmethod
    def from_orm(cls, tag) -> "TagResponse":
        """Convert Tag to TagResponse."""
        return cls(
            id=str(tag.id),
            user_id=str(tag.user_id),
            name=tag.name,
            color=tag.color,
            created_at=tag.created_at.isoformat(),
        )