from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from uuid import UUID
from src.schemas.product import CategorySchema, CategoryCreate
from src.services.category_service import CategoryService
from src.unit_of_work.sql_uow import SqlUnitOfWork
from src.database import SessionLocal

router = APIRouter()

def get_category_service():
    uow = SqlUnitOfWork(SessionLocal)
    return CategoryService(uow)

@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return service.create_category(category_in.dict())

@router.get("/{id}", response_model=CategorySchema)
def get_category(id: UUID, service: CategoryService = Depends(get_category_service)):
    category = service.get_category(str(id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[CategorySchema])
def list_categories(skip: int = 0, limit: int = 100, service: CategoryService = Depends(get_category_service)):
    return service.get_all_categories(skip, limit)

@router.put("/{id}", response_model=CategorySchema)
def update_category(id: UUID, category_in: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    category = service.update_category(str(id), category_in.dict())
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: UUID, service: CategoryService = Depends(get_category_service)):
    if not service.delete_category(str(id)):
        raise HTTPException(status_code=404, detail="Category not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
