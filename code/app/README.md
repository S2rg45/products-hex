# Product Microservice

## Descripción

El microservicio de Product es parte del sistema Linktic, diseñado para gestionar productos utilizando **Clean Architecture** y **Domain-Driven Design (DDD)**. Este servicio proporciona operaciones CRUD completas para productos y está construido con FastAPI y MongoDB.

## Arquitectura

### Clean Architecture

El microservicio sigue los principios de Clean Architecture con las siguientes capas:

```
app/
├── domain/           # Capa de dominio (reglas de negocio)
│   ├── commands/     # Comandos del dominio
│   ├── command_handler/  # Manejadores de comandos
│   └── ports/        # Interfaces/contratos
├── adapters/         # Capa de adaptadores
│   ├── driven/       # Adaptadores conducidos (base de datos)
│   ├── security/     # Adaptadores de seguridad
│   └── utils/        # Utilidades e infraestructura
└── entrypoint/       # Punto de entrada (API REST)
    └── api/          # Controladores y modelos de API
```

### Tecnologías

- **FastAPI**: Framework web para APIs REST
- **MongoDB**: Base de datos NoSQL
- **Pydantic**: Validación de datos y serialización
- **Poetry**: Gestión de dependencias
- **Uvicorn**: Servidor ASGI
- **pytest**: Framework de testing

## Endpoints

### Health Check
```http
GET /api-products/health/
```
Verifica el estado del servicio.

### Crear Producto
```http
POST /api-products/create-product/
```
Crea un nuevo producto.

**Body:**
```json
{
  "product": {
    "name": "Sample Product",
    "price": 1990
  }
}
```

### Obtener Producto por ID
```http
POST /api-products/product/
```
Obtiene un producto específico por su ID.

**Body:**
```json
{
  "product": {
    "id": "12345"
  }
}
```

### Actualizar Producto
```http
PUT /api-products/update-product/
```
Actualiza un producto existente.

**Body:**
```json
{
  "product": {
    "id": "12345",
    "name": "Updated Product",
    "price": 2500
  }
}
```

### Eliminar Producto
```http
POST /api-products/delete-product/
```
Elimina un producto por su ID.

**Body:**
```json
{
  "product": {
    "id": "12345"
  }
}
```

### Obtener Todos los Productos
```http
POST /api-products/products/
```
Obtiene una lista paginada de todos los productos.

**Body:**
```json
{
  "page": 1,
  "limits": 10
}
```

## Modelos de Datos

### Product
```python
class Product(BaseModel):
    product: Dict[str, Any] = Field(
        ..., 
        description="Product data containing id, name, and price"
    )
```

### Products (Paginación)
```python
class Products(BaseModel):
    limits: int = Field(10, description="Number of products to return")
    page: int = Field(1, description="Page number for pagination")
```

## Configuración

### Variables de Entorno
El servicio utiliza las siguientes configuraciones en `settings.py`:

- **MongoDB Connection**: Conexión a la base de datos MongoDB
- **Database Name**: Nombre de la base de datos
- **Collection Name**: Nombre de la colección de productos

### Estructura de Configuración
```python
config = {
    "local": {
        "connection": "mongodb://localhost:27017/",
        "db": "product_db",
        "collection_owner": "products"
    }
}
```

## Desarrollo

### Desbloqueo de poetry
```bash
poetry lock
```

### Instalación de Dependencias
```bash
poetry install
```

### Ejecutar en Desarrollo
```bash
poetry run python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar Tests
```bash
# Tests unitarios
poetry run pytest

# Tests con cobertura
poetry run pytest --cov=app --cov-report=html
```

### Docker
```bash
# Construir imagen
docker build -t ms-product .

# Ejecutar contenedor
docker run -p 8000:8000 ms-product
```

## Estructura del Proyecto

```
product/
├── code/
│   ├── app/
│   │   ├── domain/           # Lógica de negocio
│   │   ├── adapters/         # Adaptadores externos
│   │   ├── entrypoint/       # API REST
│   │   ├── main.py          # Punto de entrada
│   │   └── settings.py      # Configuración
│   ├── test/                # Tests
│   ├── Dockerfile           # Configuración Docker
│   ├── pyproject.toml       # Dependencias Poetry
│   └── README.md           # Este archivo
├── infra/                   # Configuración de infraestructura
└── .gitignore
```

## Patrones de Diseño

### Command Pattern
Los comandos encapsulan las operaciones del dominio:
- `ProductCommand`: Para operaciones de producto individual
- `ProductsCommand`: Para operaciones de listado con paginación

### Repository Pattern
El `ProductRepositoryPort` define la interfaz para el acceso a datos, implementado por `UserMongoRepository`.

### Handler Pattern
Los manejadores de comandos procesan las operaciones del dominio y coordinan con los repositorios.

## Logging y Manejo de Errores

El servicio incluye:
- **Structured Logging**: Usando `structlog`
- **Error Handling**: Manejo centralizado de errores
- **Health Checks**: Monitoreo del estado del servicio

