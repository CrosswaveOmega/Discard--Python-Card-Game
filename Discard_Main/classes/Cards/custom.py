import discord
import operator
import csv
import io
import random
import json
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from pathlib import Path

"""We should reduce reliance on the BTS server."""

from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')

directory = "saveData"

cipher_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                     'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y']


class CustomBase():  # Wip.
    """The class customs are derived from."""

    def __init__(self, id=0, name="None", icon="none", type=None, image=None, csvText="none"):
        self.ID = id  # • ID- The internal ID of the card.  All cards have this unique ID, consisting of a eight digit hexadecimal number
        #    Cards should be referenced by this ID, not their name.
        #    (00000000  to FFFFFFFF, makes maximum of 4,294,967,296 cards.
        self.name = ""  # • Name- The name of the card.  Customizable by a user,
        self.icon = ""  # • Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
        # • Image- Background image the card displays.   Customizable by a user,
        self.image_url = "https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"
        # • Image- Background image the card displays.   Customizable by a user,
        self.image_message_id = 0
        self.subtype = ""  # • Type- The type of card this is.
        if csvText != "none":
            print("Iterating CSV TABLE")
            self.fromCSV(csvText)
        else:
            self.ID = id  # • ID- The internal ID of the custom.  All cards have this unique ID, consisting of a eight digit hexadecimal number
            #    Cards should be referenced by this ID, not their name.
            #    (00000000  to FFFFFFFF, makes maximum of 4,294,967,296 cards.
            self.name = name  # • Name- The name of the card.  Customizable by a user,
            self.icon = icon  # • Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
            self.image_message_id = 0
            # • Image- Background image the card displays.   Customizable by a user,
            self.image_url = image
            self.subtype = type  # • Type- The type of card this is.

    def fromCSV(self, csvText):
        lines = csvText.splitlines()
        csvreader = csv.reader(lines, delimiter=',')
        # extracting field names through first row
        fields = next(csvreader)

        for row in csvreader:
            # print(row)
            key = row[0]
            value = row[1]
            print(key, value)
            if (key != "ID"):
                if (hasattr(self, key)):
                    # print(key)
                    setattr(self, key, value)

    def toCSV(self):
        csv_mode = io.StringIO()
        fieldnames = ['Key', 'Value']
        csvwriter = csv.DictWriter(csv_mode, fieldnames=fieldnames)
        csvwriter.writeheader()

        dictionary = vars(self)
        for key, value in dictionary.items():  # formatting.
            if (key != "ID"):
                csvwriter.writerow({'Key': key, 'Value': value})

        textValue = csv_mode.getvalue()
        csv_mode.close()
        return textValue

    def change_display_image(self, image_url, image_message_id):
        self.image_url = image_url
        self.image_message_id = image_message_id

    def checkForAttribute(self, attr):
        if hasattr(self, attr):
            return True
        return False

    def __str__(self):
        return self.icon + "|" + self.name + "|" + self.subtype + "|" + str(self.ID)


class CustomIDSystem:
    class __CustomIDSystem:  # Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.val = arg
            self.custom_dictionary = {}  # Every single hashfile
            self.custom_names = {}  # New names.
            self.loadFile(1)

        def loadFile(self, file_id):
            file = self.get_file_from_directory(1)
            file2 = self.get_file_from_directory(2)
            if (file != None):
                f = file.open(mode='r')
                string = f.read()
                self.custom_dictionary = json.loads(string)
                f.close()
            else:
                self.custom_dictionary = {}
                print(
                    "Should initalize new default user profile, add that into custom_dictionary under user id.")
                self.save_custom_dictionary(1)
            if (file2 != None):
                f = file2.open(mode='r')
                string = f.read()
                self.custom_names = json.loads(string)
                f.close()
            else:
                self.custom_names = {}
                print(
                    "Should initalize new default user profile, add that into custom_dictionary under user id.")
                self.save_custom_dictionary(2)

        def getCipherInternal(self, cipher_id):
            if (self.checkforidincustom_dictionary(cipher_id)):
                return self.custom_dictionary[str(cipher_id)]
            else:  # ID is not in custom_dictionary.
                return None

        def getNameInternal(self, cipher_id):
            if (self.checkforidincustom_names(cipher_id)):
                return self.custom_names[str(cipher_id)]
            else:  # ID is not in custom_dictionary.
                return None

        def get_list_of_all_ciphers(self):
            list = []
            for i, v in self.custom_dictionary.items():
                list.append(i)
            return list
            # Initalize new file.
            # Initalize new file.

        def save_custom_dictionary(self,
                                   file_id):  # Saves the UserProfile object at key id in custom_dictionary to a file.
            # if(self.checkforidincustom_dictionary(id)):
            """
            file_id is 1 for custom_dictionary
            file_id is 2 for custom_names
            """
            filename = "customdata_" + str(file_id) + \
                ".json"  # filename from json.
            to_save = {}
            if (file_id == 1):
                to_save = self.custom_dictionary
            if (file_id == 2):
                to_save = self.custom_names
            file = Path(directory + "/" + filename)
            f = file.open(mode="w+")
            string_to_write = json.dumps(to_save, sort_keys=True, indent=4)
            f.write(string_to_write)
            f.close()

        def save_all_internal(self):  # save everything in custom_dictionary.
            self.save_custom_dictionary(1)
            self.save_custom_dictionary(2)

        def add_cipher_to_dictionary(self, cipher, message_id):
            self.custom_dictionary[str(cipher)] = message_id

        def update_cipher_name(self, cipher, new_name):
            self.custom_names[str(cipher)] = new_name

        def checkforidincustom_dictionary(self, id):
            key_to_lookup = str(id)
            if key_to_lookup in self.custom_dictionary:
                return True
            else:
                return False

        def checkforidincustom_names(self, id):
            key_to_lookup = str(id)
            if key_to_lookup in self.custom_names:
                return True
            else:
                return False

        def get_number_of_all_custom_ids(self):
            return len(self.custom_dictionary)

        def get_file_from_directory(self, file_id):
            # filename from json.
            filename = "customdata_" + str(file_id) + ".json"
            file = Path(directory + "/" + filename)
            if file.exists():  # check if this file exists.
                return file
            else:
                return None

        def __str__(self):
            return repr(self) + self.val

    instance = None

    # Internally, it keeps a single instance of the __SingleDictionary class in memory.
    def __init__(self, arg="None"):
        if not CustomIDSystem.instance:
            CustomIDSystem.instance = CustomIDSystem.__CustomIDSystem(arg)
        else:
            CustomIDSystem.instance.val = arg

    def cipherIDtoMessageId(self, id):
        # Initial chekc
        return CustomIDSystem.instance.getCipherInternal(id)

    def cipherIDtoName(self, id):
        # Initial chekc
        return CustomIDSystem.instance.getNameInternal(id)

    def make_new_cipher(self):
        # we will need to change this algorithm up sometime.
        newCipher = ""
        # every new cipher needs to be unique.
        same_check = True
        chance_of_repeat = float(
            CustomIDSystem.instance.get_number_of_all_custom_ids() / 1073741824.0) * 100.0
        print("Chance of repeated CustomId is ", str(chance_of_repeat))
        while same_check:
            same_check = False
            for i in range(0, 6):
                newCipher = newCipher + random.choice(cipher_characters)
            same_check = CustomIDSystem.instance.checkforidincustom_dictionary(
                newCipher)
        return newCipher

    def add_custom_to_system(self, message_id):
        newCipher = self.make_new_cipher()
        CustomIDSystem.instance.add_cipher_to_dictionary(newCipher, message_id)
        return newCipher

    def update_name(self, cipher, name):
        CustomIDSystem.instance.update_cipher_name(cipher, name)

    def get_all_ciphers(self):
        return CustomIDSystem.instance.get_list_of_all_ciphers()

    def save_all(self):
        CustomIDSystem.instance.save_all_internal()

    def __getattr__(self, name):
        return getattr(self.instance, name)


# Make command for a new id style.

class CustomRetrievalClass():  # by no means what the final version should use.
    def __init__(self, bot=None):
        if bot:
            self.botstore = bot
        self.botstore = None

    async def addCustom(self, new_name, bot):
        # Adds blank custom, returns the new cipher id.
        """
        custom -> Custom Object.
        bot -> The current Bot.
        """
        botToUse = None
        if (bot):
            botToUse = bot
        elif self.botstore:
            botToUse = self.botstore
        if botToUse:
            print("getting id")
            print(configur.get("Default", 'bts_server'))
            # Behind The Scenes server
            checkGuild = bot.get_guild(
                int(configur.get("Default", 'bts_server')))
            # Customs Channel.
            custom_channel = checkGuild.get_channel(
                int(configur.get("Default", 'bts_custom')))
            print(custom_channel)

            # message to second
            message = await custom_channel.send(content=" Text")
            blank_custom = CustomBase(id=message.id, name=new_name)
            cipher = CustomIDSystem("Init").add_custom_to_system(message.id)
            CustomIDSystem("Name").update_name(cipher, new_name)
            CustomIDSystem("SaveNew").save_all()
            await message.edit(content=blank_custom.toCSV())
            # Custom needs to be uploaded by bot.

            return cipher
        return "CUSTOM NOT FOUND."

    def retrieve_name(self, cipher_id):
        # quickly retrieve the name
        return_value = CustomIDSystem("Name").cipherIDtoName(cipher_id)
        return return_value

    async def resync_names(self, bot):
        """This command is for debugging."""
        custom_id_list = CustomIDSystem("Name").get_all_ciphers()
        for ID in custom_id_list:
            mess_id = CustomIDSystem("start").cipherIDtoMessageId(ID)
            if (mess_id == None):
                return "INVALID CUSTOM ID."
            # Behind The Scenes server
            checkGuild = bot.get_guild(
                int(configur.get("Default", 'bts_server')))
            # Customs Channel.
            custom_channel = checkGuild.get_channel(
                int(configur.get("Default", 'bts_custom')))
            # message to get.
            message = await custom_channel.fetch_message(int(mess_id))

            custom = CustomBase(id=ID, csvText=message.content)
            CustomIDSystem("Name").update_name(ID, custom.name)
            CustomIDSystem("SaveNew").save_all()

    async def updateCustomByID(self, custom, bot):
        """
        update a custom uploaded to discord.
        custom -> Custom Object.
        bot -> The current Bot.
        """
        botToUse = None
        if (bot):
            botToUse = bot
        elif self.botstore:
            botToUse = self.botstore
        if botToUse:
            print("getting id")
            print(configur.get("Default", 'bts_server'))
            # Behind The Scenes server
            checkGuild = bot.get_guild(
                int(configur.get("Default", 'bts_server')))
            # Customs Channel.
            custom_channel = checkGuild.get_channel(
                int(configur.get("Default", 'bts_custom')))
            print(custom_channel)
            ID = custom.ID
            print(ID)
            print(custom)
            mess_id = CustomIDSystem("start").cipherIDtoMessageId(ID)
            CustomIDSystem("Name").update_name(ID, custom.name)

            CustomIDSystem("SaveNew").save_all()
            # message to get.
            message = await custom_channel.fetch_message(mess_id)
            # Custom needs to be uploaded by bot.
            await message.edit(content=custom.toCSV())
            # print(message.content)
            return CustomBase(csvText=message.content)
        return "CUSTOM NOT FOUND."

    async def getByID(self, ID, bot):
        """Retrieve a cipher by the ID.
        custom -> Custom Object.
        bot -> The current Bot.
        """
        botToUse = None
        if (bot):
            botToUse = bot
        elif self.botstore:
            botToUse = self.botstore
        if botToUse:
            print("getting id")
            print(configur.get("Default", 'bts_server'))
            # Behind The Scenes server
            checkGuild = bot.get_guild(
                int(configur.get("Default", 'bts_server')))
            # Customs Channel.
            custom_channel = checkGuild.get_channel(
                int(configur.get("Default", 'bts_custom')))
            print(custom_channel)
            print(ID)
            mess_id = CustomIDSystem("start").cipherIDtoMessageId(ID)
            if (mess_id == None):
                return "INVALID CUSTOM ID."
            # message to get.
            message = await custom_channel.fetch_message(int(mess_id))
            # print(message.content)
            return CustomBase(id=ID, csvText=message.content)
        return None

    async def cloneCustom(self, custom_to_clone, bot):
        """clone a custom ID.
        custom -> Custom Object.
        bot -> The current Bot.
        """
        botToUse = None
        if (bot):
            botToUse = bot
        elif self.botstore:
            botToUse = self.botstore
        if botToUse:
            # Behind The Scenes server
            checkGuild = bot.get_guild(
                int(configur.get("Default", 'bts_server')))
            # Customs Channel.
            custom_channel = checkGuild.get_channel(
                int(configur.get("Default", 'bts_custom')))

            new_name = custom_to_clone.name + "- Copy"

            # message to second
            message = await custom_channel.send(content=" Text")

            blank_custom = CustomBase(id=message.id, name=new_name)
            cipher = CustomIDSystem("Init").add_custom_to_system(message.id)
            CustomIDSystem("Name").update_name(cipher, new_name)
            await message.edit(content=custom_to_clone.toCSV())
            CustomIDSystem("SaveNew").save_all()

            return cipher

        return None
