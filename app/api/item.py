from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_async_db
from app.schemas import item as item_schemas
from app.models import Item, Menu

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_item(item_data: item_schemas.CreateItem, db: AsyncSession = Depends(get_async_db)):
    menu = await db.get(Menu, item_data.menu_id)
        
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    new_item = Item(**item_data.model_dump())
    db.add(new_item)
    
    try:
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not create the item")
    
    await db.refresh(new_item)
    return new_item