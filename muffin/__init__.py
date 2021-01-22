import random

from pyplanet.apps.config import AppConfig
from pyplanet.contrib.command import Command

class muffin(AppConfig):
	"""
	Original Muffin Commands Plugin for SM-Gery by Mikey
	Muffin chat command functions 
	Compatible TM2, SM                                        
	Version 0.21 - 2015                                                  
	"""

	game_dependencies = ['trackmania_next', 'trackmania']
	app_dependencies = ['core.maniaplanet']

	def __init__(self, *args, **kwargs):
		"""
		Initializes the muffin plugin.
		"""
		super().__init__(*args, **kwargs)

	async def on_start(self):
		"""
		Called on starting the application.
		"""
		
		# Register callback.
		await self.instance.command_manager.register(
			Command(command='muffin', target=self.muffin, admin=False, description='Bake a muffin').add_param(name='login', required=True))

	async def muffin(self, player, data, **kwargs):
			"""
			Called on /muffin command.
			"""
			try:
				if self.instance.game.game == 'tmnext':
					dest_player = [p for p in self.instance.player_manager.online if p.nickname == data.login]
					if not len(dest_player) == 1:
						raise Exception()
				if self.instance.game.game == 'tm':
					dest_player = [p for p in self.instance.player_manager.online if p.login == data.login]
					if not len(dest_player) == 1:
						raise Exception()
				baker = player.nickname
				nick = dest_player[0].nickname
				prefix = ''
				prefix = '$z({}$z)$m$f90'.format(baker)
				msg = ''
				fun = round(random.randint(0,100),0)
				if fun > 49 :
					fun = fun % 2
				if fun == 0 :
					msg = '{}{}{}'.format(prefix,' Muffin for ',nick)
				if fun == 1 :
					msg = '{}{}{}'.format(prefix,' Apple Cinnamon Muffin for ',nick)
				if fun == 2 :
					msg = '{}{}{}'.format(prefix,' Cornbread Muffin for ',nick)
				if fun == 3 : 
					msg = '{}{}{}'.format(prefix,' Blueberry Cream Cheese Muffin for ',nick)
				if fun == 4 :
					msg = '{}{}{}'.format(prefix,' Sweet Potato Muffin for ',nick)
				if fun == 5 :
					msg = '{}{}{}'.format(prefix,' Chocolate Muffin for ',nick)
				if fun == 6 : 
					msg = '{}{}{}'.format(prefix,' Coffee Cake Muffin for ',nick)
				if fun == 7 : 
					msg = '{}{}{}'.format(prefix,' Snickerdoodle Mini Muffin for ',nick)
				if fun == 8 : 
					msg = '{}{}{}'.format(prefix,' Peanut Butter Muffin for ',nick)
				if fun == 9 :
					msg = '{}{}{}'.format(prefix,' Oatmeal Muffin for ',nick)
				if fun == 10 :
					msg = '{}{}{}'.format(prefix,' Cinnamon Streusel Muffin for ',nick)
				if fun == 11 : 
					msg = '{}{}{}'.format(prefix,' Apple Cider Muffin for ',nick)
				if fun == 12 : 
					msg = '{}{}{}'.format(prefix,' Orange Marmalade Muffin for ',nick)
				if fun == 13 : 
					msg = '{}{}{}'.format(prefix,' Pumpkin Spice Muffin for ',nick)
				if fun == 14 : 
					msg = '{}{}{}'.format(prefix,' Cranberry Oatmeal Muffin for ',nick)
				if fun == 15 : 
					msg = '{}{}{}'.format(prefix,' Pineapple & Sour Cream Muffin for ',nick)
				if fun == 16 : 
					msg = '{}{}{}'.format(prefix,' Lemon Yogurt Muffin for ',nick)
				if fun == 17 : 
					msg = '{}{}{}'.format(prefix,' Zucchini Muffin for ',nick)
				if fun == 18 : 
					msg = '{}{}{}'.format(prefix,' Slice of apple pie for ',nick)
				if fun == 19 : 
					msg = '{}{}{}'.format(prefix,' Baklava for ',nick)
				if fun == 20 : 
					msg = '{}{}{}'.format(prefix,' Bowl of gelato for ',nick)
				if fun == 21 : 
					msg = '{}{}{}'.format(prefix,' Picarones for ',nick)
				if fun == 22 : 
					msg = '{}{}{}'.format(prefix,' Syrniki for ',nick)
				if fun == 23 : 
					msg = '{}{}{}'.format(prefix,' Lamingtons for ',nick)
				if fun == 24 : 
					msg = '{}{}{}'.format(prefix,' Cup of skyr for ',nick)
				if fun == 25 : 
					msg = '{}{}{}'.format(prefix,' Om Ali for ',nick)
				if fun == 26 : 
					msg = '{}{}{}'.format(prefix,' Bread pudding for ',nick)
				if fun == 27 : 
					msg = '{}{}{}'.format(prefix,' Slice of Spekkoek for ',nick)
				if fun == 28 : 
					msg = '{}{}{}'.format(prefix,' Slice of Slagroomtaart for ',nick)
				if fun == 29 : 
					msg = '{}{}{}'.format(prefix,' Appelflappen for ',nick)
				if fun == 30 : 
					msg = '{}{}{}'.format(prefix,' Banana Muffin for ',nick)
				if fun == 31 : 
					msg = '{}{}{}'.format(prefix,' Blue Berry Muffin for ',nick)
				if fun == 32 : 
					msg = '{}{}{}'.format(prefix,' Two Muffins for ',nick)
				if fun == 33 : 
					msg = '{}{}{}'.format(prefix,' Muffin with cream for ',nick)
				if fun == 34 : 
					msg = '{}{}{}'.format(prefix,' Choc chip Muffin for ',nick)
				if fun == 35 : 
					msg = '{}{}{}'.format(prefix,' Double Chocolate Muffin for ',nick)
				if fun == 36 : 
					msg = '{}{}{}'.format(prefix,' Chocolate Muffin for ',nick)
				if fun == 37 : 
					msg = '{}{}{}'.format(prefix,' Lemon & Poppyseed Muffin for ',nick)
				if fun == 38 : 
					msg = '{}{}{}'.format(prefix,' Apple crunch Muffin for ',nick)
				if fun == 39 : 
					msg = '{}{}{}'.format(prefix,' Raspberry Muffin for ',nick)
				if fun == 40 : 
					msg = '{}{}{}'.format(prefix,' Chocolate Muffin for ',nick)       # to do
				if fun == 41 : 
					msg = '{}{}{}'.format(prefix,' Banana Muffin for ',nick)          # to do
				if fun == 42 : 
					msg = '{}{}{}'.format(prefix,' Chocolate Muffin for ',nick)       # to do
				if fun == 43 : 
					msg = '{}{}{}'.format(prefix,' Pink cup cake for ',nick)
				if fun == 44 : 
					msg = '{}{}{}'.format(prefix,' Pumpkin pie for ',nick)
				if fun == 45 : 
					msg = '{}{}{}'.format(prefix,' Slice of Cheesecake for ',nick)
				if fun == 46 : 
					msg = '{}{}{}'.format(prefix,' Cinnamon Dohnut for ',nick)
				if fun == 47 : 
					msg = '{}{}{}'.format(prefix,' Carrot cake for ',nick)
				if fun == 48 : 
					msg = '{}{}{}'.format(prefix,' No muffins for ',nick)
				await self.instance.chat(msg)
			except Exception:
				message = '$i$f00Unknown login!'
				await self.instance.chat(message, player)