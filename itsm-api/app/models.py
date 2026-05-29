from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base
import enum


class Priority(str, enum.Enum):
    P1_CRITICAL = "P1 - Critical"
    P2_HIGH = "P2 - High"
    P3_MODERATE = "P3 - Moderate"
    P4_LOW = "P4 - Low"


class IncidentState(str, enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class ChangeType(str, enum.Enum):
    STANDARD = "Standard"
    NORMAL = "Normal"
    EMERGENCY = "Emergency"


class ChangeState(str, enum.Enum):
    DRAFT = "Draft"
    ASSESS = "Assess"
    AUTHORIZE = "Authorize"
    SCHEDULED = "Scheduled"
    IMPLEMENT = "Implement"
    REVIEW = "Review"
    CLOSED = "Closed"


class Incident(Base):
    """Mirrors the incident [incident] table in ServiceNow."""
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)        # e.g. INC0001234
    short_description = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    caller_id = Column(String, nullable=False)
    assigned_to = Column(String, nullable=True)
    assignment_group = Column(String, nullable=True)
    priority = Column(String, default=Priority.P3_MODERATE)
    state = Column(String, default=IncidentState.NEW)
    category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    opened_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)


class ChangeRequest(Base):
    """Mirrors the change_request [change_request] table in ServiceNow."""
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)        # e.g. CHG0001234
    short_description = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    requested_by = Column(String, nullable=False)
    assigned_to = Column(String, nullable=True)
    change_type = Column(String, default=ChangeType.NORMAL)
    state = Column(String, default=ChangeState.DRAFT)
    risk = Column(String, nullable=True)
    impact = Column(String, nullable=True)
    planned_start = Column(DateTime, nullable=True)
    planned_end = Column(DateTime, nullable=True)
    implementation_plan = Column(Text, nullable=True)
    backout_plan = Column(Text, nullable=True)
    opened_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    