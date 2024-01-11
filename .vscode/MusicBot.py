from discord.ext import commands
import discord, yt_dlp, os, asyncio
queuelist = []
filestodelete = []

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.command()
@commands.has_role("Test 1")
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

@bot.command()
@commands.has_role("Test 1")
async def leave(ctx, help="leaves the Voice Channel"):
    await ctx.voice_client.disconnect()

@bot.command()
@commands.has_role("Test 1")
async def play(ctx, *, searchword):
    ydl_opts = {}
    voice = ctx.voice_client

    # Get the Title
    if searchword[0:4] == "http" or searchword[0:3] == "www":
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(searchword, download=False)
            title = info["title"]
            url = searchword

    if searchword[0:4] != "http" and searchword[0:3] != "www":
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{searchword}", download=False)["entries"][0]
            title = info["title"]
            url = info["webpage_url"]

    ydl_opts = {
        'format': 'bestaudio/best',
        "outtmpl": f"{title}",
        "postprocessors":
        [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
    }

    # Downloads the Audio File with the Title, it is run in a different thread so that the bot can communicate to the discord server while downloading
    def download(url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, download, url)

    def check_queue():
        try:
            if queuelist[0] != None:
                voice.play(discord.FFmpegPCMAudio(f"{queuelist[0]}.mp3"), after=lambda e: check_queue())
                coro = bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=queuelist[0]))
                fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                fut.result()
                filestodelete.append(queuelist[0])
                queuelist.pop(0)
        except IndexError:
            for file in filestodelete:
                os.remove(f"{file}")
            filestodelete.clear()

    # Playing and Queueing Audio
    if voice.is_playing():
        queuelist.append(title)
        await ctx.send(f"Added to Queue: ** {title} **")
    else:
        voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"), after=lambda e: check_queue())
        await ctx.send(f"Playing ** {title} ** :musical_note:")
        filestodelete.append(title)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))

    # The after function that gets called after the first song ends, then it checks whether a song is in the queuelist
    # if there is a song in the queuelist, it plays that song
    # if there is no song in the queuelist, it deletes all the files in filestodelete


# Stop, Resume and Pause
@bot.command()
@commands.has_role("Test 1")
async def pause(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        voice.pause()
    else:
        await ctx.send("Bot is not playing Audio!")

@bot.command(aliases=["skip"])
@commands.has_role("Test 1")
async def stop(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        voice.stop()
    else:
        await ctx.send("Bot is not playing Audio!")

@bot.command()
@commands.has_role("Test 1")
async def resume(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        await ctx.send("Bot is playing Audio!")
    else:
        voice.resume()

# Function that displays the current queue
@bot.command()
async def viewqueue(ctx):
    await ctx.send(f"Queue:  ** {str(queuelist)} ** ")

# Error Handlers
@join.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("You have to be connected to a Voice Channel to use this command.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@leave.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@play.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@stop.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@resume.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

@pause.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")

bot.run("MTE5Mzc4MjU0MzM5MzI0NzI2Mg.GvFuWA.CJYcaFVpY5KPNi3FfLZOvtWIvpZXFruylEOjOA")