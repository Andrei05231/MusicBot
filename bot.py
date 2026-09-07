
import asyncio
import os
import time
from pathlib import Path

import discord
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ====== CONFIGURATION ======
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("Missing BOT_TOKEN or CHANNEL_ID in .env")

WATCH_FOLDER = Path(__file__).resolve().parent / "audio"

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".m4a",
    ".ogg",
    ".aac",
    ".opus",
}

# ====== DISCORD BOT ======
intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def send_audio(file_path: Path):
    """Wait for the file to finish copying, then upload it."""
    print(f"New audio detected: {file_path.name}")

    # Wait until the file is no longer changing.
    last_size = -1

    for _ in range(60):
        if not file_path.exists():
            return

        current_size = file_path.stat().st_size

        if current_size == last_size:
            break

        last_size = current_size
        await asyncio.sleep(1)

    if not file_path.exists():
        return

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print(f"Could not find channel ID: {CHANNEL_ID}")
        print("Trying to fetch the channel from Discord...")

        try:
            channel = await client.fetch_channel(CHANNEL_ID)
        except Exception as e:
            print(f"Fetch error: {e}")
            return
    try:
        await channel.send(
            content=f"New audio: **{file_path.name}**",
            file=discord.File(file_path),
        )

        print(f"Sent: {file_path.name}")

    except Exception as e:
        print(f"Error sending file: {e}")


# ====== FOLDER WATCHER ======
class AudioHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() in AUDIO_EXTENSIONS:
            # Schedule the upload on Discord's event loop.
            asyncio.run_coroutine_threadsafe(
                send_audio(file_path),
                client.loop,
            )


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Watching folder: {WATCH_FOLDER.resolve()}")

    WATCH_FOLDER.mkdir(exist_ok=True)

    observer = Observer()
    observer.schedule(
        AudioHandler(),
        str(WATCH_FOLDER),
        recursive=False,
    )
    observer.start()

    print("Watching for new audio files...")

    try:
        await asyncio.Event().wait()
    finally:
        observer.stop()
        observer.join()


client.run(BOT_TOKEN)
