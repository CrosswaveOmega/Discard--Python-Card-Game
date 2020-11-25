
import asyncio
import itertools
from random import randint

import discord
from discord.ext import commands
from discord.ext.commands import Paginator
from discord.ext.commands.help import HelpCommand


class Chelp(HelpCommand):

    def __init__(self, **options):
        self.width = options.pop("width", 58)
        self.indent = options.pop("indent", 2)
        self.sort_commands = options.pop("sort_commands", True)
        self.dm_help = options.pop("dm_help", False)
        self.dm_help_threshold = options.pop("dm_help_threshold", 1000)
        self.commands_heading = options.pop("commands_heading", "Commands:")
        self.no_category = options.pop("no_category", "No Category")
        self.paginator = options.pop("paginator", None)
        self.active = options.pop("active", 30)
        self.show_index = options.pop("show_index", True)
        self.index = options.pop("index", "Categories")
        self.paginator = Paginator()
        print("Chelp initalized.")
        super().__init__(**options)

    def add_indented_commands(self, commands, *, heading, max_size=None, group=None):
        """Indents a list of commands after the specified heading.
        The formatting is added to the :attr:`paginator`.
        The default implementation is the command name indented by
        :attr:`indent` spaces, padded to ``max_size`` followed by
        the command's :attr:`Command.short_doc` and then shortened
        to fit into the :attr:`width`.
        Parameters
        -----------
        commands: Sequence[:class:`Command`]
            A list of commands to indent for output.
        heading: :class:`str`
            The heading to add to the output. This is only added
            if the list of commands is greater than 0.
        max_size: Optional[:class:`int`]
            The max size to use for the gap between indents.
            If unspecified, calls :meth:`get_max_size` on the
            commands parameter.
        """

        if not commands:
            return

        # self.paginator.add_line(heading)
        max_size = max_size or self.get_max_size(commands)
        if group:
            self.paginator.add_line(group.name, heading)
        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = "{0}{1:<{width}} {2}".format(
                self.indent * " ", name, command.short_doc, width=width
            )
            if group:
                self.paginator.add_line(str(entry))
            else:
                self.paginator.add_line(str(entry))
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

    @property
    def _no_category(self):
        return "{0.no_category}:".format(self)

    @property
    def _index(self):
        return "{0.index}:".format(self)

    async def send_command_help(self, command):
        print("Fired.")
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
