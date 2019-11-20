import asyncio
import os

from core.commands import BaseCommand
from audio_bot.cogs import register_cog

from discord.ext import commands

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


class CreateBot(BaseCommand):
    cmd_name = "audio_bot"
    help = description = 'Manage Rythm bot'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--start', dest='start',
            action='store_true',
            help="Start Audio bot."
        )

        # TODO - not implemented
        group.add_argument(
            '--stop', dest='stop',
            action='store_true',
            help="Stop Audio bot."
        )

    def start_bot(self):
        loop = asyncio.get_event_loop()
        bot = AudioBot()
        bot.register_cog(bot)
        loop.run_until_complete(bot.start(os.getenv('BOT_TOKEN')))

    # @bot.event
    # async def on_shard_ready(shard_id):
    #     print(f"shard: {shard_id} has loaded")
    #
    # @bot.event
    # async def on_ready():
    #     print("Bot is ready")
    #
    # @bot.event
    # async def on_guild_available(guild):
    #     """
    #     TODO: Increase the guild count in redis. We use this count to compute if we require a new
    #     shard or not.
    #
    #     As per discord document only 2500 guild can be assigned to a shard. So if
    #     total_guild < total_shards * 2500 and total_guild > 2000; then create new shard.
    #     """
    #     pass # increase count
    #
    # @bot.command(pass_context=True)
    # async def play(context, arg):
    #     await context.send('Playing songs.')
    #
    # loop.run_until_complete(bot.start(TOKEN))


    def handle(self, *args, **options):
        if options.get("start"):
            self.start_bot()
        elif  options.get("start"):
            self.stop_bot()
