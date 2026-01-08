from application.data_fetcher import get_elpris_data_from_api
from application.electricity_price_visualization import create_pandas_dataframe


def _build_api_url(year: int, month: int, day: int, price_class: str) -> str:
    return f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month:02d}-{day:02d}_{price_class}.json"


def extract_date_from_elpris_data(elpris_data: list[dict]) -> str:
    return elpris_data[0]["time_start"].split("T")[0]


def fetch_and_process_elpris_data(year: int, month: int, day: int, price_class: str):
    api_url = _build_api_url(year, month, day, price_class)
    status, elpris_data = get_elpris_data_from_api(api_url)

    if status != "ok":
        return None, None, status

    current_prices = create_pandas_dataframe(elpris_data)
    date = extract_date_from_elpris_data(elpris_data)
    return current_prices, date, None
