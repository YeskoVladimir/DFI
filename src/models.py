from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Item(BaseModel):
    id: UUID
    value: str


class Action(Enum):
    insert = "insert"
    delete = "delete"
