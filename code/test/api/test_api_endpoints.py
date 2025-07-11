import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product_endpoint():
    product_data = {
        "product": {
            "name": "test-api-product",
            "price": 150
        }
    }
    response = client.post("/api-products/create-product/", json=product_data)
    assert response.status_code == 201
    assert "result" in response.json()

def test_get_product_by_id_endpoint():
    # Primero crear un producto
    product_data = {
        "product": {
            "name": "test-get-product",
            "price": 250
        }
    }
    create_response = client.post("/api-products/create-product/", json=product_data)
    created_product = create_response.json()["result"]["data"]["product"]
    product_id = created_product["id"]
    
    # Obtener el producto por ID - usar POST con body JSON
    get_data = {
        "product": {
            "id": product_id
        }
    }
    response = client.post("/api-products/product/", json=get_data)
    assert response.status_code == 200
    assert "result" in response.json()

def test_update_product_endpoint():
    # Primero crear un producto
    product_data = {
        "product": {
            "name": "test-update-api",
            "price": 350
        }
    }
    create_response = client.post("/api-products/create-product/", json=product_data)
    created_product = create_response.json()["result"]["data"]["product"]
    product_id = created_product["id"]
    
    # Actualizar el producto
    update_data = {
        "product": {
            "id": product_id,
            "name": "test-updated-api",
            "price": 450
        }
    }
    response = client.put("/api-products/update-product/", json=update_data)
    assert response.status_code == 200
    assert "result" in response.json()

def test_delete_product_endpoint():
    # Primero crear un producto
    product_data = {
        "product": {
            "name": "test-delete-api",
            "price": 550
        }
    }
    create_response = client.post("/api-products/create-product/", json=product_data)
    created_product = create_response.json()["result"]["data"]["product"]
    product_id = created_product["id"]
    
    # Eliminar el producto
    delete_data = {
        "product": {
            "id": product_id
        }
    }
    response = client.post("/api-products/delete-product/", json=delete_data)
    assert response.status_code == 200
    assert "result" in response.json()

def test_get_all_products_endpoint():
    # Usar POST con body JSON
    products_data = {
        "page": 1,
        "limits": 10
    }
    response = client.post("/api-products/products/", json=products_data)
    assert response.status_code == 200
    assert "result" in response.json() 