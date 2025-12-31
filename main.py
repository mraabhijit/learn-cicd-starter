import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import crud
import db_models
from auth import get_current_user
from database import Base, engine, get_db
from models import Note, NoteCreate, User, UserCreate

# Create tables in the database
# In a real app, you'd use migrations (like Alembic),
# but for this conversion, we'll create them if they don't exist.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Health check
@app.get("/v1/healthz")
def healthz():
    return {"status": "ok"}


# User routes
@app.post("/v1/users", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user_in.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/v1/users", response_model=User)
def get_user(current_user: db_models.User = Depends(get_current_user)):
    return current_user


# Note routes
@app.post("/v1/notes", response_model=Note)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user),
):
    try:
        return crud.create_note(db, note_in.note, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/v1/notes", response_model=list[Note])
def get_notes(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user),
):
    return crud.get_notes_for_user(db, current_user.id)


# Static files and fallback to index.html
@app.get("/")
def read_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="index.html not found")


# Serve other static files if needed
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    # ignore the binding error
    localhost = os.getenv("LOCALHOST", "0.0.0.0") # noqa: S104
    uvicorn.run(app, host=localhost, port=port)
