from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_async_db
from app.schemas import menu as menu_schemas
from app.models import Menu, Restaurant

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_menu(menu_data: menu_schemas.CreateMenu, db: AsyncSession = Depends(get_async_db)):
    restaurant = await db.get(Restaurant, menu_data.restaurant_id)
        
    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    new_menu = Menu(**menu_data.model_dump())
    db.add(new_menu)
    
    try:
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create the menu")
    
    await db.refresh(new_menu)
    return new_menu