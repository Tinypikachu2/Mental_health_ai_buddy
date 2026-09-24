from pydantic import BaseModel
from datetime import datetime

class TokenCreate(BaseModel):
    owner_name: str

class TokenResponse(BaseModel):
    id: int
    token_key: str
    owner_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
