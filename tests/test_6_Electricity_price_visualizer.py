import pandas as pd

from application.electricity_price_visualization import (
    create_chart,
    create_pandas_dataframe,
    create_pandas_table,
    create_plotly_chart,
)

# Exempeldata för testning
sample_data = [
    {"time_start": "2023-11-05T00:00:00Z", "SEK_per_kWh": 40.0},
    {"time_start": "2023-11-05T01:00:00Z", "SEK_per_kWh": 45.0},
]


# Testa create_pandas_dataframe funktionen
def test_create_pandas_dataframe():
    # Anropa funktionen med exempeldata
    df = create_pandas_dataframe(sample_data)

    # Kontrollera om det returnerade objektet är en Pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Kontrollera antalet rader i DataFrame
    assert len(df) == len(sample_data[:24])

    # Kontrollera om kolumnerna finns i DataFrame
    assert "Tidpunkt på dygnet i (hh:mm)" in df.columns
    assert "Motsvarande pris i (kr/kWh)" in df.columns


# Testa create_pandas_table funktionen
def test_create_pandas_table():
    # Skapa en exempel Pandas DataFrame
    data = {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
    current_prices = pd.DataFrame(data)

    # Anropa create_pandas_table funktionen
    pandas_table = create_pandas_table(current_prices)

    # Kontrollera att resultatet är en HTML-tabell
    assert isinstance(pandas_table, str)


# Testa create_plotly_chart funktionen
def test_create_plotly_chart():
    # Skapa en exempel Pandas DataFrame
    data = {
        "Tidpunkt på dygnet i (hh:mm)": ["00:00", "01:00", "02:00"],
        "Motsvarande pris i (kr/kWh)": [0.1, 0.2, 0.3],
    }
    current_prices = pd.DataFrame(data)
    date = "2023-01-01"
    price_class = "SE3"

    # Anropa create_plotly_chart funktionen
    chart_html = create_plotly_chart(current_prices, date, price_class)

    # Kontrollera att resultatet är en HTML-diagram
    assert chart_html is not None


# Testa create_chart funktionen
def test_create_chart():
    # Skapa en exempel Pandas DataFrame
    data = {
        "Tidpunkt på dygnet i (hh:mm)": ["00:00", "01:00", "02:00"],
        "Motsvarande pris i (kr/kWh)": [0.1, 0.2, 0.3],
    }
    current_prices = pd.DataFrame(data)
    date = "2023-01-01"
    price_class = "SE3"

    # Anropa create_chart funktionen
    chart_html = create_chart(current_prices, date, price_class)

    # Kontrollera att resultatet är ett HTML-diagram
    assert chart_html is not None
