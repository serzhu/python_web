import asyncio
from faker import Faker
from pprint import pprint as print
from async_util import async_timed

fake = Faker("en-GB")

@async_timed()
async def get_user_id(uid: int) -> dict:
    await asyncio.sleep(0.5)
    return {
        "id": uid,
        "name": fake.user_name(),
        "email": fake.email(),
    }


@async_timed()
async def main():
    tasks = []
    for i in range(5):
            tasks.append(asyncio.create_task(get_user_id(i)))
    #print(tasks)

    result = await asyncio.gather(*tasks)
    return result

if __name__ == "__main__":

    result = asyncio.run(main())
    print(result)

