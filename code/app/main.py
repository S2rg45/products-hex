from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Importing routes

from app.entrypoint.api.handler_api import router
from app.adapters.utils.infrastructure.logger_utils import Log

# from app.services.change_price.routes import change_route
# from app.services.create_property.routes import create_route
# from app.services.image_property.routes import image_routes
# from app.services.singup.routes import singup_route
# from app.services.login.routes import login_route
log = Log()
# Creating FastAPI instance
app = FastAPI(title="Api products", 
              description="API for products",
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# Including routes
app.include_router(router)


# Running server
log.logger.info("server running")
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

