from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import json


def Crawler(driver: webdriver, start_url: str, parser: str, backup_urls: list):

    current_url = start_url
    scroll_count = 5
    traversed_links = set()
    untraversed_links = set()

    def json_init():
        json_data = {"json_data": []}
        json_object = json.dumps(json_data)
        with open('output.json', 'w') as file:
            file.write(json_object)

    def dump_to_file(json_data):

        with open('output.json', 'r+') as file:

            file_data = json.load(file)

            file_data['json_data'].append(json_data)

            file.seek(0)

            json.dump(file_data, file, indent = 4)


    def set_next_url():
        global current_url

        driver.get(current_url)
        for _ in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        page_source = driver.page_source
        traversed_links.add(current_url)

        return page_source
    
    
    def get_data(page_to_crawl):
        global current_url

        soup = BeautifulSoup(page_to_crawl, 'lxml')
        json_out = {'title': None, 
                    'categories': None, 
                    'number_of_images': None, 
                    'content': None, 
                    'date': None}
        
        a_tags = soup.find_all('a', href=True)

        links = filter(lambda link: "/zpravy" in link['href'], a_tags)
        links = [link['href'] for link in links]
        links = map(lambda link: "https://www.ceskenoviny.cz" + link if link[0] == '/' else link, links)
        links = set(links)
        links = list(links)

        for link in links:
            if link not in traversed_links:
                untraversed_links.add(link)

        while True:
            current_url = untraversed_links.pop()
            if current_url not in traversed_links:
                break

        title = soup.find('title').contents[0]
        json_out['title'] = title

        categories = soup.find('meta', attrs={'name': 'keywords'})['content']
        json_out['categories'] = categories.replace(' ', '').split(',')

        images = soup.find_all('img')
        images = [img['src'] for img in images]
        json_out['number_of_images'] = len(images)

        article_content = soup.find('div', id='articlebody')
        article_content = soup.find_all('p', attrs={'class': None}, id=None)
        article_content = filter(lambda p: not p.find('span'), article_content)
        article_content = [p.text for p in article_content]
        out = ""
        for content in article_content:
            out += (content + " ")

        json_out['content'] = out

        date = soup.find('span', itemprop='datePublished')['content']
        json_out['date'] = date

        return json_out

    def crawl():
        global current_url

        try:
            while True:
                page_to_crawl = set_next_url()
                json_data = get_data(page_to_crawl)
                dump_to_file(json_data)



        except Exception:
            if len(backup_urls) <= 0:
                raise LookupError("Everything crawled")
            current_url = backup_urls.pop()
            crawl()
        

    return {'json_init': json_init,'crawl': crawl}


if __name__ == "__main__":

    crawler = Crawler(driver=webdriver.Firefox(), 
                    parser='lxml', 
                    start_url="https://www.ceskenoviny.cz/zpravy/afp-trosky-z-notre-dame-jsou-uschovane-a-studovane-na-tajnem-miste/2601030", 
                    backup_urls=["https://www.ceskenoviny.cz/zpravy/satelitni-mytny-system-za-pet-let-fungovani-vybral-722-miliardy-kc/2603629",
                                "https://www.ceskenoviny.cz/zpravy/na-znovuotevreni-notre-dame-dorazi-i-trump-v-akci-bude-6000-policistu/2603610",
                                "https://www.ceskenoviny.cz/zpravy/fotbalistky-se-v-odvete-baraze-utkaji-s-portugalskem-o-historicky-postup-na-euro/2603331",
                                "https://www.ceskenoviny.cz/zpravy/studie-vitamin-e-v-elektronickych-cigaretach-poskozuje-ochrannou-vrstvu-plic/2603337",
                                "https://www.ceskenoviny.cz/zpravy/zive-firma-compas-expert-na-prumyslovou-automatizaci-se-predstavi-na-msv-2024/2579886"])


    crawler['json_init']()
    crawler['crawl']()