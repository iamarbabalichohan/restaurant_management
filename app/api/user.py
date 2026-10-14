from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import user as user_schemas
from app.db import get_async_db
from app.models.users import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_user(user_data: user_schemas.CreateUser, db: AsyncSession = Depends(get_async_db)):
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user already exists")
    await db.refresh(new_user)
    return new_user