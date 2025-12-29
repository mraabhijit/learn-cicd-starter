from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: str
    updated_at: str
    name: str
    api_key: str


class UserCreate(BaseModel):
    name: str


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: str
    updated_at: str
    note: str
    user_id: str


class NoteCreate(BaseModel):
    note: str
