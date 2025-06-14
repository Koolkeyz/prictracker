---
applyTo: '**'
---

# PriceTracker App Agent Instructions

These instructions are for the PriceTracker app, a web application designed to track product prices across various e-commerce platforms. The app allows users to monitor price changes, set alerts, and view historical price data.

The database is MongoDB, and the backend is built with FastAPI. The frontend uses SvelteKit, leveraging its reactive features for a smooth user experience.

- You can use the `mongodb` tool to interact with the MongoDB database.
- You can use the `context7` tool to access the most up to date context information on the various technologies used in the app such as FastAPI, SvelteKit, and MongoDB. Also use this tool for correct implementation of code snippets.

## Technologies

- Python uv tool which uses Pyproject to manage Python dependencies and virtual environments.
- FastAPI for building the backend API
- SvelteKit for the frontend, utilizing its reactive features
- MongoDB for the database, storing product and price data
- Docker for containerization and deployment
- Pydantic for data validation in FastAPI
- TypeScript for type safety in SvelteKit components

## PriceTracker App Coding Guidelines

### Project Architecture
- **Backend**: Python with FastAPI, serving as both API and static file server
- **Frontend**: SvelteKit built as SPA and served by the FastAPI backend
- **Database**: MongoDB for storing products, prices, users, and tracking data
- **Deployment**: Docker containers for easy deployment

### Coding Standards

#### Python Backend
- Follow PEP 8 style guide with 4-space indentation
- Use type hints for all function parameters and return values
- Group imports: standard library, third-party, local modules
- Organize code into service/controller layers with clear responsibilities
- Use async/await for database and external API calls
- Prefer dependency injection for service components

#### SvelteKit Frontend
- Use TypeScript for all new components and scripts
- Components follow kebab-case naming convention
- CSS classes use BEM methodology
- Use SvelteKit stores for global state management
- Prefer Svelte runes `$state`, `$derived`, `$effect` over legacy reactive declarations
- Use `load` functions for data fetching in page components
- Organize components by feature in `/lib/components/` directory

### Domain Knowledge

#### Product Scraping
- Each product needs: name, current price, URL, image URL, vendor
- Price histories track: price, timestamp, availability status
- Supported vendors: Amazon, eBay, Newegg (each with custom scrapers)
- Use unique product identifiers (SKU, ASIN, etc.) when available

#### Authentication
- JWT-based authentication with refresh tokens
- Role-based access: admin, user
- User preferences include: notification thresholds, frequency, vendors

#### Scheduled Tasks
- Price updates run on configurable intervals (default: daily)
- Failed scrapes retry with exponential backoff
- Price alerts trigger when thresholds are crossed

### Common Patterns

#### API Structure
- RESTful endpoints for CRUD operations
- URLs follow `/api/v1/resource` convention
- Responses include appropriate HTTP status codes and structured error messages

#### Data Validation
- Backend: Pydantic models for input/output validation
- Frontend: Form validation with error messages before submission

#### Error Handling
- Backend: Use consistent error response format {status, message, details}
- Frontend: Error boundaries around major components, toast notifications

### Additional Notes
- Development environment uses hot-reload
- Database connections use connection pooling
- All dates stored in UTC, displayed in user's timezone