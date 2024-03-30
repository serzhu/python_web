import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from exchange import PBExchangeRates


logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)


    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            command = message.split(' ')
            if command[0] == 'exchange':
                if len(command) == 1:
                    rates = await PBExchangeRates(1).get_rates()
                    await self.send_to_clients(rates)
                elif len(command) == 2  and command[1].isnumeric() and int(command[1]) in range(1,10):
                    rates = await PBExchangeRates(command[1]).get_rates()
                    await self.send_to_clients(rates)
                else:
                    await self.send_to_clients(message)
            else:
                await self.send_to_clients(message)


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    
    asyncio.run(main())
