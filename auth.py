from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

import crud
from database import get_db


def get_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="no authorization header included")

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "ApiKey":
        raise HTTPException(status_code=401, detail="malformed authorization header")

    return parts[1]


def get_current_user(
    api_key: str = Depends(get_api_key), db: Session = Depends(get_db)
):
    user = crud.get_user_by_api_key(db, api_key)
    if not user:
        raise HTTPException(status_code=404, detail="Couldn't get user")
    return user
