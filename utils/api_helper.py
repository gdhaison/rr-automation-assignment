import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


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
