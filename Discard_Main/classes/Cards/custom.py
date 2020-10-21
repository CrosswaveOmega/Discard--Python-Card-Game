import discord
import operator
import csv
import io
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter



from configparser import ConfigParser


configur=ConfigParser()
configur.read('config.ini')

class CustomBase():  #Wip.

    def __init__(self, id=0, name="none", icon="none", type="none", image="None", csvText="none"):
        self.ID=id          #• ID- The internal ID of the card.  All cards have this unique ID, consisting of a eight digit hexadecimal number
                                #    Cards should be referenced by this ID, not their name.
                                #    (00000000  to FFFFFFFF, makes maximum of 4,294,967,296 cards.
        self.name=""      #• Name- The name of the card.  Customizable by a user,
        self.icon=""      #• Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
        self.image_url=""    #• Image- Background image the card displays.   Customizable by a user,
        self.image_message_id=0    #• Image- Background image the card displays.   Customizable by a user,
        self.type=""      #• Type- The type of card this is.
        if csvText != "none":
            print("Iterating CSV TABLE")
            self.fromCSV(csvText)
        else:
            self.ID=id          #• ID- The internal ID of the custom.  All cards have this unique ID, consisting of a eight digit hexadecimal number
                                #    Cards should be referenced by this ID, not their name.
                                #    (00000000  to FFFFFFFF, makes maximum of 4,294,967,296 cards.
            self.name=name      #• Name- The name of the card.  Customizable by a user,
            self.icon=icon      #• Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
            self.image_message_id=0
            self.image_url=image    #• Image- Background image the card displays.   Customizable by a user,
            self.type=type      #• Type- The type of card this is.
    def fromCSV(self, csvText):
        lines = csvText.splitlines()
        csvreader = csv.reader(lines, delimiter=',')
        # extracting field names through first row
        fields = next(csvreader)

        for row in csvreader:
            #print(row)
            key=row[0]
            value=row[1]
            if(key=="image-url"):
                setattr(self)
            if(key!="ID"):
                if(hasattr(self, key)):
                    #print(key)
                    setattr(self, key, value)
    def toCSV(self):
        csv_mode=io.StringIO()
        fieldnames= ['Key','Value']
        csvwriter=csv.DictWriter(csv_mode, fieldnames=fieldnames)
        csvwriter.writeheader()

        dictionary=vars(self)
        for key, value in dictionary.items(): #formatting.
            if(key!="ID"):
                csvwriter.writerow({'Key':key, 'Value':value})

        textValue=csv_mode.getvalue()
        csv_mode.close()
        return textValue

    def checkForAttribute(self, attr):
        if hasattr(self, attr):
            return True
        return False
    def __str__(self):
        return self.icon + "|" + self.name + "|" + self.type + "|"+ str(self.ID)




class CustomRetrievalClass():  #by no means what the final version should use.
    def __init__(self, bot=None):
        if bot:
            self.botstore=bot
        self.botstore=None
    async def updateCustomByID(self, custom, bot):
        """
        custom -> Custom Object.
        bot -> The current Bot.
        """
        botToUse=None
        if(bot):
            botToUse=bot
        elif self.botstore:
            botToUse=self.botstore
        if botToUse:
            print("getting id")
            print(configur.get("Default",'bts_server'))
            checkGuild= bot.get_guild(int(configur.get("Default",'bts_server'))) #Behind The Scenes server
            custom_channel= checkGuild.get_channel(int(configur.get("Default",'bts_custom'))) #Customs Channel.
            print(custom_channel)
            ID=custom.ID
            print(ID)
            message=await custom_channel.fetch_message(int(ID)) #message to get.
            await message.edit(content=custom.toCSV()) #Custom needs to be uploaded by bot.
            #print(message.content)
            return CustomBase(csvText=message.content)
        return "CUSTOM NOT FOUND."
    async def getByID(self, ID, bot):
        botToUse=None
        if(bot):
            botToUse=bot
        elif self.botstore:
            botToUse=self.botstore
        if botToUse:
            print("getting id")
            print(configur.get("Default",'bts_server'))
            checkGuild= bot.get_guild(int(configur.get("Default",'bts_server'))) #Behind The Scenes server
            custom_channel= checkGuild.get_channel(int(configur.get("Default",'bts_custom'))) #Customs Channel.
            print(custom_channel)
            message=await custom_channel.fetch_message(int(ID)) #message to get.
            #print(message.content)
            return CustomBase(id=int(ID), csvText=message.content)
        return "CUSTOM NOT FOUND."
