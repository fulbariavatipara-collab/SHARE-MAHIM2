import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# ===== DIRECT CONFIG =====
api_id = 30041446
api_hash = "78a0ef57339654c99dbf5996d7761a67"
SESSION = "1BVtsOHQBu4z_ACP6EV4-ER7LHaSGLk1WUTryvYj6sGPMNJtNSMIOYBc7t81tEUxsl10TJoLgQzwKCS0a9myQ6ENqzdNrRG_zbqpYH_DIqOUs_EiqXcuYzG5ugTY-JV0Caejr0xzUopd8FGzyqXPbY0q9hBa4s_lY531IujFVv88lGe3RiGgkEXUo1TL0mCoZp1JVLvQ3VmY0howdhhpHbGdNUHTd_hMl3hEPZDpxZu6ZIQtwKIe8SoyUnbmy9gEeXrLzr9uGDpDPasCZMPx49JqbPbvt8CCQUNB-FYoEDdnEZ4rs4XJKMoPvpGa_sibWxsv0qGD4kjlztONuI0sx7-PkgKkSsMM="

# ===== CLIENT =====
client = TelegramClient(StringSession(SESSION), api_id, api_hash)

# ===== CONFIG =====
source_channel = "@REPLITSHARE"

targets = [
    "@studywar2021",
    "@hsc234",
    "@Acs_Udvash_Link",
    "@hscacademicandadmissionchatgroup",
    "@hsc_sharing",
    "@chemistryteli",
    "@Dacs2025",
    "@linkedstudies",
    "@buetkuetruetcuet",
    "@haters_hsc",
    "@superb1k",
    "@HHEHRETW",
]

FORWARD_ON = False
MODE = "trigger"
FORWARD_DELAY = 200
MSG_LIMIT = 5

cached_msgs = []

# ===== CACHE =====
async def update_cache():
    global cached_msgs
    cached_msgs = await client.get_messages(source_channel, limit=MSG_LIMIT)
    print("Cache Updated:", len(cached_msgs))

async def auto_cache():
    while True:
        try:
            await update_cache()
        except Exception as e:
            print("Cache error:", e)
        await asyncio.sleep(300)

# ===== SEND =====
async def send_copy(target, msg):
    try:
        if msg.media:
            await client.send_file(target, msg.media, caption=msg.text or "")
        else:
            await client.send_message(target, msg.text or "")
    except FloodWaitError as e:
        print(f"Flood wait: {e.seconds}s")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"Send error to {target}:", e)

# ===== TRIGGER MODE =====
@client.on(events.NewMessage(chats=targets))
async def trigger(event):
    global FORWARD_ON, MODE

    if not FORWARD_ON or MODE != "trigger":
        return

    sender = await event.get_sender()
    if sender and sender.bot:
        return

    if not cached_msgs:
        return

    msg = random.choice(cached_msgs)
    await send_copy(event.chat_id, msg)

# ===== TIMER LOOP =====
async def loop_system():
    while True:
        if FORWARD_ON and MODE == "timer":
            if cached_msgs:
                msg = random.choice(cached_msgs)
                await asyncio.gather(*[send_copy(t, msg) for t in targets])

            await asyncio.sleep(FORWARD_DELAY)
        else:
            await asyncio.sleep(5)

# ===== COMMANDS =====
@client.on(events.NewMessage(from_users="me"))
async def commands(event):
    global FORWARD_ON, MODE, FORWARD_DELAY, MSG_LIMIT

    text = event.raw_text.lower()

    if text == "/on":
        FORWARD_ON = True
        await event.reply("✅ ON")

    elif text == "/off":
        FORWARD_ON = False
        await event.reply("⛔ OFF")

    elif text.startswith("/mode"):
        try:
            MODE = text.split()[1]
            await event.reply(f"Mode: {MODE}")
        except:
            await event.reply("Usage: /mode trigger অথবা /mode timer")

    elif text.startswith("/settime"):
        try:
            FORWARD_DELAY = int(text.split()[1])
            await event.reply(f"Delay: {FORWARD_DELAY}s")
        except:
            await event.reply("Usage: /settime 200")

    elif text.startswith("/setlimit"):
        try:
            MSG_LIMIT = int(text.split()[1])
            await update_cache()
            await event.reply(f"Limit Updated: {MSG_LIMIT}")
        except:
            await event.reply("Usage: /setlimit 5")

# ===== MAIN =====
async def main():
    await client.connect()

    if not await client.is_user_authorized():
        raise Exception("❌ Invalid SESSION")

    print("🚀 Bot Started Successfully")

    await update_cache()

    asyncio.create_task(auto_cache())
    asyncio.create_task(loop_system())

    await client.run_until_disconnected()

asyncio.run(main())# ===== CACHE =====
async def update_cache():
    global cached_msgs
    cached_msgs = await client.get_messages(source_channel, limit=MSG_LIMIT)
    print("Cache Updated")

async def auto_cache():
    while True:
        try:
            await update_cache()
        except Exception as e:
            print("Cache error:", e)
        await asyncio.sleep(300)

# ===== SEND =====
async def send_copy(target, msg):
    try:
        if msg.media:
            await client.send_file(target, msg.media, caption=msg.text or "")
        else:
            await client.send_message(target, msg.text or "")
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print("Send error:", e)

# ===== TRIGGER MODE =====
@client.on(events.NewMessage(chats=targets))
async def trigger(event):
    global FORWARD_ON, MODE

    if not FORWARD_ON or MODE != "trigger":
        return

    sender = await event.get_sender()
    if sender and sender.bot:
        return

    if not cached_msgs:
        return

    msg = random.choice(cached_msgs)
    await send_copy(event.chat_id, msg)

# ===== TIMER LOOP =====
async def loop_system():
    while True:
        if FORWARD_ON and MODE == "timer":
            if cached_msgs:
                msg = random.choice(cached_msgs)
                await asyncio.gather(*[send_copy(t, msg) for t in targets])

            await asyncio.sleep(FORWARD_DELAY)
        else:
            await asyncio.sleep(5)

# ===== COMMANDS =====
@client.on(events.NewMessage(from_users="me"))
async def commands(event):
    global FORWARD_ON, MODE, FORWARD_DELAY, MSG_LIMIT

    text = event.raw_text.lower()

    if text == "/on":
        FORWARD_ON = True
        await event.reply("ON")

    elif text == "/off":
        FORWARD_ON = False
        await event.reply("OFF")

    elif text.startswith("/mode"):
        MODE = text.split()[1]
        await event.reply(MODE)

    elif text.startswith("/settime"):
        FORWARD_DELAY = int(text.split()[1])
        await event.reply(str(FORWARD_DELAY))

    elif text.startswith("/setlimit"):
        MSG_LIMIT = int(text.split()[1])
        await update_cache()
        await event.reply("Updated")

# ===== MAIN =====
async def main():
    await client.connect()

    if not await client.is_user_authorized():
        raise Exception("Invalid SESSION")

    print("Bot Started")

    await update_cache()

    asyncio.create_task(auto_cache())
    asyncio.create_task(loop_system())

    await client.run_until_disconnected()

asyncio.run(main())
