import connect 
import redis
from redis_lru import RedisLRU
from models import Author, Quote
import timeit

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_author(author_names: list) -> list:
    quotes = []
    for name in author_names:
        authors = Author.objects(fullname__iregex=name)
        quotes.extend(Quote.objects(author__in=authors))
    return [(f'{quote.author.fullname}: {quote.quote}') for quote in quotes]

@cache
def find_tags(tags: list) -> list:
    quotes = []
    for tag in tags:
        quotes.extend(Quote.objects(tags__iexact=tag))
    return [(f'{quote.tags}: {quote.quote}') for quote in quotes]

if __name__ == '__main__':
    while True:
        query = input('>>>')
        if query.lower() in {'exit', 'q', 'e'}:
            break
        command, params = map(str.strip, query.split(':'))
        if command == 'name':
            start_time = timeit.default_timer()
            quotes = find_author(params.split(','))
            print(f'Duration: {timeit.default_timer() - start_time}')

        elif command in {'tag', 'tags'}:
            start_time = timeit.default_timer()
            quotes = find_tags(params.split(','))
            print(f'Duration: {timeit.default_timer() - start_time}')
        else:
            print("Invalid command. Please use 'name:' or 'tag:' followed by your search terms.")
            continue
        if quotes:
            for item in quotes:
                print(item)
        else:
            print("No quotes found.")