import requests
from bs4 import BeautifulSoup
import json
import sys

if __name__ == "__main__":
    starting_url = "https://www.ceskenoviny.cz/zpravy/zelenskyj-naznacil-ochotu-ukoncit-valku-za-clenstvi-v-nato/2602441" 

    downloaded_page = requests.get(starting_url)
    soup = BeautifulSoup(downloaded_page.content, 'lxml')
    json_out = {'title': None, 
                'categories': None, 
                'number_of_images': None, 
                'content': None, 
                'date': None}

    # Extract links
    a_tags = soup.find_all('a', href=True)

    links = filter(lambda link: "/zpravy" in link['href'], a_tags)
    links = [link['href'] for link in links]
    links = set(links)
    links = list(links)

    # Title
    title = soup.find('title').contents[0]
    json_out['title'] = title

    # Categories
    categories = soup.find('meta', attrs={'name': 'keywords'})['content']
    json_out['categories'] = categories.replace(' ', '').split(',')

    # Images
    images = soup.find_all('img')
    images = [img['src'] for img in images]
    json_out['number_of_images'] = len(images)

    # Content
    article_content = soup.find('div', id='articlebody')
    article_content = soup.find_all('p', attrs={'class': None}, id=None)
    article_content = filter(lambda p: not p.find('span'), article_content)
    article_content = [p.text for p in article_content]
    out = ""
    for content in article_content:
        out += (content + " ")

    json_out['content'] = out

    

    # Date
    date = soup.find('span', itemprop='datePublished')['content']
    json_out['date'] = date

    # Dump to JSON
    json_object = json.dumps(json_out)
    with open('output.json', 'w') as file:
        file.write(json_object)

    # Testing 
    try:
        if sys.argv[1] == '-t':
            print(soup.prettify())
    except:
        pass