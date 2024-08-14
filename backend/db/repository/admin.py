from fastapi import Request, Depends, status, HTTPException
from db.repository.login import get_user_by_email
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from db.session import get_db
from core.config import settings
from jose import jwt, JWTError


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})
    
    scheme, token = get_authorization_scheme_param(token)
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Invalid authentication scheme", headers={"Location": "/login"})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})

    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})
    return user


def is_admin(user_id: int) -> bool:
    return user_id == 1