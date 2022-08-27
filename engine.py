from calendar import c
import pandas as pd
import numpy as np
import requests
from chessdotcom import get_player_stats, get_player_game_archives
import chess.pgn
from io import StringIO


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


#Grabs Game Variation & Time Control
def get_variation(game):
    time_control = game['time_class']
    variation = game['rules']

    #Variation should be "Chess" for Normal Games

    return time_control, variation


#Collecting All Recently Played Openings -> (ECO_list)
ECO_list = []
all_games = get_player_games(username)
for monthly_games in all_games:
    for game in monthly_games['games']:
        if not new:
            if get_variation(game)[0] == 'bullet' or get_variation(game)[1] != 'chess':
                continue
        ECO_list.append(get_ECO(game['pgn']))


