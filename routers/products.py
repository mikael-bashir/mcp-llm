# routers/products_router.py
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text
from typing import List

from config import get_session
from schema import Product, ProductPublic

router = APIRouter(prefix="/api/products/v2", tags=["Products"])

@router.get(
    "/get-all", response_model=List[ProductPublic],
    summary="Get All Products in store",
    description="""
    This endpoint returns an array of product objects, each containing details like
    id, name, description, price, and current stock level.
    """,
    response_description="A JSON array of all products in the store."
)
async def get_products(session: AsyncSession = Depends(get_session)):
    query = text("SELECT id, name, description, price, stock FROM product")
    result = await session.exec(query)
    products = result.mappings().all()
    return products
