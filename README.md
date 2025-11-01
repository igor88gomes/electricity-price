# Elprisberäkning.se ⚡

En Flask-baserad webbapplikation där användaren kan söka efter elpriser i Sverige för ett valt datum.  
Data hämtas från en extern API, bearbetas med Pandas för korrekt databehandling, och presenteras sedan i en tabell samt som interaktiva Plotly-diagram.

---

## ✨ Funktioner

- Formulär för att välja datum
- Hämtar elprisdata automatiskt via API
- Visar resultat i tabellformat
- Interaktiv diagram-visualisering
- Hälsokontroller: `/healthz` och `/readyz`
- Prometheus-metrik på `/metrics`
- Fullt enhetstestad med `pytest`

---

## 🛠️ Teknikstack

| Komponent         |            Version / Info             |
|-------------------|---------------------------------------|
| Python            | 3.12                                  |
| Flask             | 3.0                                   |
| Pandas            | Databehandling och tabellpresentation |
| Plotly            | Interaktiva diagram                   |
| pytest            | Enhetstestning                        |
| prometheus-client | Metrik och monitoring                 |


Se `requirements.txt` för full lista av beroenden.

---

## 🚀 Installation & Körning (lokalt)

### 1️⃣ Skapa virtuell miljö

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# eller på Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
> Tips: Om PowerShell klagar på skriptpolicy, kör:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned och öppna ett nytt PowerShell-fönster.


### 2️⃣ Installera beroenden

```bash
python -m pip install --upgrade pip

# och

pip install -r requirements.txt
```

### 3️⃣ Starta applikationen

```bash
flask run

# eller

python -m application.app
```

Öppna sedan i webbläsaren:  
👉 http://localhost:5000/

---

## ✅ Testning

För att köra alla tester:

```bash
pytest -q
```

---

## 🔍 Viktiga endpoints

| Endpoint   | Funktion             |
|------------|----------------------|
| `/`        | Startvy med formulär |
| `/results` | Visar elprisdata     |
| `/healthz` | Liveness-check       |
| `/readyz`  | Readiness-check      |
| `/metrics` | Prometheus-metrik    |

---

## 🗂️ Projektstruktur

```
application/
├─ app.py
├─ data_fetcher.py
├─ date_utils.py
├─ electricity_price_data.py
├─ electricity_price_visualization.py
├─ menu_options.py
├─ user_input.py
├─ templates/
└─ static/
tests/
requirements.txt
README.md
```

---

## 👤 Kontakt

Igor Gomes — DevOps Engineer  
[LinkedIn](https://www.linkedin.com/in/igor-gomes-5b6184290) 
**E-post:** [igor88gomes@gmail.com](mailto:igor88gomes@gmail.com)

---
