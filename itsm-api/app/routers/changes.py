from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import ChangeRequest
from ..schemas import ChangeCreate, ChangeUpdate, ChangeResponse

router = APIRouter(prefix="/api/v1/changes", tags=["Change Requests"])


def generate_change_number(db: Session) -> str:
    count = db.query(ChangeRequest).count()
    return f"CHG{str(count + 1).zfill(7)}"


@router.post("/", response_model=ChangeResponse, status_code=status.HTTP_201_CREATED)
def create_change(change_data: ChangeCreate, db: Session = Depends(get_db)):
    new_change = ChangeRequest(number=generate_change_number(db), **change_data.model_dump())
    db.add(new_change)
    db.commit()
    db.refresh(new_change)
    return new_change


@router.get("/", response_model=List[ChangeResponse])
def list_changes(state: str = None, change_type: str = None, db: Session = Depends(get_db)):
    query = db.query(ChangeRequest)
    if state:
        query = query.filter(ChangeRequest.state == state)
    if change_type:
        query = query.filter(ChangeRequest.change_type == change_type)
    return query.all()


@router.get("/{change_number}", response_model=ChangeResponse)
def get_change(change_number: str, db: Session = Depends(get_db)):
    change = db.query(ChangeRequest).filter(ChangeRequest.number == change_number).first()
    if not change:
        raise HTTPException(status_code=404, detail=f"Change {change_number} not found")
    return change


@router.patch("/{change_number}", response_model=ChangeResponse)
def update_change(change_number: str, updates: ChangeUpdate, db: Session = Depends(get_db)):
    change = db.query(ChangeRequest).filter(ChangeRequest.number == change_number).first()
    if not change:
        raise HTTPException(status_code=404, detail=f"Change {change_number} not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(change, field, value)
    change.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(change)
    return change