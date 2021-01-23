import time

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.contrib.setting import Setting
from pyplanet.contrib.command import Command
from pyplanet.utils import times
from pyplanet.utils.style import STRIP_ALL, style_strip

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
		
		self.namespace = 'match'
		
		self.enabled = False
		
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
		
		await self.instance.permission_manager.register(
			'start', 'Start MatchSaving HTML/DB command', app=self, min_level=2)
		
		# Listen to signals.
		self.context.signals.listen(tm_signals.scores, self.scores)
		
		# Start MatchSaving HTML/DB on command
		await self.instance.command_manager.register(Command(command='start', namespace=self.namespace, target=self.match_start, perms='match_results:start', admin=True, description='Start MatchSaving HTML/DB').add_param('', nargs='*', type=str, required=False, help='Start MatchSaving HTML/DB'))
		
		# Stop MatchSaving HTML/DB on command
		await self.instance.command_manager.register(Command(command='stop', namespace=self.namespace, target=self.match_stop, perms='match_results:start', admin=True, description='Stop MatchSaving HTML/DB').add_param('', nargs='*', type=str, required=False, help='Stop MatchSaving HTML/DB'))		
			
	async def match_start(self, player, data, **kwargs):
		self.enabled = True
		message = '$ff0Admin $fff{}$z$s$ff0 has Started the Match !!!!'.format(player.nickname)
		await self.instance.chat(message)
		
	async def match_stop(self, player, data, **kwargs):
		self.enabled = False
		message = '$ff0Admin $fff{}$z$s$ff0 has Stopped the Match !!!!'.format(player.nickname)
		await self.instance.chat(message)
	
	async def scores(self, section, players, **kwargs):
		if not self.enabled:
			return
		else:
			if section == 'EndMap':
				await self.handle_scores(players)
			
	async def handle_scores(self, players):
		timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
		current_script = await self.instance.mode_manager.get_current_script()
		rank = 1
		for player in players:
			#print(player['player'].nickname)
			mappoints = int(player['map_points'])
			nickname = style_strip(player['player'].nickname, STRIP_ALL)
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
			with open('matchresults_{}.html'.format(timestr), 'a') as myFile:
				myFile.write('<html>')
				myFile.write('<head>')
				myFile.write('<meta http-equiv = "Content-Type" content = "text/html;charset = UTF-8" />')
				myFile.write('</head>')
				myFile.write('<body>')
				myFile.write('MapName: {} &nbsp; &nbsp; &nbsp;'.format(style_strip(self.instance.map_manager.current_map.name, STRIP_ALL)));
				myFile.write('Author: {}  &nbsp; &nbsp; &nbsp;'.format(self.instance.map_manager.current_map.author_login));
				myFile.write('Gamemode: {} &nbsp; &nbsp; &nbsp;'.format(current_script));
				myFile.write('<br>');
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