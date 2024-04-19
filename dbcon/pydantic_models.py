from pydantic import BaseModel
from datetime import datetime
from typing import List


class Doc(BaseModel):
    BaseId: int
    Mark: str
    expdate: datetime
    name: str
    barcode: str


class Package(BaseModel):
    items: List[Doc]
