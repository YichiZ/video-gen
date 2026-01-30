# Docker Setup

This project includes Docker configurations for both development and production environments.

## Prerequisites

- Docker and Docker Compose installed
- `.env` file in the root directory with `GOOGLE_API_KEY` set

## Production Build

Build and run the production containers:

```bash
docker-compose up --build
```

This will:
- Build the backend FastAPI service
- Build the frontend React app (using Bun) and serve it with Nginx
- Start both services

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development Build

For development with hot-reload:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

This will:
- Mount source code as volumes for live reloading
- Run backend with `--reload` flag
- Run frontend dev server with Bun

## Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Volumes

- `backend/generated_videos` - Persists generated video files
- Source code is mounted in dev mode for hot-reload

## Stopping Containers

```bash
# Production
docker-compose down

# Development
docker-compose -f docker-compose.dev.yml down
```

## Building Individual Services

```bash
# Backend only
docker build -f backend/Dockerfile -t video-gen-backend .

# Frontend only
docker build -f frontend/Dockerfile -t video-gen-frontend ./frontend
```

## Troubleshooting

1. **Port conflicts**: Make sure ports 3000 and 8000 are not in use
2. **API key**: Ensure `.env` file exists with `GOOGLE_API_KEY`
3. **Permissions**: Generated videos directory may need write permissions
4. **Network issues**: Containers communicate via Docker network `video-gen-network`
