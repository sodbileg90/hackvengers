from pydantic import BaseModel


class Todos(BaseModel):
    id: int