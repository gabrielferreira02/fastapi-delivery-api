from sqlalchemy.orm import Session
from app.schemas.auth_schemas import RegisterSchema, LoginSchema, AuthResponseSchema
from fastapi import HTTPException
from app.models.user import User
from app.main import bcrypt_context
from datetime import timedelta, datetime, timezone
from app.core.vars import JWT_EXPIRATION_TIME, SECRET_KEY, ALGORITHM
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm


class AuthService:

    @staticmethod
    def generate_token(user_id, duration=timedelta(minutes=int(JWT_EXPIRATION_TIME))):
        expiration_date = datetime.now(timezone.utc) + duration
        dic_info = {"sub": str(user_id), "exp": expiration_date}
        token = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
        return token
    
    @staticmethod
    def register(body: RegisterSchema, session: Session):
        if not body.first_name:
            raise HTTPException(status_code=400, detail="Campo nome vazio ou inválido")
        if not body.last_name:
            raise HTTPException(status_code=400, detail="Campo sobrenome vazio ou inválido")
        if not body.email:
            raise HTTPException(status_code=400, detail="Campo email vazio ou inválido")
        if len(body.password) < 8:
            raise HTTPException(status_code=400, detail="Campo senha precisa conter 8 ou mais caracteres")
        
        hashed_password = bcrypt_context.hash(body.password)
        user = User(body.first_name, body.last_name, body.email, hashed_password)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def login(body: LoginSchema, session: Session):
        if not body.email:
            raise HTTPException(status_code=400, detail="Campo email vazio")
        if not body.password:
            raise HTTPException(status_code=400, detail="Campo senha vazio")
        
        user = session.query(User).filter(User.email == body.email).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if not bcrypt_context.verify(body.password, user.password):
            raise HTTPException(status_code=400, detail="Email ou senha incorretos")
        
        token = AuthService.generate_token(user.id)
        refresh_token = AuthService.generate_token(user.id, timedelta(days=7))

        return AuthResponseSchema(token, refresh_token)

    @staticmethod
    def refresh_token(user: User):
        token = AuthService.generate_token(user.id)
        refresh_token = AuthService.generate_token(user.id, timedelta(days=7))

        return AuthResponseSchema(token, refresh_token)
    
    def login_docs(body: OAuth2PasswordRequestForm, session: Session):
        user = session.query(User).filter(User.email == body.username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if not bcrypt_context.verify(body.password, user.password):
            raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    
        token = AuthService.generate_token(user.id)
        refresh_token = AuthService.generate_token(user.id, timedelta(days=7))

        return AuthResponseSchema(token, refresh_token)
