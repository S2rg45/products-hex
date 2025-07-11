

from ..ports.product_repository_port import ProductRepositoryPort
from ..commands.products_comand import ProductCommand



class ProductHandler:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository


    def create_product(self, product_command: ProductCommand) -> dict:
        """Create a new product."""
        return self.product_repository.create_product(product_command.product[0])


    def get_product_by_id(self, product_id: str) -> dict:
        """Get a product by its ID."""
        return self.product_repository.get_product_by_id(product_id)


    def update_product(self, product_id: str, product_data: dict) -> dict:
        """Update an existing product."""
        return self.product_repository.update_product(product_id, product_data)


    def delete_product(self, product_id: str) -> dict:
        """Delete a product by its ID."""
        response = self.product_repository.delete_product(product_id)
        return response
    

    def get_all_products(self, page: int, limits: int) -> list:
        """Get all products."""
        return self.product_repository.get_all_products(page, limits)