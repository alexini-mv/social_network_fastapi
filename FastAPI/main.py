# Python libraries
from email import message
from enum import Enum
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Cookie, Header, UploadFile, File


app = FastAPI()


# Enum's
# Definimos la lista de colores permitida para el
# atributo dentro del modelo

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

# Definimos la lista de paises permitidos.


class Countries(Enum):
    mexico = "México"
    colombia = "Colombia"
    peru = "Perú"
    venezuela = "Venezuela"
    chile = "Chile"
    argentina = "Argentina"

# Models (Para poder validar la estructura del Body Request)


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=120
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    password: str = Field(..., min_length=8)

    # Ejemplo de como configurar unos valores de prueba para la documentacion
    # Swagger o Redoc, definiendo una subclase.
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Alejandro",
                "last_name": "Martínez",
                "age": 30,
                "hair_color": "black",
                "is_married": True,
                "password": "HolaSoyAlejandro123"
            }
        }


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Mérida"     # <---- Ejemplo de como configurar valores prueba para la documentación
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Yucatán"   # <---- Ejemplo de como configurar valores prueba para la documentación
    )
    country: Countries = Field(
        ...,
        example="México"    # <---- Ejemplo de como configurar valores prueba para la documentación
    )


class LoginOut(BaseModel):
    username: str = Field(...,
                          max_length=20,
                          example="alexini123")
    message: str = Field(default="Login Successful",
                         description="Message to return to client.")


@app.get(path="/",
         status_code=status.HTTP_200_OK,
         tags=["Home"])
def home():
    return {"Hello": "World"}


# Request and Response Body

# Enviar datos desde el cliente -> servidor
@app.post(path="/person/new",
          response_model=Person,
          response_model_exclude={"password"},
          status_code=status.HTTP_201_CREATED,
          tags=["Persons"])
def create_person(user: Person = Body(...)):
    return user


# Validaciones de Query Parameters

@app.get(path="/person/detail",
         status_code=status.HTTP_200_OK,
         tags=["Persons"])
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters.",
        example="Daniel"
    ),
    age: Optional[int] = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required.",
        example=25
    )
):
    return {name: age}


# Validaciones de Path Parameters

persons = [1, 2, 3, 4, 5]


@app.get(path="/person/detail/{person_id}",
         status_code=status.HTTP_200_OK,
         tags=["Persons"])
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID.",
        description="This is a personal id of an user.",
        example=15987
    )
):
    if person_id not in persons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This person doesn't exist!!!")

    return {person_id: "It exists!"}


# Validaciones de Request Body
@app.put(path="/person/{person_id}",
         status_code=status.HTTP_200_OK,
         tags=["Persons"])
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID.",
        description="This is the person ID.",
        gt=0,
        example=15987),
    # <------- De está manera validamos la estructura obligatoria del body
    person: Person = Body(...),
    # <------- De está manera validamos la estructura obligatoria del body
    location: Location = Body(...)
):

    results = {"id": person_id}
    results.update(person.dict())
    results.update(location.dict())
    return results

# Recibir información de Formularios


@app.post(path="/login",
          response_model=LoginOut,
          status_code=status.HTTP_200_OK,
          tags=["Login"])
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Recibir Cookies and Headers


@app.post(path="/contact",
          status_code=status.HTTP_200_OK,
          tags=["Contact"])
def contact(first_name: str = Form(...,
                                   min_length=1,
                                   max_length=20),
            last_name: str = Form(...,
                                  min_length=1,
                                  max_length=20),
            email: EmailStr = Form(...),
            message: str = Form(...,
                                min_length=20),
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None)
            ):
    return user_agent

# UploadFiles y Files


@app.post(path="/post-image",
          tags=["Image"])
def post_image(image: UploadFile = File(...)):
    return {"Filename": image.filename,
            "Format": image.content_type,
            "Size (kb)": round(len(image.file.read()) / 1024, ndigits=2)}
