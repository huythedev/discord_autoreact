# Auto React Discord Bot

This bot automatically reacts to messages in a Discord server based on your configuration.

## How It Works

- Listens for messages in your Discord server.
- Automatically adds reactions to messages according to your setup.

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Discord bot token and guild ID.

## Requirements

- Python 3.8+
- Discord bot token
- Guild (server) ID

## Configuration

Edit the `.env` file with your credentials:
```
DISCORD_TOKEN="your_discord_bot_token"
GUILD_ID="your_guild_id"
```

## Usage

Start the bot with:
```bash
python main.py
```

## Commands

- `!autoreact set @User <emoji> [#channel ...]`  
  Sets an auto-reaction for a user. Optionally specify channels.
  - Example: `!autoreact set @User 👍 #general`
- `!autoreact remove @User`  
  Removes auto-reaction for a specific user.
  - Example: `!autoreact remove @User`
- `!autoreact removeall`  
  Removes all auto-react configurations.

## Data Storage

- The bot saves auto-reaction settings in a local file named `autoreact_data.json`.
- Changes made via commands are persisted automatically.
- **Data Structure:**  
  The file stores a dictionary where each key is a user's Discord ID (as a string).  
  Each value is an object containing:
  - `channels`: a list of channel IDs (empty for all channels)
  - `emoji`: the emoji to react with

  **Example:**
  ```json
  {
    "123456789012345678": {
      "channels": [987654321098765432, 876543210987654321],
      "emoji": "\ud83d\udc4d"
    },
    "234567890123456789": {
      "channels": [],
      "emoji": "<:syag:1399003920595947591>"
    }
  }
  ```