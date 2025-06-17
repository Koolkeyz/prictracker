# PriceTracker

PriceTracker is a web application designed to track product prices across various e-commerce platforms including Amazon, eBay, and Newegg. The app allows users to monitor price changes, set alerts, and view historical price data.

## Technology Stack

- **Backend**: Python with FastAPI
- **Frontend**: SvelteKit
- **Database**: MongoDB
- **Deployment**: Docker containers

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Setup and Installation

**Step 1:** Clone the repository:

```bash
git clone <repository-url>
cd prictracker
```

**Step 2:** Create a `.env` file in the root directory (optional, defaults are provided in docker-compose.yml):

```env
JWT_SECRET=your_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password
ADMIN_EMAIL=admin@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
SENDER_EMAIL=noreply@example.com
```

**Step 3:** Build and start the Docker containers:

```bash
docker-compose up --build
```

**Step 4:** Access the application:

- Web Application: [http://localhost:8000](http://localhost:8000)
- MongoDB Express (Database Admin): [http://localhost:8081](http://localhost:8081)
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Development

#### Running in Development Mode

For local development, you can run the frontend and backend separately:

**Frontend (SvelteKit):**

```bash
cd frontend
pnpm install
pnpm dev
```

**Backend (FastAPI):**

```bash
cd backend
pip install -e .
uvicorn src.main:pricetracker --reload
```

## Project Structure

- `/backend`: FastAPI backend application
  - `/src`: Source code for the backend
  - `/logs`: Application logs
  - `/site`: Built frontend (SvelteKit) files served by FastAPI

- `/frontend`: SvelteKit frontend application
  - `/src`: Source code for the frontend
  - `/static`: Static assets

## Features

- User authentication with JWT
- Product tracking across multiple e-commerce platforms
- Email alerts when prices drop below thresholds
- Price history visualization
- Admin dashboard for system management

## Docker Deployment

The application uses a multi-stage Docker build process:

1. First stage builds the SvelteKit frontend
2. Second stage sets up the Python backend and copies the built frontend
3. The FastAPI server serves both the API endpoints and the SvelteKit frontend

To rebuild the application after changes:

```bash
docker-compose down
docker-compose up --build
```

## License

MIT License
