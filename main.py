import requests
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    content = requests.get("https://www.idnes.cz/zpravy/zahranicni/scholz-litva-estonsko-putin-rozhovor-ukrajina-rusko-valka-nemecko.A241119_093629_zahranicni_jhr")
    soup = BeautifulSoup(content.content, 'lxml')
    json_out = {'title': None, 'categories': None, 'number_of_comments': None, 'number_of_images': None, 'Content': None}

    title = soup.find('title').contents[0]
    json_out['title'] = title


    categories = soup.find('meta', attrs={'name': 'keywords'})['content']
    json_out['categories'] = categories.replace(' ', '').split(',')

    json_object = json.dumps(json_out)
    with open('output.json', 'w') as file:
        file.write(json_object)