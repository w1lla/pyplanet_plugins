"""
Maniaplanet Core Models. This models are used in several apps and should be considered as very stable.
"""
import datetime
from peewee import *

from pyplanet.apps.core.maniaplanet.models import Map, Player
from pyplanet.core.db import Model

class Save(Model):
	map = ForeignKeyField(Map, index=True)
	
	"""
	Map on which the map points was gathered.
	"""

	player = ForeignKeyField(Player, index=True)
	
	"""
	The player.
	"""

	map_points = IntegerField()
	
	"""
	Map points on EndMap
	"""
	
	rank = IntegerField()
	
	"""
	Rank Position on endMap
	"""
	
	bestracetime = IntegerField()
	
	"""
	Best Race Time driven on Map.
	"""
	
	created_at = DateTimeField(
		default=datetime.datetime.now,
	)
	"""
	When is the time driven?
	"""
	
	class Meta:
		db_table = 'match_results'
