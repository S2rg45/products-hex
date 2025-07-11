from fastapi import Header, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.responses import JSONResponse


import json
import traceback

from app.adapters.utils.infrastructure.logger_utils import Log
from app.adapters.utils.infrastructure.error_handling import ErrorHandler
from app.entrypoint.api.model.api_model import Product, Products
from app.domain.commands.products_comand import ProductCommand
from app.domain.command_handler.product_handler import ProductHandler
from app.adapters.driven.db.mongo import UserMongoRepository
from app.settings import config

log = Log()
error = ErrorHandler()
router = APIRouter(prefix="/api-products")

repo = UserMongoRepository(config=config)
handler = ProductHandler(product_repository=repo)

############################################################################################################
# endpoints to get information products
############################################################################################################


# endpoint to register a new product
@router.post('/create-product/')
async def create_product(product: Product):
    log.logger.info(f"Product: {product}")
    """
    This function is used to create a new product
    :return: created product
    """
    try:
        request = product.dict()
        print(request)
        log.logger.info(f"Product-dict: {request}")
        create_p = handler.create_product(ProductCommand(product=[request["product"]]))
        response = {"status": "success", "data": create_p}
        return JSONResponse(content={"result": response}, status_code=201)
    except Exception as error:
        return ErrorHandler.handle_error(error, "Error creating product") 

    


# endpoint to get one product by id
@router.get('/product/')
async def get_product(product_id: Product):
    """
    This function is used to get a product by id
    :param product_id: id of the product
    :return: product
    """
    try:
        request = product_id.dict()
        log.logger.info(f"Product ID: {request}")
        get_product_id = handler.get_product_by_id(product_id=request["product"]["id"])
        # Here you would typically call a service to fetch the product by ID
        response = {"status": "success", "data": {"id": request["product"]["id"], "data": get_product_id}}
        log.logger.info(f"Response: {response}")
        if not get_product_id:
            log.logger.error(f"Product with ID {product_id} not found")
            return ErrorHandler.handle_not_found_error("Product", product_id, "Product not found")
        return JSONResponse(content={"result": response}, status_code=200)
    except Exception as e:
        return ErrorHandler.handle_error(e, f"Error fetching product with ID {product_id}") 
    

# endpoint to update a product by id
@router.put('/update-product/')
async def update_product(product: Product):
    """
    This function is used to update a product by id
    :param product_id: id of the product
    :param product: updated product data
    :return: updated product
    """
    request = product.dict()
    try:
        log.logger.info(f"Product ID: {request['product']['id']}, Product Data: {request['product']}")
        update_p = handler.update_product(product_id=request["product"]["id"], product_data=request["product"])
        # Here you would typically call a service to handle the update logic
        response = {"status": "success", "data": update_p}
        log.logger.info(f"Response: {response}")
        if not update_p:
            log.logger.error(f"Product with ID {request['product']['id']} not found")
            return ErrorHandler.handle_not_found_error("Product", request["product"]["id"], "Product not found")
        return JSONResponse(content={"result": response}, status_code=200)
    except Exception as e:
        return ErrorHandler.handle_error(e, f"Error updating product with ID {request['product']['id']}")
    

# endpoint to delete a product by id
@router.post('/delete-product/')
async def delete_product(product_id: Product):
    """
    This function is used to delete a product by id
    :param product_id: id of the product
    :return: success message
    """
    request = None
    try:
        request = product_id.dict()
        log.logger.info(f"Product ID: {request['product']['id']}")
        delete_p = handler.delete_product(product_id=request['product']['id'])
        if not delete_p:
            log.logger.error(f"Product with ID {request['product']['id']} not found")
            return ErrorHandler.handle_not_found_error("Product", request["product"]["id"], "Product not found")
        log.logger.info(f"Product with ID {request['product']['id']} deleted successfully")
        # Here you would typically call a service to handle the deletion logic
        response = {"status": "success", "message": delete_p}
        return JSONResponse(content={"result": response}, status_code=200)
    except Exception as e:
        return ErrorHandler.handle_error(e, f"Error deleting product")
    

# entopoint to get all products
@router.get('/products/')
async def get_all_products(products: Products):
    """
    This function is used to get all products
    :return: list of products
    """
    try:
        request = products.dict()
        log.logger.info(f"Request: {request}")
        log.logger.info("Fetching all products")
        all_products = handler.get_all_products(request["page"], request["limits"])
        if not all_products:
            log.logger.error("No products found")
            return ErrorHandler.handle_not_found_error("Product", "all", "No products found")
        log.logger.info(f"All products: {all_products}")
        # Here you would typically call a service to fetch all products
        response = {"status": "success", "data": all_products}
        log.logger.info(f"Response: {response}")
        return JSONResponse(content={"result": response}, status_code=200)
    except Exception as e:
        return ErrorHandler.handle_error(e, "Error fetching all products")