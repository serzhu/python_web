
import aiohttp
import asyncio
import argparse
import platform
from pprint import pprint
from datetime import datetime, timedelta
from async_logger import logger, listener

URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

parser = argparse.ArgumentParser()
parser.add_argument("days", default=1, nargs='?', choices=range(1, 11), type=int)
parser.add_argument("--currency", "-c", nargs='+', required=False, default=['USD', 'EUR'], type=str)

try:
    last_days = vars(parser.parse_args()).get("days")
    currencies = vars(parser.parse_args()).get("currency")
    #print(currencies)
except argparse.ArgumentError:
    logger.info("Invalid number of days")

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

async def get_rates(session:aiohttp.ClientSession, url:str):
    result = {}  
    name = url.split('=')[1]
    logger.info(f"Task {name} getting URL: {url}")
    try:
        async with session.get(url) as response:
            if response.status == 200:
                r = await response.json()
                logger.info(f'Task {name} received data from URL')
            else:
                logger.info(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        logger.info(f'Connection error: {url}', str(err))
    data = r.get('exchangeRate')
    result[name] = await make_result(data)
    return result

async def main():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[get_rates(session, url) for url in urls])
        return result

if __name__ == "__main__":
    listener.start()
    try:
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        r = asyncio.run(main())
        pprint(r)
    finally:
        listener.stop()


    
    
