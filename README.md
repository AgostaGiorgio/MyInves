# myInves 📈 - Investment Tracking Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue.js-4C4C4C?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

**myInves** is a minimal and effective personal finance platform designed to help you track your entire net worth in one place. Whether it's **Crypto**, **ETFs**, **Cash**, **Bank Accounts**, or other assets, myInves provides a clear overview of your financial evolution over time.

---

## ✨ Key Features

| Emoji | Feature | Description |
|:-----:|---------|-------------|
| 📊 | **Multi-Asset Tracking** | Effortlessly track diverse asset classes including cryptocurrencies, traditional stocks/ETFs, cash, and precious metals |
| 💱 | **Exchange Rate Tracking** | Built-in support for EUR, USD, AED currencies |
| 💼 | **Net Worth Dashboard** | A clean, minimal summary of your current total wealth and individual asset performance |
| 📈 | **Historical Insights** | Visualize the evolution of your total portfolio and individual assets through interactive charts |
| 📉 | **Asset History** | Individual asset value tracking over time |
| 🖼️ | **Custom Icons** | Add base64-encoded icons for assets |
| 💨 | **Clean UI** | Built with a focus on simplicity and ease of use |
| 🌐 | **REST API** | Full FastAPI backend with async operations |
| 🔒 | **Self-Hosted & Private** | Keep full control over your financial data by running the stack locally |

---

## 🏗️ Project Structure

```
myinves/
├── backend/                   # 🐍 FastAPI backend
│   ├── src/
│   │   ├── main.py           # 📍 Application entry point
│   │   ├── di.py             # 🧩 Dependency injection container
│   │   ├── config/          # ⚙️ Configuration
│   │   ├── db/              # 🗄️ Database models and connection
│   │   │   └── models/      # 📋 Pydantic models
│   │   ├── routers/         # 🛤️ API endpoints
│   │   └── services/        # 🔧 Business logic
│   ├── migrations/          # 📂 SQL migrations
│   └── pyproject.toml      # 📦 Python dependencies
├── frontend/                 # 🎨 Vue.js 3 frontend
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── services/       # 📡 API client
│   └── package.json
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/v1/exchange-rates` | 🔄 Get all exchange rates |
| `GET` | `/api/v1/assets` | 📄 Get all assets with current prices |
| `GET` | `/api/v1/assets/{id}/icon` | 🖼️ Get asset icon |
| `POST` | `/api/v1/assets` | ➕ Create new asset |
| `GET` | `/api/v1/assets/history` | 📜 Get asset history |
| `GET` | `/api/v1/portfolio` | 💰 Get current portfolio |
| `GET` | `/api/v1/portfolio/history` | 📊 Get portfolio history |
| `POST` | `/api/v1/readings` | 📝 Add new readings |

---

## 🛠️ Tech Stack

### Backend
| Technology | Icon | Description |
|------------|------|-------------|
| **Python 3.10+** | 🐍 | [Documentation](https://www.python.org/) - Async/await support |
| **FastAPI** | ⚡ | [Documentation](https://fastapi.tiangolo.com/) - Modern async web framework |
| **SQLAlchemy 2.0** | 🗄️ | [Documentation](https://www.sqlalchemy.org/) - Async ORM with asyncpg |
| **Poetry** | 📦 | [Documentation](https://python-poetry.org/) - Dependency management |
| **Yoyo-migrations** | 🗂️ | [Documentation](https://ollycope.com/software/yoyo/doc/) - Database migrations |
| **Dependency Injector** | 🧩 | [Documentation](https://python-dependency-injector.ets-labs.org/) - DI container |

### Frontend
| Technology | Icon | Description |
|------------|------|-------------|
| **Vue.js 3** | 💚 | [Documentation](https://vuejs.org/) - Progressive JavaScript framework |
| **Vite** | ⚡ | [Documentation](https://vitejs.dev/) - Next-generation build tool |
| **Tailwind CSS** | 💨 | [Documentation](https://tailwindcss.com/) - Utility-first CSS framework |
| **Chart.js** | 📊 | [Documentation](https://www.chartjs.org/) - Data visualization |
| **vue-chartjs** | 📈 | [Documentation](https://vue-chartjs.org/) - Vue.js wrapper for Chart.js |
| **Axios** | 📡 | [Documentation](https://axios-http.com/) - HTTP client |

### Database
> 🐘 **PostgreSQL** - [Documentation](https://www.postgresql.org/) - Relational database

### DevOps
> ☸️ **Kubernetes** & **ArgoCD** - [Documentation](https://github.com/AgostaGiorgio/HomeLab/tree/master/apps/myinves) - Deployment via ArgoCD Application

---

## 🔄 Automation & Data

The platform leverages an **n8n pipeline** to handle automated data ingestion and historical snapshots:
- 🤖 **Automated Fetching:** Automatically retrieves the latest ETF values and currency exchange rates
- 📸 **History Tracking:** Periodically saves snapshots of assets and net worth to build the historical record
- 🔗 **n8n Workflow:** You can find the template and technical specifications in the [myInves n8n-workflows repository](https://github.com/AgostaGiorgio/N8N-workflows/tree/master/myinves)

---

## 📋 Data Models

### Asset Types
| Type | Icon | Description |
|------|-----|-------------|
| `ETF` | 📈 | Exchange-traded funds |
| `CRYPTO` | 🪙 | Cryptocurrencies |
| `CASH` | 💵 | Cash holdings |
| `GOLD` | 🥇 | Precious metals |
| `BANK_ACCOUNT` | 🏦 | Bank accounts |

### Currencies
| Code | Icon | Name |
|------|------|------|
| `EUR` | 🇪🇺 | Euro |
| `USD` | 🇺🇸 | US Dollar |
| `AED` | 🇦🇪 | UAE Dirham |

---

## 🚀 Getting Started

### Quick Start (ArgoCD)
1. Clone the repository
2. Configure your environment variables in `backend/.env` (use `.env.example` as a template)
3. The application is deployed via ArgoCD - see the [ArgoCD Application definition](https://github.com/AgostaGiorgio/HomeLab/tree/master/apps/myinves) for configuration

### Local Development

#### Backend Setup
```bash
cd backend
poetry install
yoyo apply --database <your_db_url> ./migrations
poetry run python src/main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🗂️ Database Migrations

Apply migrations:
```bash
cd backend
yoyo apply --database <db_url> ./migrations
```

---

## 📄 License

> 📝 **MIT License** - Feel free to use and modify!
