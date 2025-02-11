import discord
from discord import app_commands

def setup(client: discord.Client, guild_id: discord.Object):

    @client.tree.command(name="hello", description="Says hello", guild=guild_id)
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message("Fala, Central!")
