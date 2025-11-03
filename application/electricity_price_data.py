from datetime import datetime

from application.data_fetcher import get_elpris_data_from_api
from application.electricity_price_visualization import create_pandas_dataframe


# Funktion för att extrahera datum från elprisdata
def extract_date_from_elpris_data(elpris_data):
    """
    Extrahera datum från elprisdata.

    Denna funktion extraherar datumet från den första
    datan i den tillhandahållna datan.

    Args:
        elpris_data (list): En lista med elprisdata.

    Returns:
        str: Det extraherade datumet.
    """
    # Extrahera datumet från den första datan i den tillhandahållna datan
    date = elpris_data[0]["time_start"].split("T")[0]
    return date  # Returnera det extraherade datumet


# Funktion för att hämta och behandla elprisdata
def fetch_and_process_elpris_data(year, month, day, price_class):
    """
    Hämta och behandla elprisdata.

    Denna funktion konstruerar API URL:en med det
    angivna året, månaden, dagen och prisklassen.
    Den hämtar elprisdata från API:en och hämtar
    aktuell datum och tid. Funktionen kontrollerar om
    datan inte är tillgänglig och om aktuell tid är
    före kl. 13:00.

    Args:
        year (int): År för elprisdata.
        month (int): Månad för elprisdata.
        day (int): Dag för elprisdata.
        price_class (str): Prisklass för elprisdata.

    Returns:
        pd.DataFrame or None, str or None: En Pandas
        DataFrame med de behandlade elprisdata om datan är
        tillgänglig och aktuell tid är inte före kl. 13:00.
        Annars returneras None och ett felmeddelande.
    """
    # Konstruera API URL:en med det angivna året, månaden, dagen och prisklassen
    api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month:02d}-{day:02d}_{price_class}.json"

    # Hämta elprisdata från API:en
    elpris_data = get_elpris_data_from_api(api_url)

    # Hämta aktuell datum och tid
    current_time = datetime.now()

    # Kontrollera om datan inte är tillgänglig pga aktuell tid är före kl. 13:00
    if elpris_data is None and current_time.hour < 13:
        error_message = "Åtkomst till nästa dags elprisdata kommer att vara tillgänglig efter kl. 13:00."
        return None, error_message

    # Skapa en Pandas DataFrame från den hämtade datan
    current_prices = create_pandas_dataframe(elpris_data)

    # Extrahera datum från datan
    date = elpris_data[0]["time_start"].split("T")[0]

    return current_prices, date  # Returnera den aktuella datan och datumet
