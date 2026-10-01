"""Telegram bot process: receives updates, calls GameService, edits the live message.

Environment variables (names only in .env.example, never values in the repo):
  TELEGRAM_BOT_TOKEN  token of @thetowerwarbot
  RPG_DB_PATH         SQLite file (default data/lostrealms.sqlite3)
  RPG_WORLD_SEED      optional fixed world seed
  RPG_TIME_SCALE      1.0 normal; smaller numbers speed up timers for testing

[ES]
Para qué sirve: el proceso del bot. Recibe mensajes y botones de Telegram, se los pasa
al motor y edita el "mensaje vivo" con la vista nueva. Cada pocos segundos revisa los
viajes que terminaron y avisa al jugador.
Documento de diseño: diseno/01-plataforma/telegram.md; web-y-multiplataforma.md §4 (identidad)
Módulo: adaptador de Telegram
Depende de: aiogram, engine.service, engine.core, adapters.storage, adapters.telegram.render
Lo usan: python -m adapters.telegram.bot (Railway u otro servidor)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. El id de cuenta es "tg:<id de usuario>"; el motor no lo interpreta.
    2. El token solo se lee del entorno; nunca se escribe en el código ni en el repositorio.
Si cambias esto, revisa:
    - Motor: engine/service/game.py (view, text, act, tick)
    - Despliegue: railway.json (comando de arranque)
"""

from __future__ import annotations

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup

from adapters.storage import SqliteStore
from adapters.telegram.render import render_keyboard, render_text
from engine.core import SystemClock, load_content
from engine.messaging import View
from engine.service import GameService

log = logging.getLogger("lostrealms.telegram")

MENU_LABEL = "📍 Juego"
MENU = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=MENU_LABEL)]], resize_keyboard=True, is_persistent=True)
TICK_SECONDS = 15


def account_of(user_id: int) -> str:
    """Account id for a Telegram user. [ES] Qué hace: arma el id de cuenta del jugador. La llaman: los manejadores. Si cambia, afecta: TODAS las cuentas guardadas."""
    return f"tg:{user_id}"


def build_service() -> GameService:
    """Create the engine from environment variables. [ES] Qué hace: arranca el motor con la configuración del entorno. La llaman: main. Si cambia, afecta: el arranque."""
    seed = os.environ.get("RPG_WORLD_SEED")
    return GameService(
        load_content(),
        SqliteStore(os.environ.get("RPG_DB_PATH", "data/lostrealms.sqlite3")),
        SystemClock(),
        world_seed=int(seed) if seed else None,
        time_scale=float(os.environ.get("RPG_TIME_SCALE", "1.0")),
    )


async def send_view(bot: Bot, chat_id: int, view: View) -> None:
    """Send a view as a new message. [ES] Qué hace: manda una vista como mensaje nuevo. La llaman: manejadores y avisos. Si cambia, afecta: los mensajes del bot."""
    await bot.send_message(chat_id, render_text(view), reply_markup=render_keyboard(view))


def register(dp: Dispatcher, service: GameService) -> None:
    """Attach handlers. [ES] Qué hace: conecta los mensajes y botones con el motor. La llaman: main. Si cambia, afecta: qué responde el bot."""

    @dp.message(CommandStart())
    async def on_start(message: Message) -> None:
        await message.answer("🌅", reply_markup=MENU)
        view = service.view(account_of(message.from_user.id))
        await message.answer(render_text(view), reply_markup=render_keyboard(view))

    @dp.message(F.text)
    async def on_text(message: Message) -> None:
        account = account_of(message.from_user.id)
        if message.text == MENU_LABEL or message.text.startswith("/"):
            view = service.view(account)
        else:
            view = service.text(account, message.text)
        await message.answer(render_text(view), reply_markup=render_keyboard(view))

    @dp.callback_query()
    async def on_button(query: CallbackQuery) -> None:
        view = service.act(account_of(query.from_user.id), query.data or "")
        try:
            await query.message.edit_text(render_text(view), reply_markup=render_keyboard(view))
        except TelegramBadRequest as error:
            if "not modified" not in str(error):
                await send_view(query.bot, query.from_user.id, view)
        await query.answer()


async def notifier(bot: Bot, service: GameService) -> None:
    """Every few seconds, finish due timers and notify players. [ES] Qué hace: avisa cuando termina un viaje o una exploración. La llaman: main. Si cambia, afecta: los avisos."""
    while True:
        try:
            for account_id, view in service.tick():
                if not account_id.startswith("tg:"):
                    continue
                try:
                    await send_view(bot, int(account_id[3:]), view)
                except TelegramForbiddenError:
                    log.info("user blocked the bot: %s", account_id)
                await asyncio.sleep(0.05)
        except Exception:  # keep the loop alive; the error is logged
            log.exception("notifier error")
        await asyncio.sleep(TICK_SECONDS)


async def main() -> None:
    """Start polling. [ES] Qué hace: arranca el bot. La llaman: python -m adapters.telegram.bot. Si cambia, afecta: el arranque del bot."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")
    bot = Bot(token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    service = build_service()
    register(dp, service)
    me = await bot.get_me()
    log.info("running as @%s", me.username)
    asyncio.create_task(notifier(bot, service))
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
