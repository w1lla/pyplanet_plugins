# pyplanet_plugins
PyPlanet Apps made by W1lla

# Plugins made:

- Muffin Plugin 
- Match Results Plugin
- Inital Discord Bot
- AFK Plugin

# Muffin Plugin

in apps.py add ```'pyplanet.apps.contrib.muffin',``` and it will load, only not in ShootMania.

Muffin Plugin based on TMGery's MX /muffin command.

See 

https://w1lla.github.io/pyplanet_plugins/preview.html

for images of the plugin.

# Match Results Plugin

!!needs module pycountry!!

in apps.py add ```'pyplanet.apps.contrib.match_results',``` and it will load.

match_results Plugin that on EndMap saves Rank, BestRaceTime, Mappoints gathered into DB or HTML File (Default is HTML)
see example code:

https://w1lla.github.io/pyplanet_plugins/matchresults/matchresults_ta
https://w1lla.github.io/pyplanet_plugins/matchresults/matchresults_rounds
https://w1lla.github.io/pyplanet_plugins/matchresults/matchresults_laps
https://w1lla.github.io/pyplanet_plugins/matchresults/matchresults_team

!!! Notice !!!

In TM2020 the rank in callback trackmania.scores will be removed but the plugin doesn't use that. It uses an increment based on players.

# Discord Bot

Inital Discord Bot

Need module discord which can be found here:

py -3 -m pip install -U discord.py

Send Server chat to discord and Vice Versa.

No VoiceChat!

in apps.py add ```'pyplanet.apps.contrib.discordbot',``` and it will load.

However there are some bugs:

- Emoijs dont work.
- :flag_nl: for instance does work in server chat towards discord but not other way around, need to fix that.
- Commands arent sent to the Discord but i need to figure stuff out like discordname/nick is login from pyplanet database. (like //restart in discord should activate restartmap (It does but ingame you get a error message and not on discord.) Also it might seem that if you are offline, it might trigger it) Needs to be fully tested.

Might be forgetting more but its still initial and in alpha so beware.

# AFK Plugin

in apps.py add ```'pyplanet.apps.contrib.afk',``` and it will load.

- Current Issues:
 Timeout is set to 100 which corresponds to 50 seconds (Estimate)

# Pick And Ban

in apps.py add ```'pyplanet.apps.contrib.pick_and_ban',``` and it will load.

- Pick and Ban maps in Team Gamemodes
- ````{"steps":[{"team":1,"action":"ban"},{"team":1,"action":"pick"},{"team":2,"action":"pick"},{"team":3,"action":"pick"},{"team":4,"action":"pick"}],"stepDuration":60000,"resultDuration":10000 ``` can be changed to whom ever setting you want.
- There needs to be an altercation be made in ```\pyplanet\apps\core\trackmania\callbacks.py```:
- Add the following to the end to make it work: ```
pickban_complete = Callback(
	call='Script.PickBan.Complete',
	namespace='trackmania',
	code='pickban_complete',
	target=handle_generic
)```

To load the matchsettings with the pick or banned maps: For now do //rml testw1lla.txt and do a NextMap (There seem to be some issues in Development for me!)

There seems to be some slight issues:
- The ServerChat will be filled with the MapUID's which are fine as they will be eventually added towards the matchsettings file.
- Loading of the new MatchSettings seems to fail through pyplanet read_map_list (Do not understand why but it could be as i am checking if it is being changed in notepad++).
- For Apparent reason: Only Blue and Red can vote (Tested this alone so it needs some good testing with multiple teams as bots do not do everything.)
- Make a copy of the Matchsettings and rename it (That seems to work)
