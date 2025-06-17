# Multi-stage build Dockerfile for PriceTracker
# Stage 1: Build the SvelteKit frontend
FROM node:lts-alpine3.22 AS frontend-builder

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
FROM ghcr.io/astral-sh/uv:debian-slim AS server

# Set working directory
WORKDIR /app

# Copy the Python requirements
COPY ./backend/uv.lock  /app
COPY ./backend/pyproject.toml /app
COPY ./backend/.python-version /app

# Install All Dependencies
RUN uv sync --locked

# Copy the remaining src files
COPY ./backend/src /app/src

# Create Site directory and copy build from stage 1
RUN mkdir -p /app/site
COPY --from=frontend-builder /app/frontend/build/ /app/site/

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["uv", "run", "fastapi", "run", "src/main.py","--port", "80", "--proxy-headers"]
