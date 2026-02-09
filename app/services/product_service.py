from uuid import UUID, uuid4
from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.core.vars import UPLOAD_DIR
from app.schemas.product_schemas import UpdateProductSchema
import os
import shutil

class ProductService:
    def get_product(slug: str, session: Session):
        product = session.query(Product).filter(Product.slug==slug).first()

        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return product

    def get_products_by_category(category_slug: str, session: Session):
        products = (
            session.query(Product)
            .join(Category, Product.category_id == Category.id)
            .filter(Category.slug == category_slug)
            .filter(Product.is_active == True)
            .all()
        )
        return products

    def create_product(name: str,
                        slug: str,
                        description: str,
                        price: float,
                        category_id: UUID,
                        image: UploadFile,
                        session: Session):
        if not name:
            raise HTTPException(status_code=400, detail="Nome do produto inválido")
        if not slug:
            raise HTTPException(status_code=400, detail="Novo slug do produto inválido")
        if not description:
            raise HTTPException(status_code=400, detail="Descrição do produto inválida")
        if not category_id:
            raise HTTPException(status_code=400, detail="Categoria do produto inválida")
        if price <= 0:
            raise HTTPException(status_code=400, detail="Preço do produto precisa ser maior que 0")
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem")
        
        exist_product = session.query(Product).filter(Product.slug == slug).first()
        if exist_product:
            raise HTTPException()
        
        exist_category = session.query(Category).filter(Category.id == category_id).first()

        if not exist_category:
            raise HTTPException(status_code=400, detail="Categoria do produto não encontrada")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        ext = image.filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)


        try:
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            product = Product(name, slug, description, price, category_id, filename)
            session.add(product)
            session.commit()
            return product
        except Exception as e:
            print(e)
            session.rollback()
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=500, detail="Erro do servidor")
        


    def update_product(slug: str, 
                        body: UpdateProductSchema,
                        session: Session):
        if not body.name:
            raise HTTPException(status_code=400, detail="Nome do produto inválido")
        if not body.slug:
            raise HTTPException(status_code=400, detail="Novo slug do produto inválido")
        if not body.description:
            raise HTTPException(status_code=400, detail="Descrição do produto inválida")
        if not body.category_id:
            raise HTTPException(status_code=400, detail="Categoria do produto inválida")
        if body.price <= 0:
            raise HTTPException(status_code=400, detail="Preço do produto precisa ser maior que 0")
        
        product = session.query(Product).filter(Product.slug == slug).first()

        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        exist_category = session.query(Category).filter(Category.id == body.category_id).first()

        if not exist_category:
            raise HTTPException(status_code=400, detail="Nova categoria do produto não encontrada")
        
        exist_product = session.query(Product).filter(Product.slug == body.slug).first()

        if exist_product and exist_product.id != product.id:
            raise HTTPException(status_code=400, detail="Já existe produto cadastrado com o novo slug") 

        product.slug = body.slug
        product.name = body.name
        product.price = body.price
        product.description = body.description
        product.category_id = body.category_id

        session.commit()
        return product

    def update_product_image(slug: str,
                            image: UploadFile,
                            session: Session):
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem")
    
        product = session.query(Product).filter(Product.slug==slug).first()
        if not product:
            raise HTTPException(status_code=400, detail="Produto não encontrado")
        
        try:
            filepath = os.path.join(UPLOAD_DIR, product.image_url)
            if os.path.exists(filepath):
                os.remove(filepath)

            ext = image.filename.split(".")[-1]
            filename = f"{uuid4()}.{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
                
            product.image_url = filename
            session.commit()
            return product
        except Exception as e:
            session.rollback()
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=500, detail="Erro do servidor")

    def deactivate_product(slug: str, session: Session):
        product = session.query(Product).filter(Product.slug==slug).first()

        if not product:
            raise HTTPException(status_code=404, detail="Falha ao desativar. Produto não encontrado")
        
        product.is_active = False
        session.commit()

    def activate_product(slug: str, session: Session):
        product = session.query(Product).filter(Product.slug==slug).first()

        if not product:
            raise HTTPException(status_code=404, detail="Falha ao ativar. Produto não encontrado")
        
        product.is_active = True
        session.commit()