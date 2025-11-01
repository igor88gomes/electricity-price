import requests


def get_elpris_data_from_api(api_url):
    """
    Hämta elprisdata från en API URL.

    Denna funktion utför en HTTP GET-begäran till den angivna
    API URL:en och returnerar JSON-responsdata om begäran
    lyckas. Om begäran misslyckas eller responsens statuskod
    inte är inom området 200, hanterar funktionen undantag och
    returnerar None.

    Args:
        api_url (str): En sträng som representerar API URL:en att
        begära data från.

    Returns:
        dict or None: En dictionary med JSON-responsdata om begäran
        lyckas, annars None.
    """
    try:
        # Skicka en HTTP GET-begäran till API URL:en
        response = requests.get(api_url)

        # Kasta ett undantag om statuskoden i responsen inte är inom området 200
        response.raise_for_status()

        # Returnera JSON-responsdata
        return response.json()
    except requests.exceptions.RequestException as e:
        # Hantera undantag och returnera None om hämtning av data misslyckas
        return None
