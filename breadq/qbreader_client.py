import asyncio
import json
import uuid
import websockets


class QBReaderClient:
    def __init__(self, room, username, user_id=None):
        self.room = room
        self.username = username
        self.user_id = user_id or str(uuid.uuid4())

        self.ws = None
        self.handlers = {}
        self.send_queue = asyncio.Queue()
        self.running = False

    def on(self, message_type, handler):
        """
        Register a handler for a message type.
        """
        self.handlers[message_type] = handler

    async def send(self, payload: dict):
        """
        Queue a message to be sent.
        """
        await self.send_queue.put(payload)

    async def pause(self):
        await self.send({"type": "pause", "pausedTime": 0})

    async def start(self):
        url = (
            f"wss://www.qbreader.org/play/mp/test"
            f"?roomName={self.room}"
            f"&userId={self.user_id}"
            f"&username={self.username}"
        )

        async with websockets.connect(
            url,
            origin="https://www.qbreader.org",
            ping_interval=None
        ) as ws:

            self.ws = ws
            self.running = True

            await asyncio.gather(
                self._receiver_loop(),
                self._sender_loop(),
                self._heartbeat_loop(),
            )

    async def _receiver_loop(self):
        async for message in self.ws:
            try:
                data = json.loads(message)
            except Exception:
                continue

            msg_type = data.get("type")
            handler = self.handlers.get(msg_type)

            if handler:
                await handler(data)

    async def _sender_loop(self):
        while self.running:
            payload = await self.send_queue.get()
            await self.ws.send(json.dumps(payload))

    async def _heartbeat_loop(self):
        while self.running:
            await asyncio.sleep(1)
            await self.send({"type": "ping"})
