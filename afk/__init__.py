"""
AFK
"""
import asyncio

from pyplanet.apps.config import AppConfig
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from .views import AFKWidget
from pyplanet.core.signals import pyplanet_start_after
from pyplanet.contrib.setting import Setting

class afk(AppConfig):
    game_dependencies = ['trackmania', 'trackmania_next', 'shootmania']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = AFKWidget(self)
        self.setting_afk_timeout = Setting(
			'afk_timeout', 'afk timeout', Setting.CAT_BEHAVIOUR, type=int,
			description='Timeout for Players that are not driving and do not want to type afk.',
			default=100
		)
        
    async def on_start(self):
        self.context.signals.listen(mp_signals.player.player_connect, self.player_connect)
        self.context.signals.listen(mp_signals.map.map_begin, self.map_start)
        self.context.signals.listen(pyplanet_start_after, self.on_after_start)
        
        # Register settings
        await self.context.setting.register(self.setting_afk_timeout)

    async def player_connect(self, player, **kwargs):
        await self.widget.display(player)

    async def map_start(self, *args, **kwargs):
        await self.widget.display()

    async def on_after_start(self, *args, **kwargs):
        await asyncio.sleep(1)
        asyncio.ensure_future(asyncio.gather(*[
            self.player_connect(p) for p in self.instance.player_manager.online
        ]))