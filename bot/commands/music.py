import asyncio
import discord
from discord import app_commands
from discord.errors import ClientException
from collections import deque
from yt_dlp import YoutubeDL

def setup(client: discord.Client, guild_id: discord.Object):

    @client.tree.command(name="play", description="Plays a song", guild=guild_id)
    async def play(interaction: discord.Interaction, *, input: str):

        interaction_channel = interaction.user.voice.channel
        if not interaction_channel:
            await interaction.response.send_message("Você precisa estar em um canal de voz!")
            return

        try:
            # Conectar ao canal de voz
            client.voice_client = await interaction_channel.connect(self_deaf=True)
            print("try to connect")


            add_to_queue(client, input)
            await interaction.response.send_message(f"Fila: {client.music_queue}")


        except ClientException as e:
            print("exception")

            client_channel = client.voice_client.channel

            if client_channel != interaction_channel:
                await interaction.response.send_message("Você precisa estar no mesmo canal de voz que eu!")
                return

            add_to_queue(client, input)
            await interaction.response.send_message(f"Fila: {client.music_queue}")

        # ! Verificar se esse loop para tocar a música faz sentido nesse contexto
        # ! (acho que precisa criar uma função que roda durante todo o tempo e verifica se a fila esvaziou)
        try:
            loop = asyncio.get_event_loop()
            song = await loop.run_in_executor(None, search_youtube, input)
            if song:
                print(song["url"])

                client.voice_client.play(
                    discord.FFmpegPCMAudio(
                        song["url"],
                        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                        options="-vn"
                    )
                )

                await interaction.followup.send(f"Playing {song['title']}")

        except Exception as e:
            print(f"An error occurred: {e}")


    @client.tree.command(name="pause", description="Pauses the current song", guild=guild_id)
    async def pause(interaction: discord.Interaction):

        try:
            client.voice_client.pause()
            await interaction.response.send_message("A música foi pausada!")

        except Exception as e:
            await interaction.response.send_message("Não está tocando nenhuma música!")


    @client.tree.command(name="resume", description="Resumes the current song", guild=guild_id)
    async def resume(interaction: discord.Interaction):

        try:
            client.voice_client.resume()
            await interaction.response.send_message("A música está tocando novamente!")

        except Exception as e:
            await interaction.response.send_message("Não está tocando nenhuma música!")


    @client.tree.command(name="stop", description="Stops the current song", guild=guild_id)
    async def stop(interaction: discord.Interaction):

        try:
            await client.voice_client.disconnect()
            client.voice_client = None
            await interaction.response.send_message("A música foi parada!")

        except Exception as e:
            await interaction.response.send_message("Não está tocando nenhuma música!")


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


    # Só retorna o primeiro elemento da função atualmente. Para mudar precisa atualizar essa parte
    first_entry = results["entries"][0]
    return {
        "title": first_entry.get("title"),
        "url": first_entry.get("url"),
        "duration": first_entry.get("duration"),
    }
