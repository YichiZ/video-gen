# Video Generation Frontend

React + Vite frontend for the Video Generation API using Veo3.

## Setup

1. Install dependencies using Bun:
```bash
bun install
```

2. Start the development server:
```bash
bun run dev
```

The frontend will be available at `http://localhost:3000`

## Environment Variables

Create a `.env` file in the frontend directory (optional):
```
VITE_API_URL=http://localhost:8000/api/v1
```

If not set, it defaults to `http://localhost:8000/api/v1`

## Build

Build for production:
```bash
bun run build
```

Preview production build:
```bash
bun run preview
```

## Features

- Text prompt input for video generation
- Real-time status polling
- Video player with controls
- Download generated videos
- Responsive design
