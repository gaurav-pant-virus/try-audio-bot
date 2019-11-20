Setup instructions to create a discord bot(python)

1- Create a server
To create free server login https://discordapp.com and then click the plus sign on the left side of the main window.

2- Create an app
Visit  https://discordapp.com/developers/applications/ and click on "New Application".Please save Client ID from app deatil page which we require later.

3- Create a bot account for your app
In left pane scroll down to section "bot" and create new bot.Store token detailsfor later use.

4- Authorize the bot for your server
Visit the URL https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID>&scope=bot. Don't forget to replce CLIENT_ID in above url.Choose the server you want to add and authorize.


5- To run bot
python3 manage.py audio_bot --run



import os
import discord
import asyncio

from discord.ext import commands
import asyncio
import logging

# load .env file
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path)

# get bot token
TOKEN = os.getenv('BOT_TOKEN')


class AudioBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.shard_ids = self._get_shard_ids()
        self.shard_count = self._get_shard_count()
        self.command_prefix = self._get_commands_prefix()
        super().__init__(self.command_prefix, *args, **kwargs)

    def _get_shard_ids(self):
        """
        TODO: We will extract the shard ids for node from redis.
        """
        return range(2)

    def _get_shard_count(self):
        """
        TODO: we will extract shard count from redis.
        """
        return 2

    def _get_commands_prefix(self):
        """
        TODO: Get all prefixes for all guilds.
        """
        return "!"

    # def __call__(self):
    #     loop = asyncio.get_event_loop()
    #     bot = commands.AutoShardedBot(
    #         command_prefix=self.command_prefix,
    #         shard_ids=self.shard_ids,
    #         shard_count=self.shard_count
    #     )
    #     loop.run_until_complete(bot.start(TOKEN))
    #     return bot

loop = asyncio.get_event_loop()
bot = AudioBot()

@bot.event
async def on_shard_ready(shard_id):
    print(f"shard: {shard_id} has loaded")

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_guild_available(guild):
    """
    TODO: Increase the guild count in redis. We use this count to compute if we require a new
    shard or not.

    As per discord document only 2500 guild can be assigned to a shard. So if
    total_guild < total_shards * 2500 and total_guild > 2000; then create new shard.
    """
    pass # increase count

@bot.command(pass_context=True)
async def play(context, arg):
    await context.send('Playing songs.')

loop.run_until_complete(bot.start(TOKEN))
