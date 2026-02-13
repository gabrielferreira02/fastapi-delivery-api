from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import User
from fastapi import HTTPException

class UserService:
    
    def get_user_data(id: UUID, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        user = session.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if auth_user.id != id:
            raise HTTPException(status_code=403, detail="Acesso negado. Não pode acessar informações de outro usuário")
        
        return user

    def delete_account(id: UUID, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        user = session.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if auth_user.id != id:
            raise HTTPException(status_code=403, detail="Operação não autorizada")
        
        session.delete(user)
        session.commit()
        return {"message": "Usuário deletado com sucesso"}
