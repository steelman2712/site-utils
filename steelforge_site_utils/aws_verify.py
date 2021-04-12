from functools import wraps
import cognitojwt
import os
import time
from flask import Flask, request, redirect, url_for, session
import boto3
import logging 

REGION = os.environ.get("AWS_REGION")
USERPOOL_ID = os.environ.get("USERPOOL_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")

LOGIN_ENDPOINT = os.environ.get("LOGIN_ENDPOINT","/login")

cognito_client = boto3.client('cognito-idp')
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY

def verify_jwt(id_token):
    verified_claims= cognitojwt.decode(
        id_token,
        REGION,
        USERPOOL_ID,
        app_client_id=CLIENT_ID,  # Optional
    )
    current_time = time.time()
    if verified_claims["exp"] < current_time:
        raise ValueError("Token Expired")
    if verified_claims["aud"] != CLIENT_ID:
        raise ValueError("Client ID doesn't match")
    userpool = f"https://cognito-idp.{REGION}.amazonaws.com/{USERPOOL_ID}"
    if verified_claims["iss"] != userpool:
        raise ValueError("Userpool doesn't match")
    if verified_claims["token_use"] != "id":
        raise ValueError("Token use doesn't match")
    else:
        return True

def authed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            session["redirect_url"] = request.url
            print("Request url: ",request.url)
            print("Session: ",session["redirect_url"])
            access_token = request.cookies.get('access_token')
            token_verified = verify_access_token(access_token)
            if verify_access_token(access_token):
                return func(*args, **kwargs)
            else:
                return redirect(LOGIN_ENDPOINT)
        except Exception as e:
            logging.debug(e)
            return redirect(LOGIN_ENDPOINT)
    return wrapper


def verify_access_token(access_token):
    verified_claims= cognitojwt.decode(
        access_token,
        REGION,
        USERPOOL_ID,
        app_client_id=CLIENT_ID,  # Optional
    )
    current_time = time.time()
    if verified_claims["exp"] < current_time:
        return False
    if verified_claims["client_id"] != CLIENT_ID:
        return False
    userpool = f"https://cognito-idp.{REGION}.amazonaws.com/{USERPOOL_ID}"
    if verified_claims["iss"] != userpool:
        return False
    if verified_claims["token_use"] != "access":
        return False
    else:
        return True

def get_user_type(access_token):
    user = cognito_client.get_user(AccessToken=access_token)
    print(user)
    user_type = user.get("UserAttributes").get("UserType")
    print(user_type)
