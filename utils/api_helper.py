import os
import requests
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

logger = get_logger("test_filter")
def get_popular_movies(page_num=1):
    url = f"{BASE_URL}/movie/popular?page={page_num}&api_key={API_KEY}"
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://tmdb-discover.surge.sh/',
        'User-Agent': 'pytest-bdd-automation',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_discover_movies(filters: dict):
    endpoint = f"{BASE_URL}/discover/movie"

    params = {
        'api_key': API_KEY,
        'sort_by': filters.get('sort_by', 'popularity.desc'),
        'release_date.gte': filters.get('release_date_gte', '1900-01-01'),
        'release_date.lte': filters.get('release_date_lte', '2026-12-31'),
        'vote_average.gte': filters.get('vote_average_gte', 0),
        'vote_average.lte': filters.get('vote_average_lte', 5),
        'page': int(filters.get('page', 1)),
        'with_genres': str(filters.get('genre_id', ''))
    }

    headers = {
        'Accept': 'application/json',
        'Referer': 'https://tmdb-discover.surge.sh/',
        'User-Agent': 'pytest-bdd-automation',
    }

    response = requests.get(endpoint, params=params, headers=headers)
    response.raise_for_status()
    logger.info(f"API response: {response.json()}")
    return response.json()

def get_top_rated_movies(page_num=1):
    # Get top rated movies from TMDB API
    url = f"{BASE_URL}/movie/top_rated?page={page_num}&api_key={API_KEY}"
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://tmdb-discover.surge.sh/',
        'User-Agent': 'pytest-bdd-automation',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
