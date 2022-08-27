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

ECOs = []
#Retrives Recent Games (40%) or Most Games (80%) if Under 500 Games Were Played
def get_player_games(username):
    games = get_player_game_archives(username).json
    game_count = len(games)
    print(game_count)
    urls = games['archives'][-1]
    games = requests.get(urls).json()

def get_ECO(game):
    pass

data = pd.read_csv("games.csv")
get_player_games(username)