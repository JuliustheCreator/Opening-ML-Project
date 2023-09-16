import pandas as pd
from collections import namedtuple

Values = namedtuple('values', ['frequency', 'win_rate'])

def get_opening_info(game, username):
    if 'pgn' not in game:
        return None, None
    pgn = game['pgn'].split('\n')
    url = next((data for data in pgn if "ECOUrl" in data), pgn[11])
    name = url.split('/')[-1][:-2].replace('-',' ')

    if game['white']['username'] == username: is_win = game['white']['result'] == 'win'
    else: is_win = game['black']['result'] == 'win'
    return name, is_win

def create_matrix(games, username):
    database = {}
    for game in games:
        name, is_win = get_opening_info(game, username)
        if not name: continue
        if name not in database: database[name] = {'played': 0, 'wins': 0}
        database[name]['played'] += 1
        if is_win: database[name]['wins'] += 1   

    df = pd.DataFrame(database).T
    df['win_rate'] = (df['wins'] / df['played']) * 100
    df['frequency'] = (df['played'] / len(database)) * 100

    df_tuples = df.apply(lambda row: Values(row['frequency'], row['win_rate']), axis=1)
    user_matrix = pd.DataFrame([df_tuples], index=[username])
    return user_matrix