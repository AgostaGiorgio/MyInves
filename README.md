# myInves 📈

**myInves** is a minimal and effective personal finance platform designed to help you track your entire net worth in one place. Whether it's **Crypto**, **ETFs**, **Cash**, **Bank Accounts**, or other assets, myInves provides a clear overview of your financial evolution over time.

---

## 🚀 Key Features

- **Multi-Asset Tracking:** Effortlessly track diverse asset classes including cryptocurrencies, traditional stocks/ETFs, cash, and precious metals.
- **Net Worth Dashboard:** A clean, minimal summary of your current total wealth and individual asset performance.
- **Historical Insights:** Visualize the evolution of your total portfolio and individual assets through interactive charts.
- **Clean UI:** Built with a focus on simplicity and ease of use, ensuring you focus on the data that matters.
- **Self-Hosted & Private:** Keep full control over your financial data by running the stack locally or on your own server.

---

## 🛠️ Tech Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous API)
- **Database ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) with `asyncpg`
- **Dependency Management:** [Poetry](https://python-poetry.org/)
- **Migrations:** [Yoyo-migrations](https://ollycope.com/software/yoyo/doc/)
- **DI Container:** [Dependency Injector](https://python-dependency-injector.ets-labs.org/)

### Frontend
- **Framework:** [Vue.js 3](https://vuejs.org/) (Vite)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Charts:** [Chart.js](https://www.chartjs.org/) & [vue-chartjs](https://vue-chartjs.org/)
- **API Client:** [Axios](https://axios-http.com/)

### DevOps
- **Containerization:** [Docker](https://www.docker.com/) & Docker Compose

---

## 🔄 Automation & Data

The platform leverages an **n8n pipeline** to handle automated data ingestion and historical snapshots:
- **Automated Fetching:** Automatically retrieves the latest ETF values and currency exchange rates.
- **History Tracking:** Periodically saves snapshots of assets and net worth to build the historical record.
- **n8n Workflow:** You can find the template and technical specifications in the [myInves n8n-workflows repository](https://github.com/AgostaGiorgio/N8N-workflows/tree/master/myinves).

---

## 📁 Project Structure

```text
myinves/
├── backend/            # FastAPI Backend
│   ├── src/            # Application logic
│   ├── migrations/     # SQL schema migrations
│   └── pyproject.toml  # Python dependencies
├── frontend/           # Vue.js 3 Frontend
│   ├── src/            # Components, Views, and Services
│   └── package.json    # JS dependencies
└── ...
```

---

## ⚙️ Getting Started

### Prerequisites
- Docker & Docker Compose
- *Alternatively (for local development):* Python 3.10+, Node.js 18+, PostgreSQL.

### Quick Start (Docker)
1. Clone the repository.
2. Configure your environment variables in `backend/.env` (use `.env.example` as a template).
3. Run the stack:
   ```bash
   docker-compose up --build
   ```

### Local Development

#### Backend Setup
1. Navigate to the `backend` directory.
2. Install dependencies: `poetry install`
3. Run migrations: `yoyo apply --database <your_db_url> ./migrations`
4. Start the server: `python src/main.py`

#### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`

---

## 📄 License
This project is licensed under the MIT License.
