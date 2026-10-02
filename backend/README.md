# myInves — Backend

FastAPI-powered REST API for the **myInves** investment tracking platform. It handles assets, prices, exchange rates, readings (portfolio holdings) and historical insights on top of a PostgreSQL database.

> For user-facing documentation on how to use the platform, see the [root README](../README.md).

---

## 🛠️ Tech Stack

| Technology | Version/Notes | Description |
|------------|---------------|-------------|
| **Python** | 3.10+ (`^3.10.12`) | Runtime |
| **FastAPI** | `^0.110.0` | Modern async web framework |
| **SQLAlchemy 2.0** | `^2.0.46` | Async SQLAlchemy with `asyncpg` |
| **asyncpg** | `^0.31.0` | Async PostgreSQL driver |
| **Poetry** | — | Dependency management |
| **yoyo-migrations** | `^9.0.0` (dev) | Database migrations |
| **dependency-injector** | `^4.41.0` | DI container |
| **pydantic / pydantic-settings** | `^2.12.5` / `^2.13.1` | Validation & configuration |
| **Uvicorn** | `^0.28.0` | ASGI server |

> **Database:** PostgreSQL (via SQLAlchemy async + asyncpg).

### DevOps

> **Kubernetes & ArgoCD** — deployed via an [ArgoCD Application](https://github.com/AgostaGiorgio/HomeLab/tree/master/apps/myinves).

---

## 📁 Project Structure

```
backend/
├── src/
│   ├── main.py                  # Application entry point (FastAPI app)
│   ├── di.py                    # Dependency injection container
│   ├── config/                  # Configuration (pydantic-settings)
│   │   └── app_config.py
│   ├── clients/
│   │   └── orbit_client.py      # Optional Orbit registration/telemetry client
│   ├── db/
│   │   ├── db.py                # Async SQLAlchemy session
│   │   └── models/              # Pydantic models (asset, price, exchange, reading, lookup, enums)
│   ├── routers/
│   │   └── router.py            # API endpoints
│   └── services/
│       ├── portfolio_repository.py  # Data access layer (raw SQL queries)
│       ├── portfolio_service.py     # Business logic
│       └── queries.py               # Raw SQL statements
├── migrations/                  # Yoyo SQL migrations (0001_... to 0012_...)
├── pyproject.toml               # Python dependencies
├── .env / .env.example          # Environment configuration
└── Dockerfile
```

---

## ⚙️ Configuration

Settings are loaded from `backend/.env` via `pydantic-settings` (see `.env.example`):

| Variable | Description |
|----------|-------------|
| `POSTGRESQL_USER` | PostgreSQL user |
| `POSTGRESQL_PASSWORD` | PostgreSQL password |
| `POSTGRESQL_HOST` | PostgreSQL host |
| `POSTGRESQL_PORT` | PostgreSQL port |
| `POSTGRESQL_DATABASE` | Database name |
| `ORBIT_API_URL` | *(optional)* Orbit registration URL. When set, the backend pings it on a daemon thread every hour. Disabled when empty. |

CORS is permissive (all origins) by default.

---

## 🚀 Local Development

**Prerequisites:** Python 3.10+, [Poetry](https://python-poetry.org/), and a reachable PostgreSQL instance.

```bash
cd backend
poetry install
```

Apply the database migrations (SQL files in `backend/migrations/`):

```bash
yoyo apply --database <db_url> ./migrations
```

Start the development server:

```bash
poetry run python src/main.py
```

---

## 🗂️ Database Migrations

Migrations are SQL files under `backend/migrations/`, managed with **yoyo**.

```bash
cd backend
yoyo apply --database <db_url> ./migrations
```

Latest migrations seed the lookup tables (`currencies`, `asset_types`), add typed-asset metadata
(`assets.details`), the order ledger (`asset_orders`) and the cost basis (`asset_readings.cost_price`).

---

## 🌐 API Endpoints

All endpoints are prefixed with `/api/v1`.

### Assets
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/assets` | Get all assets with current prices and type details |
| `GET` | `/assets/{id}/icon` | Get asset icon |
| `POST` | `/assets` | Create a new asset (type-specific `details` validated) |
| `PATCH` | `/assets/{id}` | Update an asset |
| `GET` | `/assets/{id}/orders` | List buy/sell orders for a position asset |
| `POST` | `/assets/{id}/orders` | Register an order; updates position and weighted-average cost |

### Asset Prices
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/assets/{id}/prices` | List prices for an asset |
| `POST` | `/assets/{id}/prices` | Add a price for an asset |
| `PATCH` | `/prices/{price_id}` | Update a price |
| `DELETE` | `/prices/{price_id}` | Delete a price |

### Exchange Rates
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/exchange-rates` | Current month's latest rate per currency |
| `GET` | `/exchange-rates/all` | All exchange rates |
| `POST` | `/exchange-rates` | Add an exchange rate (always expressed in EUR) |
| `PATCH` | `/exchange-rates/{id}` | Update an exchange rate |
| `DELETE` | `/exchange-rates/{id}` | Delete an exchange rate |

### Portfolio & History
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/portfolio` | Current portfolio with EUR totals, cost basis and unrealized P&L |
| `GET` | `/portfolio/history?period=<all\|1d\|1w\|1m\|1y>` | Portfolio history |
| `GET` | `/assets/history` | Asset history |
| `POST` | `/readings` | Add one or more holdings readings (optional `cost_price`) |

### Lookups
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/currencies` | List currencies |
| `POST` | `/currencies` | Create a currency |
| `PATCH` | `/currencies/{code}` | Rename a currency label |
| `GET` | `/asset-types` | List asset types (fixed catalog, read-only) |

> `asset_types` is a **fixed catalog** managed via migrations — it can no longer be created or renamed at runtime.

Interactive OpenAPI docs are available at `{host}/docs` when the server is running.

---

## 📋 Data Models

### Asset Types
| Type | Description |
|------|-------------|
| `ETF` | Exchange-traded funds |
| `CRYPTO` | Cryptocurrencies |
| `METAL` | Precious metals (gold/silver via `details.metal`) |
| `CASH` | Cash holdings |
| `BANK_ACCOUNT` | Bank accounts with interest |
| `BANK_ACCOUNT_STATIC` | Static bank accounts |
| `OTHER` | Generic assets (watches, cars, real estate, ...) |

> `currencies` is stored as a lookup table with `TEXT` code columns; `asset_types` is a fixed catalog seeded via migrations.

### Assets: type-specific details and tracking
Each asset stores optional type-specific metadata in `assets.details` (JSONB), validated per `asset_type`
(e.g. ETF `isin`/`ticker`, METAL `metal`/`purity`, bank `iban`/`interest_rate`). Fields not valid for the
chosen type are rejected with `422`.

Tracking is implicit:
- `CASH`, `BANK_ACCOUNT`, `BANK_ACCOUNT_STATIC`, `OTHER` are **value-tracked**: the reading is the value
  held, market prices are rejected.
- `ETF`, `CRYPTO`, `METAL` use **quantity × market price** when prices exist, otherwise fall back to the
  value held (e.g. tracking a whole broker total like "Binance"/"IBKR").

Position assets can record **orders** (`/assets/{id}/orders`). Each order updates the latest reading and the
weighted-average `cost_price`, which powers the unrealized P&L shown in `/portfolio` and `/statistics`.

### Currencies (seeded)
| Code | Name |
|------|------|
| `EUR` | Euro |

> Exchange rates are always relative to EUR (i.e. value of 1 unit of the currency in EUR).

---

## 🔄 Automation & Data Ingestion

The platform leverages an **n8n pipeline** for automated data ingestion and historical snapshots:

- **Automated Fetching** — retrieves the latest ETF values and currency exchange rates
- **History Tracking** — periodically saves snapshots of assets and net worth to build the historical record
- **n8n Workflow** — template & technical specs in the [myInves n8n-workflows repository](https://github.com/AgostaGiorgio/N8N-workflows/tree/master/myinves)

---

## 🐳 Docker

```sh
# Backend (linux/amd64)
docker buildx build --platform linux/amd64 -t registry/myinves_be:x.y.z .
```

The image runs `uvicorn src.main:app --port 8080 --host 0.0.0.0`.
