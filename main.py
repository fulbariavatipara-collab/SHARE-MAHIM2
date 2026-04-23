import asyncio
import random
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# ===== CONFIG =====
api_id = int(os.getenv("30041446"))
api_hash = os.getenv("78a0ef57339654c99dbf5996d7761a67")
SESSION = os.getenv("1BVtsOJIBu5MWmY20fZgMRv-ItHra1aml68s7D_Gm9S_f8bayF1uWOlfgbHkOq8tdXbUqA5YfTfXzhxPhGbVuvh2BZu-B7mbZoIBDiEfxaszRC-WKRqMJDyz-kmM8z-oHpRscj730-dwDqWawASvoqWmZEY5aGvtRhEuyTreZJMEn9KkVY0DmQUuy-bzPbJa0oSyTXKSJaWUE-FI_mjjyf8N7DI93uIX2PPi2KHyeSkz6hWdBDaqoSArrH2g4Q_4ipIRxVbDMaND9fgXjL2Op17iFQEA6WJTG21TWZjv8dfIV0tkeQRnrnlClU3mJ3qYA09RufPNWcTpLLtEgrV0zv0x51rAZdFQ=")

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

client = TelegramClient(StringSession(SESSION), api_id, api_hash)

# ===== CONTROL =====
FORWARD_ON = False
MODE = "trigger"
FORWARD_DELAY = 200
MSG_LIMIT = 5

cached_msgs = []

# ===== CACHE =====
async def update_cache():
    global cached_msgs
    cached_msgs = await client.get_messages(source_channel, limit=MSG_LIMIT)
    print("⚡ Cache Updated")

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
        print("Send error:", e)

# ===== TRIGGER MODE =====
@client.on(events.NewMessage(chats=targets))
async def trigger_mode(event):
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

# ===== TIMER MODE =====
async def loop_system():
    while True:
        if FORWARD_ON and MODE == "timer":
            if not cached_msgs:
                await asyncio.sleep(5)
                continue

            msg = random.choice(cached_msgs)
            await asyncio.gather(*[send_copy(t, msg) for t in targets])
            await asyncio.sleep(FORWARD_DELAY)
        else:
            await asyncio.sleep(5)

# ===== COMMAND =====
@client.on(events.NewMessage(from_users='me'))
async def command_handler(event):
    global FORWARD_ON, MODE, FORWARD_DELAY, MSG_LIMIT

    if not event.is_private:
        return

    text = event.raw_text.lower()

    if text == "/on":
        FORWARD_ON = True
        await event.reply("✅ Forward ON")

    elif text == "/off":
        FORWARD_ON = False
        await event.reply("❌ Forward OFF")

    elif text.startswith("/mode"):
        MODE = text.split()[1]
        await event.reply(f"⚙ Mode: {MODE}")

    elif text.startswith("/settime"):
        FORWARD_DELAY = int(text.split()[1])
        await event.reply(f"⏱ Timer Delay: {FORWARD_DELAY}s")

    elif text.startswith("/setlimit"):
        MSG_LIMIT = int(text.split()[1])
        await update_cache()
        await event.reply(f"📩 Cache Limit: {MSG_LIMIT}")

    elif text == "/refresh":
        await update_cache()
        await event.reply("♻ Cache Refreshed")

    elif text == "/status":
        await event.reply(
            f"Forward: {'ON' if FORWARD_ON else 'OFF'}\n"
            f"Mode: {MODE}\n"
            f"Timer Delay: {FORWARD_DELAY}s\n"
            f"Limit: {MSG_LIMIT}"
        )

    elif text == "/help":
        await event.reply(
            "📌 Commands:\n"
            "/on\n/off\n"
            "/mode trigger\n"
            "/mode timer\n"
            "/settime 200\n"
            "/setlimit 5\n"
            "/refresh\n"
            "/status"
        )

# ===== START =====
async def main():
    await client.connect()

    if not await client.is_user_authorized():
        raise Exception("❌ Invalid SESSION")

    print("🔥 Userbot Started")

    await update_cache()
    client.loop.create_task(auto_cache())
    client.loop.create_task(loop_system())

    await client.run_until_disconnected()

asyncio.run(main())
