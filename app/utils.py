from uuid import uuid4

from fastapi import HTTPException, status
import jwt
from datetime import datetime, timezone, timedelta
from app.config import security_settings

def generate_access_token(data: dict, expiry: timedelta = timedelta(seconds=30)):
    return jwt.encode(
        payload={
            **data,
            "jwti":str(uuid4()),
            "exp":datetime.now(timezone.utc) + expiry
        },
        key=security_settings.JWT_SECRET,
        algorithm=security_settings.JWT_ALGORITHM
    )
    
def decode_access_token(token: str)-> dict | None:
    try:
        return jwt.decode(
                    jwt=token,
                    key=security_settings.JWT_SECRET,
                    algorithms=[security_settings.JWT_ALGORITHM]
                )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Access Token")
    except jwt.PyJWTError:
        return None