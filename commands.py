import datetime
import json
import os
import time

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import is_owner

start_time = time.time()


class Twitter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        # logger.info('Addon "{}" loaded'.format(self.__class__.__name__))
    
    @commands.group()
    async def twitter(self, ctx):
        """All Commands to manage the Twitter Notifications"""
        if ctx.invoked_subcommand is None:
            cmds = self.bot.get_command("twitter")
            subcmds = []
            for key, value in cmds.all_commands.items():
                desc: str = value.short_doc.format(prefix=ctx.prefix)
                subcmds.append(f"{ctx.prefix}{cmds.qualified_name} {key} || {desc} \n")
            await ctx.send(embed=discord.Embed(title="Twitch Stream Twitter Bot", color=0x722f37,
                                               description=f"{' '.join(sorted(subcmds))}"))
    
    @twitter.command()
    @is_owner()
    async def activate(self, ctx):
        """Activate the Twitter Notifications"""
        with open('config/cfg.json', 'r') as f:
            config = json.load(f)
        config['Twitter']['Notifications'] = True  # or whatever
        with open('config/cfg.json', 'w') as f:
            json.dump(config, f)
        await ctx.send(embed=discord.Embed(
            description=f"Hello {ctx.author.name}. \n"
            f"You've successfully activated the Twitter notifications", color=0x722f37))
    
    @twitter.command()
    @is_owner()
    async def deactivate(self, ctx):
        """Deactivate the Twitter Notifications"""
        with open('config/cfg.json', 'r') as f:
            config = json.load(f)
        config['Twitter']['Notifications'] = False
        with open('config/cfg.json', 'w') as f:
            json.dump(config, f)
        await ctx.send(embed=discord.Embed(
            description=f"Hello {ctx.author.name}. \n"
            f"You've successfully deactivated the Twitter notifications", color=0x722f37))
    
    @twitter.command()
    @is_owner()
    async def status(self, ctx):
        """Show the Status of the Twitter Notifications"""
        with open('config/cfg.json', 'r') as f:
            config = json.load(f)
        if config['Twitter']['Notifications']:
            await ctx.send(embed=discord.Embed(
                title=f"Your Twitterbot is activated:",
                description=f"Twitch Channel: **{config['Twitch']['TwitchChannelName']}**\n\n"
                f"The actual Tweet Content is: \n```{config['Twitter']['Message']}```",
                color=0x9b006f))
        else:
            await ctx.send(embed=discord.Embed(
                title=f"Your Twitterbot is deactivated:",
                description=f"Twitch Channel: **{config['Twitch']['TwitchChannelName']}**\n\n"
                f"The actual Tweet Content is: \n```{config['Twitter']['Message']}```",
                color=0x9b006f))
    
    @twitter.command()
    @is_owner()
    async def message(self, ctx, *, message: str):
        """Set the Twitter Message Text"""
        if len(message) < 280:
            with open('config/cfg.json', 'r') as f:
                config = json.load(f)
            config['Twitter']['Message'] = message
            with open('config/cfg.json', 'w') as f:
                json.dump(config, f)
            await ctx.send(embed=discord.Embed(
                title=f"Your new Tweet Content is:",
                description=f"{message}", color=0x722f37))
        else:
            await ctx.send(embed=discord.Embed(color=0x722f37,
                                               description=f"This Message is too long! Twitter "
                                               f"only allows a maximum of 280 characters"))
    
    @twitter.command()
    async def botinfo(self, ctx):
        """Show Informations about the Bot"""
        py = psutil.Process(os.getpid())
        memoryuse = py.memory_info()[0] / float(2 ** 20)
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title="Twitch Stream Twitter Bot", color=0x722f37,
                              description=f"Twitter Notification Bot by NoirPi.")
        embed.add_field(
            name="Hardware Informations:",
            value=f"CPU Usage:\n ``{psutil.cpu_percent()} %``\n"
            f"Memory Usage:\n ``{memoryuse:9.2f} MB``\n Uptime:\n ``{text}``", inline=True)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Twitter(bot))
