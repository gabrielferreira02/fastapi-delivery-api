from sqlalchemy.orm import Session, sessionmaker
from app.models.base import db
from app.models.user import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.vars import SECRET_KEY, ALGORITHM
from app.core.security import oauth2_schema
from uuid import UUID

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = UUID(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado")
    
    user = session.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return user
        