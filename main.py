import os
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import User, UserCreate, Note, NoteCreate
from auth import get_current_user
from database import get_db, engine, Base
import crud
import db_models

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
    uvicorn.run(app, host="0.0.0.0", port=port)
