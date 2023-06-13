import os
from pprint import pprint
import inquirer
import json
import requests
import lxml.html

# def show():
#     root_destination = "C:/Users/fadia/Documents/LEO/SHOWS/"
#     possible_shows = os.listdir(root_destination)
#     possible_shows.append("not one of these")
#     questions = [
#         inquirer.List(
#             "show",
#             message="What show do you want to watch?",
#             choices=possible_shows,
#         ),
#     ]
#     answers = inquirer.prompt(questions)
#     return answers["show"]

def search():
    search = input('What do you want to watch ? \n')

    r = requests.post("https://anime-sama.fr/catalogue/searchbar.php", {
        "query": search
    })
    tree = lxml.html.fromstring(r.text)
    title_elem = tree.xpath('//div[@class="px-4 py-2"]/h1')
    link_elem = tree.xpath('//img/@src')
    # el = {"title":tree.xpath('//h3')[0].text_content(), "link":link_elem[0]}
    results = {}
    for i in range(len(title_elem)):
        link = link_elem[i].split('https://cdn.statically.io/gh/Anime-Sama/IMG/img/contenu/')
        results[title_elem[i].text_content()] = link[1].split(".jpg")[0]
    questions = [
        inquirer.List(
            "show",
            message="What show do you want to watch?",
            choices=results,
        ),
    ]
    answers = inquirer.prompt(questions)
    list = [answers['show'], results[answers['show']]]
    # print(list)

    # with open('shows.json', 'r+') as file:
    #     data = json.load(file)
    #     data[list[0]] = list[1]
    #     print(data)
    #     json.dump(data, file)

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