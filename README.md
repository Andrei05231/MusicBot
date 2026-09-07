# MusicBOT

Automatically uploads new audio files from the `audio` folder to a Discord channel.

## Setup

1. Install Python 3.10 or newer.
2. Open a terminal with run as admin in this folder.
3. Create and activate the virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install the dependencies:

```powershell
py -m pip install -r requirements.txt
```

5. Create a `.env` file next to `bot.py`:

```env
BOT_TOKEN=your_discord_bot_token
CHANNEL_ID=your_discord_channel_id
```

6. Create an `audio` folder next to `bot.py`.

## Run manually

```powershell
py bot.py
```

## Run in the background

Open **Command Prompt as Administrator**, then run:

```cmd
py make_task.py
```

For the first run do '''
schtasks /Run /TN "Audio Discord Bot"
'''

After that the bot will start automatically when you log in to Windows without opening a terminal.


## Required Discord permissions

The bot needs permission to:

- View the channel
- Send messages
- Attach files
