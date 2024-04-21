import json
from pathlib import Path
import connect
from models import Author, Quote, Tag

p = Path(__file__)

with open(p.parent / 'authors.json') as file:
    authors_list = json.load(file)

with open(p.parent / 'quotes.json') as file:
    quotes_list = json.load(file)

for item in authors_list:
    a = Author(fullname = item['fullname'], born_date = item['born_date'], born_location = item['born_location'], description = item['description'])
    a.save()
    for quote in quotes_list:
        if quote['author'] == item['fullname']:
            q = Quote(quote = quote['quote'], author = a)
            q.save()
            for tag in quote['tags']:
                t = Tag(quote = q, tag = tag)
                t.save()


   


