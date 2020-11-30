import discord
import operator
import io
import aiohttp
import asyncio





from .tiebreaker import *
class CallandResponse ():
    """CallandResponse is for the purpose of getting responces from a user,
    via a prompt.
    and putting them in a loop."""
    def __init__(self):
        """This class is for getting a list of arguments, and returning them."""
        self.fields=[]


    def add_field(self, name, prompt, can_skip=False):
        this_entry={}
        this_entry["name"]=name
        this_entry["prompt"]=prompt
        this_entry["canskip"]=can_skip
        self.fields.append(this_entry)

    async def execute_field(self, ctx, field):
        message = await ctx.channel.send(field["prompt"])
        name=field["name"]
        choices = []
        choices.append(['back', "", '◀️'])
        if field["canskip"]:
            choices.append(['skip', "", '⏭️'])
        out=await make_tiebreaker(ctx, choices, message=message, timeout_enable=True, timeout_time=150, delete_after=True, no_match_message=True)
        if out=='back':
            return name, False
        if out=='timeout':
            return name, 'timeout'
        if out=='skip':
            return name, ""
        return name, out

    async def field_loop(self, ctx):
        to_return={}
        this_spot=0
        complete=False
        length=len(self.fields)
        while 0<=this_spot<length:
            thisfield=self.fields[this_spot]
            name, val=await self.execute_field(ctx, thisfield)
            if val==False:
                this_spot=this_spot-1
            elif val=='timeout':
                await ctx.channel.send("You took way too long to respond.  Terminating.")
                return False, {}
            else:
                to_return[name]=val
                this_spot=this_spot+1
        if(this_spot>=length):
            complete=True
        return complete, to_return
