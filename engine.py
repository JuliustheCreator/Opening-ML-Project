from calendar import c
import pandas as pd
import numpy as np
import requests
from chessdotcom import get_player_stats, get_player_game_archives
import pprint

username = input("Input Player Name: ")
printer = pprint.PrettyPrinter()

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

def get_ECO_from_pgn(pgn, index):
    i = 0
    ECO = ""
    while True:
        i += 1
        if pgn[index] == '"':
            return ECO
        ECO += pgn[index + 1]
        

ECOs = []
#Retrives Recent Games (40%) or Most Games (80%) if Under 500 Games Were Played
def get_player_games(username):
    games = get_player_game_archives(username).json
    game_count = len(games)
    urls = games['archives'][-1]
    games = requests.get(urls).json()
    for game in games['games']:
            ECOindex = game['pgn'].index('ECO')
            ECOs.append(get_ECO_from_pgn(game['pgn'], ECOindex))


data = pd.read_csv("games.csv")