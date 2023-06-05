from elements import *
import downloadEpisode
import chooseShow
import videoPlayer
import os

LIST = os.listdir(f'{root_destination}{show[1]}/saison{season}')
print(LIST)
print(min(LIST))
if len(LIST) == 0:
    downloadEpisode.download(url, root_destination, show, season, episode)
else:
    videoPlayer.player(videoSource=f'{root_destination}{show[1]}/saison{season}/{min(LIST)}', episode=min(LIST))
