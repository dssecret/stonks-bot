# Copyright (C) tiksan - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by tiksan <webmaster.deeksh@gmail.com>

import discord
from discord.ext import commands, tasks
import requests


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bollinger.start()
        
    @tasks.loop(minutes=1)
    async def bollinger(self):
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
            print(requests.get(f'https://tornsy.com/api/{stock.lower()}'))
