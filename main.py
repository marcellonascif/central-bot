import discord
import os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')



if __name__ == '__main__':
    print('Hello, World!')

    intents = discord.Intents.default()
    intents.messages = True

    client = Client(intents=intents)
    client.run(ACCESS_TOKEN)
