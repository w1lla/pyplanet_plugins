import datetime
from peewee import *
from pyplanet.apps.core.maniaplanet.models import Map
from pyplanet.core.db import Model


class PickAndBan(Model):
	map_uid =  CharField()
