
import requests

BASE_URL = "https://httpbin.org"


# 1. GET without custom headers
def get_data():
    response = requests.get(f"{BASE_URL}/get", timeout=5)

    response.raise_for_status()
    print(response.json())


# 2. GET with custom headers
def get_with_headers():
    headers = {
        "Accept": "application/json",
        "X-Client": "my-python-app"
    }

    response = requests.get(f"{BASE_URL}/get", headers=headers, timeout=5)

    response.raise_for_status()
    print(response.json())
    print(response.status_code)


# 3. POST with a JSON body
def create_data():
    payload = {
        "name": "Raman",
        "role": "backend-engineer"
    }

    response = requests.post(
        f"{BASE_URL}/post",
        json=payload,
        timeout=5
    )

    response.raise_for_status()
    print(response.json())


# 4. GET with a Bearer token
def get_with_token():
    token = "my-example-token"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/bearer",
        headers=headers,
        timeout=5
    )

    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    get_data()
    get_with_headers()
    create_data()
    get_with_token()
