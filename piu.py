__version__ = (2, 1, 0)
# module by:
# █▀ █▄▀ █ █░░ █░░ ▀█
# ▄█ █░█ █ █▄▄ █▄▄ █▄

# █▀▄▀█ █▀▀ █▀█ █░█░█
# █░▀░█ ██▄ █▄█ ▀▄▀▄▀
# you can edit this module
# 2022

# scope: hikka_only
# meta developer: @skillzmeow
# ya botik

import logging

from .. import loader, utils, main
from telethon.tl.types import Message
import datetime
import time

logger = logging.getLogger(__name__)


class PingerMeowMod(loader.Module):
    """Узнай свой пинг"""

    strings = {
        "name": "Pinger",
        "uptime": "👩‍💼 <b>Uptime</b>",
        "com": "{} <code>{}</code> <b>ms</b>\n{}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                "no",
                doc=lambda: "Модуль поддерживает {time}, {uptime}",
            ),
            loader.ConfigValue(
                "ping_message",
                "⏱ <b>Response time:</b>",
                lambda: "put your custom ping text",
            ),
            loader.ConfigValue(
                "timezone",
                "0",
                lambda: "use 1, -1, -3 etc. to correct the server time on {time}",
            ),
        )

    def _render_ping(self):
        offset = datetime.timedelta(hours=self.config["timezone"])
        tz = datetime.timezone(offset)
        time2 = datetime.datetime.now(tz)
        time = time2.strftime("%H:%M:%S")
        uptime = utils.formatted_uptime()
        return (
            self.config["custom_message"].format(
                time=time,
                uptime=uptime,
            )
            if self.config["custom_message"] != "no"
            else (f'{self.strings("uptime")}: <b>{uptime}</b>')
        )

    @loader.unrestricted
    async def piucmd(self, message: Message):
        """Узнай свой пинг"""
        ping = self.config["ping_message"]
        start = time.perf_counter_ns()
        message = await utils.answer(message, "<code>🐻 Focus....</code>")
        try:
            await utils.answer(
                message,
                self.strings("com").format(
                    ping,
                    round((time.perf_counter_ns() - start) / 10**6, 3),
                    self._render_ping(),
                ),
            )
        except TypeError:
            await utils.answer(
                message,
                "Invalid number on .config -> Pinger -> timezone, pls update it",
            )