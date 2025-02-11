import discord
from discord import app_commands

def setup(client: discord.Client, guild_id: discord.Object):
    @client.tree.command(name="play", description="Plays a song", guild=guild_id)
    async def play(interaction: discord.Interaction, *, input: str):
        await interaction.response.send_message(f"Playing song: {input}")

        try:
            voice_channel = interaction.user.voice.channel
            if not voice_channel:
                await interaction.response.send_message("Você precisa estar em um canal de voz!")
                return

            # Conectar ao canal de voz
            voice_response = await voice_channel.connect(self_deaf=True)
        except AttributeError:
            await interaction.response.send_message("Não consegui conectar ao canal de voz.")
