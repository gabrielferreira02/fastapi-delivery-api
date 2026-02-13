from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category_schemas import UpdateCategoryNameAndSlugSchema
from fastapi import UploadFile, HTTPException
from app.core.vars import UPLOAD_DIR
from app.models.user import User
import os
import shutil

class CategoryService:
    def get_all_categories(session: Session):
        categories = session.query(Category).all()
        return categories
    
    def get_category(slug: str, session: Session):
        category = session.query(Category).filter(Category.slug==slug).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return category

    def create_category(name: str, 
                          slug: str,
                          image: UploadFile,
                          session: Session,
                          auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="Não autenticado")
        if auth_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Apenas admins podem realizar essa operação")
        if not name:
            raise HTTPException(status_code=400, detail="Nome do produto inválido")
        if not slug:
            raise HTTPException(status_code=400, detail="Slug do produto inválido")
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem")
    
        exist_category = session.query(Category).filter(Category.slug==slug).first()
        if exist_category:
            raise HTTPException(status_code=400, detail="Slug já existente")
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        ext = image.filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)


        try:
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            category = Category(name, slug, filename)
            session.add(category)
            session.commit()
            return category
        except Exception as e:
            session.rollback()
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=500, detail="Erro do servidor")

    def update_category(slug: str,
                        body: UpdateCategoryNameAndSlugSchema, 
                        session: Session,
                        auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="Não autenticado")
        if auth_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Apenas admins podem realizar essa operação")      
        if not body.name:
            raise HTTPException(status_code=400, detail="Nome da categoria inválido")
        if not body.slug:
            raise HTTPException(status_code=400, detail="Slug da categoria inválido")
        
        category = session.query(Category).filter(Category.slug==slug).first()

        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        category.name = body.name
        category.slug = body.slug
        session.commit()
        return category

    def update_category_image(slug: str, image: UploadFile, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="Não autenticado")
        if auth_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Apenas admins podem realizar essa operação")
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem")
    
        category = session.query(Category).filter(Category.slug==slug).first()
        if not category:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")
        

        try:
            filepath = os.path.join(UPLOAD_DIR, category.image_url)
            if os.path.exists(filepath):
                os.remove(filepath)

            ext = image.filename.split(".")[-1]
            filename = f"{uuid4()}.{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
                
            category.image_url = filename
            session.commit()
            return category
        except Exception as e:
            session.rollback()
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=500, detail="Erro do servidor")

    def delete_category(slug: str, session: Session, auth_user: User):
        if not auth_user:
            raise HTTPException(status_code=401, detail="Não autenticado")
        if auth_user.is_admin == False:
            raise HTTPException(status_code=403, detail="Apenas admins podem realizar essa operação")
        
        category = session.query(Category).filter(Category.slug==slug).first()
        if not category:
            raise HTTPException(status_code=404, detail="Falha ao deletar. Categoria não encontrada")
    
        try:
            filepath = os.path.join(UPLOAD_DIR, category.image_url)

            session.delete(category)
            session.commit()

            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            session.rollback()
            raise HTTPException(status_code=500, detail="Erro do servidor")