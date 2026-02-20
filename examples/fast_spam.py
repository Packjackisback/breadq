import asyncio
import multiprocessing
from breadq import QBReaderClient
import random

"""
    Fast spammer
    Please don't use this on a public room, I don't condone this.
    Adds a bunch of bots to a room.

    Seriously don't be an asshole, it really reflects on you that you find enjoyment in annoying others.
    Nobody is sitting here thinking you are cool. Not a single person is even impressed.
"""

async def launch_bot(i, room):
    client = QBReaderClient(
        room=room,
        username="SPAMBOT",
        user_id=f"bot{random.randrange(1,10000000)}"
    )
    await client.start()


async def worker(start, count, room):
    tasks = []
    for i in range(start, start + count):
        tasks.append(asyncio.create_task(launch_bot(i, room)))
        await asyncio.sleep(0.2)
    await asyncio.gather(*tasks, return_exceptions=True)


def run_worker(start, count, room):
    asyncio.run(worker(start, count, room))


if __name__ == "__main__":
    room = input("Enter room name: ")
    processes = []
    workers = 3 #only 3 will probably run, oh well
    bots_per_worker = 250

    for w in range(workers):
        p = multiprocessing.Process(
            target=run_worker,
            args=(w * bots_per_worker, bots_per_worker, room)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
