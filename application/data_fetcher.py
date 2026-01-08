import requests


def get_elpris_data_from_api(api_url, timeout=5):
    try:
        response = requests.get(api_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
