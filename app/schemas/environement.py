from pydantic import BaseModel
from typing import Any, Optional, List
from datetime import datetime

class EnvironmentCreate(BaseModel):
    name: str
    address: str
    cords: Any  # Peut être une liste ou dict, selon ce que tu mets
    pathCartographie: str
    scale: Optional[int] = None

class EnvironmentOut(EnvironmentCreate):
    id: int
    createdAt: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    role: str
    email: str
    createdAt: str
    lastLogin: Optional[str]
    firstname: Optional[str] = None
    lastname: Optional[str] = None


class EnvironmentResponse(BaseModel):
    id: int
    name: str
    address: str
    pathCartographie: str
    scale: int
    createdAt: str
    users: List[UserResponse]



class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    cords: Optional[Any] = None
    pathCartographie: Optional[str] = None
    scale: Optional[int] = None
