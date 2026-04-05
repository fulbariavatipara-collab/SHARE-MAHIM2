import asyncio
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# ===== CONFIG =====
api_id = 30041446
api_hash = "78a0ef57339654c99dbf5996d7761a67"

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

client = TelegramClient("session_name", api_id, api_hash)

# ===== CONTROL =====
FORWARD_ON = False
MODE = "trigger"        # "trigger" or "timer"
FORWARD_DELAY = 200     # seconds
MSG_LIMIT = 5

# ===== CACHE =====
cached_msgs = []


async def update_cache():
    global cached_msgs
    cached_msgs = await client.get_messages(source_channel, limit=MSG_LIMIT)
    print("⚡ Cache Updated")


async def auto_cache():
    while True:
        try:
            await update_cache()
        except Exception as e:
            print(e)
        await asyncio.sleep(300)


async def send_copy(target, msg):
    try:
        if msg.media:
            await client.send_file(target, msg.media, caption=msg.text or "")
        else:
            await client.send_message(target, msg.text)
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(e)


@client.on(events.NewMessage(chats=targets))
async def trigger_mode(event):

    global FORWARD_ON, MODE
    if not FORWARD_ON or MODE != "trigger":
        return

    sender = await event.get_sender()
    if sender.bot:
        return

    if not cached_msgs:
        return

    msg = random.choice(cached_msgs)

    await send_copy(event.chat_id, msg)
    print(f"⚡ Trigger sent to {event.chat.title if hasattr(event.chat,'title') else event.chat_id}")


async def loop_system():
    while True:
        if FORWARD_ON and MODE == "timer":

            if not cached_msgs:
                await asyncio.sleep(5)
                continue

            msg = random.choice(cached_msgs)

            await asyncio.gather(*[send_copy(t, msg) for t in targets])
            print(f"⏱ Timer sent → Next in {FORWARD_DELAY}s")

            await asyncio.sleep(FORWARD_DELAY)
        else:
            await asyncio.sleep(5)


@client.on(events.NewMessage(from_users='me'))
async def command_handler(event):

    global FORWARD_ON, MODE, FORWARD_DELAY, MSG_LIMIT

    if not event.is_private or event.chat_id != event.sender_id:
        return

    text = event.raw_text.lower()

    if text == "/on":
        FORWARD_ON = True
        await event.reply("✅ Forward ON")

    elif text == "/off":
        FORWARD_ON = False
        await event.reply("⛔ Forward OFF")

    elif text.startswith("/mode"):
        MODE = text.split()[1]
        await event.reply(f"⚙ Mode set to {MODE}")

    elif text.startswith("/settime"):
        FORWARD_DELAY = int(text.split()[1])
        await event.reply(f"⏱ Timer set {FORWARD_DELAY}s")

    elif text.startswith("/setlimit"):
        MSG_LIMIT = int(text.split()[1])
        await update_cache()
        await event.reply(f"📩 Limit {MSG_LIMIT}")

    elif text == "/refresh":
        await update_cache()
        await event.reply("♻ Cache refreshed")

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
            "/on           → Forward ON\n"
            "/off          → Forward OFF\n"
            "/mode trigger → Ultra Fast Trigger mode\n"
            "/mode timer   → Timer mode\n"
            "/settime 200  → Timer delay\n"
            "/setlimit 5   → Cache limit\n"
            "/refresh      → Refresh cache\n"
            "/status       → Show status\n"
            "/help         → Help"
        )


async def main():
    await client.start()
    print("🔥 Userbot Started")

    await update_cache()
    client.loop.create_task(auto_cache())
    client.loop.create_task(loop_system())

    await client.run_until_disconnected()


asyncio.run(main())
