from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_async_db
from app.models import DeliveryAddress, Item, Menu, Order, OrderItem, Restaurant
from app.schemas import order as order_schemas

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: order_schemas.CreateOrder,
    db: AsyncSession = Depends(get_async_db),
):
    restaurant = await db.get(Restaurant, order_data.restaurant_id)
    if restaurant is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Restaurant not found")


    wanted: dict[int, int] = defaultdict(int)
    for _item in order_data.items:
        wanted[_item.item_id] += _item.quantity

    stmt = (
        select(Item)
        .join(Menu, Item.menu_id == Menu.menu_id)
        .where(
            Menu.restaurant_id == order_data.restaurant_id,
            Item.item_id.in_(wanted.keys()),
        )
        .order_by(Item.item_id)
        .with_for_update()
    )
    items = {i.item_id: i for i in (await db.execute(stmt)).scalars()}

    missing = set(wanted) - items.keys()
    if missing:
        await db.rollback()
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Items not found for this restaurant: {sorted(missing)}",
        )

    new_order = Order(
        restaurant_id=order_data.restaurant_id,
        payment_method=order_data.payment_method,
    )

    for item_id, qty in wanted.items():
        item = items[item_id]
        if qty > item.quantity:
            await db.rollback()
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Not enough stock for '{item.name}': "
                f"requested {qty}, available {item.quantity}",
            )
        item.quantity -= qty
        new_order.order_items.append(OrderItem(item=item, quantity=qty))

    new_order.delivery_address = DeliveryAddress(
        latitude=order_data.delivery_address.latitude,
        longitude=order_data.delivery_address.longitude,
    )
    
    db.add(new_order)
    try:
        await db.flush()
        order_id = new_order.order_id
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Could not create the order",
        )
    except Exception:
        await db.rollback()
        raise

    result = await db.execute(
        select(Order)
        .where(Order.order_id == order_id)
        .options(
            selectinload(Order.order_items).selectinload(OrderItem.item),
            selectinload(Order.delivery_address),
        )
        .execution_options(populate_existing=True)
    )
    return result.scalar_one()