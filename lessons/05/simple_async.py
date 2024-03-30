import asyncio
from time import time, sleep

async def sub_f():
    await asyncio.sleep(1)
    return 'Hello SUB_F!'

async def main():
    result = []
    print('Hello!')
    result = await asyncio.gather(sub_f(), sub_f())
    print(f'coro {result = }')
    #print(sub_f())
    return result

if __name__ == '__main__':
    start = time()
    result = asyncio.run(main())
    end = time() - start
    print(f'entry point {result = }, {end = }')