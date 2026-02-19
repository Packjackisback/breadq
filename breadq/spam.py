import asyncio
from qbreader_client import QBReaderClient
import json

async def launch_bot(i):
    client = QBReaderClient(room="msquizbowl", username=f"$", user_id=f"bot{i}")

    async def handle_chat(msg):
        print(f"bot{i} Chat:", msg)

    async def handle_pause(msg):
        print(f"bot{i} Pause:", msg)
        if msg["username"] != client.username:
            await client.pause()

    client.on("chat", handle_chat)
    client.on("pause", handle_pause)

    await client.start()


async def main():
    tasks = []

    for i in range(100):
        tasks.append(asyncio.create_task(launch_bot(i)))

    await asyncio.gather(*tasks)


asyncio.run(main())
