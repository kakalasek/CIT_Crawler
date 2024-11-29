import requests
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    starting_url = "https://www.ceskenoviny.cz/zpravy/zelenskyj-naznacil-ochotu-ukoncit-valku-za-clenstvi-v-nato/2602441" 

    content = requests.get(starting_url)
    soup = BeautifulSoup(content.content, 'lxml')
    json_out = {'title': None, 'categories': None, 'number_of_comments': None, 'number_of_images': None, 'Content': None}

    title = soup.find('title').contents[0]
    json_out['title'] = title


    categories = soup.find('meta', attrs={'name': 'keywords'})['content']
    json_out['categories'] = categories.replace(' ', '').split(',')

    json_object = json.dumps(json_out)
    with open('output.json', 'w') as file:
        file.write(json_object)