#!/usr/bin/env python3
"""
Radarr Tag Updater
Fetches movies from Radarr API and updates tags.
"""

import os
import sys
import json
import logging
from typing import Dict, List
import requests
from requests.exceptions import RequestException

def parse_args():
    """Parse command line arguments"""
    import argparse
    parser = argparse.ArgumentParser(description='Radarr Tag Updater')
    parser.add_argument('--config', default='config.json',
                      help='Path to config file (default: config.json)')
    parser.add_argument('--test', action='store_true',
                      help='Run in test mode (only process first 5 movies)')
    parser.add_argument('--format', choices=['json', 'csv'],
                      help='Override output format from config')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      help='Override log level from config')
    parser.add_argument('--version', action='store_true',
                      help='Show version and exit')
    return parser.parse_args()

def load_config(config_path: str):
    """Load configuration from JSON file"""
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        # Create output directory if needed
        output_dir = config.get('output_directory', 'results')
        os.makedirs(output_dir, exist_ok=True)
        
        return config
    except Exception as e:
        logging.error(f"Failed to load config: {str(e)}")
        sys.exit(1)

VERSION = "1.0.0"

def main():
    """Main execution flow"""
    args = parse_args()
    
    if args.version:
        print(f"Radarr Tag Updater v{VERSION}")
        sys.exit(0)
    
    # Load configuration
    config = load_config(args.config)
    
    # Apply argument overrides
    if args.format:
        config['output_format'] = args.format
    if args.log_level:
        config['log_level'] = args.log_level
    
    # Set global config
    RADARR_URL = config['radarr_url']
    RADARR_API_KEY = config['radarr_api_key']
    LOG_LEVEL = config.get('log_level', 'INFO')
    OUTPUT_DIR = config.get('output_directory', 'results')

    setup_logging(LOG_LEVEL)
    logging.info("Starting Radarr Tag Updater v%s", VERSION)
    
    try:
        # Initialize API client
        api = RadarrAPI(RADARR_URL, RADARR_API_KEY)
        
        # Fetch data
        movies = api.get_movies()
        custom_formats = api.get_custom_formats()
        
        if args.test:
            movies = movies[:5]
            logging.info("TEST MODE: Processing first 5 movies only")

        # Output raw movie data for testing
        raw_movies_file = os.path.join(OUTPUT_DIR, 'raw_movies.json')
        with open(raw_movies_file, 'w') as f:
            json.dump(movies, f, indent=2)
        logging.info(f"Saved raw movie data to {raw_movies_file}")
        
    except Exception as e:
        logging.error(f"Script failed: {str(e)}")
        sys.exit(1)

class RadarrAPI:
    """Client for Radarr API interactions"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': self.api_key,
            'Accept': 'application/json'
        })
    
    def get_movies(self) -> List[Dict]:
        """Fetch all movies from Radarr"""
        endpoint = f"{self.base_url}/api/v3/movie"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Failed to fetch movies: {str(e)}")
            raise

def setup_logging(log_level):
    """Configure logging for cron job"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('radarr_tag_updater.log'),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    main()
