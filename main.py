import discord
from discord.ext import commands

from config.config import cfg
from loop import logger


# noinspection PyShadowingNames
def __init__(self, bot: commands.Bot):
    self.bot = bot
    self._last_result = None
    self.sessions = set()


self = bot = commands.Bot(command_prefix=str(cfg['Bot-Data']['BotPrefix']),
                          case_insensitive=True, owner_id=cfg['Bot-Data']['Bot-OwnerID'])


@bot.event
async def on_ready():
    """Output after the Bot is fully loaded"""
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


MODULES = [
    'commands',
    'loop'
]

for module in MODULES:
    bot.load_extension(module)

bot.run(cfg['Bot-Data']['Token'])
