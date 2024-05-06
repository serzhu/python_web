import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')

django.setup()

from pymongo import MongoClient
from app_quotes.models import Author, Quote, Tag
import configparser
from pathlib import Path

file_config = Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

client = MongoClient(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}?retryWrites=true&w=majority""")
db = client[db_name]

authors = db['author']
quotes = db['quote']
tags_collection = db['tag']

for author in authors.find():
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )

for tag in tags_collection.find():
    print(tag['tag'])
    Tag.objects.get_or_create(tag=tag['tag'])

for quote in quotes.find():
    author = authors.find_one({'_id': quote['author']})
    tags = tags_collection.find({'quote': quote['_id']})
    q = Quote.objects.create(
        quote=quote['quote'],
        author=Author.objects.get(fullname = author['fullname']),
        )
    for tag in tags:
        q.tags.add(Tag.objects.get(tag=tag['tag']))
