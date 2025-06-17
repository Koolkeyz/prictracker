# Multi-stage build Dockerfile for PriceTracker
# Stage 1: Build the SvelteKit frontend
FROM node:lts-jod AS frontend-builder

# Set working directory for frontend
WORKDIR /app/frontend

# Install pnpm
RUN npm install -g pnpm

# Copy package.json and lock files
COPY ./frontend/package.json ./frontend/pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the frontend code
COPY ./frontend/ ./

# Build the SvelteKit app
RUN pnpm run build

# Stage 2: Set up the Python backend and copy the built frontend
FROM python:3.12-bookworm AS server

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy Python project files
COPY ./backend/pyproject.toml ./backend/uv.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install uv \
    && uv pip install --no-cache-dir -e .

# # Create site directory
# RUN mkdir -p /app/backend/site

# # Copy the built frontend from the frontend-builder stage
# COPY --from=frontend-builder /app/frontend/build/ /app/backend/site/

# # Copy the backend source code
# COPY ./backend/src/ /app/backend/src/

# # Create necessary directories
# RUN mkdir -p /app/backend/logs

# # Set working directory to backend
# WORKDIR /app/backend

# # Expose the port the app runs on
# EXPOSE 80

# # Command to run the application
# CMD ["fastapi", "run", "src/main.py","--port", "80", "--proxy-headers"]
