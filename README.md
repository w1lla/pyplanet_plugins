# pyplanet_plugins
PyPlanet Apps made by W1lla

# Plugins made:

- Match Results Plugin

# Match Results Plugin

in apps.py add ```'pyplanet.apps.contrib.match_results',``` and it will load.

match_results Plugin that on EndMap saves Rank, BestRaceTime, Mappoints gathered into DB or HTML File (Default is HTML)
see example code:

https://w1lla.github.io/pyplanet_plugins/matchresults_2021-01-23_10-07-38.html

!!! Notice !!!

In TM2020 the rank in callback trackmania.scores will be removed but the plugin doesn't use that. It uses an increment based on players.
