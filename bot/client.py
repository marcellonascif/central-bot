import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, guild_id: int):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.guild_id = discord.Object(guild_id)

    async def on_ready(self):
        try:
            synced = await self.tree.sync(guild=self.guild_id)
            print(f"Synced {len(synced)} commands to guild {self.guild_id.id}")
        except Exception as e:
            print(f"An error occurred: {e}")

        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
