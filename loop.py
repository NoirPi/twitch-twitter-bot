import asyncio
import json
import logging
from datetime import datetime

import aiohttp
from discord.ext import commands
from TwitterAPI import TwitterAPI

from config.config import cfg

# Basic Logging Features
logger = logging.getLogger('noirpi-twitterbot')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=f'./config/noirpi-twitterbot-{datetime.now().strftime("%Y.%m.%d-%H.%M")}.log',
    encoding='utf-8', mode='w+')
logger.addHandler(handler)

# Definitions for the Twitch API
HEADERS = {'Client-ID': cfg['Twitch']['TwitchToken']}
URI = 'https://api.twitch.tv/kraken/streams/'
URL = 'https://twitch.tv/'

# Definitions for the Twitter API
api = TwitterAPI(cfg['Twitter']['ConsumerAPIKey'], cfg['Twitter']['ConsumerAPISecret'],
                 cfg['Twitter']['AccessToken'], cfg['Twitter']['AccessSecret'])


class TwitchTwitterLoop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.twitch_loop = self.bot.loop.create_task(self.stream_check())
        # logger.info('Addon "{}" loaded'.format(self.__class__.__name__))
    
    def __unload(self):
        self.twitch_loop.cancel()
    
    async def stream_check(self):
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            if cfg['Twitter']['Notifications']:
                while True:
                    async with aiohttp.ClientSession() as session:  # Async HTTP request
                        with open('config/cfg.json', 'r', encoding='utf-8') as config:
                            conf = json.load(config)
                            streamer = conf['Twitch']['TwitchChannelName']
                            raw_response = await session.get(URI + streamer, headers=HEADERS)
                            response = await raw_response.json()
                            if response['stream'] is not None:
                                if not conf['Twitter']['Sended']:
                                    r = api.request('statuses/update', {'status': conf[
                                        'Twitter']['Message']})
                                    if r.status_code == 200:
                                        with open('config/cfg.json', 'r', encoding='utf-8') as f:
                                            config = json.load(f)
                                        config['Twitter']['Sended'] = True
                                        with open('config/cfg.json', 'w', encoding='utf-8') as f:
                                            json.dump(config, f)
                                            logger.info(
                                                f"{datetime.now().strftime('%H:%M:%S - %d.%m.%Y')}"
                                                f" || Tweet Successfully sended|| ")
                                    else:
                                        logger.error(
                                            f"{datetime.now().strftime('%H:%M:%S - %d.%m.%Y')}"
                                            f" || An ERROR occured || "
                                            f"Please report this to the Bot Developer. "
                                            f"Status Code: {r.status_code}")
                            else:
                                if response['stream'] is None:
                                    if conf['Twitter']['Sended']:
                                        with open('config/cfg.json', 'r', encoding='utf-8') as f:
                                            config = json.load(f)
                                        config['Twitter']['Sended'] = False
                                        with open('config/cfg.json', 'w', encoding='utf-8') as f:
                                            json.dump(config, f)
                    
                    await asyncio.sleep(300)


def setup(bot):
    bot.add_cog(TwitchTwitterLoop(bot))
