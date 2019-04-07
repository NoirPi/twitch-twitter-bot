# coding=utf-8
import json
import traceback

import discord
from discord.ext import commands

from config.config import cfg
from loop import logger


# noinspection PyShadowingNames
def __init__(self, bot: commands.Bot):
    self.bot = bot
    self._last_result = None
    self.sessions = set()


bot = commands.Bot(command_prefix=str(cfg['Bot-Data']['BotPrefix']),
                   case_insensitive=True, owner_id=cfg['Bot-Data']['Bot-OwnerID'])


@bot.event
async def on_ready():
    """Output after the Bot is fully loaded"""
    with open('config/cfg.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    if not config['Bot-Data']['Token']:
        logger.info, print("Please add a Discord Bot Token to the cfg.json")
        return
    if not config['Bot-Data']['Bot-OwnerID']:
        logger.info, print("Please add your Discord ID to the Bot-OwnerID in the cfg.json")
        return
    if not config['Twitter']['ConsumerAPIKey']:
        logger.info, print("No Twitter Consumer API Key provided")
        return
    if not config['Twitter']['ConsumerAPISecret']:
        logger.info, print("No Twitter Consumer API Secret provided")
        return
    if not config['Twitter']['AccessToken']:
        logger.info, print("No Twitter Access Token provided")
        return
    if not config['Twitter']['AccessSecret']:
        logger.info, print("No Twitter Access Secret provided")
        return
    if not config['Twitch']['TwitchToken']:
        logger.info, print("No Twitch Token provided")
        return
    if not config['Twitch']['TwitchChannelName']:
        logger.info, print("No Twitch Channel Name provided")
        return
    await bot.change_presence(status=discord.Status.idle)
    logger.info(f'#-------------------------------#\n'
                f'| Successfully logged in\n'
                f'#-------------------------------#\n'
                f'| Username:  {bot.user.name}\n'
                f'| User ID:   {bot.user.id}\n'
                f'| Developer: NoirPi\n'
                f'# ------------------------------#')
    print(f'#-------------------------------#\n'
          f'| Successfully logged in\n'
          f'| Twitter Notification Bot\n'
          f'| OAuth URL: {discord.utils.oauth_url(bot.user.id)}\n'
          f'#-------------------------------#\n')


# noinspection PyUnusedLocal
@bot.event
async def on_error(event, *args):
    logger.info(traceback.format_exc())


MODULES = [
    'commands',
    'loop'
]

for module in MODULES:
    bot.load_extension(module)

bot.run(cfg['Bot-Data']['Token'])
