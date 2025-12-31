from sqlalchemy import Column, ForeignKey, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False, index=True)


class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    note = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
