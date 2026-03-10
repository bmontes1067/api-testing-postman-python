from pydantic import BaseModel, EmailStr
from typing import Optional


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class PostCreate(BaseModel):
    title: str
    body: str
    userId: int
    id: Optional[int] = None  # returned by server on creation


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str


class Todo(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool
