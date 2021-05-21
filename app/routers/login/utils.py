import jwt
import pkgutil
import requests
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

def verify_decode_token(jwt_token):
    return jwt.decode(jwt_token, public_key, algorithms=JWT_ALGORITHM,options={"verify_exp": False})

def validate_facebook_token(token: str):
    # clientId = FACEBOOK_CLIENT_ID
    # clientSecret = FACEBOOK_SECRET
    # clientId = '139487954713006'
    # clientSecret = '27fad3ab556a4c1dac003e6828e1a146'
    # appLink = 'https://graph.facebook.com/oauth/access_token?client_id=' + \
    #     clientId + '&client_secret=' + clientSecret + '&grant_type=client_credentials'

    # From appLink, retrieve the second accessToken: app access_token
    # appToken = requests.get(appLink).json()['access_token']
    # https://graph.facebook.com/me?fields=email&access_token=${token}
    # link = 'https://graph.facebook.com/debug_token?input_token=' + \
    #     token + '&access_token=' + appToken
    link = 'https://graph.facebook.com/me?fields=email&access_token=' + token
    try:
        userId = requests.get(link).json()
    except (ValueError, KeyError, TypeError) as error:
        return error
    return userId
