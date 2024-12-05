import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

if __name__ == "__main__":
    driver = webdriver.Firefox()
    current_url = "https://www.idnes.cz/plzen/zpravy/strelba-zapadoceska-univerzita-plzen-utok-policie.A241204_164724_plzen-zpravy_rapc" 
    traversed_links = []
    untraversed_links = []
    scroll_count = 5
    json_data = {"json_data": []}
    json_object = json.dumps(json_data)
    with open('output.json', 'w') as file:
        file.write(json_object)
    while True:
        try:
            driver.get(current_url)
            for _ in range(scroll_count):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            page_source = driver.page_source
            traversed_links.append(current_url)
            soup = BeautifulSoup(page_source, 'lxml')
            json_out = {'title': None, 
                        'categories': None, 
                        'number_of_images': None, 
                        'content': None, 
                        'date': None}

            # Extract links
            a_tags = soup.find_all('a', href=True)

            links = filter(lambda link: 'www.idnes.cz/zpravy' in link['href'] and '?' not in link['href'] and '/foto' not in link['href'] and '/tisk' not in link['href'] and '/diskuse' not in link['href'] or '.jpg' not in link['href'], a_tags)
            links = [link['href'] for link in links]
            #links = map(lambda link: "https://www.ceskenoviny.cz" + link if link[0] == '/' else link, links)
            links = set(links)
            links = list(links)


            for link in links:
                if link not in traversed_links:
                    untraversed_links.append(link)

            while True:
                current_url = untraversed_links.pop()
                if current_url not in traversed_links:
                    break

            # Title
            title = soup.find('title').contents[0]
            json_out['title'] = title

            # Categories
            print(current_url)
            categories = soup.find('meta', attrs={'name': 'keywords'})['content']
            json_out['categories'] = categories.replace(' ', '').split(',')

            # Images
            images = soup.find_all('img')
            images = [img['src'] for img in images if 'src' in img]
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
            with open('output.json', 'r+') as file:

                file_data = json.load(file)

                file_data['json_data'].append(json_out)

                file.seek(0)

                json.dump(file_data, file, indent = 4)
        except IndexError as e:
            print(e)
        except Exception as e:
            continue