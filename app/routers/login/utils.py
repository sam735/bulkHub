import jwt
import pkgutil
from hashlib import sha256
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from constant import JWT_ISSUER, JWT_ALGORITHM

private_key = pkgutil.get_data(__name__, "keys/jwt-key")
public_key = pkgutil.get_data(__name__, "keys/jwt-key.pub")

def check_password(plain_password: str, hashed_password: str) -> bool:
    password, salt = hashed_password.split(':')
    return password == sha256(salt.encode() + plain_password.encode()).hexdigest()

def generate_token(payload: dict):
    id = str(ObjectId())
    payload_with_claims = {
        "data": payload,
        "sub": payload["user_id"],
        #    "exp": '365d',
        "iss": JWT_ISSUER,
        "jti": id,
        #    "aud": JWT_AUDIENCE, // TODO add this once you have the actual certiicate
        "iat": datetime.utcnow()
        }
    encoded = jwt.encode(
        payload_with_claims, private_key,
        algorithm=JWT_ALGORITHM
    )
    return encoded, id