import random

from helpers.helpers import get_random_image_file


def generate_pet_data() -> dict:
    category = {"id": random.randint(1, 100), "name": "category name"}
    photo_urls = [get_random_image_file().name]
    tags = [{"id": random.randint(1, 100), "name": "tag name"}]
    status = random.choice(["available", "pending", "sold"])
    return {
        "id": random.randint(1, 100),
        "category": category,
        "name": f"pet name {random.randint(1, 100)}",
        "photoUrls": photo_urls,
        "tags": tags,
        "status": status,
    }


def generate_order_data() -> dict:
    pet_id = random.randint(1, 100)
    quantity = random.randint(1, 10)
    ship_date = "2023-02-26T10:00:00.000Z"
    status = random.choice(["placed", "approved", "delivered"])
    return {
        "id": random.randint(1, 100),
        "petId": pet_id,
        "quantity": quantity,
        "shipDate": ship_date,
        "status": status,
        "complete": True,
    }
