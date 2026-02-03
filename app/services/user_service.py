from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import User
from fastapi import HTTPException

class UserService:
    
    def get_user_data(id: UUID, session: Session):
        user = session.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return user

    def delete_account(id: UUID, session: Session):
        user = session.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        session.delete(user)
        session.commit()
        return {"message": "Usuário deletado com sucesso"}
