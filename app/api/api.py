from fastapi import APIRouter
from app.api.restaurant import router as restaurant_router
from app.api.user import router as user_router
from app.api.item import router as item_router
from app.api.menu import router as menu_router
from app.api.order import router as order_router

api_router = APIRouter()
api_router.include_router(router=restaurant_router, prefix="/restaurants", tags=["Restaurants"])
api_router.include_router(router=user_router, prefix="/users", tags=["Users"])
api_router.include_router(router=item_router, prefix="/items", tags=["Items"])
api_router.include_router(router=menu_router, prefix="/menus", tags=["Menus"])
api_router.include_router(router=order_router, prefix="/orders", tags=["Orders"])