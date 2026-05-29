from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import Incident, IncidentState
from ..schemas import IncidentCreate, IncidentUpdate, IncidentResponse

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])


def generate_incident_number(db: Session) -> str:
    """Auto-generates INC number — mirrors ServiceNow's auto-number feature."""
    count = db.query(Incident).count()
    return f"INC{str(count + 1).zfill(7)}"


@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(incident_data: IncidentCreate, db: Session = Depends(get_db)):
    """Open a new incident. Auto-assigns an INC number."""
    new_incident = Incident(
        number=generate_incident_number(db),
        **incident_data.model_dump()
    )
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident


@router.get("/", response_model=List[IncidentResponse])
def list_incidents(state: str = None, priority: str = None, db: Session = Depends(get_db)):
    """List all incidents. Filter by state or priority like a ServiceNow list view."""
    query = db.query(Incident)
    if state:
        query = query.filter(Incident.state == state)
    if priority:
        query = query.filter(Incident.priority == priority)
    return query.all()


@router.get("/{incident_number}", response_model=IncidentResponse)
def get_incident(incident_number: str, db: Session = Depends(get_db)):
    """Fetch a single incident by INC number."""
    incident = db.query(Incident).filter(Incident.number == incident_number).first()
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident {incident_number} not found")
    return incident


@router.patch("/{incident_number}", response_model=IncidentResponse)
def update_incident(incident_number: str, updates: IncidentUpdate, db: Session = Depends(get_db)):
    """
    Update an incident. Automatically sets resolved_at and closed_at timestamps
    based on state changes — this mirrors a ServiceNow Business Rule.
    """
    incident = db.query(Incident).filter(Incident.number == incident_number).first()
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident {incident_number} not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)

    # Business Rule logic: auto-stamp timestamps on state transitions
    if updates.state == IncidentState.RESOLVED and not incident.resolved_at:
        incident.resolved_at = datetime.utcnow()
    if updates.state == IncidentState.CLOSED and not incident.closed_at:
        incident.closed_at = datetime.utcnow()

    incident.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(incident)
    return incident
