from fastapi import APIRouter, Depends, UploadFile, status, Form, File
from sqlalchemy.orm import Session
from app.api.deps import get_session, verify_token
from uuid import UUID
from app.schemas.product_schemas import ProductResponseSchema, UpdateProductSchema
from app.services.product_service import ProductService
from app.models.user import User

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.get("/{slug}", response_model=ProductResponseSchema)
async def get_product(slug: str, session: Session = Depends(get_session)):
    return ProductService.get_product(slug, session)

@product_router.get("/category/{category_slug}", response_model=list[ProductResponseSchema])
async def get_products_by_category(category_slug: str, session: Session = Depends(get_session)):
    return ProductService.get_products_by_category(category_slug, session)

@product_router.post("", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_product(name: str = Form(...),
                         slug: str = Form(...),
                         description: str = Form(...),
                         price: float = Form(...),
                         category_id: UUID = Form(...),
                         image: UploadFile = File(...),
                         session: Session = Depends(get_session),
                         user: User = Depends(verify_token)):
    return ProductService.create_product(name, slug, description, price, category_id, image, session, user)

@product_router.put("/{slug}", response_model=ProductResponseSchema)
async def update_product(slug: str, 
                         body: UpdateProductSchema,
                         session: Session = Depends(get_session),
                         user: User = Depends(verify_token)):
    return ProductService.update_product(slug, body, session, user)

@product_router.patch("/{slug}", response_model=ProductResponseSchema)
async def update_product_image(slug: str,
                               image: UploadFile,
                               session: Session = Depends(get_session),
                               user: User = Depends(verify_token)):
    return ProductService.update_product_image(slug, image, session, user)

@product_router.delete("/{slug}/deactivate")
async def deactivate_product(slug: str, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    ProductService.deactivate_product(slug, session, user)

@product_router.patch("/{slug}/activate")
async def deactivate_product(slug: str, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    ProductService.activate_product(slug, session, user)