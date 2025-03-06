import asyncio
import discord
from discord import app_commands
from discord.errors import ClientException
from yt_dlp import YoutubeDL
import time

def setup(client: discord.Client, guild_id: discord.Object):

    @client.tree.command(name="play", description="Play a song", guild=guild_id)
    async def play(interaction: discord.Interaction, input: str):

        interaction_channel = interaction.user.voice.channel
        if not interaction_channel:
            await interaction.response.send_message("Você precisa estar em um canal de voz!")
            return

        await interaction.response.defer()

        try:
            # Conectar ao canal de voz
            client.voice_client = await interaction_channel.connect(self_deaf=True)

            # deixa a troca muito mais rapida em compensacao
            # ! isso guarda o link de uma vez mas trava o bot para procurar a música

            start_time = time.time()
            song = await asyncio.to_thread(search_youtube, input)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Search took {elapsed_time:.2f} seconds")

            client.add_to_queue(song)
            await interaction.followup.send(f"{song["title"]} foi adicionado à fila!")


        except ClientException as e:
            client_channel = client.voice_client.channel

            if client_channel != interaction_channel:
                await interaction.response.send_message("Você precisa estar no mesmo canal de voz que eu!")
                return

            # ! isso guarda o link de uma vez mas trava o bot para procurar a música
            start_time = time.time()
            song = await asyncio.to_thread(search_youtube, input)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Search took {elapsed_time:.2f} seconds")
            client.add_to_queue(song)
            await interaction.followup.send(f"{song["title"]} foi adicionado à fila!")

        if not client.voice_client.is_playing():
            await play_next(interaction)

    async def play_next(interaction: discord.Interaction):
        if client.music_queue and client.voice_client:
                song = client.music_queue.popleft()
                # song = await asyncio.to_thread(search_youtube, input)

                player = discord.FFmpegPCMAudio(
                        song["url"],
                        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug",
                        options="-vn",
                    )

                client.voice_client.play(
                    player,
                    after=lambda e: asyncio.run_coroutine_threadsafe(play_next(interaction), client.loop)
                )

                await interaction.followup.send(f"Playing {song['title']}")


    @client.tree.command(name="pause", description="Pause the current song", guild=guild_id)
    async def pause(interaction: discord.Interaction):

        try:
            client.voice_client.pause()
            await interaction.response.send_message("A música foi pausada!")

        except Exception as e:
            await interaction.response.send_message("Não está tocando nenhuma música!")


    @client.tree.command(name="resume", description="Resume the current song", guild=guild_id)
    async def resume(interaction: discord.Interaction):

        try:
            client.voice_client.resume()
            await interaction.response.send_message("A música está tocando novamente!")

        except Exception as e:
            await interaction.response.send_message("Não está tocando nenhuma música!")


    @client.tree.command(name="stop", description="Stop the current song", guild=guild_id)
    async def stop(interaction: discord.Interaction):

        try:
            await client.voice_client.disconnect()
            client.voice_client = None
            client.music_queue.clear()
            await interaction.response.send_message("A música foi parada!")

        except Exception as e:
            await interaction.response.send_message("Não está tocando nenhuma música!")


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
