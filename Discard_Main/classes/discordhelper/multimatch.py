import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import re

from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from ..Cards.cardretrieval import CardRetrievalClass
from ..Cards.custom import CustomRetrievalClass

def is_hex(string):
    try:
        value = int(string, 16)
        return True
    except ValueError:
        return False

        #probably a custom_id

def card_multimatch_with_type(profile, to_match="", match_by_custom_name=True, match_by_card_id=True,
                              match_by_custom_id=True):
    """
    returns: type of match, match result
    """
    print("TODO: ADD MATCH BY INV KEY.")
    list1 = profile.get_inv_cards_by_custom_name(str(to_match))  # returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    list2=[]
    if(is_hex(to_match)):
        list2 = profile.get_inv_cards_by_id(int(to_match, 16))  # returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    custom = profile.check_customs_by_id(str(to_match))  # returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    if (len(list1) >= 1 and match_by_custom_name):
        return "custom_name", list1
    elif (len(list2) >= 1 and match_by_card_id):
        print(list2)
        return "card_id", list2
    elif custom != None and match_by_custom_id:
        return "custom_id", custom
    return "No_Match_Found", None


def card_multimatch(profile, to_match="", match_by_custom_name=True, match_by_card_id=True, match_by_custom_id=True):
    print(
        "TODO: THIS FUNCTION SHOULD DETERMINE WHICH ELEMENT to_match is.  for now, it will only check if custom_name matches or if card_id matches")


    #Match by inv key.
    if(profile.check_key(to_match)):
        print("Inventory key takes priority.")
        return [profile.get_inventory_entry_by_key(to_match)]

    list1 = profile.get_inv_cards_by_custom_name(to_match)
     # returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    list2=[]
    if(is_hex(to_match)):
        list2 = profile.get_inv_cards_by_id(int(to_match, 16))
          # returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    custom = profile.check_customs_by_id(to_match)
         # returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    if (len(list1) >= 1 and match_by_custom_name):
        return list1
    elif (len(list2) >= 1 and match_by_card_id):
        return list2
    elif custom != None:
        return custom
    return None
