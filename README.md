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

## 🧭 The three main screens

The app is split into three sections, reachable from the bottom navigation bar:

### 1. Dashboard (home)
Your financial overview at a glance:
- **Ticker** — a carousel showing the current price/value of your assets and the latest exchange rates.
- **Total balance** — your current total net worth in EUR.
- **Portfolio value chart** — how your total wealth evolved over a chosen time period (all / day / week / month / year).
- **Asset comparison** — compare the performance of selected assets side by side.
- **Asset allocation** — a doughnut chart of how your money is split by asset type.
- **Asset list** — every asset with its name, type, quantity and value in EUR.
- The **＋ button** (bottom right) opens a form to **add a new reading** (see below).

### 2. Statistics
A dedicated space for historical insights — the evolution of your total portfolio and individual assets over time.

### 3. Settings
Where you manage the "building blocks" of your portfolio, in collapsible sections:
- **Assets** — add, rename, change type/currency, set an icon, and manage each asset's **prices**.
- **Exchange Rates** — add, edit or delete currency exchange rates (always relative to EUR).
- **Currencies** — add new currencies and rename them.
- **Asset Types** — add new types and rename them.

---

## ✏️ How to use it

### Adding a new asset
1. Go to **Settings → Assets**.
2. Fill in the asset **name** (e.g. "Bitcoin"), choose its **type** (e.g. CRYPTO) and **currency** (e.g. EUR).
3. Optionally paste an **icon** (a base64 image) to make it recognizable.
4. Click **Add Asset**.

> 💡 Most new accounts start with a "Cash" asset in EUR (a default `EUR` / `CASH` asset is created automatically when you install).

### Recording a price for an asset
An asset's **price** is how much one unit is worth (e.g. price of 1 BTC in EUR).
1. In **Settings → Assets**, open the asset row and expand **Prices**.
2. Click **Add** and enter the **date** and **price**.
3. To correct an existing entry, just edit the date or price directly (changes are saved automatically). Use ✕ to delete a price.

### Recording what you own (readings/holdings)
A **reading** is how much of an asset you currently hold.
- On the **Dashboard**, tap the **＋** button.
- Choose the asset and enter the **quantity** (leave fields empty for assets you don't want to change).
- Click **Save**.

> 💡 myInves calculates each asset's EUR value as: **quantity × price × exchange rate to EUR**.

### Adding an exchange rate
Rates are always **relative to EUR** — i.e. the value of 1 unit of that currency in EUR (for example, 1 USD = 0.90 EUR).
1. Go to **Settings → Exchange Rates**, expand the section and select the **currency** (EUR is excluded).
2. Enter the **date** and the **rate**.
3. Click **Add**. Existing entries can be edited or deleted the same way.

### Managing currencies and asset types
- Add a **new currency** via **Settings → Currencies**.
- Add a **new asset type** via **Settings → Asset Types**.
- Rename a currency/type by editing its label (saved automatically). The code (e.g. `EUR`, `CASH`) cannot be changed, since it's the technical identifier.

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
