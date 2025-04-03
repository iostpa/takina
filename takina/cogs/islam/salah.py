import nextcord
from nextcord.ext import commands
from config import *
from ..libs.oclib import *
import aladhan


class Salawat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        help="Fetch a list of the Islāmic prayer times. \nUsage: `salawat Riyadh Saudi Arabia`."
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def salawat(self, ctx: commands.Context, location_name: str):
        client = aladhan.Client(is_async=True)
        try:
            prayer_times = await client.get_timings_by_address(location_name)
            embed = nextcord.Embed(color=EMBED_COLOR)
            embed.description = ""
            embed.title = f"Islāmic Prayer Times for {location_name.capitalize()}"
            for prayer in [
                prayer_times.fajr,
                prayer_times.dhuhr,
                prayer_times.asr,
                prayer_times.maghrib,
                prayer_times.isha,
            ]:
                embed.description += f"\n> **{prayer.name.capitalize()}**: {prayer.time.strftime("%H:%M")}"

            embed.set_footer(
                text="Please note that these times are in the timezone of the location specified, not your timezone."
            )
            await ctx.reply(embed=embed, mention_author=False)

        except Exception as e:
            embed = nextcord.Embed(color=ERROR_COLOR)
            embed.description = ":x: The location specified was not recognized."
            await ctx.reply(embed=embed, mention_author=False)

        finally:
            await client.close()


class SlashSalawat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="salawat", description="Fetch a list of the Islāmic prayer times."
    )
    async def slash_salawat(
        self,
        interaction: nextcord.Interaction,
        location_name: str = nextcord.SlashOption(
            description="The location for which to fetch prayer times", required=True
        ),
    ):
        await interaction.response.defer()
        client = aladhan.Client(is_async=True)
        try:
            prayer_times = await client.get_timings_by_address(location_name)
            embed = nextcord.Embed(color=EMBED_COLOR)
            embed.description = ""
            embed.title = f"Islāmic Prayer Times for {location_name.capitalize()}"
            for prayer in [
                prayer_times.fajr,
                prayer_times.dhuhr,
                prayer_times.asr,
                prayer_times.maghrib,
                prayer_times.isha,
            ]:
                embed.description += f"\n> **{prayer.name.capitalize()}**: {prayer.time.strftime("%H:%M")}"

            embed.set_footer(
                text="Please note that these times are in the timezone of the location specified, not your timezone."
            )
            await interaction.send(embed=embed)

        except Exception as e:
            embed = nextcord.Embed(color=ERROR_COLOR)
            embed.description = ":x: The location specified was not recognized."
            await interaction.send(embed=embed, ephemeral=True)

        finally:
            await client.close()


def setup(bot: commands.Bot):
    bot.add_cog(Salawat(bot))
    bot.add_cog(SlashSalawat(bot))
