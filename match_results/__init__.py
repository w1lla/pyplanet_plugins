
from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.contrib.setting import Setting
from pyplanet.utils import times
from pyplanet.utils import style
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
		self.setting_html = Setting(
			'html', 'Use HTML or DB as output', Setting.CAT_BEHAVIOUR, type=bool,
			description='Where HTML is true, DB is False',
			default=False
		)

	async def on_start(self):
		"""
		Called on starting the application.
		"""
		
		# Init settings.
		await self.context.setting.register(self.setting_html)
		
		# Listen to signals.
		self.context.signals.listen(tm_signals.scores, self.scores)
		
	async def scores(self, section, players, **kwargs):
		if section == 'EndMap':
			await self.handle_scores(players)
			
	async def handle_scores(self, players):
		rank = 1
		for player in players:
			print(player['player'].nickname)
			mappoints = int(player['map_points'])
			nickname = style.style_strip(player['player'].nickname)
			login = player['player'].login
			increment_rank = rank
			position_endmap = int(increment_rank)
			best_racetime = int(player['best_race_time'])
			#print(mappoints)
			#print(position_endmap)
			#print(best_racetime)
			if await self.setting_html.get_value():
				end_map = Save(map=self.instance.map_manager.current_map, player=player['player'], map_points=mappoints, rank=position_endmap, bestracetime=best_racetime)
				#print(end_map)
				await end_map.save()
			else:
				with open('matchresults.html', 'a') as myFile:
					myFile.write('<html>')
					myFile.write('head')
					myFile.write('<meta http-equiv = "Content-Type" content = "text/html;charset = UTF-8" />')
					myFile.write('</head>')
					myFile.write('<body>')
					myFile.write('MapName: {} &nbsp; &nbsp; &nbsp;'.format(self.instance.map_manager.current_map.name));
					myFile.write('<table width=\"100%\" border=\"0\" align=\"center\">');
					myFile.write('<tr>');
					myFile.write('<td width=\"60\" class=\"tablehead\" bgcolor="#FFFFF">Rank</td>');
					myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Nickname</td>');
					myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Login</td>');
					myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Best Race Time</td>');
					myFile.write('<td width=\"80\" class=\"tablehead\" bgcolor="#FFFFF">Points</td>');
					myFile.write('</td>');
					myFile.write('<tr>');
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(position_endmap));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(nickname));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(login));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(times.format_time(int(best_racetime))));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(mappoints));
					myFile.write('</tr>');
					myFile.write('</table>');
					myFile.write('</body>');
					myFile.write('</html>');
					rank += 1