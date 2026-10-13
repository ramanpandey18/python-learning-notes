import requests
from requests.exceptions import HTTPError

BASE_URL = "https://httpbin.orgs"

def get_data():
  try:
    res = requests.get(f"{BASE_URL}/get", timeout = 5)
    res.raise_for_status()
    print(res.status_code)
    print(res.json())
  except HTTPError as http_error:
    print(f"HTTP error occurred: {http_error.response.status_code}")
  except Exception as err:
    print(f"Other error occurred: {err}")


if __name__ == "__main__":
  get_data()
