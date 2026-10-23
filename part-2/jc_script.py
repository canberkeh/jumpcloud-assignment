import os

from dotenv import load_dotenv
import requests

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
SYSTEM_ID = os.getenv("SYSTEM_ID")
BASE_URL = "https://console.jumpcloud.com/"
DEFAULT_TIMEOUT = 10
HEADERS = {
    "x-api-key": API_KEY,
    "content-type": "application/json"
}

def send_request(method, endpoint: str, payload=None, query_params=None) -> requests.Response:
    response = requests.request(
        method,
        BASE_URL + endpoint,
        json=payload,
        params=query_params,
        headers=HEADERS,
        timeout=DEFAULT_TIMEOUT,
        )
    return response

def create_user(user: dict) -> str:
    endpoint = "api/systemusers"
    try:
        response = send_request("POST", endpoint, payload=user)
        created_user_id = response.json().get("_id")
        if created_user_id:
            return created_user_id
    except Exception as e:
        print(f"Error creating users: {e}")
    return None

def activate_user(user_id: str) -> bool:
    endpoint = f"api/systemusers/{user_id}/state/activate"
    try:
        response = send_request("POST", endpoint)
        return response.status_code == 200
    except Exception as e:
        print(f"Error activating user: {e}")
        return False

def create_user_group(group_name: str) -> str:
    endpoint = "api/v2/usergroups"
    try:
        payload = {"name": group_name}
        response = send_request("POST", endpoint, payload)
        return response.json().get("id", "")
    except Exception as e:
        print(f"Error creating user group: {e}")
        return ""

def associate_user_to_group(user_id: str, group_id: str) -> bool:
    endpoint = f"api/v2/usergroups/{group_id}/members"
    payload = {
        "id": user_id,
        "op": "add",
        "attributes": {},
        "type": "user"
    }
    try:
        response = send_request("POST", endpoint, payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error associating user with group: {e}")
        return False

def get_members_by_group_id(group_id: str) -> list:
    endpoint = f"api/v2/usergroups/{group_id}/members"
    try:
        response = send_request("GET", endpoint)
        return response.json().get("results", [])
    except Exception as e:
        print(f"Error retrieving members by group ID: {e}")
        return []

def associate_user_to_system(user_id: str):
    endpoint = f"api/v2/systems/{SYSTEM_ID}/associations"
    payload = {
        "id": user_id,
        "op": "add",
        "attributes": {},
        "type": "user"
    }
    try:
        response = send_request("POST", endpoint, payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error associating user with system: {e}")
        return False

def get_systems() -> list[dict]:
    """
        Get system ids.
    """
    endpoint = "api/systems"
    try:
        response = send_request("GET", endpoint)
        return response.json().get("results", [])
    except Exception as e:
        print(f"Error retrieving systems: {e}")
        return []

def get_system_associations() -> list[dict]:
    endpoint = f"api/v2/systems/{SYSTEM_ID}/associations"
    query_params = {
        "targets": "user"
    }
    try:
        response = send_request("GET", endpoint, None, query_params)
        return response.json()
    except Exception as e:
        print(f"Error retrieving system associations: {e}")
        return []


if __name__ == '__main__':
    users = [
        {
            "username": "TestUser55",
            "email": "testuser55@gmail.com",
            "firstname": "Test55",
            "lastname": "User55",
            "password": "MyP@ssw0rd55"
        },
        {
            "username": "TestUser66",
            "email": "testuser66@gmail.com",
            "firstname": "Test66",
            "lastname": "User66",
            "password": "MyP@ssw0rd66"
        }
    ]
    user_ids = []
    for user in users:
        user_id = create_user(user)
        if user_id:
            user_ids.append(user_id)
            activate_user(user_id)

    user_group_name = "TestUserGroup3"
    user_group_id = create_user_group(user_group_name)

    for user_id in user_ids:
        associate_user_to_group(user_id, user_group_id)

    system_details = get_systems()
    if user_ids:
        associate_user_to_system(user_ids[0])

    system_associations_detail = get_system_associations()
