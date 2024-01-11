import discord

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

bot = discord.Client(intents=intents)

token = "MTE5Mzc4MjU0MzM5MzI0NzI2Mg.GvFuWA.CJYcaFVpY5KPNi3FfLZOvtWIvpZXFruylEOjOA"

@bot.event
async def on_ready():
    print("I'm in")
    print(f"Bot connected to guilds: {[guild.name for guild in bot.guilds]}")

@bot.event
async def on_message(msg):
    username = msg.author.display_name

    if msg.author == bot.user:
        return
    if msg.content == "Hello":
        await msg.channel.send("Hello there! " + username)
        print("Message sent")

@bot.event
async def on_member_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildname}")
    print("Welcome message sent")

@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    
    if emoji == "🕸️" and message_id == 1193956735044550757:
        role = discord.utils.get(guild.roles, name = "Test 1")
        await member.add_roles(role)

    if emoji == "❤️" and message_id == 1193956735044550757:
        role = discord.utils.get(guild.roles, name = "Test2")
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    user_id = payload.user_id
    emoji = payload.emoji.name
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)

    if emoji == "🕸️" and message_id == 1193956735044550757:
        role = discord.utils.get(guild.roles, name = "Test 1")
        await member.remove_roles(role)

    if emoji == "❤️" and message_id == 1193956735044550757:
        role = discord.utils.get(guild.roles, name = "Test2")
        await member.remove_roles(role)

bot.run(token)