import csv
from dataclasses import dataclass, fields, astuple
from bs4 import BeautifulSoup, Tag
import requests

BASE_URL = 'https://quotes.toscrape.com/'


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


QUOTES_FIELDS = [field.name for field in fields(Quote)]


def parse_quotes(quote: Tag) -> Quote:
    return Quote(
        text=quote.select_one(".text").text,
        author=quote.select_one(".author").text,
        tags=[tag.text for tag in quote.select(".tag")]
    )


def get_num_pages(page_soup: Tag) -> int:
    num_pages = 1
    while True:
        pager = page_soup.select_one(".pager")
        next_button = pager.select_one(".next a")

        if next_button:
            next_url = next_button["href"]
            next_page_content = requests.get(BASE_URL + next_url).content
            page_soup = BeautifulSoup(next_page_content, 'html.parser')
            num_pages += 1
        else:
            break

    return num_pages


def get_single_page_quotes(page_soup: Tag) -> [Quote]:
    quotes = page_soup.select(".quote")
    return [parse_quotes(quote) for quote in quotes]


def get_page_quotes() -> [Quote]:
    text = requests.get(BASE_URL).content
    first_page_soup = BeautifulSoup(text, 'html.parser')

    # num of pages
    all_quotes = get_single_page_quotes(first_page_soup)
    num_pages = get_num_pages(first_page_soup)

    # iterate

    for page_num in range(2, num_pages + 1):
        next_url = f"/page/{page_num}/"
        text = requests.get(BASE_URL + next_url).content
        next_page_soup = BeautifulSoup(text, 'html.parser')
        all_quotes.extend(get_single_page_quotes(next_page_soup))
    return all_quotes


def write_quotes_to_csv(quotes: [Quote]) -> None:
    with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(QUOTES_FIELDS)
        writer.writerows([astuple(quote) for quote in quotes])


def main(output_csv_path: str) -> None:
    write_quotes_to_csv(get_page_quotes())


if __name__ == "__main__":
    main("quotes.csv")
