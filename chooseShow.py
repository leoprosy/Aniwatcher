import os
from pprint import pprint
import inquirer
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import *
from lxml import etree
import lxml

root_destination = "C:/Users/fadia/Documents/LEO/SHOWS/"
possible_shows = os.listdir(root_destination)
possible_shows.append("not one of these")

def show():
    questions = [
        inquirer.List(
            "show",
            message="What show do you want to watch?",
            choices=possible_shows,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers["show"]

def search():
    search = input('What do you want to watch so ? \n')

    f = open('shows.json', 'r+')
    data = json.load(f)
    if search in data:
        list = [[data[search], search]]
    else:
        new = input('go to anime-sama.fr and then search the anime you want to watch and paste it there \n')
        data[search] = new
        list = [[new, search]]
        with open('shows.json', 'r+') as jsonFile:
            json.dump(data, jsonFile)
        # obj = {search: new}
        # json_obj = json.dumps(obj, indent=1)
        # list = [obj[search]]
        # f.update(json_obj)

    # op = webdriver.ChromeOptions()
    # op.add_argument('headless')
    # op.add_argument("--log-level=3")
    # driver = webdriver.Chrome("C:/Users/fadia/AppData/Roaming/chromedriver_win32/chromedriver.exe", options=op)
    # driver.get('https://anime-sama.fr/catalogue/')
    # driver.find_element(By.ID, "search_text_catalogue").send_keys(search)
    # # driver.find_element(By.ID, "search_text").send_keys(search)
    # results = driver.find_element(By.XPATH, "//div[@id='result_catalogue']")
    # # results = driver.find_element(By.XPATH, "//div[@id='result']")
    # # print(results)
    # try:
    #     result = driver.find_elements(By.XPATH, "//div[@id='result_catalogue']/div/div/a")
    # except StaleElementReferenceException:
    #     result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/div/div/a')))
    # # result = results.find_elements(By.XPATH, "//div[@id='result_catalogue']/div/div/a")
    # # print(result[0])
    # # print(result.__getattribute__('href'))
    # list= []
    # for i in range(len(result)):
    #     try:
    #         # print('hi '+str(i+1))
    #         # res = etree.parse(result[i])
    #         # print(result)
    #         link = result[i].get_attribute('href')
    #     except StaleElementReferenceException:
    #         # print('here ' +str(i+1))
    #         res = driver.find_elements(By.XPATH, "//div[@id='result_catalogue']/div/div/a")
    #         # print(res)
    #         link = res[i].get_attribute('href')
    #     name = link.split('https://anime-sama.fr/catalogue/')
    #     title = name[1].split('/')
    #     list.append(title[0])
    # driver.close()
    return list

def title(list):
    # if len(list) > 1:
    #     questions = [
    #         inquirer.List(
    #             "show",
    #             message="What show do you want to watch in this list?",
    #             choices=list,
    #         ),
    #     ]
    #     answer = inquirer.prompt(questions)
    #     answers = [answer["show"]]
    #     answers.append(str(answer["show"]).replace('-', ' '))
    # else:
    answers = list[0]
    return answers