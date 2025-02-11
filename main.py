import os
import discord
from bot.client import Client
import bot.commands as cmds

if __name__ == '__main__':
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    GUILD_ID = int(os.getenv("GUILD_ID"))

    intents = discord.Intents.all()
    intents.messages = True

    client = Client(command_prefix="!", intents=intents, guild_id=GUILD_ID)

    # Configurar comandos
    cmds.setup_hello(client, client.guild_id)
    cmds.setup_music(client, client.guild_id)

    client.run(ACCESS_TOKEN)
