from api import *
from processing import *


def main():
    username = input("Input username: ")
    archives = fetch_archives(username)
    container = []

    for archive in archives:
        games = fetch_games_from_archive(archive)
        container.extend(games)
        
    user_matrix = create_matrix(container, username)
    print(user_matrix)

if __name__ == "__main__":
    main()