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
]

client = TelegramClient(
    "session_name",
    api_id,
    api_hash,
    device_model="Railway",
    system_version="Linux",
    app_version="1.0"
)

# ===== CONTROL =====
FORWARD_ON = False
MODE = "trigger"
FORWARD_DELAY = 120
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
            print("♻ Auto refreshed")
        except Exception as e:
            print("❌ Cache error:", e)
        await asyncio.sleep(180)

# ===== SAFE SEND =====
async def send_copy(target, msg):
    try:
        await asyncio.sleep(random.randint(1,3))  # anti-ban delay

        if msg.media:
            await client.send_file(target, msg.media, caption=msg.text or "")
        else:
            await client.send_message(target, msg.text)

    except FloodWaitError as e:
        print(f"⏳ FloodWait {e.seconds}s")
        await asyncio.sleep(e.seconds)

    except Exception as e:
        print("❌ Send error:", e)

# ===== TRIGGER MODE =====
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

    print("⚡ Trigger sent")

# ===== TIMER MODE =====
async def loop_system():
    while True:
        try:
            if FORWARD_ON and MODE == "timer":

                if not cached_msgs:
                    await asyncio.sleep(5)
                    continue

                msg = random.choice(cached_msgs)

                await asyncio.gather(*[
                    send_copy(t, msg) for t in targets
                ])

                print(f"⏱ Timer sent → {FORWARD_DELAY}s")

                await asyncio.sleep(FORWARD_DELAY)
            else:
                await asyncio.sleep(5)

        except Exception as e:
            print("❌ Loop error:", e)
            await asyncio.sleep(5)

# ===== COMMAND HANDLER =====
@client.on(events.NewMessage)
async def command_handler(event):

    global FORWARD_ON, MODE, FORWARD_DELAY, MSG_LIMIT

    me = await client.get_me()

    if event.sender_id != me.id:
        return

    text = event.raw_text.lower()

    if text == "/on":
        FORWARD_ON = True
        await event.reply("✅ ON")

    elif text == "/off":
        FORWARD_ON = False
        await event.reply("⛔ OFF")

    elif text.startswith("/mode"):
        MODE = text.split()[1]
        await event.reply(f"⚙ Mode → {MODE}")

    elif text.startswith("/settime"):
        FORWARD_DELAY = int(text.split()[1])
        await event.reply(f"⏱ {FORWARD_DELAY}s")

    elif text.startswith("/setlimit"):
        MSG_LIMIT = int(text.split()[1])
        await update_cache()
        await event.reply(f"📩 Limit {MSG_LIMIT}")

    elif text == "/refresh":
        await update_cache()
        await event.reply("♻ Refreshed")

    elif text == "/status":
        await event.reply(
            f"ON: {FORWARD_ON}\nMODE: {MODE}\nTIME: {FORWARD_DELAY}s\nLIMIT: {MSG_LIMIT}"
        )

    elif text == "/help":
        await event.reply(
            "/on /off\n"
            "/mode trigger|timer\n"
            "/settime 120\n"
            "/setlimit 5\n"
            "/refresh\n"
            "/status"
        )

# ===== MAIN =====
async def main():
    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Session invalid")
        return

    print("🔥 Bot Started")

    await update_cache()

    client.loop.create_task(auto_cache())
    client.loop.create_task(loop_system())

    await client.run_until_disconnected()

# ===== AUTO RESTART =====
async def safe_main():
    while True:
        try:
            await main()
        except Exception as e:
            print("💥 Crash:", e)
            await asyncio.sleep(5)
            print("🔄 Restarting...")

asyncio.run(safe_main())
