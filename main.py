import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# --- Bot Configuration ---
load_dotenv() # Load variables from the .env file
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_PREFIX = "!" # You can change the bot's prefix here

# --- Data File for Storing Auto-React Settings ---
DATA_FILE = "autoreact_data.json"

# --- Bot Intents ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

# --- Bot Initialization ---
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


# --- Data Loading and Saving ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

autoreact_data = load_data()


# --- Bot Events ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message: discord.Message):
    # Don't react to our own messages or other bots' messages
    if message.author == bot.user or message.author.bot:
        return

    # Process commands first, so they don't get reacted to
    await bot.process_commands(message)

    # Check for auto-reaction after processing commands
    author_id_str = str(message.author.id)
    if author_id_str in autoreact_data:
        config = autoreact_data[author_id_str]
        channels = config.get("channels")
        emoji_to_react = config.get("emoji")

        if not emoji_to_react:
            return

        # If channels are specified, only react in those channels
        # If channels list is empty, it means all channels are allowed
        if channels and message.channel.id not in channels:
            return

        try:
            await message.add_reaction(emoji_to_react)
        except discord.Forbidden:
            print(f"I don't have permission to add reactions in channel {message.channel.name}")
        except discord.HTTPException as e:
            print(f"Failed to add reaction: {e}")


# --- Prefix Commands ---

# Using a command group to structure the commands: !autoreact set, !autoreact remove, etc.
@bot.group(invoke_without_command=True)
async def autoreact(ctx):
    """Lists the available autoreact commands."""
    await ctx.send(f"**Invalid command.** Please use `{BOT_PREFIX}autoreact set`, `{BOT_PREFIX}autoreact remove`, or `{BOT_PREFIX}autoreact removeall`.")

@autoreact.command(name="set")
async def autoreact_set(ctx, user: discord.User, emoji: str, *channels: discord.TextChannel):
    """Sets an auto-reaction for a user.
    Usage: !autoreact set @User 👍 #optional-channel-1 #optional-channel-2
    """
    user_id_str = str(user.id)
    channel_ids = [c.id for c in channels]

    # Validate the emoji
    try:
        await ctx.message.add_reaction(emoji)
    except discord.HTTPException:
        await ctx.send("❌ That doesn't seem to be a valid emoji that I can use.")
        return

    autoreact_data[user_id_str] = {"channels": channel_ids, "emoji": emoji}
    save_data(autoreact_data)

    if channel_ids:
        channel_mentions = [c.mention for c in channels]
        await ctx.send(f"✅ I will now auto-react with {emoji} to messages from {user.mention} in {', '.join(channel_mentions)}.")
    else:
        await ctx.send(f"✅ I will now auto-react with {emoji} to all messages from {user.mention}.")


@autoreact.command(name="remove")
async def autoreact_remove(ctx, user: discord.User):
    """Removes an auto-reaction setting for a specific user.
    Usage: !autoreact remove @User
    """
    user_id_str = str(user.id)
    if user_id_str in autoreact_data:
        del autoreact_data[user_id_str]
        save_data(autoreact_data)
        await ctx.send(f"🗑️ I will no longer auto-react to messages from {user.mention}.")
    else:
        await ctx.send(f"🤔 I am not currently auto-reacting to messages from {user.mention}.")


@autoreact.command(name="removeall")
async def autoreact_removeall(ctx):
    """Removes all auto-react configurations from the bot.
    Usage: !autoreact removeall
    """
    autoreact_data.clear()
    save_data(autoreact_data)
    await ctx.send("🗑️ All auto-react configurations have been removed.")


# --- Running the Bot ---
if BOT_TOKEN:
    bot.run(BOT_TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in .env file.")