import os
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
import db_models


def create_user(db: Session, name: str):
    user_id = str(uuid.uuid4())
    api_key = os.urandom(32).hex()
    now = datetime.utcnow().isoformat()

    db_user = db_models.User(
        id=user_id, created_at=now, updated_at=now, name=name, api_key=api_key
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_api_key(db: Session, api_key: str):
    return db.query(db_models.User).filter(db_models.User.api_key == api_key).first()


def create_note(db: Session, note: str, user_id: str):
    note_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    db_note = db_models.Note(
        id=note_id, created_at=now, updated_at=now, note=note, user_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes_for_user(db: Session, user_id: str):
    return db.query(db_models.Note).filter(db_models.Note.user_id == user_id).all()
