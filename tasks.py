# Copyright (C) tiksan - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by tiksan <webmaster.deeksh@gmail.com>

import discord
from discord.ext import commands, tasks
import requests
import pandas
import logging


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bollinger.start()
        
    @tasks.loop(minutes=1)
    async def bollinger(self, window=1000, std=2):
        stocks = [
            'TSB',
            'TCB',
            'SYS',
            'LAG',
            'IOU',
            'GRN',
            'THS',
            'YAZ',
            'TCT',
            'CNC',
            'MSG',
            'TMI',
            'TCP',
            'IIL',
            'FHG',
            'SYM',
            'LSC',
            'PRN',
            'EWM',
            'TCM',
            'ELT',
            'HRG',
            'TGP',
            'MUN',
            'WSU',
            'IST',
            'BAG',
            'EVL',
            'MCS',
            'WLT',
            'TCC',
            'ASS'
        ]
        
        for stock in stocks:
            try:
                data = requests.get(f'https://tornsy.com/api/{stock.lower()}')
                data = data.json()['data']
            except Exception:
                continue
            prices = pandas.DataFrame(data, columns=['timestamp', 'price', 'total_shares'])
            prices['ma'] = prices.price.rolling(window=window).mean()
            prices['uma'] = prices.price.rolling(window=window).mean() + (prices.price.rolling(window=window).std() * std)
            prices['lma'] = prices.price.rolling(window=window).mean() - (prices.price.rolling(window=window).std() * std)
            if float(prices.tail(1)['uma']) < float(prices.tail(1)['price']):
                embed = discord.Embed()
                embed.title = f'SELL Order on {stock}'
                embed.description = f'Sell order on {stock} due to Bollinger Bands.'
                embed.add_field(name='Current Price', value=float(prices.tail(1)['price']))
                embed.add_field(name='Lower Moving Average', value=prices.tail(1)['lma'])
                embed.add_field(name='Upper Moving Average', value=prices.tail(1)['uma'])
                
                channel = discord.utils.get(self.bot.guilds[0].channels, name=stock.lower())
                
                if channel is None:
                    channel = await self.bot.guilds[0].create_text_channel(stock.lower(), category=discord.utils.get(self.bot.guilds[0].categories, name='Stocks'))

                await channel.send(embed=embed)
            elif float(prices.tail(1)['lma']) > float(prices.tail(1)['price']):
                embed = discord.Embed()
                embed.title = f'BUY Order on {stock}'
                embed.description = f'Buy order on {stock} due to Bollinger Bands.'
                embed.add_field(name='Current Price', value=float(prices.tail(1)['price']))
                embed.add_field(name='Lower Moving Average', value=prices.tail(1)['lma'])
                embed.add_field(name='Upper Moving Average', value=prices.tail(1)['uma'])
                
                channel = discord.utils.get(self.bot.guilds[0].channels, name=stock.lower())
                if channel is None:
                    channel = await self.bot.guilds[0].create_text_channel(stock.lower(), category=discord.utils.get(self.bot.guilds[0].categories, name='Stocks'))
                await channel.send(embed=embed)
            
