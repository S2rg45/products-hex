import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from app.domain.command_handler.product_handler import ProductHandler
from app.domain.commands.products_comand import ProductCommand

class MockRepo:
    def create_product(self, product):
        return {"data": product}
    
    def get_product_by_id(self, product_id):
        return {"product": {"id": product_id, "name": "test-product", "price": 100}}
    
    def update_product(self, product_id, product_data):
        return {"product": {"id": product_id, **product_data}}
    
    def delete_product(self, product_id):
        return {"status": "success", "message": f"Product {product_id} deleted"}
    
    def get_all_products(self, page=1, limits=10):
        return [{"data": [{"id": "1", "name": "product1", "price": 100}]}]

@pytest.fixture
def handler():
    repo = MockRepo()
    return ProductHandler(product_repository=repo)

def test_create_product(handler):
    product_data = {"name": "test-product", "price": 100}
    command = ProductCommand(product=[product_data])
    result = handler.create_product(command)
    assert result["data"]["name"] == "test-product"
    assert result["data"]["price"] == 100

def test_get_product_by_id(handler):
    product_id = "test-id-123"
    result = handler.get_product_by_id(product_id)
    assert result["product"]["id"] == product_id
    assert result["product"]["name"] == "test-product"

def test_update_product(handler):
    product_id = "test-id-123"
    update_data = {"name": "updated-product", "price": 200}
    result = handler.update_product(product_id, update_data)
    assert result["product"]["id"] == product_id
    assert result["product"]["name"] == "updated-product"
    assert result["product"]["price"] == 200

def test_delete_product(handler):
    product_id = "test-id-123"
    result = handler.delete_product(product_id)
    assert result["status"] == "success"
    assert "deleted" in result["message"]

def test_get_all_products(handler):
    result = handler.get_all_products(page=1, limits=10)
    assert len(result) > 0
    assert "data" in result[0] 