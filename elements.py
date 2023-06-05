import os
import chooseShow
import downloadEpisode
import json

root_destination = "C:/Users/fadia/Documents/LEO/SHOWS/"

list = chooseShow.show()
if list == 'not one of these':
    list = chooseShow.search()
    show = chooseShow.title(list)
else:
    with open('shows.json', 'r+') as jsonFile:
        data = json.load(jsonFile)
        show = [data[list], list]

if os.path.exists(root_destination+show[1]):
    downloaded_seasons = os.listdir(root_destination+show[1])
    txt = []
    for seasons in downloaded_seasons:
        txt.append(str(seasons).replace("saison",""))
    season = f"{max(txt)}"
else:
    os.mkdir(root_destination+show[1])
    season = "1"
    os.mkdir(f"{root_destination+show[1]}/saison{season}")

episodes = os.listdir(f"{root_destination}{show[1]}/saison{season}")
if len(episodes) == 0:
    episode = 1
else:
    number = []
    for nb in episodes:
        number.append(nb.replace(".mp4", ""))
    episode = int(max(number))+1

url = downloadEpisode.getLink(show, season, str(episode), root_destination)