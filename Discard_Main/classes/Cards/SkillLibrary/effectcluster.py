from .. import card
import aiohttp
import asyncio

from ...main.effect import Effect


class GetCommonEffect():
    #for common effects, this does not Initialize anything/

    def FreezeData(self, arg=1, disable_arg=1):
        #Stops the piece from doing anything this turn
        name="Freeze"
        time="before"
        print("DISABLE ARG ",disable_arg)
        context="turn"
        icon="❄️"
        async def effect_res(dictionary, game_ref, arg):
            #dictionary should just contain user.
            if 'this_piece' in dictionary:
                piece=dictionary['this_piece']
                for key, value in piece.current_actions.items():
                    if key != "END":
                        piece.current_actions[key]=0
                await game_ref.send_announcement("Frozen!  Can't move.")
            else:
                await game_ref.send_announcement("error, did not set 'this_piece'...")
            return dictionary
        disable_condition='turns_passed'
        description="Frozen for {} turns.".format(disable_arg)
        return name, Effect(time, context, effect_res, arg, disable_condition, disable_arg, level=3, description=description, icon="❄️")
