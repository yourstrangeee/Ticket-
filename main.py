import os
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix="=",intents=discord.Intents.all())
tuken = "your_bot_token_here"

@bot.event
async def on_ready():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        await bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename}")
      except Exception as e:
        print(e)
        pass
@bot.event
async def on_ready():
  print(f"Connected in as {bot.user} | {bot.user.id}")
  await bot.change_presence(status=discord.Status.online)

bot.run(token)
