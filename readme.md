# Short URL API

Short URL API is a web service written in Python using the FastAPI framework. This service is used to shorten long links into more compact and user-friendly ones. The service consists of various handles (GET, POST, DELETE, PUT)

### API Endpoints:

### Health Check
`GET /health/`  
- Check service health status


### Short URL Management
`GET /short/`  
- Retrieve all short URLs


`GET /short/lookup`  
- Retrieve a short URL by ID or code  

`POST /short/`  
- Create a new short URL  


`DELETE /short/`  
- DANGER: Delete ALL short URLs

`DELETE /short/{id}`  
- Delete a specific short URL by ID  

`PUT /short/{id}`  
- Update a short URL's properties  

### Redirection
`GET /redirect/{code}`  
- Redirect to original URL  

(Full API documentation available via Swagger UI at `/` (or `/redoc`) when service is running.)

### Technology Stack:

- Framework: FastAPI;
- Database: PostgreSQL;
- ORM: SQLAlchemy;
- Migrations: Alembic;
- Validation: Pydantic;
- ASGI Server: Uvicorn;

(More details can be found in pyproject.toml and docker files)

### Project structure:

```
./shorter
├── infrastructure
│   └── database
│       ├── crud
│       │   ├── abc.py
│       │   ├── base.py
│       │   ├── __init__.py
│       │   └── short.py
│       ├── migrations
│       │   ├── versions
│       │   │   └── 2025_07_10_2100-273eeb780890_initial.py
│       │   ├── env.py
│       │   ├── README
│       │   └── script.py.mako
│       ├── models
│       │   ├── base.py
│       │   ├── __init__.py
│       │   └── short.py
│       ├── base.py
│       ├── database.py
│       ├── __init__.py
│       └── mixins.py
├── src
│   ├── config
│   │   ├── components
│   │   │   ├── cors
│   │   │   │   ├── cors.py
│   │   │   │   └── __init__.py
│   │   │   └── database
│   │   │       ├── database.py
│   │   │       └── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── __init__.py
│   ├── routers
│   │   ├── health
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── redirect
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py
│   │   │   └── views.py
│   │   ├── short
│   │   │   ├── service
│   │   │   │   ├── base.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── service.py
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py
│   │   │   └── views.py
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── __init__.py
│   └── main.py
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml
└── readme.md
```

### Running the Service

The project is built on Docker and to run it you will need to install it (instructions: https://docs.docker.com/engine/install/)

In project directory use this command: `docker compose down && docker compose up --build -d`

The service will be available at http://localhost:8080 by default.

### Project configuration

The project contains various settings, more detailed information can be found in the configuration files (`./src/config`). To apply the settings, you need to create a `.env` file in the root folder of the project and fill it in according to the example. An example of such a file: `.env.example`
