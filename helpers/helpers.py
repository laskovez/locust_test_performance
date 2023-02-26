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


def check_response(response:  Union[LocustResponse, requests.Response], expected_status_code: int,
                   max_response_time: float) -> Union[str, dict]:
    """
    Method to check the response time and status code of an HTTP request.

    Args:
        response: Response object returned by the HTTP request.
        expected_status_code: Expected status code of the HTTP request.
        max_response_time: Maximum response time in seconds allowed for the HTTP request.

    Returns:
        Response of the HTTP request.
    """
    try:
        response_body = response.json()
    except JSONDecodeError:
        response_body = response.text

    if response.status_code != expected_status_code:
        response.failure(f"Received status code {response.status_code} != {expected_status_code}. --------->"
                         f"Response body: {response_body}")
    elif response.elapsed.total_seconds() > max_response_time:
        response.failure(f"Response time {response.elapsed.total_seconds()}s > {max_response_time}s. --------->"
                         f"Response body: {response_body}")
    else:
        response.success()

    return response_body
