import requests


def get_elpris_data_from_api(api_url, timeout=5):
    try:
        response = requests.get(api_url, timeout=timeout)
        response.raise_for_status()
        return "ok", response.json()
    except requests.exceptions.HTTPError:
        if getattr(response, "status_code", None) == 404:
            return "no_data_yet", None
        return "upstream_error", None
    except requests.exceptions.RequestException:
        return "upstream_error", None
