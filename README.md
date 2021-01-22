# pyplanet_plugins
PyPlanet Plugins made by W1lla

# Plugins made:

- Muffin Plugin 
- Match Results Plugin

#Muffin Plugin

in apps.py add ```'pyplanet.apps.contrib.muffin',``` and it will load, only not in ShootMania.

Muffin Plugin based on TMGery's MX /muffin command.

See preview map for images of the plugin.

#Match Results Plugin

in apps.py add ```'pyplanet.apps.contrib.match_results',``` and it will load.


match_results Plugin that on EndMap saves Rank, BestRaceTime, Mappoints gathered.

For example

```INSERT INTO `match_results` (`id`, `map_id`, `player_id`, `map_points`, `rank`, `bestracetime`, `created_at`) VALUES
(1, 1, 1, 10, 1, 196347, '2021-01-22 11:53:32');```

To query it out of the database its quite easy:

```SELECT * FROM player INNER JOIN match_results ON match_results.player_id = player.id Where match_results.map_id=1 ORDER BY match_results.rank ASC```

Where map_id = 1 you can change it to anything you like but for each map you need to do the same query.

see example code under [folder=www] for more information.

#notice TM2020 Bug:

In TM2020 the Rank for 1st is 2 and for 2 is 1??.

Nadeo has been notified.

