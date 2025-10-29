# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: orangc
from motor.motor_asyncio import AsyncIOMotorClient
from nextcord.ext import commands
import nextcord
import datetime
import config
import os


start_time = datetime.datetime.now(datetime.UTC)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db = AsyncIOMotorClient(config.MONGO_URI).get_database(config.DB_NAME)

    async def setup_database(self) -> None:
        # Setup MongoDB connection and collections
        if not os.getenv("HASDB"):
            raise Exception("No Mongo found. Set the HASDB variable in case you do have a Mongo instance runnin'.")
        self.db_client = AsyncIOMotorClient(config.MONGO_URI)
        self.db = self.db_client.get_database(config.DB_NAME)

    async def get_prefix(self, message):
        if message.guild:
            guild_id = message.guild.id
            guild_data = await self.db.prefixes.find_one({"guild_id": guild_id})
            if guild_data and "prefix" in guild_data:
                return [guild_data["prefix"], "takina ", "Takina "]
            return [".", "takina ", "Takina "]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.user} is now online!")
        await self.setup_database()


bot = Bot(
    intents=nextcord.Intents.all(),
    command_prefix=Bot.get_prefix,
    case_insensitive=True,
    help_command=None,
    owner_ids=[961063229168164864, 716306888492318790],  # orangc, iostpa
    allowed_mentions=nextcord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
    activity=nextcord.Activity(type=nextcord.ActivityType.streaming, name="the stars"),
)


def load_exts(directory):
    blacklist_subfolders = ["libs", "sesp/isadev/libs", "sesp/theanimeflow/libs"]

    cogs = []
    for root, dirs, files in os.walk(directory):
        if any(blacklisted in root for blacklisted in blacklist_subfolders):
            continue

        for file in files:
            if file.endswith(".py"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                cog_name = relative_path[:-3].replace(os.sep, ".")
                cogs.append(cog_name)
    return cogs


REQUIRED_ENV_VARS = ["TOKEN", "HASDB", "MONGO", "BOT_NAME", "DB_NAME", "EMBED_COLOR"]
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}.")


cogs_blacklist = ["fun.snipe", "fun.esnipe"]
cogs = load_exts("takina/cogs")

for cog in cogs:
    if cog not in cogs_blacklist:
        try:
            bot.load_extension("cogs." + cog)
        except Exception as e:
            print(f"Failed to load {cog}: {e}")

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
