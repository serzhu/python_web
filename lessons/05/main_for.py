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

async def make_result(data: dict):
    await asyncio.sleep(0)
    day_rates = {}
    for currency in currencies:
        for item in data:
            if item.get('currency') == currency:
                day_rates[currency] = {}
                day_rates[currency]['sale'] = item.get('saleRate')
                day_rates[currency]['purchase'] = item.get('purchaseRate')
    return day_rates 

# async def get_rates(url:str):
#     result = {}
#     name = url.split('=')[1]
#     async with aiohttp.ClientSession() as session:
#         print(f"Task {name} getting URL: {url}")
#         async with session.get(url) as response:
#             r = await response.json()
#             print(f'received data from URL')
#             data = r.get('exchangeRate')
#             result[name] = await make_result(data)
#     return result

async def main():
    result = []
    day_result = {}
    async with aiohttp.ClientSession() as session:
        for url in urls:
            name = url.split('=')[1]
            print(f"Task {name} getting URL: {url}")
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        r = await response.json()
                        print(f'received data from URL')
                        data = r.get('exchangeRate')
                        day_result[name] = await make_result(data)
                        result.append(day_result)
                    else:
                        print(f"Error status: {response.status} for {url}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {url}', str(err))
        return day_result

# async def main():
#     r = []
#     for url in urls:
#         r.append(get_rates(url))
#     return await asyncio.gather(*r)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    pprint(r)