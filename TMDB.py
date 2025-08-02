import argparse
import requests
from rich import print
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('api_key')
BASE_URL = 'https://api.themoviedb.org/3/movie'

MOVIE_TYPES = {
    'playing': 'now_playing',
    'popular': 'popular',
    'top_rated': 'top_rated',
    'upcoming': 'upcoming'
}

def fetch_movies(movie_type):
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer -here goes your token-'
    }
    endpoint = MOVIE_TYPES.get(movie_type)
    if not endpoint:
        print('[red]Invalid movie type[/red]')
        return
    url = f'{BASE_URL}/{endpoint}?api_key={API_KEY}&language=en-US&page=1'

    if not API_KEY:
        print('[red]Missing API_KEY. Set it in your .env file[/red]')
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        for movie in data.get('results', []):
            print(f'[bold]{movie['title']}[/bold] - {movie['release_date']}')
    except requests.exceptions.RequestException as e:
        print(f'[red]Error fetching data: {e} [/red]')

def main():
    parser = argparse.ArgumentParser(description='TMDB CLI Tool')
    parser.add_argument('--type', required=True, help='Type of movies: playing, popular, top, upcoming')
    args = parser.parse_args()
    fetch_movies(args.type)

if __name__ == '__main__':
    main()