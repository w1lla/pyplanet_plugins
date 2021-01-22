
from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.trackmania import callbacks as tm_signals
from .models import Save

class match_results(AppConfig):
	
	"""
	Save RoundPoints on EndMap to DB                                                  
	"""

	game_dependencies = ['trackmania_next', 'trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, *args, **kwargs):
		"""
		Initializes the plugin.
		"""
		super().__init__(*args, **kwargs)

	async def on_start(self):
		"""
		Called on starting the application.
		"""
				# Listen to signals.
		self.context.signals.listen(tm_signals.scores, self.scores)
		
	async def scores(self, section, players, **kwargs):
		if section == 'EndMap':
			await self.handle_scores(players)
			
	async def handle_scores(self, players):
		for player in players:
			#print(player['player'])
			mappoints = int(player['map_points'])
			position_endmap = int(player['rank'])
			best_racetime = int(player['best_race_time'])
			#print(mappoints)
			#print(position_endmap)
			#print(best_racetime)
			end_map = Save(map=self.instance.map_manager.current_map, player=player['player'], map_points=mappoints, rank=position_endmap, bestracetime=best_racetime)
			#print(end_map)
			await end_map.save()
		