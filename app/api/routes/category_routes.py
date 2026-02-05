from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session
from app.api.deps import get_session
from app.schemas.category_schemas import UpdateCategoryNameAndSlugSchema, CategoryResponseSchema
from app.services.category_service import CategoryService

category_router = APIRouter(prefix="/category", tags=["Category"])

@category_router.get("/all", response_model=list[CategoryResponseSchema])
async def get_all_categories(session: Session = Depends(get_session)):
    return CategoryService.get_all_categories(session)

@category_router.post("", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(name: str, 
                          slug: str,
                          image: UploadFile, 
                          session: Session = Depends(get_session)):
    return CategoryService.create_category(name, slug, image, session)

@category_router.get("/{slug}", response_model=CategoryResponseSchema)
async def get_category(slug: str, session: Session = Depends(get_session)):
    return CategoryService.get_category(slug, session)

@category_router.put("/{slug}", response_model=CategoryResponseSchema)
async def update_category(slug: str, body: UpdateCategoryNameAndSlugSchema, session: Session = Depends(get_session)):
    return CategoryService.update_category(slug, body, session)

@category_router.patch("/{slug}", response_model=CategoryResponseSchema)
async def update_category_image(slug: str, image: UploadFile,session: Session = Depends(get_session)):
    return CategoryService.update_category_image(slug, image, session)

@category_router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(slug: str, session: Session = Depends(get_session)):
    return CategoryService.delete_category(slug, session)
