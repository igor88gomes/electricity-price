from flask import request


# Funktion för att hämta användarinput från formuläret
def get_user_input():
    # Hämta värdena från formuläret och konvertera dem till lämpliga datatyper
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])
    price_class = request.form["price_class"]
    return year, month, day, price_class
