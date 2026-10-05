from typing import List, Optional

from pydantic import BaseModel


class ProductItem(BaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    discountedTotal: float


class CartSchema(BaseModel):
    id: int
    userId: int
    total: float
    discountedTotal: float
    totalProducts: int
    totalQuantity: int
    products: List[ProductItem]


class UserSchema(BaseModel):
    id: int
    firstName: str
    lastName: str
    age: int
    gender: str
    email: str
    city: str
    state: str
    country: str
    role: str


class ProductSchema(BaseModel):
    id: int
    title: str
    category: str
    price: float
    discountPercentage: float
    stock: int
    rating: float
    description: str
    weight: int
    returnPolicy: Optional[str] = None
    availabilityStatus: Optional[str] = None
    brand: Optional[str] = None
    sku: str
    minimumOrderQuantity: Optional[str] = None
