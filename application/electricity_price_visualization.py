import pandas as pd
import plotly.graph_objects as go


def create_pandas_dataframe(elpris_data: list[dict]) -> pd.DataFrame:
    if not isinstance(elpris_data, list) or len(elpris_data) < 24:
        raise ValueError("Förväntade minst 24 timposter från upstream-API")

    current_prices = [(hour, price["SEK_per_kWh"]) for hour, price in enumerate(elpris_data[:24])]

    return pd.DataFrame(
        {
            "Tidpunkt på dygnet i (hh:mm)": [f"{hour:02d}:00" for hour, _ in current_prices],
            "Motsvarande pris i (kr/kWh)": [price for _, price in current_prices],
        }
    )


def create_pandas_table(current_prices: pd.DataFrame) -> str:
    return current_prices.to_html(
        classes="table table-bordered table-striped",
        justify="left",
        index=False,
        escape=False,
    )


def create_chart(current_prices: pd.DataFrame, date: str, price_class: str) -> str:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=current_prices["Tidpunkt på dygnet i (hh:mm)"],
            y=current_prices["Motsvarande pris i (kr/kWh)"],
            mode="lines",
        )
    )

    fig.update_layout(
        title=f"Datum: {date}<br>Prisklass: {price_class}",
        xaxis_title="Tidpunkt på dygnet i (hh:mm)",
        yaxis_title="Motsvarande pris i (kr/kWh)",
    )

    return fig.to_html(full_html=False)
