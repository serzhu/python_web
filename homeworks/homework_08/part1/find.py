import connect 
import redis
from redis_lru import RedisLRU
from models import Author, Quote, Tag
import timeit

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_author(author_name: str) -> list:
    a = Author.objects(fullname__iregex=author_name)
    quotes = Quote.objects(author__in=a)
    return [(f'{quote.author.fullname}: {quote.quote}') for quote in quotes]

@cache
def find_tag(tag: str) -> list:
    t = Tag.objects(tag__iregex=tag)
    return [(f'{tag.tag}: {tag.quote.quote}') for tag in t]

@cache
def find_tags(tags: list) -> list:
    t = Tag.objects(tag__in=tags)
    return [(f'{tag.tag}: {tag.quote.quote}') for tag in t]

if __name__ == '__main__':
    while True:
        query = input('>>>')
        if query.lower() in {'exit', 'q', 'e'}:
            break
        command, params = map(str.strip, query.split(':'))
        if command == 'name':
            start_time = timeit.default_timer()
            quotes = find_author(params.split(',')[0])
            print(f'Duration: {timeit.default_timer() - start_time}')
        elif command == 'tag':
            start_time = timeit.default_timer()
            quotes = find_tag(params.split(',')[0])
            print(f'Duration: {timeit.default_timer() - start_time}')
        elif command == 'tags':
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