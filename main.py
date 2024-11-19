import requests
import beautifulsoup


if __name__ == "__main__":
    x = requests.get("https://www.idnes.cz/zpravy/zahranicni/scholz-litva-estonsko-putin-rozhovor-ukrajina-rusko-valka-nemecko.A241119_093629_zahranicni_jhr")
    print(x.content)
