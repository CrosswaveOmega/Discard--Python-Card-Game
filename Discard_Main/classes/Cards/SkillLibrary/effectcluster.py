from .. import card
import aiohttp
import asyncio

from ...main.effect import Effect


class GetCommonEffect():
    #for common effects, this does not Initialize anything/
    def FreezeData(self, arg=1, disable_arg=1):
        name="Freeze"
        time="before"
        context="command_setting" #Stops the
        async def effect_res(dictionary, game_ref, arg):
            for key, value in dictionary.items():
                if key != "END":
                    dictionary[key]=0
            await self.game_ref.send_announcement("Frozen!  Can't move.")
            return dictionary
        disable_condition="turns_passed"
        description="Frozen for {} turns.".format(disable_arg)
        return name, Effect(time, context, effect_res, arg, disable_condition, disable_check, level=3, description=description)
