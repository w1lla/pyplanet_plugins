"""
Maniaplanet Core Models. This models are used in several apps and should be considered as very stable.
"""
import datetime
from peewee import *
from pyplanet.core.db import TimedModel
from pyplanet.apps.core.maniaplanet.models import Map, Player

class team(TimedModel):

	player = ForeignKeyField(Player, index=True)

	"""
	The player.
	"""
	
	teamname = CharField(max_length=255)

	teamdisplayname = CharField(max_length=255)

	"""
	Map points on EndMap
	"""

	rank = IntegerField()

	"""
	Rank Position on endMap
	"""

	created_at = DateTimeField(
		default=datetime.datetime.now,
	)
	"""
	When is the time driven?
	"""
	
class Meta:
		db_table = 'match_results'
		indexes = (
			(('player', 'map'), True),
		)
		primary_key = False