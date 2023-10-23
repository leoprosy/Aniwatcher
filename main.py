import chooseShow
import downloadEpisode
import videoPlayer
import os
import inquirer
import colorama
from visual import *
import requests
import lxml.html

root_destination = "C:/Users/lepro/Videos/SHOWS/"

def getEpisodeProperties():
    #getting the the show
    downloaded = os.listdir(root_destination)
    downloaded.append('no')
    question = [
        inquirer.List(
            "downloaded",
            message="Do you want to continue an anime you're currently watching ?",
            choices=downloaded,
        ),
    ]
    answers = inquirer.prompt(question)
    if answers['downloaded'] != 'no':
        show = chooseShow.search(search=answers['downloaded'])
    else: show = chooseShow.search()
    
    #getting the season
    #fetching and selecting available seasons
    try:
        r = requests.get(url=f"https://anime-sama.fr/catalogue/{show[1]}/").text
    except: 
        print('error fetching')

    tree = lxml.html.fromstring(r)
    seasons = tree.xpath('//div/div/script')

    saisons = []
    for i in range(len(seasons)):
        s = seasons[i].text_content().split('"')

        for a in s:
            if 'saison' in a or 'film' in a:
                saisons.append(a[:-7])

    #choosing season
    question = [
        inquirer.List(
            "season",
            message="Which season do you want to watch?",
            choices=saisons,
        ),
    ]
    answers = inquirer.prompt(question)
    season = answers["season"]
    
    #creating folder for the show if doesn't exists already
    if not os.path.exists(root_destination+show[0]):
        os.mkdir(f"{root_destination+show[0]}")
        os.mkdir(f"{root_destination+show[0]}/{season}")
    
    #fetching and selecting available episodes
    available = downloadEpisode.getLink(show, season)
    if available == 'error':
        return "error"
    episodes = len(available)

    #choosing episode
    episode = int(input(f'{IN}Which episode do you want to watch ? (1-{episodes}) : '))
    while episode > episodes or episode < 1:
        episode = int(input(f'{IN}Which episode do you want to watch ? (1-{episodes}) : '))

    return show, season, episode

def getUrl(SHOW, SEASON, EPISODE):
    list = downloadEpisode.getLink(SHOW, SEASON)
    for link in list:
        if f"_{str(EPISODE).rjust(1,'0')}_" in link or f"_{str(EPISODE).rjust(2,'0')}_" in link:
            link = link
    
    if link == "error": 
        print('error downloading')
        while True:
            response = input(f"{IN} Do you want to watch another anime? (y|n)")
            if response == "n":
                return 'error'
            elif response == "y":
                SHOW, SEASON, EPISODE = getEpisodeProperties()
                link = downloadEpisode.getLink(SHOW, SEASON, str(EPISODE))
                if link != "error":
                    return link
            else:
                print(f"{ERR}Invalid input. Please try again.")
    else: return link

def app():
    print(f"""
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

    try:
        show, season, episode = getEpisodeProperties()
    except:
        return

    while True:
        LIST = os.listdir(f'{root_destination}{show[0]}/{season}')
        
        if not f'{episode}.mp4' in LIST:
            url = getUrl(show, season, episode)
            if url == 'error':
                pass
            downloadEpisode.download(url, root_destination, show, season, episode)
            videoPlayer.player(videoSource=f'{root_destination}{show[0]}/{season}/{episode}.mp4', episode=min(LIST), show=show)
            remove = input(f'{IN}Do you want to remove this episode ? (y|n) : ')
            if remove == 'y':
                os.remove(f'{root_destination}{show[0]}/{season}/{episode}.mp4')
        else:
            videoPlayer.player(videoSource=f'{root_destination}{show[0]}/{season}/{episode}.mp4', episode=episode, show=show)
            remove = input(f'{IN}Do you want to remove this episode ? (y|n) : ')
            if remove == 'y':
                os.remove(f'{root_destination}{show[0]}/{season}/{episode}.mp4')

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
    
        show, season, episode = getEpisodeProperties()

if __name__ == "__main__":
    app()