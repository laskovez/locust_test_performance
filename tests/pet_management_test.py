from locust import HttpUser, SequentialTaskSet, task, between

from helpers.data_generators import generate_pet_data
from helpers.helpers import get_auth_token
from tests import check_response, check_test_results


class TestPetManagement(SequentialTaskSet):
    wait_time = between(0, 1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updated_data = None
        self.creation_data = None
        self.pet_id = None

    @task
    def create_pet(self):
        self.creation_data = generate_pet_data()
        with self.client.post("/pet", json=self.creation_data, name='create_pet', catch_response=True) as response:
            response = check_response(response, 200, 1)
            self.pet_id = response.get("id")

            if not self.pet_id:
                self.interrupt()

    @task
    def get_pets_with_created_status(self):
        with self.client.get(f'/pet/findByStatus?status={self.creation_data["status"]}', name='get_pet_wth_status',
                             catch_response=True) as response:
            response = check_response(response, 200, 1)

        assert self.creation_data in response, f'Added Pet is not visible in list of pets with set status: ' \
                                               f'\n{self.updated_data} not in:\n {response}'

    @task
    def get_created_pet(self):
        with self.client.get(f"/pet/{self.pet_id}", name='get_pet', catch_response=True) as response:
            response = check_response(response, 200, 1)

        assert self.creation_data == response, f'Pet data was not updated: Actual data:\n{response} ' \
                                               f'Expected data: \n{self.creation_data}'

    @task
    def update_pet(self):
        self.updated_data = generate_pet_data()
        self.updated_data["id"] = self.pet_id
        with self.client.put("/pet", json=self.updated_data, name='update_pet', catch_response=True) as response:
            check_response(response, 200, 1)

    @task
    def get_pets_with_updated_status(self):
        with self.client.get(f'/pet/findByStatus?status={self.updated_data["status"]}', name='get_pet_wth_status',
                             catch_response=True) as response:
            response = check_response(response, 200, 1)

        assert self.updated_data in response, f'Added Pet is not visible in list of pets with set status:' \
                                              f'\n{self.updated_data} not in:\n {response}'

    @task
    def get_updated_pet(self):
        with self.client.get(f"/pet/{self.pet_id}", name='get_pet', catch_response=True) as response:
            response = check_response(response, 200, 1)

        assert self.updated_data == response, f'Pet data was not updated: Actual data:\n{response} ' \
                                              f'Expected data: \n{self.updated_data}'

    @task
    def delete_pet(self):
        with self.client.delete(f"/pet/{self.pet_id}", name='delete_pet', catch_response=True) as response:
            check_response(response, 200, 1)

    @task
    def get_not_existing_pet(self):
        with self.client.get(f"/pet/{self.pet_id}", name='get_deleted_pet', catch_response=True) as response:
            check_response(response, 404, 1)


class SmokeTestUser(HttpUser):
    tasks = [TestPetManagement]

    def setup(self):
        self.client.headers.update({'Authorization': f'Bearer {get_auth_token(self.host)}'})
        self.environment.events.add_listener(check_test_results)
