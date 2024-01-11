import discord
from discord.ext import commands
import random
from datetime import datetime
import asyncio, os
import youtube_dl
import yt_dlp

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command= None)

queuelist = []
filestodelete = []

token = "MTE5Mzc4MjU0MzM5MzI0NzI2Mg.GvFuWA.CJYcaFVpY5KPNi3FfLZOvtWIvpZXFruylEOjOA"

def is_me(ctx):
        return ctx.author.id == 180884087806885888

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def coinflip(ctx):
    coin = random.randint(1,2)
    if coin == 1:
        await ctx.send("Heads!")
    else:
        await ctx.send("Tails!")

@bot.command()
async def roll(ctx, arg):
    roll = random.randint(1,int(arg))
    await ctx.send("You rolled a " + str(roll) + "!")

@bot.command()
async def rps(ctx, hand):
    hands = ["rock", "paper", "scissors"]
    bot_hand = random.choice(hands)
    await ctx.send("I chose " + bot_hand + "!")
    
    if hand == bot_hand:
        await ctx.send("Its a tie")
    elif hand == "rock":
        if bot_hand == "paper":
            await ctx.send("You lose!")
        if bot_hand == "scissors":
             await ctx.send("You win!")
    elif hand == "paper":
         if bot_hand == "scissors":
              await ctx.send("You lose!")
         if bot_hand == "rock":
              await ctx.send("You win!")
    elif hand == "scissors":
         if bot_hand == "rock":
              await ctx.send("You lose!")
         if bot_hand == "paper":
              await ctx.send("You win!")

@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(
        title = "Commands", 
        description = "These are the Commands i can do!", 
        color = discord.Colour.dark_purple())
    MyEmbed.add_field(name = "Ping", value = "Returns Pong!", inline = False)
    MyEmbed.set_thumbnail(url = "https://i.pinimg.com/474x/bf/b4/b6/bfb4b6bf038b30c42116828d2f539b30.jpg")
    MyEmbed.add_field(name = "Coinflip", value = "Flips a coin!", inline = False)
    MyEmbed.add_field(name = "Roll", value = "Rolls a number between 1 and the number you choose!", inline = False)
    MyEmbed.add_field(name = "Rps", value = "Play rock paper scissors with me!", inline = False)
    MyEmbed.add_field(name = "Help", value = "Shows this message!", inline = False)
    MyEmbed.add_field(name = "About", value = "Shows this message!", inline = False)
    MyEmbed.add_field(name = "Edit", value = "Edit the server!", inline = False)
    MyEmbed.add_field(name = "Servername", value = "Changes the server name!", inline = False)
    MyEmbed.add_field(name = "Createtextchannel", value = "Creates a text channel!", inline = False)
    MyEmbed.add_field(name = "Createvoicechannel", value = "Creates a voice channel!", inline = False)
    MyEmbed.add_field(name = "Deletechannel", value = "Deletes a channel!", inline = False)
    MyEmbed.set_footer(text = "Made by: Hawky#2715")
    await ctx.send(embed = MyEmbed)

            
@bot.group()
async def edit(ctx):
    pass

@edit.command()
async def servername(ctx,*,input):
    await ctx.guild.edit(name = input)

@edit.command()
async def createtextchannel(ctx,*,input):
    await ctx.guild.create_text_channel(name = input)

@edit.command()
async def createvoicechannel(ctx,*,input):
    await ctx.guild.create_voice_channel(name = input)

@edit.command()
async def createrole(ctx,*,input):
    await ctx.guild.create_role(name = input)

@edit.command()
async def deletechannel(ctx,*,input):
    channel = discord.utils.get(ctx.guild.channels, name = input)
    await channel.delete()

@bot.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await ctx.guild.kick(member, reason = reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await ctx.guild.ban(member, reason = reason)

@bot.command()
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    async for entry in ctx.guild.bans(limit=150):
        username = entry.user.name
        disc = entry.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(entry.user)

@bot.command()
@commands.has_role("Test 1")
async def purge(ctx, amount, day = None, month = None, year : int = datetime.now().year):
    if amount == "/":
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after = datetime(year, month, day))
    else:
        await ctx.channel.purge(limit = int(amount)+1)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the required role to use this command!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify an amount of messages to delete!")
    if isinstance(error, commands.BadArgument):
        await ctx.send("You need to specify a number of messages to delete!")

@bot.command()
async def mute(ctx, user : discord.Member):
    await user.edit(mute = True)

@bot.command()
async def unmute(ctx, user : discord.Member):
    await user.edit(mute = False)

@bot.command()
async def deafen(ctx, user : discord.Member):
    await user.edit(deafen = True)

@bot.command()
async def undeafen(ctx, user : discord.Member):
    await user.edit(deafen = False)

@bot.command()
async def voicekick(ctx, user : discord.Member):
    await user.edit(voice_channel = None)


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
                os.remove(f"{file}.mp3")
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
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Testing"))
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



async def main():
    await bot.load_extension("Cogs")
    print("Loaded Cogs")

asyncio.run(main())
bot.run(token)

