from collections import namedtuple
from io import StringIO
import pandas as pd
import chess.pgn


ECO = pd.read_csv(
    'main\data\ECO.csv', 
    header = None, 
    names = ["ECO", "Opening"]
    ).set_index('ECO').to_dict()['Opening']

Values = namedtuple('values', ['frequency', 'win_rate'])

def get_opening_info(game, username):
    if 'pgn' not in game:
      return None, None
    
    pgn = game['pgn']

    if 'ECO' not in pgn:
      return None, None

    pgn = StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    code = game.headers['ECO']

    name = ECO.get(code, "Unknown Opening")

    return name, game.headers['Result'] == "1-0"

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