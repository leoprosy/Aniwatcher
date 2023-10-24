import setup
import videoPlayer
import os
from visual import *

try:
    import requests
    import lxml.html
    import inquirer
    import colorama
    from tqdm import tqdm
except:
    setup.install_depedencies()

root_destination = "C:/Users/lepro/Videos/ANIMES/"

def search(search=False):
    if not search:
        search = input(f'\n{IN}What do you want to watch ? ')

    r = requests.post("https://anime-sama.fr/catalogue/searchbar.php", {
        "query": search
    })
    tree = lxml.html.fromstring(r.text)
    title_elem = tree.xpath('//div[@class="px-4 py-2"]/h1')
    link_elem = tree.xpath('//img/@src')

    results = {}
    for i in range(len(title_elem)):
        link = link_elem[i].split('https://cdn.statically.io/gh/Anime-Sama/IMG/img/contenu/')
        results[title_elem[i].text_content()] = link[1].split(".jpg")[0]
    print('\n')
    questions = [
        inquirer.List(
            "show",
            message="What show do you want to watch?",
            choices=results,
        ),
    ]
    answers = inquirer.prompt(questions)
    list = [answers['show'], results[answers['show']]]
    
    return list

def getLink(show, season):
    url = f"https://anime-sama.fr/catalogue/{show[1]}/{season}/vostfr/episodes.js"
    r = requests.get(url)

    if "epsAS" in r.text:
        links = r.text.replace('var epsAS = [', '').replace('var eps1 = [', '').replace('var eps2 = [', '').replace('var eps3 = [', '').split()
        list = [
            link.translate({ord(i): None for i in "\n]',;"})
            for link in links
            if "anime-sama" in link
        ]
        return list
    
    else:
        print(f"{ERR}We don't deserve this show for the moment but we're working on adding it \n")
        return "error"

def download(url, urlOnPc, show, season, episode):
    if url == "error":
        return "error"
    print(f"Downloading {show[0]} - {season} episode {episode}")
    r = requests.get(url, stream=True)
    total_size_in_bytes = int(r.headers.get('Content-Length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(urlOnPc, 'wb') as file:
        for data in r.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

def urlOnPc(show, season, episode):
    return f'{root_destination}{show[0]}/{season}/{episode}.mp4'

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
        show = search(search=answers['downloaded'])
    else: show = search()
    
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
    available = getLink(show, season)
    if available == 'error':
        return "error"
    episodes = len(available)

    #choosing episode
    episode = int(input(f'{IN}Which episode do you want to watch ? (1-{episodes}) : '))
    while episode > episodes or episode < 1:
        episode = int(input(f'{IN}Which episode do you want to watch ? (1-{episodes}) : '))

    return show, season, episode

def getUrl(SHOW, SEASON, EPISODE):
    list = getLink(SHOW, SEASON)
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
                link = getLink(SHOW, SEASON, str(EPISODE))
                if link != "error":
                    return link
            else:
                print(f"{ERR}Invalid input. Please try again.")
    else: return link

ASCII = r"""
           _____    _______  ____ __      __  _________________________   ___ ________________________ 
          /  _  \   \      \ |   /  \    /  \/  _  \__    ___/\_   ___ \ /   |   \_   _____/\______   \ 
         /  /_\  \  /   |   \|   \   \/\/   /  /_\  \|    |   /    \  \//    ~    \    __)_  |       _/
        /    |    \/    |    \   |\        /    |    \    |   \     \___\    Y    /        \ |    |   \ 
        \____|__  /\____|__  /___| \__/\  /\____|__  /____|    \______  /\___|_  /_______  / |____|_  /
                \/         \/           \/         \/                 \/       \/        \/         \/   
        """

def app():
    print(f"""{colorama.Fore.LIGHTRED_EX}
    {ASCII}
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
        
        localUrl = urlOnPc(show, season, episode)
        if not f'{episode}.mp4' in LIST:
            url = getUrl(show, season, episode)
            if url == 'error':
                pass
            download(url, localUrl, show, season, episode)
            videoPlayer.player(videoSource=localUrl, episode=episode, show=show)
            remove = input(f'{IN}Do you want to remove this episode ? (y|n) : ')
            if remove == 'y':
                os.remove(localUrl)
        else:
            videoPlayer.player(videoSource=localUrl, episode=episode, show=show)
            remove = input(f'{IN}Do you want to remove this episode ? (y|n) : ')
            if remove == 'y':
                os.remove(localUrl)

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