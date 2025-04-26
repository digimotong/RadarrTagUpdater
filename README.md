# Radarr Tag Updater

Automatically updates movie tags in Radarr based on custom format scores and other criteria.

## Features

- **Score-based tagging**:
  - `negative_score` when customFormatScore < 0
  - `positive_score` when customFormatScore > threshold (default: 100)
  - `no_score` when score is None or between 0-threshold

- **Release group tagging**:
  - Adds `motong` tag when release group is "motong"

- **Resolution tagging**:
  - Adds `4k` tag when resolution is 2160p

## Containerized Deployment

The application can be run in a Docker container:

1. Copy `.env.example` to `.env` and edit:
   ```bash
   cp .env.example .env
   nano .env
   ```

2. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. View logs:
   ```bash
   docker logs radarr-tagger
   ```

### Environment Variables

- `RADARR_URL`: Radarr instance URL (required)
- `RADARR_API_KEY`: Radarr API key (required)
- `LOG_LEVEL`: Logging level (default: INFO)
- `OUTPUT_DIR`: Results directory (default: /data/results)
- `OUTPUT_FORMAT`: Output format (json/csv, default: json)
- `SCORE_THRESHOLD`: Score threshold for positive_score (default: 100)

## Requirements

- Python 3.6+ (for direct usage)
- Docker (for containerized usage)
- Radarr v3+
- API key with write permissions

## Direct Installation (Alternative)

1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `config.example.json` to `config.json` and edit:
   ```json
   {
     "radarr_url": "http://your-radarr:7878",
     "radarr_api_key": "your-api-key",
     "score_threshold": 100,
     "log_level": "INFO"
   }
   ```

## Usage

### Containerized:
```bash
docker-compose up -d
```

### Direct:
```bash
python radarr_tag_updater.py [options]
```

Options:
- `--config`: Specify alternate config file (default: config.json)
- `--test`: Test mode (only processes first 5 movies)
- `--log-level`: Override log level (DEBUG, INFO, WARNING, ERROR)

## Automation

### Cron Job Setup (Direct Usage)

To run automatically on a schedule:

1. Find your Python path:
   ```bash
   which python3
   ```

2. Edit crontab:
   ```bash
   crontab -e
   ```

3. Add entries like:
   ```bash
   # Daily at 2am
   0 2 * * * /full/path/to/python3 /path/to/radarr_tag_updater.py >> /path/to/radarr_tag_updater.log 2>&1
   ```

## Tags

The script will automatically create these tags if missing:
- `negative_score` (red)
- `positive_score` (green) 
- `no_score` (gray)
- `motong` (purple)
- `4k` (blue)

## Logging

Detailed logs are written to `radarr_tag_updater.log` (direct usage) or container logs (docker usage)

## Example Output

```
2025-04-10 09:30:00 - INFO - Starting Radarr Tag Updater v1.0.0
2025-04-10 09:30:02 - DEBUG - Movie: The Matrix - Score: 150 - Tag: positive_score
2025-04-10 09:30:02 - DEBUG - Added 4k tag for The Matrix
2025-04-10 09:30:05 - INFO - Processing complete. Updated 42/100 movies
