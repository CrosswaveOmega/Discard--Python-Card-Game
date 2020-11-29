
import asyncio
import itertools
from random import randint

import discord
from discord.ext import commands
from discord.ext.commands import Paginator
from discord.ext.commands.help import HelpCommand


class Chelp(HelpCommand):

    def __init__(self, **options):
        super().__init__(**options)

    async def prepare_help_command(self, ctx, command):
        print("Fired.")
        await super().prepare_help_command(ctx, command)
    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        channel = ctx.channel
        print("SEND")
        print(mapping)
        cogs = bot.cogs
        embed=discord.Embed(title="Discard: Help",
        colour=discord.Colour(0x7289da),
        description="All commands")
        for i, v in cogs.items():
            print(i)
            commands=""
            nameval=v.qualified_name
            for comm in v.get_commands():
                if comm.hidden!= True:
                    commands=commands + " `{}`".format(comm.name)
            if commands:
                embed.add_field(name=nameval, value=commands, inline=True)
        mess = await ctx.channel.send(embed=embed)

        #await super().send_bot_help(mapping)
    async def send_command_help(self, command):
        ctx = self.context
        bot = ctx.bot
        channel = ctx.channel
        print("Fired.")
        embed=discord.Embed(title="Help: {}".format(command.name),
        colour=discord.Colour(0x7289da),
        description="All commands")
        embed.description=command.help
        mess = await ctx.channel.send(embed=embed)
        await super().send_command_help(command)

    async def send_group_help(self, group):
        print("Fired.")
        await super().send_group_help(group)

    async def send_cog_help(self, cog):
        ctx = self.context
        bot = ctx.bot
        channel = ctx.channel

        embed=discord.Embed(title="Discard: Help",
        colour=discord.Colour(0x7289da),
        description="All commands")
        print(cog)
        commands=""
        nameval=cog.qualified_name
        for comm in cog.get_commands():
            if comm.hidden!= True:
                commands=commands + " `{}`".format(comm.name)
        if commands:
            embed.add_field(name=nameval, value=commands, inline=True)
        mess = await ctx.channel.send(embed=embed)
        await super().send_cog_help(cog)
