from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class TodoModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    task: str = Field(..., max_length=100)
    done: Optional[bool]

