from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import Field
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get("/movies", tags=["movies"], response_model = List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies()
  return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
  db = Session()
  result = MovieService(db).get_movie(id)
  if not result:
    return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"}) 
  return JSONResponse(status_code=200, content=jsonable_encoder(result)) 


@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)) -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies_by_category(category)
  return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
  db = Session()
  MovieService(db).create_movie(movie)
  return JSONResponse(status_code=201, content={"message": "Pelicula creada correctamente"})


@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"error": "Pelicula no encontrada"}, status_code=401)
    MovieService(db).update_movie(id, movie)
    db.commit()
    return JSONResponse(content={"message": "Pelicula actualizada correctamente"}, status_code=200)


@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict)
def delete_movie(id: int):
  db = Session()
  result = MovieService(db).get_movie(id)
  if not result:
    return JSONResponse(content={"error": "Pelicula no encontrada"}, status_code=401)
  MovieService(db).delete_movie(id)
  return JSONResponse(content={"message": "Pelicula eliminada correctamente"}, status_code=200)
