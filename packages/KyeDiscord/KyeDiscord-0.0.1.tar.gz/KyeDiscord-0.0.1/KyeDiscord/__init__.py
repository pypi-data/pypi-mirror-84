import discord

from discord.ext import commands

client = commands.Bot(command_prefix = "!", case_insensitive=True)

def test():
    @client.command()
    async def donald(ctx):
        await ctx.send('boo')



