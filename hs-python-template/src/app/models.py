from pydantic import BaseModel


class Item(BaseModel):
    id: str
    name: str
    description: str


class CreateItem(BaseModel):
    name: str
    description: str
