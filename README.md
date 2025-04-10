# Radarr Custom Format Calculator

A Python script to calculate and export custom format scores for all movies in Radarr.

## Features

- Fetches movies and custom formats from Radarr API
- Calculates scores matching Radarr's frontend logic
- Outputs results in JSON or CSV format
- Supports cron job scheduling
- Test mode for development/debugging
- Configurable logging levels

## Requirements

- Python 3.6+
- requests library

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the `config.json` file with your Radarr details

## Configuration

Edit `config.json` with your settings:
```json
{
    "radarr_url": "http://localhost:7878",
    "radarr_api_key": "your_api_key_here",
    "output_format": "json",
    "log_level": "INFO",
    "output_directory": "results"
}
```

## Usage

Basic usage:
```bash
python radarr_format_calculator.py
```

Command line options:
```
--config      Path to config file (default: config.json)
--test        Run in test mode (only process first 5 movies)
--format      Override output format (json/csv)
--log-level   Override log level (DEBUG/INFO/WARNING/ERROR)
--version     Show version and exit
```

## Cron Job Setup

Example cron entry to run daily at 2am:
```bash
0 2 * * * /usr/bin/python3 /path/to/radarr_format_calculator.py
```

## Output

Results are saved to:
- `results/radarr_format_scores.json` (default)
- Or `results/radarr_format_scores.csv` if CSV format selected

Logs are written to `radarr_format_calculator.log`
