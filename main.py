from fastapi import FastAPI
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"
app.description = "Esta es una app de ejemplo para FastAPI"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["home"])
def message():
    return {"message": "Hello, World"}