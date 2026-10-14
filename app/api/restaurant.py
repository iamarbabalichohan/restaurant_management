from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import restaurant as restaurant_schemas
from app.db import get_async_db
from app.models import Restaurant, User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_restaurant(restaurant_data: restaurant_schemas.CreateRestaurant, db: AsyncSession = Depends(get_async_db)):
    admin = await db.get(User, restaurant_data.admin_id)
    
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    new_restaurant = Restaurant(name=restaurant_data.name, admin_id=restaurant_data.admin_id)
    db.add(new_restaurant)
    
    try:
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create the restaurant")
    
    await db.refresh(new_restaurant)
    return restaurant_data