from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
import json


from ...config.settings import config
from ..models.schemas import User_Process_Files, TokenPayload
from .store.validate_store import ValidateStore


class OAuth2PasswordBearerWithCookie():
    def __init__(self):
        self.db = ValidateStore()      
    

    reuseable_oauth = OAuth2PasswordBearer(
        tokenUrl="/token",
        scheme_name="JWT"
    )


    async def validate_token(self, token: str = Depends(reuseable_oauth)) -> bool:
        try:
            payload = jwt.decode(
                token, config["local"]["jwt_secret_key"], algorithms=config["local"]["algorithm"]
            )
            token_data = TokenPayload(**payload)
            
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except(jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Por favor genere el login nuevamente",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        data_email = dict(token_data)["sub"].replace("'", '"')
        email = json.loads(data_email)
        user = self.db.validate_token({"email": email["email"]})
        print(user)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        
        return True