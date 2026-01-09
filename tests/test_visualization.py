import pandas as pd
import pytest

from application.electricity_price_visualization import (
    create_chart,
    create_pandas_dataframe,
    create_pandas_table,
)


def test_create_pandas_dataframe():
    sample_data = [
        {"time_start": f"2023-11-05T{hour:02d}:00:00Z", "SEK_per_kWh": 40.0 + hour}
        for hour in range(24)
    ]

    df = create_pandas_dataframe(sample_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 24
    assert "Tidpunkt på dygnet i (hh:mm)" in df.columns
    assert "Motsvarande pris i (kr/kWh)" in df.columns


def test_create_pandas_dataframe_raises_on_incomplete_data():
    sample_data = [
        {"time_start": "2023-11-05T00:00:00Z", "SEK_per_kWh": 40.0},
        {"time_start": "2023-11-05T01:00:00Z", "SEK_per_kWh": 45.0},
    ]

    with pytest.raises(ValueError, match="Förväntade minst 24 timposter från upstream-API"):
        create_pandas_dataframe(sample_data)


def test_create_pandas_table():
    current_prices = pd.DataFrame(
        {
            "Tidpunkt på dygnet i (hh:mm)": ["00:00", "01:00"],
            "Motsvarande pris i (kr/kWh)": [0.1, 0.2],
        }
    )

    html = create_pandas_table(current_prices)
    assert isinstance(html, str)
    assert "<table" in html


def test_create_pandas_table_includes_bootstrap_classes():
    current_prices = pd.DataFrame(
        {
            "Tidpunkt på dygnet i (hh:mm)": ["00:00"],
            "Motsvarande pris i (kr/kWh)": [0.1],
        }
    )

    html = create_pandas_table(current_prices)
    assert "table table-bordered table-striped" in html


def test_create_chart():
    current_prices = pd.DataFrame(
        {
            "Tidpunkt på dygnet i (hh:mm)": ["00:00", "01:00", "02:00"],
            "Motsvarande pris i (kr/kWh)": [0.1, 0.2, 0.3],
        }
    )

    html = create_chart(current_prices, "2023-01-01", "SE3")
    assert isinstance(html, str)
    assert "<div" in html
