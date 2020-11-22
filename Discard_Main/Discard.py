import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import queue
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from .classes.imagemakingfunctions.imaging import *
from .classes.main.piece import *
from .classes.main.player import *
from .classes.main.GridClass import Grid
# from classes.main import *
# The main game.


from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')


class Card_Duel():
    """Where the game will be played."""

    def __init__(self, bot):
        dicti = vars(Grid())
        print(json.dumps(dicti))
        self.game_id = 0
        self.val = 0
        self.players = []
        self.entity_list = []
        self.bot = bot

        self.mode = "Test"  # the "mode" of the game.  a simplified setting.
        self.settings = None  # Settings of the game.
        self.duel_helper = Card_Duel_Helper(self)
        self.grid = Grid(5, 5, self.duel_helper)

        self.grid_message = None  # The message containing the grid object
        self.gridchange = True
        self.grid_image_url = ""
        self.queue_preview = ""

        self.round = 0
        self.log = []  # Log of everything that happened.
        self.game_is_active = False

        self.current_piece = None

    def apply_settings(self, settings=None):
        if settings != None:
            self.settings = settings

    def addPlayer(self, player=None):
        if (player != None):
            self.players.append(player)

    async def move_preview(self, spaces=[]):
        pilgrid = self.grid.grid_to_PIL_array(spaces)
        img = make_image_from_grid(pilgrid, self.grid.columns, self.grid.rows)
        return img

    def grid_updated(self):
        """Sets the boolean value gridchange to True."""
        self.gridchange = True

    # A WIP function.  it sends a grid to all players.
    async def send_grid(self):
        pilgrid = self.grid.grid_to_PIL_array()
        img = make_image_from_grid(pilgrid, self.grid.columns, self.grid.rows)
        for player in self.players:
            if (player.get_PlayerType() == "Discord"):
                await player.get_dpios().send_pil_image(img)

    async def send_grid_update(self):
        """UPDATE ALL DPIOS OF PLAYERS."""
        print(self.round)
        embed = self.to_embed()
        for player in self.players:
            if (player.get_PlayerType() == "Discord"):
                await player.get_dpios().update_grid_message(embed)

    async def send_current_piece_embed(self, current):
        """UPDATE ALL DPIOS OF PLAYERS.  CHANGES EMBED FOR THE CURRENT CREATURE"""
        print(self.round)
        for player in self.players:
            if (player.get_PlayerType() == "Discord"):
                await player.get_dpios().update_current_message(current.get_embed())

    async def send_announcement(self, content):
        """UPDATE ALL DPIOS OF PLAYERS.  SENDS A ANNOUNCEMENT."""
        print(self.round)
        for player in self.players:
            if (player.get_PlayerType() == "Discord"):
                await player.get_dpios().send_announcement(content)

    def add_piece(self, piece):
        self.entity_list.append(piece)

    def remove_piece(self, piece):
        self.entity_list.remove(piece)

    def entity_clear(self):
        """remove all entities with a hp less than zero."""
        for entity in self.entity_list:
            if entity.get_hp() <= 0:
                player = entity.player
                if entity.type == "Creature":
                    player.card_to_graveyard(entity.get_card())
                self.remove_piece(entity)

    async def update_all(self, resend_messages=False):
        """DPIOS HAS THREE MESSAGES.  THE PLAYER, THE GRID, AND THE CURRENT PIECE.  THIS RESENDS THEM."""
        for player in self.players:
            if (player.get_PlayerType() == "Discord"):
                if(resend_messages):
                    await player.get_dpios().send_order()
                await player.send_embed_to_user()
        await self.update_grid_image()
        if self.current_piece != None:
            await self.send_current_piece_embed(self.current_piece)

    async def update_grid_image(self):
        # Refresh the grid image.
        checkGuild = self.bot.get_guild(
            int(configur.get("Default", 'bts_server')))  # Behind The Scenes server
        # Customs Channel.
        image_channel = checkGuild.get_channel(
            int(configur.get("Default", 'bts_game_images')))
        if (self.gridchange):
            pilgrid = self.grid.grid_to_PIL_array()
            img = make_image_from_grid(
                pilgrid, self.grid.columns, self.grid.rows)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG')  # Returns pil object.
                image_binary.seek(0)
                image_msg = await image_channel.send(file=discord.File(fp=image_binary, filename='image.png'))
                self.grid_message = image_msg
            self.gridchange = False
        url = "p"
        for attach in self.grid_message.attachments:
            self.grid_image_url = attach.url
            print(self.grid_image_url)
        await self.send_grid_update()

    def turn_sort(self):
        def sortFunction(e):  # this is python.  We can have nested functions.
            return e.get_speed()

        queue_list = self.entity_list
        queue_list.sort(key=sortFunction)  # sort by lowest to highest speed
        # list is also a stack with the highest speed at the end that can be called using pop()
        return queue_list

    async def turn_queue(self, queue_list):
        # Might need to revise later.
        queue = []
        for i in queue_list:
            queue.append(i)
        stack = []
        for i in range(len(queue)):
            self.queue_preview = [piece.get_name() for piece in queue]
            self.queue_preview.reverse()
            current_piece = queue.pop()
            print(queue)
            self.current_piece = current_piece

            # await self.send_current_piece_embed(current_piece)
            # add to stack from queue the piece with the highest speed and perform its action one a time
            stack.append(current_piece)
            if(stack[i].get_hp() > 0):
                current_piece.toggle_active()
                await self.update_all()
                await stack[i].get_action(self.duel_helper)
            current_piece.toggle_active()

        return stack  # stack will now contain entity_list from highest to lowest speed

    async def start_game(self):
        # Game Loop is here.
        self.game_is_active = True
        while (self.game_is_active):
            print("PUT GAME LOOP HERE.")
            # not sure if this is correct
            await self.turn_queue(self.turn_sort())
            self.round = self.round + 1
            print(self.round)
            self.entity_clear()
            await self.update_grid_image()
            await asyncio.sleep(0.02)
            if (self.round > 5):
                self.game_is_active = False
        await self.send_announcement("THE GAME IS OVER.")
        print("TBD.")

    def to_embed(self):
        embed = discord.Embed(title="Game.", colour=discord.Colour(0x7289da))
        print(self.queue_preview)
        embed.description = "Round: {} \n, queue = {}".format(
            self.round, str(self.queue_preview))
        embed.set_image(url="{imgurl}".format(imgurl=self.grid_image_url))
        embed.set_footer(
            text="{}".format(str(self.queue_preview)))
        return embed


class Card_Duel_Helper():
    # This class will help with processing game events game.
    def __init__(self, Duel):
        print("TBD.  Might do something.")
        self.__card_duel = Duel

    def add_creature(self, creature):
        self.__card_duel.add_piece(creature)
        self.set_update()

    def get_entity_list(self):
        new_list = []
        for v in self.__card_duel.entity_list:
            new_list.append(v)
        return new_list

    def get_grid(self):
        return self.__card_duel.grid

    async def send_announcement(self, announe="Unset Announcement"):
        await self.__card_duel.send_announcement(announe)

    async def make_move_preview(self, spaces):
        img = await self.__card_duel.move_preview(spaces)
        return img

    def set_update(self):
        self.__card_duel.grid_updated()

    def request_termination(self):
        print("To Be Completed.")

    async def send_user_updates(self):
        await self.__card_duel.update_grid_image()

    async def resend_info_messages(self):
        await self.__card_duel.update_all()
