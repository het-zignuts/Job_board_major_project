from pydantic import BaseModel

class Token(BaseModel):
    token_type: str = "bearer"

class AccessToken(Token):
    access_token: str
    refresh_token: str

class RefreshToken(Token):
    refresh_token: str