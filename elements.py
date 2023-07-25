import os
import chooseShow
import downloadEpisode
from visual import *


def show():
    show = chooseShow.search()
    return show

def season(show):
    if os.path.exists(root_destination+show[0]):
        downloaded_seasons = os.listdir(root_destination+show[0])
        txt = [
            str(seasons).replace('saison', '')
            for seasons in downloaded_seasons
        ]
        season = f"{max(txt)}"
    else:
        os.mkdir(root_destination+show[0])
        season = "1"
        os.mkdir(f"{root_destination+show[0]}/saison{season}")
    return season

def episode(episodes):
    if len(episodes) == 0:
        episode = 1
    else:
        number = [
            nb.replace('.mp4', '')
            for nb in episodes]
        print(number)
        episode = int(max(number))+1
    return episode

root_destination = "C:/Users/fadia/Documents/LEO/SHOWS/"

def url(SHOW, SEASON, EPISODE):
    link = downloadEpisode.getLink(SHOW, SEASON, str(EPISODE))
    if link == "error": 
        while True:
            response = input(f"{IN}Do you want to watch another anime? (y|n)")
            if response == "n":
                return 'error'
            elif response == "y":
                SHOW = show()
                SEASON = season(SHOW)
                EPISODE = episode(episodes=os.listdir(f"{root_destination}{SHOW[0]}/saison{SEASON}"))
                link = downloadEpisode.getLink(SHOW, SEASON, str(EPISODE))
                if link != "error":
                    return link
            else:
                print(f"{ERR}Invalid input. Please try again.")
    else: return link