import asyncio
import json
import uuid
import websockets

from . import actions

# gotta enable that logging
import logging

class QBReaderClient:
    def __init__(self, room, username, user_id=None, debug_mode=False):
        if debug_mode:
            logging.basicConfig(level=logging.DEBUG)
            logging.getLogger("websockets").setLevel(logging.DEBUG)
            print("Debug Mode ON")
            print("Loading ", username)

        

        self.room = room
        self.username = username
        self.user_id = user_id or str(uuid.uuid4())

        self.ws = None
        self.handlers = {}
        self.send_queue = asyncio.Queue()
        self.running = False
        self.debug_mode = debug_mode

        actions.register(self)
        if debug_mode:
            print(username, " Loaded: ", hasattr(self, "buzz"))

    def on(self, message_type, handler):
        self.handlers[message_type] = handler

    async def emit(self, event_type: str, **data):
        payload = {"type": event_type, **data}
        await self.send(payload)

    async def send(self, payload: dict):
        if self.debug_mode:
            print(f"[{self.user_id}] SEND -> {payload}")
        await self.send_queue.put(payload)

    async def start(self):
        url = (
            f"wss://www.qbreader.org/play/mp/test"
            f"?roomName={self.room}"
            f"&userId={self.user_id}"
            f"&username={self.username}"
        )


        try:
            async with websockets.connect(
                url,
                origin="https://www.qbreader.org",
                ping_interval=None,
                max_size=None,
            ) as ws:
                self.ws = ws
                self.running = True

                await asyncio.gather(
                    self._receiver_loop(),
                    self._sender_loop(),
                    self._heartbeat_loop(),
                )

        except websockets.exceptions.ConnectionClosed as e:
            print(
                f"[{self.user_id}] CLOSED "
                f"code={e.code} reason={e.reason}"
            )
            raise

        except Exception as e:
            print(f"[{self.user_id}] START ERROR -> {e}")
            raise


 
    async def _receiver_loop(self):
        try:
            async for message in self.ws:
                if self.debug_mode:
                    print(f"[{self.user_id}] RECV RAW -> {message}")

                try:
                    data = json.loads(message)
                except Exception as e:
                    print(f"[{self.user_id}] JSON ERROR -> {e}")
                    continue

                msg_type = data.get("type")
                handler = self.handlers.get(msg_type)

                if handler:
                    await handler(data)

        except Exception as e:
            print(f"[{self.user_id}] RECEIVER ERROR -> {e}")
            raise


    async def _sender_loop(self):
        while self.running:
            payload = await self.send_queue.get()
            await self.ws.send(json.dumps(payload))

    async def _heartbeat_loop(self):
        while self.running:
            await asyncio.sleep(20)
            await self.emit("ping")
