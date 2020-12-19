import discord
import operator
import io
import json
import aiohttp
import asyncio
from .generic.operators import compare_with_operator

#assorted commands for evaluationg the game.

def duel_evaluator(game, property, operator, value):
    property_dict={
        "active_teams":game.get_active_teams,
        "rounds":game.get_round
    }
    if property in property_dict:
        value_A=property_dict[property]()
        res=compare_with_operator(value_A, operator, value)
        return res
    print("Property not found.")
    return False
