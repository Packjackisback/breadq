import asyncio

def register(client):

    async def pause(paused_time=0):
        await client.emit("pause", pausedTime=paused_time)

    async def buzz():
        await client.emit("buzz")
        await give_answer_live_update()

    async def ban(userId, username):
        await client.emit("ban", targetId=userId, targetUsername=username)

    async def chat_live_update(message=""):
        await client.emit("chat-live-update", message=message)

    async def chat(message=""):
        await chat-live-update("")
        await client.emit("chat", message=message)

    async def clear_stats():
        await client.emit("clear-stats")

    async def give_answer_live_update(message=""):
        await client.emit("give-answer-live-update", givenAnswer=message)

    async def give_answer(message=""):
        await give_answer_live_update()
        await client.emit("give-answer", givenAnswer=message)



    client.pause = pause
    client.buzz = buzz
    client.ban = ban
    client.chat_live_update = chat_live_update
    client.chat = chat
    client.clear_stats = clear_stats
    client.give_answer_live_update = give_answer_live_update
    client.give_answer = give_answer

    async def do(action_name, **kwargs):
        action = getattr(client, action_name, None)
        if not action:
            raise ValueError(f"Unknown action: {action_name}")
        await action(**kwargs)

    client.do = do
