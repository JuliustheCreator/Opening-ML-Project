from calendar import c
import pandas as pd
import numpy as np
import requests
from chessdotcom import get_player_stats, get_player_game_archives
import chess.pgn
from io import StringIO

'''
Preparing LiChess Dataframe:
    Will Be Used To Compare Openings With Respect To Rating (Collaborate-Based Filtering)
'''

username = input("Input Player Name: ")

#Chooses Highest Rating Between Rapid and Blitz
def get_player_rating(username):
    playerinfo = get_player_stats(username).json
    print(playerinfo)
    timecontrols = ['chess_rapid', 'chess_blitz']
    ratings = []

    for timecontrol in timecontrols:
        ratings.append(playerinfo['stats'][timecontrol]['last']['rating'])
    if ratings[0] > ratings[1]:
        return ratings[0]
    return ratings[1]


'''
The "new" variable is true if the player has not played longer than 3 months.
If the player is "new" then bullet games will be used.
'''

new = False

#Retrives Last 6 Months of Games Played; Checks To See if Player is New
def get_player_games(username):
    all_games = []
    games = get_player_game_archives(username).json
    months_played = len(games['archives'])
    if months_played < 6:
        urls = games['archives']
        if months_played < 3:
            new = True
    else:
        urls = games['archives'][-6:]

    for url in urls:
        monthly_games = requests.get(url).json()
        all_games.append(monthly_games)
    return all_games


#Grabs ECO (Opening ID) From PGN
def get_ECO(pgn):
    pgn = StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    ECO = game.headers['ECO']
    return ECO

#Grabs FEN from Game
def get_FEN(game):
    FEN = game['fen']
    return FEN

#Grabs Side (White or Black): 0 for Black, 1 for White
def get_side(game):
    side = game['white']['username']
    if side == username:
        return 'white'
    return 'black'

#Checks If Player Won
def check_for_win(game, side):
    if game[side]['result'] == 'win':
        return 1
    return 0
    

#Grabs Game Variation & Time Control
def get_variation(game):
    time_control = game['time_class']
    variation = game['rules']

    #Variation should be "Chess" for Normal Games

    return time_control, variation


#Collecting All Recently Played Openings -> (ECO_list)
white_eco = []
white_fen = []
white_result = []

black_fen = []
black_eco = []
black_result = []

all_games = get_player_games(username)
for monthly_games in all_games:
    for game in monthly_games['games']:
        if not new:
            if get_variation(game)[0] == 'bullet' or get_variation(game)[1] != 'chess':
                continue
        if get_side(game):
            white_eco.append(get_ECO(game['pgn']))
            white_fen.append(get_FEN(game))
            white_result.append(check_for_win(game, get_side(game)))
        else:
            black_eco.append(get_ECO(game['pgn']))
            black_fen.append(get_FEN(game))
            black_result.append(check_for_win(game, get_side(game)))

#Creating Seperate Dataframes Depending on if Player is Black or White
blackdf = pd.DataFrame()
whitedf = pd.DataFrame()

blackdf['ECO'] = black_eco
blackdf['FEN'] = black_fen
blackdf['Result'] = black_result

whitedf['ECO'] = white_eco
whitedf['FEN'] = white_fen
whitedf['Result'] = white_result

#Converts FEN to Vector which Can Be Used To Compare Different Positions
def fen_to_vector(fen):
    pieces = {"r":5,"n":3,"b":3.5,"q":9.5,"k":20,"p":1,"R":-5,"N":-3,"B":-3.5,"Q":-9.5,"K":-20,"P":-1}
    fen = list(str(fen.split()[0]))
    vector = []
    for i in range(len(fen)):
        if fen[i] == "/":
            continue
        if fen[i] in pieces:
            vector.append(pieces[fen[i]])
    return vector

#Adding Vector Columnn to Dataframes
whitedf['Vector'] = whitedf['FEN'].apply(fen_to_vector)
blackdf['Vector'] = blackdf['FEN'].apply(fen_to_vector)


