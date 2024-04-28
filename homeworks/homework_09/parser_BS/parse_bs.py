import json
import requests
from bs4 import BeautifulSoup

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')

def scrape_quotes(start_url):
    quotes_data = []
    authors_data = []
    author_links = set()
    url = start_url
    next_url = ''

    while True:
        soup = get_soup(url)
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        author_links.update(link['href'] for link in soup.select('div[class=quote] span a'))
        next_url = soup.find('li', class_='next').find('a')['href'] if soup.find('li', class_='next') else None
        if next_url == None:
            break
        url = start_url + next_url[1:]
        print(url)

        for quote, author, tag in zip(quotes, authors, tags):
            tags_for_quote = [tag.text for tag in tag.find_all('a', class_='tag')]
            quotes_data.append({
                'quote': quote.text,
                'author': author.text,
                'tags': tags_for_quote
            })

    for link in author_links:
        soup = get_soup(start_url + link[1:])
        fullname = soup.find('h3', class_='author-title').text.split('-')[0].strip()
        print(fullname)
        born_date = soup.find('span', class_='author-born-date').text.strip()
        born_location = soup.find('span', class_='author-born-location').text.strip()
        description = soup.find('div', class_='author-description').text.strip()
        authors_data.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        })

    return quotes_data, authors_data

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    start_url = 'https://quotes.toscrape.com/'
    quotes_data, authors_data = scrape_quotes(start_url)
    save_to_json(quotes_data, 'quotes.json')
    save_to_json(authors_data, 'authors.json')
