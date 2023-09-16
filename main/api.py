import requests


HEADERS = {
    'User-Agent': 'Chess.py (Python 3.9) (username: smonkr6; contact: broomfieldjuliusr@gmail.com)' #This is my contact email
}
   

def fetch_archives(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  
    return response.json()['archives']

def fetch_games_from_archive(archive_url):
    response = requests.get(archive_url, headers=HEADERS)
    response.raise_for_status()
    return response.json()['games']