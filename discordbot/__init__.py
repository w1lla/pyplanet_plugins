from pyplanet.apps.config import AppConfig
from pyplanet.apps.contrib.discordbot.connect import discordConnect

class discordbot(AppConfig):  # pragma: no cover

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
		self.discordconnect = discordConnect(self)
		
	async def on_start(self):
		await self.discordconnect.on_start()
