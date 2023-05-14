# Python
import json
from uuid import UUID   # Clase que nos ayuda a trabajar con id únicos
from datetime import date
from datetime import datetime
from typing import List, Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body


app = FastAPI()


# MODELS

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )


class User(UserBase):
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
    birth_date: Optional[date] = Field(default=None)


class UserRegister(User):
        password: str = Field(
        ...,
        min_length=8
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(
        default=datetime.now()
    )
    updated_at: Optional[datetime] = Field(
        default=None
    )
    by: User = Field(...)


# Path Operations

## Path Operations of Users

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operations register a user in the app.

    Parameters:
        - Request body parameter
            - user: UserRegister

    Returns a json with the basic user information:
        - user_id: UUID
        - emai: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        # results = json.loads(f.read())    # Lee primero el archivo y lo guarda en un string. Y después ese string lo parsea a objetos tipo json 
        results = json.load(f)              # Le deja todo el trabajo de leer e interpretar a la libreria JSON
        user_dict = user.dict()             # Request Body to Dictionary
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])

        results.append(user_dict)

        f.seek(0)                           # Me muevo al inicio del archivo
        # f.write(json.dumps(results))      # Convierte string a json 
        json.dump(results, f)               # Lo mismo que el anterior pero en automatico
        return user


@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass


@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operation shows all users in the app

    Parameters:
        -
    Return a json list with all users in the app, with the follow keys:
        - user_id: UUID
        - emai: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)

        
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def delete_a_user():
    pass

## Path Operations of Tweets

@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    """
    This path operation shows all tweets in the app

    Parameters:
        -
    Return a json list with all tweets in the app, with the follow keys:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        return json.load(f)


@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operations post a tweet in the app.

    Parameters:
        - Request body parameter
            - tweet: Tweet

    Returns a json with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User

    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        # results = json.loads(f.read())    # Lee primero el archivo y lo guarda en un string. Y después ese string lo parsea a objetos tipo json 
        results = json.load(f)              # Le deja todo el trabajo de leer e interpretar a la libreria JSON
        tweet_dict = tweet.dict()             # Request Body to Dictionary
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)

        f.seek(0)                           # Me muevo al inicio del archivo
        # f.write(json.dumps(results))      # Convierte string a json 
        json.dump(results, f)               # Lo mismo que el anterior pero en automatico
        return tweet


@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass


@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass


@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass