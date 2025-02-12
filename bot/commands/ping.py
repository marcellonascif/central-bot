import discord
from discord import app_commands

def setup(client: discord.Client, guild_id: discord.Object):

    @client.tree.command(name="ping", description="Shows Bot ping", guild=guild_id)
    async def ping(interaction: discord.Interaction):

        latency = round(client.latency * 1000)

        await interaction.response.send_message(f"pong! Latência = {latency}ms")
