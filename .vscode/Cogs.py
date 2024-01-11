from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

class MyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "hello":
            await msg.channel.send("Hello!")

    @commands.command()
    async def black(self,ctx):
        await ctx.send("White!")

    @tasks.loop(seconds = 5)
    async def hello(self,ctx):
        await ctx.send("Hello task!")

    @tasks.loop(seconds = 1)
    async def alarm(self,ctx,hour,minute,msg):
        now = datetime.now().time()
        if now.hour == hour and now.minute == minute:
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send("Its time. " + msg)
            self.alarm.stop()

    @commands.command()
    async def setAlarm(self,ctx,date,msg):
        hour,minute = date.split(":")
        hour = int(hour)
        minute = int(minute)
        msg = str(msg)
        self.alarm.start(ctx,hour,minute,msg)

    @commands.command()
    async def startTestLoop(self,ctx):
        await self.hello.start(ctx)

    @commands.command()
    async def stopTestLoop(self,ctx):
        await self.hello.stop()


async def setup(bot):
    await bot.add_cog(MyCog(bot))
    