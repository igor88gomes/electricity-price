from datetime import datetime, timedelta


def get_min_max_allowed_dates():
    """
    Hämta minsta och största tillåtna datum.

    Denna funktion sätter det minsta tillåtna datumet till
    '2022-11-01' och det största tillåtna datumet till
    dagens datum plus en dag.

    Returns:
        datetime, datetime: Det minsta och det största
        tillåtna datumet som datetime-objekt.
    """
    # Sätt det minsta tillåtna datumet till '2022-11-01'
    min_date = datetime(2022, 11, 1)

    # Sätt det största tillåtna datumet till dagens datum plus en dag
    max_date = datetime.now() + timedelta(days=1)

    return min_date, max_date  # Returnera det minsta och det största tillåtna datumet


# Funktion för att hämta standardvärden för formulär
def get_default_form_field_values():
    """
    Hämta standardvärden för formuläret.

    Denna funktion hämtar det aktuella datumet och
    extraherar året, månaden och dagen. Den sätter
    standardprisklassen till 'SE3'.

    Returns:
        int, int, int, str: År, månad, dag och
        standardprisklass.
    """
    # Hämta aktuellt datum och tid
    current_date = datetime.now()

    # Extrahera år, månad och dag från aktuellt datum
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Sätt standardprisklassen till 'SE3'
    price_class = "SE3"

    return year, month, day, price_class  # Returnera standardvärden för formuläret


# Funktion för att kontrollera om ett angivet datum är giltigt
def is_valid_date(year, month, day):
    """
    Kontrollera om ett angivet datum är giltigt.

    Denna funktion skapa ett datetime-objekt från
    det angivna året, månaden och dagen. Den sätter
    det minsta tillåtna datumet till '2022-11-01'
    och det största tillåtna datumet till dagens
    datum plus en dag. Funktionen kontrollerar om
    det angivna datumet ligger inom det tillåtna
    intervallet.

    Args:
        year (int): År som ska kontrolleras.
        month (int): Månad som ska kontrolleras.
        day (int): Dag som ska kontrolleras.

    Returns:
        bool: True om datumet är giltigt, annars False.
    """
    try:
        # Skapa ett datetime-objekt från det angivna året, månaden och dagen
        date = datetime(year, month, day)

        # Sätt det minsta tillåtna datumet till '2022-11-01'
        min_date = datetime(2022, 11, 1)

        # Sätt det största tillåtna datumet till dagens datum plus en dag
        max_date = datetime.now() + timedelta(days=1)

        # Kontrollera om datumet ligger inom det tillåtna intervallet
        return min_date <= date <= max_date
    except ValueError:
        return False  # Hantera fallet där datumet inte är giltigt


# Funktion för att validera ett angivet datum
def validate_date(year, month, day):
    """
    Validera ett angivet datum.

    Denna funktion använder is_valid_date-funktionen
    för att kontrollera om det angivna datumet är
    giltigt. Om datumet inte är giltigt, returneras
    en felmeddelande och en statuskod 404.

    Args:
        year (int): År att validera.
        month (int): Månad att validera.
        day (int): Dag att validera.

    Returns:
        str or None, int: Ett felmeddelande om datumet
        inte är giltigt, annars None, och statuskod 404
        om fel uppstår.
    """
    if not is_valid_date(year, month, day):
        return "Sidan är begränsad till en dag i förväg och senast 2022-11-01 bakåt i tiden.", 404
