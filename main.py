import elements
import downloadEpisode
import videoPlayer
import os
import inquirer
import colorama

print(f"""\
{colorama.Fore.LIGHTRED_EX}
       _____    _______  .___ __      __  _________________________   ___ ________________________ 
      /  _  \   \      \ |   /  \    /  \/  _  \__    ___/\_   ___ \ /   |   \_   _____/\______   \ 
     /  /_\  \  /   |   \|   \   \/\/   /  /_\  \|    |   /    \  \//    ~    \    __)_  |       _/
    /    |    \/    |    \   |\        /    |    \    |   \     \___\    Y    /        \ |    |   \ 
    \____|__  /\____|__  /___| \__/\  /\____|__  /____|    \______  /\___|_  /_______  / |____|_  /
            \/         \/           \/         \/                 \/       \/        \/         \/   
{colorama.Fore.LIGHTYELLOW_EX}
                                        By leoprosy
                          Github: https://github.com/leoprosy/Watcher                                                              
""")

show = elements.show()
season = elements.season(show)
episode = elements.episode(episodes=os.listdir(f"{elements.root_destination}{show[0]}/saison{season}"))

while True:
    LIST = os.listdir(f'{elements.root_destination}{show[0]}/saison{season}')
    if len(LIST) == 0:
        LIST = ['1.mp4']
    if len(LIST) in [0, 1] :
        url = elements.url(show, season, episode)
        if url == "error":
            # print("There was an error downloading \n")
            break
        else:
            downloadEpisode.download(url, elements.root_destination, show, season, episode)
            videoPlayer.player(videoSource=f'{elements.root_destination}{show[0]}/saison{season}/{min(LIST)}', episode=min(LIST), show=show)
            # os.remove(f"{elements.root_destination}/{show[0]}/saison{season}/{min(LIST)}")
    else:
        videoPlayer.player(videoSource=f'{elements.root_destination}{show[0]}/saison{season}/{min(LIST)}', episode=min(LIST), show=show)
        # os.remove(f"{elements.root_destination}/{show[0]}/saison{season}/{min(LIST)}")

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
