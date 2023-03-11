import logging
from json import JSONDecodeError
from typing import Union

import requests
from locust import events
from locust.clients import Response as LocustResponse


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


@events.quitting.add_listener
def check_test_results(environment):
    if environment.stats.total.fail_ratio > 0.02:
        logging.error("Test failed due to failure ratio > 2%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 500:
        logging.error("Test failed due to average response time > 500 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0
