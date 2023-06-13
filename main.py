import elements
import downloadEpisode
import videoPlayer
import os
import inquirer


show = elements.show()
season = elements.season(show)
episode = elements.episode(episodes=os.listdir(f"{elements.root_destination}{show[0]}/saison{season}"))

while 1 == 1:
    LIST = os.listdir(f'{elements.root_destination}{show[0]}/saison{season}')
    if len(LIST) == 0:
        LIST = ['1.mp4']
    if len(LIST) == 0 or len(LIST) == 1:
        url = elements.url(show, season, episode)
        if url == "error":
            # print("There was an error downloading \n")
            pass
        else:
            downloadEpisode.download(url, elements.root_destination, show, season, episode)
            videoPlayer.player(videoSource=f'{elements.root_destination}{show[0]}/saison{season}/{min(LIST)}', episode=min(LIST), show=show[1])
            os.remove(f"{elements.root_destination}/{show[0]}/saison{season}/{min(LIST)}")
    else:
        videoPlayer.player(videoSource=f'{elements.root_destination}{show[0]}/saison{season}/{min(LIST)}', episode=min(LIST), show=show[1])
        os.remove(f"{elements.root_destination}/{show[0]}/saison{season}/{min(LIST)}")

    question = [
        inquirer.List(
            "continue",
            message="Do you want to continue to watch?",
            choices=["Yes", "No"],
        ),
    ]
    answers = inquirer.prompt(question)
    if answers["continue"] == "No":
        break

    show = elements.show()
    season = elements.season(show)
    episode = elements.episode(episodes=os.listdir(f"{elements.root_destination}{show[0]}/saison{season}"))
