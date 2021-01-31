import time
import asyncio
import os
import shutil

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.contrib.setting import Setting
from pyplanet.contrib.command import Command
from pyplanet.utils import times
from pyplanet.utils.style import STRIP_ALL, style_strip
from .models import Save
from .views import MatchResultsView
from peewee import *

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
		self.list_view = None

	async def on_start(self):
		"""
		Called on starting the application.
		"""
		
		# Init settings.
		
		await self.instance.permission_manager.register(
			'start', 'Start MatchSaving HTML command', app=self, min_level=2)
		
		# Listen to signals.
		self.context.signals.listen(tm_signals.scores, self.scores)
		
		# Register commands.
		await self.instance.command_manager.register(Command(command='results', target=self.show_matchresults,
															 description='Displays Latest Match Results.'))
		
		# Start MatchSaving HTML on command
		await self.instance.command_manager.register(Command(command='start', aliases=['mstart'], namespace=self.namespace, target=self.match_start, perms='match_results:start', admin=True, description='Start MatchSaving HTML/DB').add_param('', nargs='*', type=str, required=False, help='Start MatchSaving HTML'))
		
		# Stop MatchSaving HTML on command
		await self.instance.command_manager.register(Command(command='stop', aliases=['mstop'], namespace=self.namespace, target=self.match_stop, perms='match_results:start', admin=True, description='Stop MatchSaving HTML/DB').add_param('', nargs='*', type=str, required=False, help='Stop MatchSaving HTML'))		
		
	
	async def show_matchresults(self, player, **kwargs):
		"""
		Show map list to player for current map or map provided.. Provide player instance.

		:param player: Player instance.
		:param map: Map instance or current map.
		:param kwargs: ...
		:type player: pyplanet.apps.core.maniaplanet.models.Player
		:return: View instance.
		"""
		
		self.list_view = MatchResultsView(self)
		await self.list_view.display(player=player.login)
		
	async def match_start(self, player, data, **kwargs):
		message = '$o$ff0Admin $fff{}$z$s$ff0 has decided the match will start after a map restart.'.format(player.nickname)
		await Save.execute(Save.delete())
		#make a copy of the matchresults.html to work with
		filename = "matchresults/matchresults.html"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		if not os.path.exists(filename):
			open(filename, 'w').close()
		src="matchresults/matchresults.html"
		dst="matchresults/previous_matchresults_{}.html".format(time.strftime("%Y-%m-%d_%H-%M-%S"))
		shutil.copy(src,dst)
		os.remove('matchresults/matchresults.html')
		self.enabled = True
		await self.instance.chat(message)
		await asyncio.sleep(5)
		await self.instance.gbx('RestartMap')
		
	async def match_stop(self, player, data, **kwargs):
	
		self.enabled = False
		self.running = False
		message = '$o$ff0Admin $fff{}$z$s$ff0 has decided the match ended on the previous map.'.format(player.nickname)
		await self.instance.chat(message)
	
	async def scores(self, section, players, teams, **kwargs):
		if not self.enabled:
			return
		else:
			if section == 'EndMap':
				await self.handle_scores(players, teams)
			
	async def handle_scores(self, players, teams):
		timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
		current_script = await self.instance.mode_manager.get_current_script()
		with open('matchresults/matchresults.html','a', encoding="utf-8") as myFile:
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
			if 'Laps' in current_script or 'TrackMania/TM_Laps_Online' in current_script:
				myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Total CP:</td>');
			if 'Rounds' in current_script or 'TrackMania/TM_Rounds_Online' in current_script:
				myFile.write('<td width=\"80\" class=\"tablehead\" bgcolor="#FFFFF">Map Points</td>');
				myFile.write('<td width=\"80\" class=\"tablehead\" bgcolor="#FFFFF">Match Points</td>');
				myFile.write('</tr>');
				
			rank = 1
			for player in players:
				#print(player['player'])
				player_id = player['player'].get_id()
				#print(player_id)
				mappoints = int(player['map_points'])
				nickname = style_strip(player['player'].nickname, STRIP_ALL)
				login = player['player'].login
				increment_rank = rank
				position_endmap = int(increment_rank)
				if player['best_race_time'] == -1:
					best_racetime = int(0)
				else:
					best_racetime = int(player['best_race_time'])
				#print(mappoints)
				#print(position_endmap)
				#print(best_racetime)
				end_map = Save(map=self.instance.map_manager.current_map, nickname=player['player'].nickname, player=player['player'], map_points=mappoints, rank=position_endmap)
				#print(end_map)
				await end_map.save()
				if 'Rounds' in current_script or 'TrackMania/TM_Rounds_Online' in current_script:
					mapPointsTotal = await Save.execute(Save.select(Save.map_points).where(Save.player == player_id))
					sum = 0
					for row in mapPointsTotal:
						sum = sum + int(row.map_points)
				else:
					sum = 0
				
				myFile.write('<tr>');
				myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(position_endmap));
				myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(nickname));
				myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(login));
				myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(times.format_time(int(best_racetime))));
				if 'Laps' in current_script or 'TrackMania/TM_Laps_Online' in current_script:
					cpcount = len(player['best_race_checkpoints'])
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(cpcount));
				if 'Rounds' in current_script or 'TrackMania/TM_Rounds_Online' in current_script:
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(mappoints));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(sum));
					myFile.write('</tr>');
					rank += 1
			myFile.write('</table>');
			myFile.write('<br>');
			if 'Rounds' in current_script or 'TrackMania/TM_Rounds_Online' in current_script:
				myFile.write('Current MatchStandings:&nbsp; &nbsp; &nbsp;');
				myFile.write('<table width=\"100%\" border=\"0\" align=\"center\">');
				myFile.write('<tr>');
				myFile.write('<td width=\"60\" class=\"tablehead\" bgcolor="#FFFFF">Rank</td>');
				myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Nickname</td>');
				myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">TotalMatchpoints</td>');
				myFile.write('</tr>');
				datas = await Save.execute(Save.select(Save.player_id, Save.nickname, fn.SUM(Save.map_points).alias('totalmappoints')).group_by(Save.player_id, Save.nickname).order_by(fn.SUM(Save.map_points).desc()))
				index = 0
				for row in datas:
					index += 1
					endmatch_player_nickname = row.nickname
					endmatch_rank = index
					endmatch_totalmappoints = row.totalmappoints
					myFile.write('<tr>');
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(endmatch_rank));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(style_strip(endmatch_player_nickname, STRIP_ALL)));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(endmatch_totalmappoints));
					myFile.write('</tr>');
				myFile.write('</table>');
			if 'Team' in current_script or 'TrackMania/TM_Teams_Online' in current_script:
				myFile.write('Current MatchStandings:&nbsp; &nbsp; &nbsp;');
				myFile.write('<table width=\"100%\" border=\"0\" align=\"center\">');
				myFile.write('<tr>');
				myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Team:</td>');
				myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">MapPoints:</td>');
				myFile.write('<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">MatchPoints:</td>');
				myFile.write('</tr>');
				for team in teams:
					#print(team)
					myFile.write('<tr>');
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(team['name']));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(team['map_points']));
					myFile.write('<td class=\"celltext\" bgcolor=\"#FFFFF\">{}</td>'.format(team['match_points']));
					myFile.write('</tr>');
				myFile.write('</table>');
			myFile.write('</body>');
			myFile.write('</html>');