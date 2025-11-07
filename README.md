[![CI – main](https://github.com/igor88gomes/electricity-price/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/ci.yaml)
[![Test Coverage](https://github.com/igor88gomes/electricity-price/raw/main/.github/badges/coverage.svg)](https://github.com/igor88gomes/electricity-price/actions/workflows/ci.yaml)
[![Secret Scan](https://github.com/igor88gomes/electricity-price/actions/workflows/secret-scan.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/secret-scan.yaml)
[![CD – DEV](https://github.com/igor88gomes/electricity-price/actions/workflows/docker-publish.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/docker-publish.yaml)
[![Promote STAGING](https://github.com/igor88gomes/electricity-price/actions/workflows/promote-staging.yaml/badge.svg)](https://github.com/igor88gomes/electricity-price/actions/workflows/promote-staging.yaml)
[![Release PROD](https://github.com/igor88gomes/electricity-price/actions/workflows/release-prod.yaml/badge.svg)](https://github.com/igor88gomes/electricity-price/actions/workflows/release-prod.yaml)
[![Multi-arch](https://img.shields.io/badge/multi--arch-amd64%20%7C%20arm64-blue)](#)
[![GHCR image](https://img.shields.io/badge/GHCR-image-blue)](https://github.com/users/igor88gomes/packages/container/package/electricity-price)

# Elprisberäkning.se ⚡

En Flask-baserad webbapplikation där användaren kan söka efter elpriser i Sverige för ett valt datum.  
Data hämtas från en extern API, bearbetas med Pandas för korrekt databehandling, och presenteras sedan i en tabell samt som interaktiva Plotly-diagram.

---

## Funktioner

- Formulär för att välja datum
- Hämtar elprisdata automatiskt via API
- Visar resultat i tabellformat
- Interaktiv diagram-visualisering
- Hälsokontroller: `/healthz` och `/readyz`
- Prometheus-metrik på `/metrics`
- Fullt enhetstestad med `pytest`

---

## Teknikstack

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

## Installation & Körning (lokalt)

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

## Testning

För att köra alla tester:

```bash
pytest -q
```

---

## Viktiga endpoints

| Endpoint   | Funktion             |
|------------|----------------------|
| `/`        | Startvy med formulär |
| `/results` | Visar elprisdata     |
| `/healthz` | Liveness-check       |
| `/readyz`  | Readiness-check      |
| `/metrics` | Prometheus-metrik    |

---

## Projektstruktur

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

## Kontakt

Igor Gomes — DevOps Engineer  
[LinkedIn](https://www.linkedin.com/in/igor-gomes-5b6184290) 
**E-post:** [igor88gomes@gmail.com](mailto:igor88gomes@gmail.com)

---
