from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field



class Product(BaseModel):
    product: Dict[str, Any] = Field(..., description="Product data containing id, name, and price", example=[{"id": "12345","name": "Sample Product","price": 1990}])


class Products(BaseModel):
    limits: int = Field(10, description="Number of products to return", example=10)
    page: int = Field(1, description="Page number for pagination", example=1)


