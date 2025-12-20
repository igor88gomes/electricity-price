[![Version](https://img.shields.io/github/v/tag/igor88gomes/electricity-price?label=version&sort=semver&color=%238b5cf6)](https://github.com/igor88gomes/electricity-price/tags)
[![CI – main](https://github.com/igor88gomes/electricity-price/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/ci.yaml)
[![Coverage](https://github.com/igor88gomes/electricity-price/raw/main/.github/badges/coverage.svg)](https://github.com/igor88gomes/electricity-price/actions/workflows/ci.yaml)
[![Secret Scan](https://github.com/igor88gomes/electricity-price/actions/workflows/secret-scan.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/secret-scan.yaml)
[![CD – DEV](https://github.com/igor88gomes/electricity-price/actions/workflows/docker-publish.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/docker-publish.yaml)
[![Promote STAGING](https://github.com/igor88gomes/electricity-price/actions/workflows/promote-staging.yaml/badge.svg?branch=main)](https://github.com/igor88gomes/electricity-price/actions/workflows/promote-staging.yaml)
[![Release PROD](https://github.com/igor88gomes/electricity-price/actions/workflows/release-prod.yaml/badge.svg)](https://github.com/igor88gomes/electricity-price/actions/workflows/release-prod.yaml)
[![Multi-arch](https://img.shields.io/badge/multi--arch-amd64%20%7C%20arm64-blue)](#)
[![GHCR image](https://img.shields.io/badge/GHCR-image-blue)](https://github.com/users/igor88gomes/packages/container/package/electricity-price)
![Trivy](https://img.shields.io/badge/Trivy-image%20scan-red)

> Av Igor Gomes

> Del av en GitOps-baserad leveranslösning (DEV/STAGING/PROD) med separat GitOps-repository.

## TL;DR

**Vad:** Flask-baserad webbapplikation som visar elpriser för olika delar av Sverige per datum (tabell + diagram), baserat på extern realtids-API.  

**Varför:** Byggd för att demonstrera produktionsnära DevOps- och plattformspraktiker kring en enkel applikation.  

**Värde:** Stateless design utan databas som ger en lättviktig applikation med enkel drift, säkra deployer och horisontell skalning. CI med tester/coverage, secret scanning och container image build; leverans sker via GitOps-promotion DEV/STAGING/PROD med immutable image-digest.
  
**Begränsningar:** Beroende av extern API och dess publiceringstider; begränsat datumintervall. Ingen autentisering eller caching (avsiktligt utanför scope).


# Elprisberäkning.se

Den Flask-baserade webbapplikationen låter användaren söka efter elpriser för olika delar av Sverige för ett valt datum. Applikationen visar timvisa elpriser (00:00–23:00). Data hämtas från en extern API, bearbetas med Pandas och presenteras i tabellform samt som interaktiva Plotly-diagram.


## Frontend – HTML, Jinja2 och Bootstrap

Applikationens frontend använder **Jinja2‑templates** och **Bootstrap 5** för en enkel och responsiv UI‑upplevelse ovanpå den API‑drivna logiken.

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

### Klona projektet

```bash
git clone https://github.com/igor88gomes/electricity-price.git
cd electricity-price
```

### Förutsättningar för containerbaserad körning

Följande behöver vara installerat på systemet:

- **Docker** med **Docker Compose**
  *eller*
- **Podman** med **Podman Compose**

Instruktionerna nedan använder **Docker** som standard.  
Vid användning av **Podman**, ersätt:
- `docker` med `podman`
- `docker compose` med `podman-compose`

### Välj ett alternativ för att komma igång

### Alternativ A: Kör med Docker Compose 

#### 1️⃣ Bygg och starta applikationen med ett kommando

```bash
docker compose up --build -d 
```

#### 2️⃣ Öppna i webbläsaren:

- Applikationen: http://localhost:38080/
- Health check: http://localhost:38080/healthz

> Första bygget kan ta några minuter (beroenden laddas ner). Efterföljande builds går snabbare tack vare cache.

### Alternativ B: Kör applikationen lokalt med virtuell miljö (utan container)

#### 1️⃣ Skapa virtuell miljö

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate  

# eller på Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
> Tips: Om PowerShell klagar på skriptpolicy, kör:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned och öppna ett nytt PowerShell-fönster.

#### 2️⃣ Installera beroenden

```bash
python -m pip install --upgrade pip

# och

pip install -r requirements.txt
```

#### 3️⃣ Starta applikationen

```bash

python -m application.app
```

#### 4️⃣ Öppna sedan i webbläsaren:  

http://localhost:5000/

---

### Testning lokalt (virtuell miljö)

För att köra alla tester:

```bash
pytest -q
```

---

## Viktiga endpoints

| Endpoint     | Funktion                             |
|--------------|--------------------------------------|
| `/`          | Startvy med formulär                 |
| `/calculate` | Beräknar och visar elprisdata (POST) |
| `/healthz`   | Liveness-check                       |
| `/readyz`    | Readiness-check                      |
| `/metrics`   | Prometheus-metrik                    |

Exempel på åtkomst:

http://localhost:38080/metrics

> **Obs:** Endpointen `/calculate` används via formuläret i webbgränssnittet och är inte avsedd att anropas direkt i webbläsaren (HTTP POST).

## CI/CD-pipelines (Build → PR till GitOps → Deployment)

Applikationen använder ett komplett GitOps-flöde över tre miljöer (DEV, STAGING, PROD).
Alla miljöer drivs av automatiska PR:er och alla pipelines återanvänder samma multi-arch manifest-digest som byggs i DEV.

### ● Secret Scan – Gitleaks 
### ● CI – Testning 
### ● CD till DEV – bygger multi-arch, kör SBOM-generering, Trivy image scan och publicerar manifest-digest innan PR öppnas
### ● Promote STAGING – återanvänder exakt samma digest som DEV
### ● Release PROD – retaggar samma manifest (ingen rebuild)

**GitOps-repo (DEV/STAGING/PROD):** https://github.com/igor88gomes/electricity-price-gitops


## Projektstruktur

```text
electricity-price/
├── .github/workflows/      # CI/CD-workflows (CI, Docker publish, secret-scan, promote-staging, release-prod)
├── application/            # Flask-applikation: routes, logik, templates och statiska filer
├── docs/                   # Dokumentation (t.ex. skärmdumpar, extra beskrivningar)
├── tests/                  # Pytest-tester för applikationen
├── .dockerignore           # Utesluter onödiga filer från Docker build-context
├── .gitignore              # Ignorerade filer (virtuell miljö, cache, rapporter, etc.)
├── .gitleaks.toml          # Regler för secret scanning (Gitleaks)
├── .ruff.toml              # Konfiguration för Ruff (lint och format)
├── docker-compose.yaml     # Lokal körning med Docker Compose
├── Dockerfile              # Bygger Docker-image för Flask-applikationen
├── pytest.ini              # Pytest-konfiguration (plugins, options)
├── requirements.txt        # Python-beroenden för app + tester
└── README.md               # Projektöversikt, användning och arkitektur
```

---

## Kontakt

Igor Gomes — DevOps Engineer  

**E-post:** [igor88gomes@gmail.com](mailto:igor88gomes@gmail.com)
[LinkedIn](https://www.linkedin.com/in/igor-gomes-5b6184290) 