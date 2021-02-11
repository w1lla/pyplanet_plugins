"""
Discord BOT
"""
import asyncio
import discord as discordbot
from threading import Thread
from pyplanet import __version__ as version
from pyplanet.core.gbx import GbxClient
from pyplanet.core.instance import Controller
from pyplanet.apps.core.maniaplanet.callbacks.player import player_chat
from pyplanet.apps.core.maniaplanet.models import Player

class discordConnect():
	def __init__(self, app):
		"""
		:param app: App instance.
		:type app: pyplanet.apps.contrib.admin.app.Admin
		"""
		self.app = app
		self.instance = app.instance

	async def on_start(self):
		# Register signal receivers.
		DThread = Threader()
		# Register signal receivers.
	
class Threader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.start()

    async def starter(self):
        self.discord_client = discordHost()
        await self.discord_client.start('')
		# create the background task and run it in the background
		
    def run(self):
        self.loop.create_task(self.starter())
        self.loop.run_forever()
		
class discordHost(discordbot.Client):
	
	async def on_ready(self):
		message = 'We have logged in as {0.user}'.format(discordbot.Client)
		self.instance = Controller.instance
		activity = discordbot.Game(name="ManiaPlanet")
		await self.change_presence(status=discordbot.Status.idle, activity=activity)
		#await discord.Client.change_presence(activity=discord.Game(name='Trackmania'))
		player_chat.register(self.on_chat)
		
	async def on_message(self, message):
		## Create instance to send discord chat to PyPlanet
		# we do not want the bot to reply to itself
		if message.author.id == self.user.id:
			return
		else:
			discordmessagetoPyplanet = 'DiscordChat:[{}] {}'.format(message.author.name, message.content)
			await self.instance.gbx.execute('ChatSendServerMessage', discordmessagetoPyplanet)
		
		# we do not want the bot to reply to itself
		if message.author.id == self.user.id:
			return
		
		## Commands like //restart needs to have player_instance.
		if message.content.startswith('//'):
			return

		if message.content.startswith('!pypversion'):
			pyplanet_message = 'PyPlanet Responds back with: {}!'.format(version)
			await message.reply(pyplanet_message, mention_author=True)
	
	async def on_chat(self, player, text, cmd, **kwargs):
		if not cmd:
			await self.send(text, player)
		
	async def send(self,content,player):
		channel = self.get_channel(807503258192445473)
		message = '[{}]: {}'.format(player, content)
		await channel.send(message)
