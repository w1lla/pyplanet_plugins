import datetime
from pyplanet.views.generics.list import ManualListView
from .models import Save
from peewee import *
from pyplanet.apps.core.maniaplanet.models import Player

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
				'index': 'Index',
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
		data = await Save.execute(Save.select(Save, Player, fn.SUM(Save.map_points).alias('totalmappoints')).join(Player).group_by(Player.id).order_by(fn.SUM(Save.map_points).desc()))
		rank = 1
		items = []
		for row in data:
			date_time_obj = datetime.datetime.strptime(str(row.created_at), '%Y-%m-%d %H:%M:%S')
			items.append({
				'Index': rank,
				'Nickname': row.player.nickname,
				'Score': row.totalmappoints,
				'Date': date_time_obj.date()
			})
			rank += 1
		return items
