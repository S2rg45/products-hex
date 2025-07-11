
from abc import ABC, abstractmethod


class ProductRepositoryPort(ABC):
    @abstractmethod
    def create_product(self, product: dict) -> dict:
        """Create a new product."""
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> dict:
        """Get a product by its ID."""
        pass

    @abstractmethod
    def update_product(self, product_id: str, product_data: dict) -> dict:
        """Update an existing product."""
        pass

    @abstractmethod
    def delete_product(self, product_id: str) -> dict:
        """Delete a product by its ID."""
        pass

    @abstractmethod
    def get_all_products(self, page: int, limits: int) -> list:
        """Get all products."""
        pass