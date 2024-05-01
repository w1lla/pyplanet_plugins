from pyplanet.apps.config import AppConfig
from pyplanet.core import Controller
from pyplanet.core.events import Callback, handle_generic, Signal
from pyplanet.contrib.command import Command
from pyplanet.apps.core.trackmania import callbacks as tm_signals
import os
import lxml.etree as et
import time
from peewee import RawQuery
from pyplanet.apps.contrib.pick_and_ban.models import PickAndBan
import asyncio

class PickorBan(AppConfig):
	game_dependencies = ['trackmania_next', 'trackmania']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	async def on_start(self):
		self.context.signals.listen(tm_signals.pickban_complete, self.handle_pickban)
		await self.instance.command_manager.register(
            Command(command='pbtest', aliases=['pbcall'], target=self.set_pickban, admin=True, description='Start Pick and Ban.'),
			)
		
	async def set_pickban(self, player, data, **kwargs):
		pickbandata = '{"steps":[{"team":1,"action":"ban"},{"team":1,"action":"pick"},{"team":2,"action":"pick"},{"team":3,"action":"pick"},{"team":4,"action":"pick"}],"stepDuration":60000,"resultDuration":10000}'
		
		await self.instance.gbx.script('PickBan.Start', pickbandata, encode_json=False, response_id=False),
		await self.instance.chat('$ff0Admin $fff{}$z$s$ff0 tried to do a pickban with following data: {}.'.format(
				player.nickname,pickbandata)
		)
	async def handle_pickban(self, *args, **kwargs):
		try:
			async with self.instance.storage.driver.open('UserData/Maps/MatchSettings/{}.txt'.format('testw1lla'), 'rb+') as ghost_file:
				#print(await ghost_file.read())
				data_xml = await ghost_file.read()
				tree=et.fromstring(data_xml)
				for bad in tree.xpath("//map"):
					bad.getparent().remove(bad)     # here I grab the parent of the element to call the remove directly on it
				items = []
				for uid in kwargs['playlist']:
					await self.instance.chat('$f0f Following maps are being added: {}.'.format(uid['uid']))
					query = RawQuery(PickAndBan, 'SELECT file FROM `map` WHERE `uid` = "{}" ORDER BY `id` DESC'.format(uid['uid']))
					data = await PickAndBan.execute(query)
					for filename_db in data:
						#print(filename_db.file)
						items.append(filename_db.file)
						items.append(uid['uid'])
						contentnav = tree.find(".//startindex")
						contentdiv = contentnav.getparent()
						data_new_xml = '<map><file>{}</file><ident>{}</ident></map>\n\n'.format(filename_db.file, uid['uid'])
						contentdiv.insert(contentdiv.index(contentnav)+1,
						et.XML(data_new_xml))
				GameDataDirectory = await self.instance.gbx('GameDataDirectory')
				MatchSettings_file = '{}{}{}.txt'.format(GameDataDirectory,'/Maps/MatchSettings/','testw1lla') #testwllla.txt
				#print(MatchSettings_file)
				with open(MatchSettings_file, 'wb') as f:
					f.write(et.tostring(tree, pretty_print=False, xml_declaration=True, encoding='utf-8'))
		except FileNotFoundError as e:
			return e
		time.sleep(12)
		await self.instance.chat('$f0f Going to Restart the Match with the correct Pick & Ban Maps ! Can take a while (approx: 1 Minute!) please be patient!')
		time.sleep(12)
		
		# Need to figure out why pyplanet doesn't want to load the matchsettings file.