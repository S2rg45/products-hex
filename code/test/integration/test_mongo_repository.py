import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from app.adapters.driven.db.mongo import UserMongoRepository
from app.domain.commands.products_comand import ProductCommand
from app.settings import config
import uuid

@pytest.fixture(scope="module")
def repo():
    return UserMongoRepository(config)

def test_create_and_get_product(repo):
    # Producto único para evitar colisiones
    product_data = {"id": str(uuid.uuid4()), "name": "integration-test", "price": 123}
    command = ProductCommand(product=[product_data])
    created = repo.create_product(command.product[0])
    assert "product" in created
    # Recuperar el producto
    product_id = created["product"]["id"]
    fetched = repo.get_product_by_id(product_id)
    assert fetched["product"] is not None

def test_get_all_products(repo):
    # Crear un producto para asegurar que hay datos
    product_data = {"name": "test-product-all", "price": 200}
    created = repo.create_product(product_data)
    
    # Obtener todos los productos
    all_products = repo.get_all_products(page=1, limits=10)
    assert len(all_products) > 0
    assert "data" in all_products[0] or "message" in all_products[0]

def test_update_product(repo):
    # Crear un producto
    product_data = {"name": "test-update", "price": 300}
    created = repo.create_product(product_data)
    product_id = created["product"]["id"]
    
    # Actualizar el producto
    update_data = {"name": "test-updated", "price": 400}
    updated = repo.update_product(product_id, update_data)
    assert "product" in updated
    assert updated["product"]["name"] == "test-updated"
    assert updated["product"]["price"] == 400

def test_delete_product(repo):
    # Crear un producto
    product_data = {"name": "test-delete", "price": 500}
    created = repo.create_product(product_data)
    product_id = created["product"]["id"]
    
    # Eliminar el producto
    result = repo.delete_product(product_id)
    assert "status" in result
    assert result["status"] == "success"
    
    # Verificar que el producto ya no existe
    deleted_product = repo.get_product_by_id(product_id)
    assert deleted_product["product"] is None 