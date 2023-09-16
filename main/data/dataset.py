import requests
import pandas as pd
from collections import namedtuple


HEADERS = {
    'User-Agent': 'Chess.py (Python 3.9) (username: smonkr6; contact: broomfieldjuliusr@gmail.com)' #This is my contact email
    }

ECO = pd.read_csv(
    'ECO.csv', 
    header = None, 
    names = ["ECO", "Opening"]
    ).set_index('ECO').to_dict()['Opening']

Values = namedtuple('values', ['frequency', 'win_rate'])

dataset = pd.DataFrame()

def create_matrix(games, username):
    database = {}
    for game in games:
        name, is_win = get_opening_info(game, username)
        if not name: continue
        if name not in database: database[name] = {'played': 0, 'wins': 0}
        database[name]['played'] += 1
        if is_win: database[name]['wins'] += 1   

    df = pd.DataFrame(database).T

    if 'wins' not in df.columns: df['wins'] = 0
    if 'played' not in df.columns: df['played'] = 0

    df['win_rate'] = (df['wins'] / df['played']) * 100
    df['frequency'] = (df['played'] / len(database)) * 100

    df_tuples = df.apply(lambda row: Values(row['frequency'], row['win_rate']), axis=1)
    user_matrix = pd.DataFrame([df_tuples], index=[username])
    return user_matrix


def fetch_archives(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  
    return response.json()['archives']


def fetch_games_from_archive(archive_url):
    response = requests.get(archive_url, headers=HEADERS)
    response.raise_for_status()
    return response.json()['games']


def get_opening_info(game, username):
    # if 'pgn' not in game:
    #     return None, None
    # pgn = game['pgn'].split('\n')
    # url = next((data for data in pgn if "ECOUrl" in data), pgn[11])
    # name = url.split('/')[-1][:-2].replace('-',' ')

    # if game['white']['username'] == username: is_win = game['white']['result'] == 'win'
    # else: is_win = game['black']['result'] == 'win'
    # return name, is_win

    if 'pgn' not in game:
        return None, None

    code = game.get('ECO', None)
    name = ECO.get(code, "Unknown Opening")


    if game['white']['username'] == username: 
        is_win = game['white']['result'] == 'win'
    else: 
        is_win = game['black']['result'] == 'win'
    
    return name, is_win

url = f"https://api.chess.com/pub/club/chess-com-developer-community/members"
response = requests.get(url, headers=HEADERS)
response.raise_for_status()


keys = ['weekly', 'monthly', 'all_time']
members = [object['username'] for key in keys for object in response.json()[key]]

dataset = pd.DataFrame()

for i, member in enumerate(members):
    try:
        archives = fetch_archives(member)

    except:
        dataset.to_parquet('dataset.parquet', engine='pyarrow')

    container = []

    for archive in archives:
        games = fetch_games_from_archive(archive)
        container.extend(games)
        
    matrix = create_matrix(container, member)
    dataset = pd.concat([dataset, matrix])

    print(i)

print(dataset)

dataset.to_parquet('dataset.parquet', engine='pyarrow')