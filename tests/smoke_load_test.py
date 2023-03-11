import random

from locust import HttpUser, TaskSet, task, between

from helpers.data_generators import generate_pet_data, generate_order_data
from helpers.helpers import get_auth_token, get_random_image_file
from tests import check_response, check_test_results


class SmokeTestSet(TaskSet):
    wait_time = between(0, 1)

    @task
    def test_create_pet(self):
        pet_data = generate_pet_data()
        with self.client.post("/pet", json=pet_data, catch_response=True) as response:
            check_response(response, 200, 1)

    @task
    def test_find_by_status(self):
        with self.client.get(f'/pet/findByStatus?status={random.choice(["available", "sold", "pending"])}',
                             catch_response=True) as response:
            check_response(response, 200, 1)

    @task
    def test_create_order(self):
        order_data = generate_order_data()
        with self.client.post("/store/order", json=order_data, catch_response=True) as response:
            check_response(response, 200, 1)

    @task
    def test_get_store_inventory(self):
        with self.client.get("/store/inventory", catch_response=True) as response:
            check_response(response, 200, 1)

    @task
    def test_upload_pet_image(self):
        pet_id = random.choice([1, 2, 3])
        files = {'file': get_random_image_file()}

        with self.client.post(f'/pet/{pet_id}/uploadImage', files=files, catch_response=True) as response:
            check_response(response, 200, 1)


class SmokeTestUser(HttpUser):
    tasks = [SmokeTestSet]

    def setup(self):
        self.client.headers.update({'Authorization': f'Bearer {get_auth_token(self.host)}'})
        self.environment.events.add_listener(check_test_results)
