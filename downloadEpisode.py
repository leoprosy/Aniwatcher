import requests
from tqdm import tqdm
from visual import *

def getLink(show, season, episode):
    url = f"https://anime-sama.fr/catalogue/{show[1]}/saison{season}/vostfr/episodes.js"
    r = requests.get(url)

    if "epsAS" in r.text:
        links = r.text.replace('var epsAS = [', '').replace('var eps1 = [', '').replace('var eps2 = [', '').replace('var eps3 = [', '').split()
        list = [
            link.translate({ord(i): None for i in "\n]',;"})
            for link in links
            if "anime-sama" in link
        ]
        for link in list:
            if f"_{str(episode).rjust(2,'0')}_" in link:
                return link
            else:
                print(f'{ERR}error')
                return "error" 
    else:
        print(f"{ERR}We don't deserve this show for the moment but we're working on adding it \n")
        return "error"

def download(url, root_destination, show, season, episode):
    if url == "error":
        return
    r = requests.get(url, stream=True)
    total_size_in_bytes = int(r.headers.get('Content-Length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(f"{root_destination}/{show[0]}/saison{season}/{episode}.mp4", 'wb') as file:
        for data in r.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
