import discord
from discord.ext import commands
from discord import app_commands
from collections import deque

class Client(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, guild_id: int):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.guild_id = discord.Object(guild_id)
        self.voice_client = None
        self.music_queue = deque()

    async def on_ready(self):
        try:
            synced = await self.tree.sync(guild=self.guild_id)
            print(f"Synced {len(synced)} commands to guild {self.guild_id.id}")
        except Exception as e:
            print(f"An error occurred: {e}")

        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    def add_to_queue(self, input: str):
        self.music_queue.append(input)
