import nextcord
from nextcord.ext import commands


def is_in_guild():
    def predicate(ctx: commands.Context):
        return ctx.guild and ctx.guild.id == SERVER_ID

    return commands.check(predicate)


# the anime flow
SERVER_ID = 1255285392911892651

# celebrating cirno's power
SERVER_ID = 1281898369236602903
