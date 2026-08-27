# myInves — Frontend

Vue 3 single-page application for the **myInves** investment tracking platform. It renders the dashboard, statistics and settings, and talks to the FastAPI backend.

> For user-facing documentation on how to use the platform, see the [root README](../README.md).

---

## 🛠️ Tech Stack

| Technology | Version/Notes | Description |
|------------|---------------|-------------|
| **Vue.js 3** | `^3.5.25` | Progressive JavaScript framework |
| **vue-router** | `^5.2.0` | Client-side routing (lazy-loaded views) |
| **Vite** | `^7.3.1` | Build tool & dev server |
| **Tailwind CSS** | `^3.4.19` | Utility-first CSS framework (Orbit Ecosystem dark theme) |
| **Chart.js** | `^4.5.1` | Data visualization |
| **vue-chartjs** | `^5.3.3` | Vue wrapper for Chart.js |
| **lucide-vue-next** | `^1.0.0` | Icons |
| **Axios** | `^1.13.6` | HTTP client |

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── main.js                 # App entry point
│   ├── App.vue                 # Root component
│   ├── style.css               # Global styles
│   ├── router/
│   │   └── index.js            # Route definitions
│   ├── services/
│   │   └── api.js              # Axios API client
│   ├── views/                  # Route views
│   │   ├── DashboardView.vue
│   │   ├── StatisticsView.vue
│   │   └── SettingsView.vue
│   └── components/             # Reusable UI components
│       ├── AppNavbar.vue       # Bottom navigation
│       ├── AppHeader.vue
│       ├── MarketTicker.vue    # Carousel
│       ├── BalanceHero.vue
│       ├── TotalChart.vue      # Portfolio value chart
│       ├── AssetComparison.vue
│       ├── AssetAllocation.vue # Doughnut chart
│       ├── AssetList.vue
│       └── AddReadingModal.vue # Add holdings
├── nginx.conf                  # SPA fallback config (Docker)
├── orbit-ecosystem-preset.js   # Tailwind theme preset
├── index.html
├── package.json
└── Dockerfile
```

**Routing** (`src/router/index.js`):
- `/` → **Dashboard**
- `/statistics` → **Statistics**
- `/settings` → **Settings**

---

## ⚙️ Configuration

The API base URL is read from the `VITE_API_BASE_URL` environment variable (default `http://localhost:8000`).

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API base URL |

---

## 🚀 Local Development

**Prerequisites:** Node.js + npm.

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies to the API URL from `.env` (default `http://localhost:8000`).

### Build (production)

```bash
cd frontend
npm run build
```

Static output is written to `dist/`, served via nginx in the Docker image.

---

## 🐳 Docker

```sh
# Frontend (linux/amd64) — VITE_API_BASE_URL is needed at build time for the nginx stage
docker buildx build --platform linux/amd64 \
  --build-arg VITE_API_BASE_URL=https://backend:8000 \
  -t registry/myinves_fe:x.y.z .
```

The image runs nginx and serves the built SPA. `nginx.conf` includes a fallback to `index.html` so client-side routes refresh correctly.
