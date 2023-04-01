from datetime import datetime, timezone
from typing import Union
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    last_name: str
    first_name: str
    disabled: Union[bool, None] = False
    password: str
    last_update: Union[datetime, None] = datetime.now(timezone.utc)

class UserLogin(BaseModel):
    username: str
    password: str

class UserChangePW(BaseModel):
    username: str
    old_password: str
    new_password:str