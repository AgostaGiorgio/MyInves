# myInves 📈

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue.js-4C4C4C?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

> 👋 This guide is written for people who want to **use** myInves. It focuses on *how* the platform works and how to get the most out of it. For technical/developer details (setup, configuration, API), see the **[Backend](backend/README.md)** and **[Frontend](frontend/README.md)** READMEs.

---

## What is myInves?

**myInves** is a personal finance platform that lets you track your **entire net worth in one place**. Whether you own crypto, ETFs, cash, gold, or bank accounts, myInves gives you a clear, up-to-date overview of your money and how it changes over time.

Everything runs **self-hosted**, so your financial data stays completely private and under your control.

## What can it do for me?

| Feature | What it means for you |
|---------|----------------------|
| 📊 **Track many asset types** | Cryptocurrencies, stocks/ETFs, cash, precious metals, bank accounts |
| 💱 **Multi-currency support** | Holdings in different currencies are converted and shown in EUR |
| 💼 **Net worth dashboard** | One clean screen with your total wealth and each asset's performance |
| 📈 **Historical insights** | Interactive charts showing how your total portfolio and individual assets evolved |
| 🖼️ **Custom icons** | Give each asset a recognizable icon (e.g. a logo) |
| 🔒 **Private & self-hosted** | Full control over your data by running it yourself |

---

## 🐳 Quick start (Docker Compose)

Run the whole platform (**PostgreSQL 15 + backend + frontend**) with a single command. All you need is **Docker** with the Compose plugin.

```sh
git clone <this-repo> && cd myinves
docker compose up --build
```

Then open **http://localhost:3000**.

- The backend API is exposed at **http://localhost:8000**.
- The database lives in a named volume (`myinves_db`) and survives restarts.
- On startup the backend **automatically applies the database migrations**.
- Stop with `Ctrl+C` (or `docker compose down`); add `-v` to also wipe the data.

You can override the defaults with environment variables (or a `.env` file next to `docker-compose.yml`):

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRESQL_USER` | `myinves` | Database user |
| `POSTGRESQL_PASSWORD` | `myinves` | Database password |
| `POSTGRESQL_DATABASE` | `myinves` | Database name |
| `BACKEND_PORT` | `8000` | Host port for the API |
| `FRONTEND_PORT` | `3000` | Host port for the web app |
| `VITE_API_BASE_URL` | `http://localhost:8000` | API URL as seen by the **browser** |
| `ORBIT_API_URL` | *(empty)* | Optional Orbit registration URL |

> 💡 If you serve the frontend on a different host/port, set `VITE_API_BASE_URL` accordingly — it is baked into the frontend at **build time**.

---

## 🧭 The main screens

The app is split into four sections, reachable from the navigation bar (a bottom bar on mobile, a vertical rail on desktop):

### 1. Dashboard (home)
Your financial overview at a glance:
- **Period filter** — 3M / 6M / 12M / 24M / All.
- **Hero card** — your current total net worth, the change vs last month, and two tabs:
  - **Performance** — line chart of how your total wealth evolved over the selected period.
  - **Composition** — doughnut of your holdings split by **asset type**.
- **Markets** — the latest asset prices and currency exchange rates, each with a small sparkline of its last readings.

### 2. Assets
- Every asset is listed **grouped by type**; tap one to open its **detail page**.
- The **＋** button (top right) creates a new asset.
- The detail page shows current value, P&L, quantity/average cost, a **value-over-time** chart, its **orders**, **details** and **prices**; from there you can update the position, add an order, edit the average cost, manage prices and change the icon.

### 3. Statistics
A dedicated space for insights:
- **Growth** — monthly change bars (green for gains, red for losses).
- **Allocation** — doughnut split into **Dynamic / Static / Other** (tap the ⓘ to see how types are grouped).
- **By type** and **Assets** — month-over-month and average monthly growth, with P&L.

### 4. Currencies
Where you manage the "building blocks":
- **Currencies** — add new currencies and rename them.
- **Exchange rates** — add, edit or delete currency exchange rates (always relative to EUR).

### Add reading (header button)
The **＋ Add reading** button in the header opens a dedicated page to update several assets at once (see below).


---

## ✏️ How to use it

### Adding a new asset
1. Go to the **Assets** page and tap the **＋** button.
2. Enter the asset **name** (e.g. "Bitcoin"), choose its **type** (e.g. CRYPTO) and **currency** (e.g. EUR), and optionally **upload an icon** (stored as base64).
3. Optionally fill in the type-specific **details** (e.g. ISIN/ticker for an ETF, bank/interest rate for an account).
4. Tap **Create asset**.

> 💡 A "Cash" asset in EUR (a default `EUR` / `CASH` asset) is created automatically when you install. The set of asset types is fixed.

### Recording a price for an asset
An asset's **price** is how much one unit is worth (e.g. price of 1 BTC in EUR).
1. Open the asset **detail page** and scroll to **Prices**.
2. Tap **Add** and enter the **date** and **price**.
3. Edit or delete existing entries from the same list (pencil / trash icons).

### Recording what you own (readings) and orders
- Tap **＋ Add reading** in the header to update **several assets at once**:
  - enter the **new total value/quantity** (leave blank for assets you don't want to change), or
  - for assets that support orders (ETF / Crypto / Metal), switch the row to **Order** and record a **buy/sell** (side, quantity, amount).
- For a single asset, open its detail page and use **Update position** (quantity, average cost, cost basis) or **Add order**.

> 💡 myInves calculates each asset's EUR value as: **quantity × price × exchange rate to EUR**. For value-tracked types (cash, bank accounts, generic assets) the reading itself is the value.

### Adding an exchange rate
Rates are always **relative to EUR** — i.e. the value of 1 unit of that currency in EUR (for example, 1 USD = 0.90 EUR).
1. Go to **Currencies → Exchange rates** and tap **＋**.
2. Select the **currency** (EUR is excluded) and enter the **date** and the **rate**.
3. Tap **Add rate**. Existing entries can be edited or deleted the same way.

### Managing currencies
- Add a **new currency** from the **Currencies** page (tap **＋**).
- Rename a currency by opening it and editing its label. The code (e.g. `EUR`) cannot be changed, since it's the technical identifier.
- **Asset types are fixed** — they are seeded with the platform and cannot be created or renamed from the UI.


---

## 🤖 Automation (optional)

myInves can be combined with an **n8n pipeline** to automate data ingestion and history snapshots:
- Automatically fetches the latest ETF values and currency exchange rates.
- Periodically saves snapshots of your assets and net worth to build the historical record.

You can find the workflow template & specs in the [myInves n8n-workflows repository](https://github.com/AgostaGiorgio/N8N-workflows/tree/master/myinves).

---

## 🚀 Deployment

The platform is deployed via **ArgoCD** — see the [ArgoCD Application definition](https://github.com/AgostaGiorgio/HomeLab/tree/master/apps/myinves) for configuration.

**Docker build commands** (run from the repository root):

```sh
# Backend (linux/amd64)
docker buildx build --platform linux/amd64 -t registry/myinves_be:x.y.z backend/

# Frontend (linux/amd64) — VITE_API_BASE_URL is needed at build time for the nginx stage
docker buildx build --platform linux/amd64 \
  --build-arg VITE_API_BASE_URL=https://backend:8000 \
  -t registry/myinves_fe:x.y.z frontend/
```

---

## 📄 License

> 📝 **MIT License** — Feel free to use and modify!
