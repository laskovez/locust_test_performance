import os
import random
import time
from json import JSONDecodeError

from locust.clients import Response as LocustResponse
import requests
from dotenv import load_dotenv
from typing import BinaryIO, Callable, Type, Union
from locust import HttpUser

load_dotenv()


def get_auth_token(host: str, email: str = None, password: str = None) -> str:
    username = email or os.environ.get('USERNAME')
    password = password or os.environ.get('PASSWORD')
    response = requests.get(host + f'/user/login?username={username}&password={password}')
    response_json = response.json()
    auth_token = response_json['message']
    return auth_token


def get_random_image_file() -> BinaryIO:
    files = os.listdir("test_data")
    image_files = [file for file in files if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")]

    return open(os.path.join("test_data", random.choice(image_files)), "rb")
