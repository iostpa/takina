import nextcord
from nextcord.ext import application_checks, commands
import asyncio
import re
from datetime import timedelta
from __main__ import BOT_NAME, EMBED_COLOR
from ..libs.oclib import *


class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: str, duration: str, reason: str = "No reason provided"):
        timeout_duration = duration_calculator(duration)
        if timeout_duration is None:
            await ctx.reply(
                "Invalid duration format. Use <number>[d|h|m].", mention_author=False
            )
            return

        member = extract_user_id(member, ctx)
        can_proceed, message = perms_check(member, ctx=ctx)
        if not can_proceed:
            await ctx.reply(message, mention_author=False)
            return
        
        await member.timeout(
            timeout=nextcord.utils.utcnow() + timedelta(seconds=timeout_duration),
            reason=f"Muted by {ctx.author} for: {reason}",
        )
        embed = nextcord.Embed(
            description=f"✅ Successfully muted **{member.name}** for {duration}.",
            color=EMBED_COLOR,
        )
        dm_embed = nextcord.Embed(
            description=f"You were muted in **{ctx.guild}** for {duration}.",
            color=EMBED_COLOR,
        )
        try:
            await member.send(embed=dm_embed)
        except nextcord.Forbidden:
            embed.set_footer(text="I was unable to DM this user.")
        await ctx.reply(embed=embed, mention_author=False)


class Unmute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="unmute")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx: commands.Context, member: str, reason: str = "No reason provided"):
        member = extract_user_id(member, ctx)
        can_proceed, message = perms_check(member, ctx=ctx)
        if not can_proceed:
            await ctx.reply(message, mention_author=False)
            return

        await member.timeout(None, reason=f"Unmuted by {ctx.author} for:")
        embed = nextcord.Embed(
            description=f"✅ Successfully unmuted **{member.name}**.",
            color=EMBED_COLOR,
        )
        dm_embed = nextcord.Embed(
            description=f"You were unmuted in **{ctx.guild}**.",
            color=EMBED_COLOR,
        )
        try:
            await member.send(embed=dm_embed)
        except nextcord.Forbidden:
            embed.set_footer(text="I was unable to DM this user.")
        await ctx.reply(embed=embed, mention_author=False)


class MuteSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="mute", description="Mute a member for a specified duration."
    )
    @application_checks.has_permissions(moderate_members=True)
    async def mute(
        self, interaction: nextcord.Interaction, member: nextcord.Member =nextcord.SlashOption(description="The user to mute", required=True), duration: str = nextcord.SlashOption(description="The duration of time to mute the user for", required=True), reason: str = "No reason provided"
    ):
        timeout_duration = duration_calculator(duration)
        can_proceed, message = perms_check(member, ctx=interaction)
        if not can_proceed:
            await interaction.send(message, ephemeral=True)
            return

        await member.timeout(
            timeout=nextcord.utils.utcnow() + timedelta(seconds=timeout_duration),
            reason=f"Muted by {interaction.user} for: {reason}",
        )
        embed = nextcord.Embed(
            description=f"✅ Successfully muted **{member.name}** for {duration}.",
            color=EMBED_COLOR,
        )
        dm_embed = nextcord.Embed(
            description=f"You were muted in **{interaction.guild}** for {duration}.",
            color=EMBED_COLOR,
        )
        try:
            await member.send(embed=dm_embed)
        except nextcord.Forbidden:
            embed.set_footer(text="I was unable to DM this user.")
        await interaction.send(embed=embed)


class UnmuteSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="unmute", description="Unmute a member.")
    @application_checks.has_permissions(moderate_members=True)
    async def unmute(
        self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description="The user to unmute", required=True), reason: str = "No reason provided"
    ):
        can_proceed, message = perms_check(member, ctx=interaction)
        if not can_proceed:
            await interaction.send(message, ephemeral=True)
            return

        await member.timeout(None, reason=f"Unmuted by {interaction.user} for: {reason}")
        embed = nextcord.Embed(
            description=f"✅ Successfully unmuted **{member.name}**.",
            color=EMBED_COLOR,
        )
        dm_embed = nextcord.Embed(
            description=f"You were unmuted in **{interaction.guild}**.",
            color=EMBED_COLOR,
        )
        try:
            await member.send(embed=dm_embed)
        except nextcord.Forbidden:
            embed.set_footer(text="I was unable to DM this user.")
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Mute(bot))
    bot.add_cog(Unmute(bot))
    bot.add_cog(MuteSlash(bot))
    bot.add_cog(UnmuteSlash(bot))
