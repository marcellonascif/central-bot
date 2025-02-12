import discord
from discord.errors import ClientException
from discord import app_commands
from collections import deque

def setup(client: discord.Client, guild_id: discord.Object):

    @client.tree.command(name="play", description="Plays a song", guild=guild_id)
    async def play(interaction: discord.Interaction, *, input: str):

        interaction_voice_channel = interaction.user.voice.channel

        if not interaction_voice_channel:
            await interaction.response.send_message("Você precisa estar em um canal de voz!")
            return

        print(interaction_voice_channel.name)
        try:
            # Conectar ao canal de voz\
            voice_response = await interaction_voice_channel.connect(self_deaf=True)
            print("try")

            insert_music_queue(client, input)
            await interaction.response.send_message(f"Fila: {client.music_queue}")


        except ClientException as e:
            print("exception")
            insert_music_queue(client, input)
            await interaction.response.send_message(f"Fila: {client.music_queue}")


def insert_music_queue(client: discord.Client, input: str):
    client.music_queue.append(input)
    print(f"Added {input} to the queue.")
