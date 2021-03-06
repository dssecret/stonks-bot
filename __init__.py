# Copyright (C) tiksan - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by tiksan <webmaster.deeksh@gmail.com>

import json
import logging
import sys

import aiohttp
import discord
from discord.ext import commands, tasks

import tasks

assert sys.version_info >= (3, 6), "Requires Python 3.6 or newer"

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

botlogger = logging.getLogger('bot')
botlogger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
botlogger.addHandler(handler)

try:
    file = open('settings.json')
    file.close()
except FileNotFoundError:
    data = {
        'bottoken': '',
        'prefix': '!',
        'keys': []
    }
    with open(f'settings.json', 'w') as file:
        json.dump(data, file, indent=4)
    exit(0)

with open('settings.json', 'r') as file:
    data = json.load(file)

client = discord.client.Client()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=data['prefix'], intents=intents)


@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print(f'Bot is in {guild_count} guilds.')
    bot.add_cog(tasks.Tasks(bot))


@bot.command()
async def version(ctx):
    embed = discord.Embed()
    embed.title = "Version"
    embed.description = "v1.0.0 in-dev"
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    latency = bot.latency
    botlogger.info(f'Latency: {latency}')

    embed = discord.Embed()
    embed.title = "Latency"
    embed.description = f'{latency} seconds'
    await ctx.send(embed=embed)


if __name__ == '__main__':
    bot.run(data['bottoken'])
