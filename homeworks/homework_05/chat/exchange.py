import asyncio
import aiohttp
from aiopath import AsyncPath
from aiofile import async_open
from datetime import datetime, timedelta


BASE_DIR = AsyncPath(__file__).parent
LOGFILE = BASE_DIR / 'log.txt'

class PBExchangeRates():
    def __init__(self, days=1):
        self.url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
        self.currencies = ['USD','EUR']
        self.days = int(days)

    async def write_to_file(self, msg):
        async with async_open(LOGFILE, 'a') as af:
            await af.write(msg + '\n')

    def make_result(self, data: dict):
        day_rates = {}
        for currency in self.currencies:
            for item in data:
                if item.get('currency') == currency:
                    day_rates[currency] = {}
                    day_rates[currency]['sale'] = item.get('saleRate')
                    day_rates[currency]['purchase'] = item.get('purchaseRate')
        return day_rates 

    async def get_from_bank(self, session:aiohttp.ClientSession, url:str):
        result = {}
        name = url.split('=')[1]
        await self.write_to_file(f"Task {name} getting URL: {url}")
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    await self.write_to_file(f'Task {name} received data from URL')
                else:
                    await self.write_to_file(f"Error status: {response.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            await self.write_to_file(f'Connection error: {url}', str(err))
        data = r.get('exchangeRate')
        result[name] =  self.make_result(data)
        return result

    async def get_rates(self):

        await self.write_to_file('Starting get exchange rates')
        d = datetime.today()
        period = [(d - timedelta(days = day)).strftime('%d.%m.%Y') for day in range(self.days)]
        urls = [self.url + day for day in period]
        async with aiohttp.ClientSession() as session:
            rates = await asyncio.gather(*[self.get_from_bank(session, url) for url in urls])
            await self.write_to_file('Finishing get exchange rates')
            return '\n'.join(str(item) for item in rates)


