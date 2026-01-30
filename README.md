# Video Generation API

FastAPI backend for generating videos using Google's Veo3 model.

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Set up your Google API key:
   - Copy `.env.example` to `.env`
   - Add your Google API key to `.env`:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```
   
   Alternatively, you can export it as an environment variable:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

3. Run the server:
```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Generate Video
- **POST** `/api/v1/video/generate`
- **Body**: `{"prompt": "Your video description here"}`
- **Response**: Returns an `operation_id` to track the generation

### Check Status
- **GET** `/api/v1/video/status/{operation_id}`
- **Response**: Returns the current status and video URL when ready

### Download Video
- **GET** `/api/v1/video/download/{operation_id}`
- **Response**: Downloads the generated video file

## Example Usage

```bash
# Start video generation
curl -X POST "http://localhost:8000/api/v1/video/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A close up of two people staring at a cryptic drawing on a wall, torchlight flickering."}'

# Check status
curl "http://localhost:8000/api/v1/video/status/{operation_id}"

# Download video when ready
curl "http://localhost:8000/api/v1/video/download/{operation_id}" --output video.mp4
```

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
