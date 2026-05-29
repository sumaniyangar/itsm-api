from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .models import Priority, IncidentState, ChangeType, ChangeState


class IncidentCreate(BaseModel):
    short_description: str = Field(..., example="Application is down for all users")
    description: Optional[str] = None
    caller_id: str = Field(..., example="john.doe@company.com")
    assignment_group: Optional[str] = None
    priority: Priority = Priority.P3_MODERATE
    category: Optional[str] = None
    subcategory: Optional[str] = None


class IncidentUpdate(BaseModel):
    short_description: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    assignment_group: Optional[str] = None
    priority: Optional[Priority] = None
    state: Optional[IncidentState] = None
    resolution_notes: Optional[str] = None


class IncidentResponse(BaseModel):
    id: int
    number: str
    short_description: str
    description: Optional[str]
    caller_id: str
    assigned_to: Optional[str]
    assignment_group: Optional[str]
    priority: str
    state: str
    category: Optional[str]
    subcategory: Optional[str]
    resolution_notes: Optional[str]
    opened_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ChangeCreate(BaseModel):
    short_description: str = Field(..., example="Upgrade database to PostgreSQL 16")
    description: Optional[str] = None
    requested_by: str = Field(..., example="suman.m@company.com")
    change_type: ChangeType = ChangeType.NORMAL
    risk: Optional[str] = None
    impact: Optional[str] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    implementation_plan: Optional[str] = None
    backout_plan: Optional[str] = None


class ChangeUpdate(BaseModel):
    short_description: Optional[str] = None
    assigned_to: Optional[str] = None
    state: Optional[ChangeState] = None
    risk: Optional[str] = None
    impact: Optional[str] = None
    implementation_plan: Optional[str] = None
    backout_plan: Optional[str] = None


class ChangeResponse(BaseModel):
    id: int
    number: str
    short_description: str
    description: Optional[str]
    requested_by: str
    assigned_to: Optional[str]
    change_type: str
    state: str
    risk: Optional[str]
    impact: Optional[str]
    planned_start: Optional[datetime]
    planned_end: Optional[datetime]
    implementation_plan: Optional[str]
    backout_plan: Optional[str]
    opened_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        