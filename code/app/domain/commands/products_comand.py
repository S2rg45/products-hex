
from pydantic import BaseModel, Field


class ProductCommand(BaseModel):
    product: list[dict] = Field(
        ...,
        description="Product data containing id, name, and price",
        example=[{"id": "12345", "name": "Sample Product", "price": 1990}],
    )   


class ProductsCommand(BaseModel):
    limits: int = Field(10, description="Number of products to return", example=10)
    page: int = Field(1, description="Page number for pagination", example=1)

    def __init__(self, **data):
        super().__init__(**data)
        if not isinstance(self.limits, int) or not isinstance(self.page, int):
            raise ValueError("Limits and page must be integers")

