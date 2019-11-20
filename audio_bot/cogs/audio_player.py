from discord.ext import commands
import discord
import youtube_dl

import asyncio


ytdl = youtube_dl.YoutubeDL()

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **{'options': '-vn'}), data=data)

class AudioPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, context, args):
        channel = context.message.author.voice.channel
        # code to determine sorce through mappig
        player = await YTDLSource.from_url('https://agiin-static.s3.ap-south-1.amazonaws.com/songs/Aasan+Nahin+Yahan.mp3', loop=self.bot.loop, stream=True)  # FIXME
        context.voice_client.play(player, after=lambda e: print('Error: %s' % e) if e else None)

    @play.before_invoke
    async def ensure_voice_channel(self, ctx):
        if ctx.voice_client is None:
            if ctx.message.author.voice:
                await ctx.message.author.voice.channel.connect()
            else:
                await ctx.send("You are not on voice channel.")
                raise commands.CommandError("connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
