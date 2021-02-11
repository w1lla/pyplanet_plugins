# pyplanet_plugins
PyPlanet Apps made by W1lla

# Plugins made:

- Muffin Plugin 
- Match Results Plugin
- Inital Discord Bot

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
