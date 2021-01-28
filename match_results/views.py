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
			}
		]
		
	async def get_data(self):
		data = await Save.execute(Save.select(fn.SUM(Save.map_points).alias('totalmappoints'), Save.player_id, Player.nickname, Player.id).join(Player).where(Save.player_id == Player.id).group_by(Player.id, Save.player_id).order_by(fn.SUM(Save.map_points).desc()))
		# Now we will order by the count, which was aliased to "ct"
		rank = 1
		items = []
		for row in data:
			items.append({
				'Index': rank,
				'Nickname': row.player.nickname,
				'Score': row.totalmappoints,
			})
			rank += 1
		return items
