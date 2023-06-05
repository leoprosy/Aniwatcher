from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from tqdm import tqdm
import os

def getLink(show, season, episode, root_destination):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument("--log-level=3")
    driver = webdriver.Chrome("C:/Users/fadia/AppData/Roaming/chromedriver_win32/chromedriver.exe", options=op)
    driver.get(f'https://anime-sama.fr/catalogue/{show[0]}/saison{season}/vostfr/')
    select = Select(driver.find_element(By.ID, 'selectEpisodes'))
    last = [option.text for option in select.options][-1]
    for option in select.options:
        if option.text == f'EPISODE {episode}':
            option.click()
            if option.text == last:
                os.mkdir(f'{root_destination}{show[1]}/saison{str(int(season)+1)}')
            break
    # for option in select.find_elements_by_xpath('.//option'):
    #     # print(f'option text = {option.text}')
    #     if option.text == f'EPISODE {episode}':
    #         option.click() # select() in earlier versions of webdriver
    #         break
    # select.select_by_visible_text(f'Episode {episode}')
    url = driver.find_element(By.ID, "playerASsrc")
    url = url.get_attribute('src')
    return url

def download(url, root_destination, show, season, episode):
    r = requests.get(url, stream=True)
    open(f"{root_destination}/{show[1]}/saison{season}/{episode}.mp4", "wb").write(r.content)
    total_size_in_bytes = int(r.headers.get('Content-Length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(f"{root_destination}/{show[1]}/saison{season}/{episode}.mp4", 'wb') as file:
        for data in r.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
