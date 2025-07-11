from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from ...config.settings import config


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SettingsToken():
    def __init__(self):
        self.init = None
    
   
    def hashed_password(slef, password: str) -> str:
        return password_context.hash(password)


    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)


    def create_access_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=30)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, config["local"]["jwt_secret_key"], config["local"]["algorithm"])
        return encoded_jwt


    def create_refresh_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=config["local"]["refresh_token_expire_minutes"])
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, config["local"]["refresh_token_expire_minutes"], config["local"]["algorithm"])
        return encoded_jwt