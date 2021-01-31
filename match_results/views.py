import datetime
from pyplanet.views.generics.list import ManualListView
from .models import Save
from peewee import *
from pyplanet.apps.core.maniaplanet.models import Map, Player

class MatchResultsView(ManualListView):
	title = 'Match Results'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Challenge'

	def __init__(self, app):
		super().__init__(self)
		self.app = app
		self.manager = app.context.ui

	async def get_fields(self):
		return [
			{
				'name': 'Rank',
				'index': 'Rank',
				'sorting': True,
				'searching': False,
				'width': 10,
				'type': 'label'
			},
			{
				'name': 'Nickname',
				'index': 'Nickname',
				'sorting': True,
				'searching': True,
				'width': 100,
			},
			{
				'name': 'Score',
				'index': 'Score',
				'sorting': True,
				'searching': True,
				'width': 20,
			},
			{
				'name': 'Date',
				'index': 'Date',
				'sorting': True,
				'searching': True,
				'width': 20,
			}
		]
		
	async def get_data(self):
	
	## POSTGRESQL hates some stuff....
	
	##SELECT player_id, nickname, SUM(map_points) AS total FROM save GROUP BY player_id, nickname ORDER BY total DESC MARIADB QUERY
	##
	
	#SELECT *, SUM(`t1`.`map_points`) FROM `match_results` AS t1 GROUP BY `t1`.`player_id` order by SUM(`t1`.`map_points`)
		datas = await Save.execute(Save.select(Save.player_id, Save.nickname, fn.SUM(Save.map_points).alias('totalmappoints')).group_by(Save.player_id, Save.nickname).order_by(fn.SUM(Save.map_points).desc()))
		scores = list()
		index = 0
		for score_in_list in datas:
			index += 1
			date_object = score_in_list.created_at.strftime('%Y-%m-%d')
			score = dict()
			score['Rank'] = index
			score['Nickname'] = score_in_list.nickname
			score['Score'] = score_in_list.totalmappoints
			score['Date'] = date_object
			scores.append(score)
		return scores