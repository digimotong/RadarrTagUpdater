# Radarr Tag Updater

Automatically updates movie tags in Radarr based on custom format scores, release groups, and quality information.

## Features

- **Score-based tagging**:
  - `negative_score` (red) when customFormatScore < 0
  - `positive_score` (green) when customFormatScore > threshold (default: 100)
  - `no_score` (gray) when score is None or between 0-threshold

- **Release group tagging**:
  - `motong` (purple) when release group is "motong" (configurable via MOTONG env var)

- **Quality tagging**:
  - `4k` (blue) when resolution is 2160p

## Containerized Deployment

The application is designed to run in Docker with Radarr. Here's a sample compose configuration:

```yaml
services:
  radarr-tagger:
    image: digimotong/radarr-tagger:latest
    container_name: radarr-tagger
    restart: unless-stopped
    depends_on:
      - radarr
    environment:
      RADARR_URL: http://radarr:7878  # Radarr instance URL
      RADARR_API_KEY: your-api-key    # Radarr API key (required)
      LOG_LEVEL: INFO                 # DEBUG, INFO, WARNING, ERROR
      SCORE_THRESHOLD: 100            # Threshold for positive_score
      INTERVAL_MINUTES: 20            # Minutes between runs
      MOTONG: true                    # Enable motong tagging
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `RADARR_URL` | Radarr instance URL | `http://radarr:7878` |
| `RADARR_API_KEY` | Radarr API key with write permissions | `your-api-key` |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `SCORE_THRESHOLD` | `100` | Score threshold for positive_score tag |
| `INTERVAL_MINUTES` | `20` | Minutes between automatic runs |
| `MOTONG` | `false` | Enable motong release group tagging |

## Tag Management

The application automatically creates and manages these tags:

| Tag Name | Color | Trigger Condition |
|----------|-------|-------------------|
| negative_score | #ff0000 | customFormatScore < 0 |
| positive_score | #00ff00 | customFormatScore > threshold |
| no_score | #808080 | No score or 0 ≤ score ≤ threshold |
| motong | #800080 | Release group contains "motong" |
| 4k | #0000ff | Resolution is 2160p |

Tags are created automatically if they don't exist in Radarr.

## Monitoring

View container logs to monitor operation:

```bash
docker logs radarr-tagger
```

Example log output:
```
2025-04-27 12:00:00 - INFO - Starting Radarr Tag Updater v1.0.0
2025-04-27 12:00:02 - INFO - Processing 125 movies
2025-04-27 12:00:05 - DEBUG - Movie: Inception - Score: 150 - Tag: positive_score
2025-04-27 12:00:05 - DEBUG - Added 4k tag for Inception
2025-04-27 12:00:10 - INFO - Processing complete. Updated 18/125 movies
2025-04-27 12:00:10 - INFO - Next run in 20 minutes
```

## Requirements

- Docker
- Radarr v3+
- API key with write permissions
- Network access to Radarr instance
