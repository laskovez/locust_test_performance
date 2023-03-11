import os
import random
from typing import BinaryIO

import requests
from dotenv import load_dotenv

load_dotenv()


def get_auth_token(host: str, email: str = None, password: str = None) -> str:
    username = email or os.environ.get('USERNAME')
    password = password or os.environ.get('PASSWORD')
    response = requests.get(host + f'/user/login?username={username}&password={password}')
    response_json = response.json()
    auth_token = response_json['message']
    return auth_token


def get_random_image_file() -> BinaryIO:
    files_directory = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
    files = os.listdir(files_directory)
    image_files = [file for file in files if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")]

    return open(os.path.join(files_directory, random.choice(image_files)), "rb")
