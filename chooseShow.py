import inquirer
import requests
import lxml.html

def search():
    search = input('What do you want to watch ? \n')

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

def title(list):
    answers = list[0]
    return answers