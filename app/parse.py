from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
import requests

BASE_URL = 'https://quotes.toscrape.com/'


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def parse_quotes(quote: Tag) -> Quote:
    print(Quote(
        text=quote.select_one(".text").text,
        author=quote.select_one(".author").text,
        tags=[tag.text for tag in quote.select(".tag")]
    ))


def get_quotes() -> [Quote]:
    text = requests.get(BASE_URL).content
    soup = BeautifulSoup(text, 'html.parser')
    quotes = soup.select(".quote")
    return [parse_quotes(quote) for quote in quotes]


def main(output_csv_path: str) -> None:
    print(get_quotes())


if __name__ == "__main__":
    main("quotes.csv")
