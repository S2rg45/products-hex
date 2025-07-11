from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from bson import json_util
from ....domain.ports.product_repository_port import ProductRepositoryPort
from ...utils.infrastructure.logger_utils import Log

# --------------------------------------------------------------------------------
# Class ConnectionDb donde se obtiene la conexión a la base de datos
class UserMongoRepository(ProductRepositoryPort):
    def __init__(self, config: dict):
        # Establecer conexión a MongoDB
        self.config = config
        self.logger = Log().logger
        self.client = MongoClient(self.config["local"]["connection"])
        # Obtener la base de datos y la colección
        self.db = self.client[self.config["local"]["db"]]
        self.collection = self.db[self.config["local"]["collection_owner"]]


    def get_product_by_id(self, product_id: str) -> dict:
        try:
            doc = self.collection.find_one({"_id": ObjectId(product_id)})
            if doc:
                doc["id"] = str(doc.pop("_id"))
            return {"product":doc}
        except Exception as e:
            self.logger.error(f"Error retrieving product by ID {product_id}: {e}")
            return {"error": str(e)}


    def create_product(self, product: dict) -> dict:
        print(self.collection)
        result = self.collection.insert_one(product)
        self.logger.info(f"Product created with ID: {result}")
        result = self.get_product_by_id(str(result.inserted_id))
        return result


    def update_product(self, product_id: str, product_data: dict) -> dict:
        self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
        info = self.get_product_by_id(product_id)
        return info
    

    def get_all_products(self, page: int, limits: int) -> list:
        users = []
        products_count = self.collection.count_documents({})
        fetch_products = self.collection.find().sort('_id', -1).skip((page - 1) * limits).limit(limits)
        products = list(json.loads(json_util.dumps(fetch_products)))
        if not products:
            return [{"status": "success", "message": "No products found."}]
        response = [{
            "message": f"Products found: {len(products)}",
            "data": products,
            "pagination": {
                "page": page,
                "limits": limits,
                "total_products_collection": products_count
            }
        }]
        return response


    def delete_product(self, product_id: str) -> dict:
        self.collection.delete_one({"_id": ObjectId(product_id)})
        return {"status": "success", "message": f"Product with ID {product_id} deleted successfully."}