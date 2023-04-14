import os
from dotenv import load_dotenv
from twitchio.ext import commands


load_dotenv()
twitch_token=os.getenv('TMI_TOKEN')
prefix=os.getenv('PREFIX')
channel=os.getenv('CHANNEL')
nick=os.getenv('NICK')

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=twitch_token, prefix=prefix, initial_channels=[channel])

    async def event_ready(self):
        # Notify us when everything is ready!
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        print(message.content)
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()