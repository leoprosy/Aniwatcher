import os
import chooseShow
import downloadEpisode


def show():
    show = chooseShow.search()
    return show

def season(show):
    if os.path.exists(root_destination+show[0]):
        downloaded_seasons = os.listdir(root_destination+show[0])
        txt = []
        for seasons in downloaded_seasons:
            txt.append(str(seasons).replace("saison",""))
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
        number = []
        for nb in episodes:
            number.append(nb.replace(".mp4", ""))
        episode = int(max(number))+1
    return episode

root_destination = "C:/Users/fadia/Documents/LEO/SHOWS/"

def url(show, season, episode):
    link = downloadEpisode.getLink(show, season, str(episode))
    if link == 'error' or 'not deserved':
        return 'error'
    else:
        return link