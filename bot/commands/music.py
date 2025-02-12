import asyncio
import discord
from discord import app_commands
from discord.errors import ClientException
from collections import deque
from yt_dlp import YoutubeDL
import os

def setup(client: discord.Client, guild_id: discord.Object):

    @client.tree.command(name="play", description="Plays a song", guild=guild_id)
    async def play(interaction: discord.Interaction, *, input: str):

        interaction_channel = interaction.user.voice.channel
        if not interaction_channel:
            await interaction.response.send_message("Você precisa estar em um canal de voz!")
            return

        try:
            # Conectar ao canal de voz
            voice_response = await interaction_channel.connect(self_deaf=True)
            print("try")

            add_to_queue(client, input)
            await interaction.response.send_message(f"Fila: {client.music_queue}")


        except ClientException as e:
            print("exception")

            client_channel = discord.utils.get(client.voice_clients, guild=interaction.guild).channel

            if client_channel != interaction_channel:
                await interaction.response.send_message("Você precisa estar no mesmo canal de voz que eu!")
                return

            add_to_queue(client, input)
            await interaction.response.send_message(f"Fila: {client.music_queue}")

        try:
            loop = asyncio.get_event_loop()
            song = await loop.run_in_executor(None, search_youtube, input)
            if song:
                print(song[0]["url"])

                voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
                voice_client.play(
                    discord.FFmpegPCMAudio(
                        song[0]["url"],
                        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                        options="-vn"
                    )
                )

                await interaction.followup.send(f"Playing {song[0]['title']}")

        except Exception as e:
            print(f"An error occurred: {e}")

def add_to_queue(client: discord.Client, input: str):
    client.music_queue.append(input)
    print(f"Added {input} to the queue.")


def search_youtube(query: str, max_results: int = 1):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    search_query = f"ytsearch{max_results}:{query}"
    with YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(search_query, download=False)

    return [
        {
            "title": entry.get("title"),
            "url": entry.get("url"),
            "duration": entry.get("duration"),
        }
        for entry in results["entries"]
    ]
