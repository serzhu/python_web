import asyncio
import aiohttp
import argparse
import logging
import platform
from pprint import pprint
#from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

parser = argparse.ArgumentParser()
parser.add_argument("days", default=1, nargs='?', choices=range(1, 11), type=int)
parser.add_argument("--currency", "-c", nargs='+', required=False, default=['USD', 'EUR'], type=str)

try:
    last_days = vars(parser.parse_args()).get("days")
    currencies = vars(parser.parse_args()).get("currency")
    #print(currencies)
except argparse.ArgumentError:
    print("Invalid number of days")

d = datetime.today()
period = [(d - timedelta(days = day)).strftime('%d.%m.%Y') for day in range(last_days)]
urls = [URL + day for day in period]

async def get_rate(name:str, requests_queue):
    result = {}
    day_rates = {}
    
    async with aiohttp.ClientSession() as session:
        url = await requests_queue.get()
        print(f"Task {name} getting URL: {url}")
        async with session.get(url) as response:
            r = await response.json()
            data = r.get('exchangeRate')
            #print(f"Task {name} got data: {data}")

    for currency in currencies:
        for item in data:
            if item.get('currency') == currency:
                day_rates[currency] = {}
                day_rates[currency]['sale'] = item.get('saleRate')
                day_rates[currency]['purchase'] = item.get('purchaseRate')
    result[name]=day_rates 
    return result

async def main():
    requests_queue = asyncio.Queue()
    for url in urls:
        await requests_queue.put(url)
    tasks = [asyncio.create_task(get_rate(name, requests_queue)) for name in period]
    #print(f'created tasks: {tasks}')
    result = await asyncio.gather(*tasks, return_exceptions=True)
    return result

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    pprint(r)