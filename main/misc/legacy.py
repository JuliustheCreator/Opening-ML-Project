import pandas as pd
import numpy as np
import sys
import requests
from chessdotcom import get_player_stats, get_player_game_archives
import chess.pgn
from io import StringIO
from functions import *
    

username = input("Input Player Name: ")

# #Chooses Highest Rating Between Rapid and Blitz
# def get_player_rating(username):
#     try:
#         playerinfo = get_player_stats(username).json
#     except:
#         print("User Not Found.")
#         return None

#     timecontrols = ['chess_rapid', 'chess_blitz']
#     ratings = []

#     for timecontrol in timecontrols:
#         ratings.append(playerinfo['stats'][timecontrol]['last']['rating'])
#     if ratings[0] > ratings[1]:
#         return ratings[0]
#     return ratings[1]

# new = False

# # Retrives Last 6 Months of Games Played; Checks To See if Player is New
# def get_player_games(username):
#     all_games = []
#     games = get_player_game_archives(username).json
#     months_played = len(games['archives'])
#     if months_played < 6:
#         urls = games['archives']
#         if months_played < 3:
#             new = True
#     else:
#         urls = games['archives'][-6:]

#     for url in urls:
#         monthly_games = requests.get(url).json()
#         all_games.append(monthly_games)
#     return all_games

# # Grabs ECO (Opening ID) From PGN
# def get_ECO(pgn):
#     pgn = StringIO(pgn)
#     game = chess.pgn.read_game(pgn)
#     ECO = game.headers['ECO']
#     return ECO

# # Grabs FEN from Game
# def get_FEN(game):
#     FEN = game['fen']
#     return FEN

# # Grabs Side (White or Black): 0 for Black, 1 for White
# def get_side(game):
#     side = game['white']['username']
#     if side == username:
#         return 'white'
#     return 'black'

# #Checks If Player Won
# def check_for_win(game, side):
#     if game[side]['result'] == 'win':
#         return 1
#     return 0
    
# # Grabs Game Variation & Time Control
# def get_variation(game):
#     time_control = game['time_class']
#     variation = game['rules']
#     #Variation should be "Chess" for Normal Games
#     return time_control, variation

# # Grabs Opening Name from Game
# def get_opening_name(pgn):
#     pgn = StringIO(pgn)
#     game = chess.pgn.read_game(pgn)
#     ECO_url = game.headers['ECOUrl']
#     #Grabbing Substring (Contains Opening Name) from ECO Url 
#     opening_name = ECO_url[31:]
#     return opening_name.replace('-',' ')

# # Extracts Opening Name Without Using Chess Module
# def extract_opening_name(pgn):
#     pgn = pgn.split('\n')
#     url = pgn[11]
#     for data in pgn:
#         if data[1:7] == "ECOUrl":
#             url = data
#             break
#     name = url.split('/')[-1] 
#     name = name[:-2].replace('-',' ')
#     return name

#Collecting All Recently Played Openings
white_eco = []
white_fen = []
white_result = []
white_names = []

black_fen = []
black_eco = []
black_result = []
black_names = []

try:
    get_player_games(username)
except:
    print("User Not Found.")
    sys.exit()

all_games = get_player_games(username)
for monthly_games in all_games:
    for game in monthly_games['games']:
        if not new:
            if get_variation(game)[0] == 'bullet' or get_variation(game)[1] != 'chess':
                continue
        if get_side(game) == 'white':
            white_eco.append(get_ECO(game['pgn']))
            white_fen.append(get_FEN(game))
            white_result.append(check_for_win(game, get_side(game)))
            white_names.append(get_opening_name(game['pgn']))
        else:
            black_eco.append(get_ECO(game['pgn']))
            black_fen.append(get_FEN(game))
            black_result.append(check_for_win(game, get_side(game)))
            black_names.append(get_opening_name(game['pgn']))

#Creating Seperate Dataframes Depending on if Player is Black or White
blackdf = pd.DataFrame()
whitedf = pd.DataFrame()

blackdf['Name'] = black_names
blackdf['ECO'] = black_eco
blackdf['FEN'] = black_fen
blackdf['Result'] = black_result

whitedf['Name'] = white_names
whitedf['ECO'] = white_eco
whitedf['FEN'] = white_fen
whitedf['Result'] = white_result

'''
Grabbing The User's Rating.
Only the User's Rating & The Openings They Play Will Be Taken Into Account in Choosing New Openings.
'''

user_rating = get_player_rating(username)

#Adding Frequency Column to Player Dataframe
whitedf['Frequency'] = whitedf['Name'].map(whitedf['Name'].value_counts(normalize = True) * 100)
blackdf['Frequency'] = blackdf['Name'].map(blackdf['Name'].value_counts(normalize = True) * 100)

#Sorting by Most Played Openings
whitedf.sort_values(by = ['Frequency'], inplace = True, ascending = False)
blackdf.sort_values(by = ['Frequency'], inplace = True, ascending = False)

#Creating Win Rate Column for Player Dataframe
white_win_rate = whitedf.rename(columns = {"Result":"Count"}).groupby("Name").sum().reset_index()
black_win_rate = blackdf.rename(columns = {"Result":"Count"}).groupby("Name").sum().reset_index()

white_win_rate = pd.DataFrame(white_win_rate)
black_win_rate = pd.DataFrame(black_win_rate)

white_win_rate.sort_values(by = ['Frequency'], inplace = True, ascending = False)
black_win_rate.sort_values(by = ['Frequency'], inplace = True, ascending = False)

#Number of Openings - Needed For Calculating Number of Same Opening
whiteopcount = len(whitedf)
blackopcount = len(blackdf)

#Deleting Duplicate Openings in Player Dataframe
whitedf.drop_duplicates(subset = 'Name', inplace = True)
blackdf.drop_duplicates(subset = 'Name', inplace = True)

#Adding on Win Rate Column
white_win_rate = list(white_win_rate['Count'])
black_win_rate = list(black_win_rate['Count'])

whitedf['Win Rate'] = white_win_rate
blackdf['Win Rate'] = black_win_rate

white_op_win_percent = whitedf['Frequency'].multiply(0.01).apply(lambda x: x * whiteopcount)
black_op_win_percent = blackdf['Frequency'].multiply(0.01).apply(lambda x: x * blackopcount)

whitedf['Win Rate'] = whitedf['Win Rate'].div(white_op_win_percent).multiply(100)
blackdf['Win Rate'] = blackdf['Win Rate'].div(black_op_win_percent).multiply(100)

whitedf.drop(['Result'], axis = 1, inplace = True)
blackdf.drop(['Result'], axis = 1, inplace = True)

# Doesn't Return List Unlike "get_variation()"
def validate_variation(game):
    pgn = StringIO(game['pgn'])
    game_pgn = chess.pgn.read_game(pgn)
    event = game_pgn['pgn'].headers['Event']
    if event != "Live Chess":
        del game
    variation = game['rules']
    if variation != "normal":
        del game

# Creating Chess.com Dataframe from 40,000 Games & 37,000+ Users
chesscomgames = pd.read_csv('/Users/jrbroomfield1/Desktop/Opening-Recommendation-System/system/data/chesscomgames.csv')
chesscomgames = chesscomgames[['white_username','black_username','pgn','white_rating','black_rating','white_result','black_result']]

# Creating Opening Name for Each Game
chesscomgames['Opening Name'] = chesscomgames['pgn'].apply(extract_opening_name)
chesscomgames.drop(['pgn'], axis = 1, inplace = True)

# Separating User Profile for Each User in Chess.com Dataframe
white_users = pd.DataFrame(index = chesscomgames['white_username'].unique(), columns = chesscomgames['Opening Name'].unique())
black_users = pd.DataFrame(index = chesscomgames['black_username'].unique(), columns = chesscomgames['Opening Name'].unique())

white_users = white_users.fillna(0)
black_users = black_users.fillna(0)

# Creating Item Matrix using Chess.com Data
for i in range(len(chesscomgames)):
    whiteuser = chesscomgames.iloc[i]['white_username']
    blackuser = chesscomgames.iloc[i]['black_username']
    opening = chesscomgames.iloc[i]['Opening Name']
    
    white_users.at[whiteuser, opening] += 1
    black_users.at[blackuser, opening] += 1

# Calculating win rate for each opening
chesscomgames['white_win'] = chesscomgames['white_result'].apply(lambda x: 1 if x == 'win' else 0)
chesscomgames['black_win'] = chesscomgames['black_result'].apply(lambda x: 1 if x == 'win' else 0)

white_win_rates = chesscomgames.groupby(['white_username', 'Opening Name']).agg({'white_win': 'mean'})
black_win_rates = chesscomgames.groupby(['black_username', 'Opening Name']).agg({'black_win': 'mean'})

white_win_rates.rename(columns={'white_win': 'win_rate'}, inplace=True)
black_win_rates.rename(columns={'black_win': 'win_rate'}, inplace=True)

white_win_rates.reset_index(inplace=True)
black_win_rates.reset_index(inplace=True)

# Merging win rates with user-item matrices
white_users = white_users.merge(white_win_rates, how='left', left_index=True, right_on='white_username')
black_users = black_users.merge(black_win_rates, how='left', left_index=True, right_on='black_username')

white_users.to_csv('white_userbyitem.csv', index=True)
black_users.to_csv('black_userbyitem.csv', index=True)

for opening in chesscomgames['Opening Name'].unique():
    white_users[opening + '_count'] = 0
    black_users[opening + '_count'] = 0
    white_users[opening + '_win_rate'] = np.nan
    black_users[opening + '_win_rate'] = np.nan

for i in range(len(chesscomgames)):
    whiteuser = chesscomgames.iloc[i]['white_username']
    blackuser = chesscomgames.iloc[i]['black_username']
    opening = chesscomgames.iloc[i]['Opening Name']
    white_win = chesscomgames.iloc[i]['white_win']
    black_win = chesscomgames.iloc[i]['black_win']

    white_users.at[whiteuser, opening + '_count'] += 1
    black_users.at[blackuser, opening + '_count'] += 1

    if white_win:
        white_users.at[whiteuser, opening + '_win_rate'] = ((white_users.at[whiteuser, opening + '_win_rate'] * (white_users.at[whiteuser, opening + '_count'] - 1)) + 1) / white_users.at[whiteuser, opening + '_count']
    else:
        white_users.at[whiteuser, opening + '_win_rate'] = (white_users.at[whiteuser, opening + '_win_rate'] * (white_users.at[whiteuser, opening + '_count'] - 1)) / white_users.at[whiteuser, opening + '_count']

    if black_win:
        black_users.at[blackuser, opening + '_win_rate'] = ((black_users.at[blackuser, opening + '_win_rate'] * (black_users.at[blackuser, opening + '_count'] - 1)) + 1) / black_users.at[blackuser, opening + '_count']
    else:
        black_users.at[blackuser, opening + '_win_rate'] = (black_users.at[blackuser, opening + '_win_rate'] * (black_users.at[blackuser, opening + '_count'] - 1)) / black_users.at[blackuser, opening + '_count']


def transform_user_data(users, side):
    transformed_data = []

    for index, row in users.iterrows():
        for col in row.index:
            if col.endswith('_win_rate'):
                opening_name = col[:-9]
                opening_freq = row[opening_name]
                opening_win_rate = row[col]
                if opening_freq > 0:
                    transformed_data.append({
                        'Username': row['username'],
                        'Side': side,
                        'Opening Name': opening_name,
                        'Frequency': opening_freq,
                        'Win Rate': opening_win_rate
                    })

    return pd.DataFrame(transformed_data)

transformed_white_users = transform_user_data(white_users, 'white')
transformed_black_users = transform_user_data(black_users, 'black')

transformed_users = pd.concat([transformed_white_users, transformed_black_users])
transformed_users.to_csv('transformed_userbyitem.csv', index=False)

print(transformed_users)