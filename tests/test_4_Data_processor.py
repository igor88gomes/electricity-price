from application.electricity_price_data import fetch_and_process_elpris_data


def test_fetch_and_process_elpris_data():
    # Testa värden för year, month, day och price_class
    year = 2023
    month = 1
    day = 1
    price_class = "SE3"

    # Anropa funktionen fetch_and_process_elpris_data
    current_prices, date = fetch_and_process_elpris_data(year, month, day, price_class)

    # Påståenden för de returnerade datavärdena
    assert current_prices is not None
    assert date is not None
