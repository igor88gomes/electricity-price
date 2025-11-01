import pandas as pd
import plotly.graph_objects as go


# Funktion för att skapa en Pandas DataFrame från elpris_data
def create_pandas_dataframe(elpris_data):
    """
    Skapa en Pandas DataFrame från elprisdata.

    Denna funktion extraherar de första 24 timmarna
    av prisdata och skapar en Pandas DataFrame
    med två kolumner: tid och pris.

    Args:
        elpris_data (list): En lista med elprisdata.

    Returns:
        pd.DataFrame: En Pandas DataFrame som innehåller
        tid och prisdata.
    """
    # Extrahera de första 24 timmarna av prisdata
    current_prices = [(hour, price['SEK_per_kWh']) for hour, price in enumerate(elpris_data[:24])]

    # Skapa en Pandas DataFrame med två kolumner: tid och pris
    df = pd.DataFrame({'Tidpunkt på dygnet i (hh:mm)': [f"{hour:02d}:00" for hour, _ in current_prices],
                       'Motsvarande pris i (kr/kWh)': [price for _, price in current_prices]})
    return df


# Funktion för att skapa en HTML-tabell från en Pandas DataFrame
def create_pandas_table(current_prices):
    """
    Skapa en HTML-tabell från en Pandas DataFrame.

    Denna funktion konverterar en Pandas DataFrame
    till en HTML-tabell med specificerad formatering.

    Args:
        current_prices (pd.DataFrame): En Pandas
        DataFrame med prisdata.

    Returns:
        str: En HTML-tabell som en sträng.
    """
    # Konvertera Pandas DataFrame till en HTML-tabell med specificerad formatering
    pandas_table = current_prices.to_html(classes="table table-bordered table-striped", justify='left', index=False,
                                          escape=False)
    return pandas_table  # Returnera HTML-tabellen


# Funktion för att skapa en Plotly-diagram
def create_plotly_chart(current_prices, date, price_class):
    """
    Skapa ett Plotly-diagram från prisdata.

    Denna funktion skapar ett Plotly-diagram baserat
    på prisdata, datum och prisklass.

    Args:
        current_prices (pd.DataFrame): En Pandas
        DataFrame med prisdata.

        date (str): Datum för datan.
        price_class (str): Prisklass för datan.

    Returns:
        str: Ett HTML-diagram som en sträng.
    """
    # Skapa en ny Plotly-figur
    fig = go.Figure()

    # Lägg till en linjetrajekt till figuren med tid och prisdata
    fig.add_trace(go.Scatter(
        x=current_prices['Tidpunkt på dygnet i (hh:mm)'],
        y=current_prices['Motsvarande pris i (kr/kWh)'],
        mode='lines'
    ))

    # Ställ in diagramlayout med titel och axelrubriker
    fig.update_layout(
        title=f'Datum: {date}<br>Prisklass: {price_class}',
        xaxis_title='Tidpunkt på dygnet i (hh:mm)',
        yaxis_title='Motsvarande pris i (kr/kWh)'
    )

    # Konvertera diagrammet till HTML och returnera det
    chart_html = fig.to_html(full_html=False)
    return chart_html


# Funktion för att skapa ett Plotly-diagram från prisdata, datum och prisklass
def create_chart(current_prices, date, price_class):
    """
    Skapa ett Plotly-diagram från prisdata, datum
    och prisklass.

    Denna funktion skapar ett Plotly-diagram baserat
    på den tillhandahållna datan, datum och prisklass.

    Args:
        current_prices (pd.DataFrame): En Pandas
        DataFrame med prisdata.

        date (str): Datum för datan.
        price_class (str): Prisklass för datan.

    Returns:
        str: Ett HTML-diagram som en sträng.
    """
    # Skapa ett Plotly-diagram med den tillhandahållna datan
    chart_html = create_plotly_chart(current_prices, date, price_class)
    return chart_html  # Returnera HTML-diagrammet
