import asyncio
import multiprocessing
from breadq import QBReaderClient

"""
    Room Locker
    Please don't use this on a public room, I don't condone this.
    Adds a bunch of bots to a room that buzz instantly.

    Seriously don't be an asshole, it really reflects on you that you find enjoyment in annoying others.
    Nobody is sitting here thinking you are cool. Not a single person is even impressed.
"""



async def launch_bot(room_name, i):
    client = QBReaderClient(
        room=room_name,
        username=f"blocking_bot{i}",
        user_id=f"blocking_bot{i}",
        debug_mode=True # uncomment me for debug mode
    )

    async def handle_pause(msg):
        await client.pause()
    async def handle_update(*msg):
        await client.buzz()
    client.on("pause", handle_pause)
    client.on("update-question", handle_update)
    await client.start()


async def worker(start, count, room_name):
    tasks = []
    for i in range(start, start + count):
        tasks.append(asyncio.create_task(launch_bot(room_name, i)))
        await asyncio.sleep(0.2)
    #await asyncio.gather(*tasks, return_exceptions=True) # this eats all of the errors, stops it from exixting early
    await asyncio.gather(*tasks)  # if you want to debug, uncomment this, and uncomment the thing in the client constructor

def run_worker(start, count, room_name):
    asyncio.run(worker(start, count, room_name))


if __name__ == "__main__":
    room = input("Enter the room name (No spaces): ")

    processes = []
    workers = int(input("Enter the number of workers (Recommend 1-3): "))
    bots_per_worker = int(input("Enter the number of bots per worker (Recommend 1-20): "))

    for w in range(workers):
        p = multiprocessing.Process(
            target=run_worker,
            args=(w * bots_per_worker, bots_per_worker, room)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
