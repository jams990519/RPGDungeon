"""Telegram bot process: receives updates, calls GameService, edits the live message.

Environment variables (names only in .env.example, never values in the repo):
  TELEGRAM_BOT_TOKEN  token of @LostRealmsbot
  RPG_DB_PATH         SQLite file (default data/lostrealms.sqlite3)
  RPG_WORLD_SEED      optional fixed world seed
  RPG_TIME_SCALE      1.0 normal; smaller numbers speed up timers for testing
  RPG_REPORTS_CHAT_ID chat that receives the daily player report and the 💬 Feedback notes (default: the team's reports chat)

[ES]
Para qué sirve: el proceso del bot. Recibe mensajes y botones de Telegram, se los pasa
al motor y edita el "mensaje vivo" con la vista nueva. Cada pocos segundos revisa los
viajes que terminaron y avisa al jugador. D-260 (0.33): también manda al chat de informes cada mensaje de
💬 Feedback y, una vez por día, el informe de jugadores como archivo (adapters/reports.py). D-262 (0.33.1): el juego se
juega solo por privado; en un grupo el bot no juega: a un comando responde "🔒 se juega por privado" con un botón a su chat,
a un botón viejo le muestra ese aviso aparte y la charla del grupo la ignora.
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
    3. D-262: el juego solo se juega en el chat privado con el bot. En un grupo, ni una jugada: ningún mensaje ni botón de
       un grupo llega al motor como jugada.
    4. El informe y el 💬 Feedback van solo al chat configurado (RPG_REPORTS_CHAT_ID) o a la otra forma de su número; nunca
       a un grupo cualquiera al que agreguen al bot.
Si cambias esto, revisa:
    - Motor: engine/service/game.py (view, text, act, tick, menu, commands: los atajos /stats, /doble, /opciones... salen
      del motor; el menú fijo tiene 5 botones desde D-190: 📖 Historia salió). Un texto con "/" que no es un atajo exacto
      va a service.text(), que entiende los atajos con texto (/bio <texto>, /saludar <nombre>, /brindar, /diario <nombre>,
      /dudas <palabras> y los códigos /d07 de ❓ Dudas, D-192). El texto "📖 Historia" de un teclado viejo también va a
      service.text(), que lo entiende como el botón viejo
    - Despliegue: railway.json (comando de arranque)
"""

from __future__ import annotations

import asyncio
import html
import logging
import os
import re
import sys
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramMigrateToChat
from aiogram.filters import CommandStart
from aiogram.types import (BufferedInputFile, CallbackQuery, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup, User)

from adapters import reports
from adapters.storage import SqliteStore
from adapters.telegram import render as render_module
from adapters.telegram.render import render_keyboard, render_text
from engine.core import SystemClock, load_content
from engine.messaging import View
from engine.service import GameService

log = logging.getLogger("lostrealms.telegram")

MENU_LABEL = "📍 Juego"  # old single-button keyboard; still accepted


def menu_keyboard(service: GameService, account: str | None = None) -> ReplyKeyboardMarkup:
    """Bottom keyboard built from the engine's global menu, 2 per row, in the player's language. [ES] Qué hace: arma el menú fijo de abajo (Zona, Explorar, Campamento, Héroe y ⚙️ Opciones, D-114; D-190 quitó 📖 Historia: 2 por fila, así 5 botones son filas de 2, 2 y 1 que entran en el celular; D-46 deja hasta 6), en el idioma del jugador (D-250). Los jugadores reciben el teclado nuevo con /start, con "📍 Juego", con el aviso del parche y al cambiar de idioma. La llaman: los manejadores. Si cambia, afecta: la navegación en Telegram (tests/test_options.py)."""
    labels = [KeyboardButton(text=a.label) for a in service.menu(account)]
    rows = [labels[i:i + 2] for i in range(0, len(labels), 2)]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)
TICK_SECONDS = 15
REPORTS_CHAT_DEFAULT = "-1004365890113"   # D-260: the team's reports chat (the owner gave it, 17-oct-2026); not a credential
REPORT_RETRY_SECONDS = 3600              # a report Telegram refused is tried again an hour later, not every tick
TOKEN_RE = re.compile(r"^\d{6,12}:[A-Za-z0-9_-]{30,}$")


def clean_token(raw: str) -> str:
    """Remove spaces, quotes or a pasted "NAME=" prefix from the token.

    [ES]
    Qué hace: limpia el token si se pegó con espacios, comillas o con "TELEGRAM_BOT_TOKEN=" delante.
    La llaman: main.
    Si cambia, afecta: el arranque del bot.
    """
    token = raw.strip().strip("\"'").strip()
    if token.startswith("TELEGRAM_BOT_TOKEN="):
        token = token.split("=", 1)[1].strip().strip("\"'").strip()
    return token


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


def private_notice(service: GameService, user: User) -> tuple[str, InlineKeyboardMarkup | None]:
    """The "🔒 played in private" notice for a group, with a button to the bot's chat, in the player's language (D-262).

    [ES]
    Qué hace: arma el aviso de que Lost Realms se juega por privado, en el idioma del jugador (o el de su Telegram si nunca
    eligió), con el botón "▶️ Jugar por privado" que abre el chat con el bot. La llaman: los manejadores de grupos.
    Si cambia, afecta: lo que ve quien escribe un comando o toca un botón en un grupo.
    """
    account = account_of(user.id)
    hint = (user.language_code or "")[:2].lower() or None
    text = service.say(account, "client.private_only", lang_hint=hint)
    username = render_module.BOT_USERNAME[0]
    if not username:
        return text, None
    button = InlineKeyboardButton(text=service.say(account, "client.play_private", lang_hint=hint), url=f"https://t.me/{username}")
    return text, InlineKeyboardMarkup(inline_keyboard=[[button]])


def in_group(query: CallbackQuery) -> bool:
    """A button pressed on a message that lives in a group or channel, not in the private chat (D-262)."""
    return query.message is not None and query.message.chat.type != ChatType.PRIVATE


async def send_view(bot: Bot, chat_id: int, view: View) -> None:
    """Send a view as a new message. [ES] Qué hace: manda una vista como mensaje nuevo. La llaman: manejadores y avisos. Si cambia, afecta: los mensajes del bot."""
    await bot.send_message(chat_id, render_text(view), reply_markup=render_keyboard(view))


def register(dp: Dispatcher, service: GameService) -> None:
    """Attach handlers. [ES] Qué hace: conecta los mensajes y botones con el motor; los de grupos van primero y nunca
    llegan al motor (D-262). La llaman: main. Si cambia, afecta: qué responde el bot."""

    @dp.message(F.chat.type != ChatType.PRIVATE)
    async def on_group_message(message: Message) -> None:
        # D-262: never played in a group. A command gets the short notice; plain chat is ignored so the group stays quiet
        if message.from_user and (message.text or "").startswith("/"):
            text, markup = private_notice(service, message.from_user)
            await message.reply(text, reply_markup=markup)

    @dp.callback_query(in_group)
    async def on_group_button(query: CallbackQuery) -> None:
        # D-262: a game button left in a group does nothing; the notice shows only to whoever pressed it
        text, _ = private_notice(service, query.from_user)
        await query.answer(text, show_alert=True)

    @dp.my_chat_member()
    async def on_bot_membership(update: ChatMemberUpdated) -> None:
        # The log says which chat the bot joined or left, with its real id (handy for RPG_REPORTS_CHAT_ID); a new chat
        # also lets the waiting report try again right away. It never plays there (D-262)
        log.info("bot membership: chat %s (%s, %r) -> %s", update.chat.id, update.chat.type, update.chat.title,
                 update.new_chat_member.status)
        _report_failed_at[0] = float("-inf")

    @dp.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
    async def on_start(message: Message) -> None:
        account = account_of(message.from_user.id)
        parts = (message.text or "").split(maxsplit=1)
        if len(parts) == 2 and parts[1].startswith("ref_"):
            service.register_referral(account, parts[1][4:])
        await message.answer("🌅 Lost Realms", reply_markup=menu_keyboard(service, account))
        view = service.view(account)
        await message.answer(render_text(view), reply_markup=render_keyboard(view))

    @dp.message(F.text, F.chat.type == ChatType.PRIVATE)
    async def on_text(message: Message) -> None:
        account = account_of(message.from_user.id)
        menu_ids = service.menu_labels()           # D-250: the bottom buttons in every language (an old keyboard works)
        commands = service.commands()
        word = (message.text or "").split("@")[0].strip().lower()
        if message.text in menu_ids:
            view = service.act(account, menu_ids[message.text])
        elif word in commands:
            view = service.act(account, commands[word])
        elif message.text == MENU_LABEL:
            await message.answer("🌅 Lost Realms", reply_markup=menu_keyboard(service, account))
            view = service.view(account)
        elif message.text.startswith("/"):
            view = service.text(account, message.text)      # D-117: /bio <texto>, /saludar <nombre>... (unknown ones show the game)
        else:
            view = service.text(account, message.text)
        await message.answer(render_text(view), reply_markup=render_keyboard(view))
        if view.meta.get("menu_changed"):          # D-250: a new language also changes the bottom keyboard
            await message.answer("🌅 Lost Realms", reply_markup=menu_keyboard(service, account))

    @dp.callback_query(lambda query: not in_group(query))
    async def on_button(query: CallbackQuery) -> None:
        account = account_of(query.from_user.id)
        view = service.act(account, query.data or "")
        try:
            await query.message.edit_text(render_text(view), reply_markup=render_keyboard(view))
        except TelegramBadRequest as error:
            if "not modified" not in str(error):
                await send_view(query.bot, query.from_user.id, view)
        await query.answer()
        if view.meta.get("menu_changed"):          # D-250: a new language also changes the bottom keyboard
            await query.bot.send_message(query.from_user.id, "🌅 Lost Realms", reply_markup=menu_keyboard(service, account))


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
        try:
            await send_reports(bot, service)          # D-260: 💬 Feedback and the daily player report
        except Exception:
            log.exception("reports error")
        await asyncio.sleep(TICK_SECONDS)


def report_chats() -> list[int]:
    """The reports chat id (RPG_REPORTS_CHAT_ID, else the team's chat) and its other form; [] if it is not a number.

    [ES]
    Qué hace: da el número del chat de informes y su otra forma, por si se copió mal: un grupo común tiene un número como
    -4365890113 y un supergrupo, -100 delante (-1004365890113). El bot prueba el primero y, si Telegram dice "chat no
    encontrado", el otro. La llama: post_to_reports. Si cambia, afecta: a dónde llegan el informe y el feedback.
    """
    raw = (os.environ.get("RPG_REPORTS_CHAT_ID") or REPORTS_CHAT_DEFAULT).strip()
    try:
        chat = int(raw)
    except ValueError:
        log.error("RPG_REPORTS_CHAT_ID is not a chat id")
        return []
    digits = str(abs(chat))
    if chat >= 0:
        return [chat]
    other = -int(digits[3:]) if digits.startswith("100") and len(digits) > 3 else int(f"-100{digits}")
    return [chat, other]


_reports_chat: list[int | None] = [None]   # the reports chat id that worked last (one of report_chats()), once known
_report_failed_at = [float("-inf")]       # when the reports chat last refused us (loop time); none yet


async def post_to_reports(send: Callable[[int], Awaitable[Any]]) -> None:
    """Run send(chat) on the reports chat: the id that worked before, else each form of it; raise if none works.

    [ES]
    Qué hace: manda algo al chat de informes. Usa el número que ya funcionó; si todavía no hay, prueba report_chats() en
    orden. Si el grupo pasó a supergrupo (su número cambió), sigue al número nuevo. Recuerda el que funcionó y lo anota
    en el registro. Si ninguno funciona, lanza el último error. La llama: send_reports. Si cambia, afecta: el informe y el
    feedback.
    """
    chats = [_reports_chat[0]] if _reports_chat[0] is not None else report_chats()
    error: Exception | None = None
    for chat in chats:
        try:
            try:
                await send(chat)
            except TelegramMigrateToChat as moved:          # a group that became a supergroup has a new id
                chat = moved.migrate_to_chat_id
                await send(chat)
        except (TelegramBadRequest, TelegramForbiddenError) as refused:
            error = refused
            continue
        if _reports_chat[0] != chat:
            _reports_chat[0] = chat
            log.info("reports chat: %s", chat)
        return
    _reports_chat[0] = None                                # next time, try every form again
    raise error or RuntimeError("no reports chat configured")


async def send_reports(bot: Bot, service: GameService) -> None:
    """Post every new 💬 Feedback note and, once a day, the player report file to the reports chat (D-260).

    [ES]
    Qué hace: manda al chat de informes cada mensaje de 💬 Feedback nuevo (con el héroe, su nivel y su idioma) y, una vez por
    día, el informe de jugadores como archivo .txt (adapters/reports.py). Si Telegram no deja (por ejemplo, el bot no está
    en el chat), lo anota en el registro, el feedback vuelve a la cola (return_feedback) y todo se intenta de nuevo a la
    hora, o apenas agregan al bot a un chat. Un error nunca para al bot.
    La llama: notifier, en cada vuelta. Si cambia, afecta: lo que recibe el equipo.
    """
    loop_now = asyncio.get_event_loop().time()
    if loop_now - _report_failed_at[0] < REPORT_RETRY_SECONDS:
        return                                             # refused not long ago: wait (the feedback stays queued)
    notes = service.take_feedback()
    for index, note in enumerate(notes):
        text = (f"💬 <b>Feedback</b> · {html.escape(str(note.get('hero', '?')))} · nivel {note.get('level', '?')} · "
                f"{html.escape(str(note.get('lang', '?')))}\n{html.escape(str(note.get('text', '')))}")
        try:
            await post_to_reports(lambda chat, text=text: bot.send_message(chat, text))
        except Exception:
            service.return_feedback(notes[index:])         # nothing is lost: they go out on the next try
            _report_failed_at[0] = loop_now
            log.exception("could not post feedback; %d note(s) wait", len(notes) - index)
            return
    if reports.due(service):
        try:
            name, body = reports.build(service)
            document = BufferedInputFile(body.encode("utf-8"), filename=name)
            await post_to_reports(lambda chat: bot.send_document(chat, document, caption="📊 Informe de jugadores"))
            reports.mark_sent(service)
            log.info("player report sent: %s", name)
        except Exception:
            _report_failed_at[0] = loop_now
            log.exception("could not send the player report (tried %s)", report_chats())


async def announce_patch(bot: Bot, service: GameService) -> None:
    """Send the new patch notes to every Telegram player, once per version, slowly (Telegram limits).

    [ES]
    Qué hace: avisa a todos los jugadores lo nuevo de cada parche, una sola vez por versión.
    La llaman: main, al arrancar.
    Si cambia, afecta: los avisos de parches.
    """
    if service.pending_announcement() is None:
        return
    sent = 0
    for account_id in service.players():
        if not account_id.startswith("tg:"):
            continue
        view = service.announcement_view(account_id)     # D-250: each player reads it in their language
        if view is None:
            continue
        try:
            await bot.send_message(int(account_id[3:]), render_text(view), reply_markup=menu_keyboard(service, account_id))
            sent += 1
        except Exception:  # blocked the bot, deleted account, etc.
            log.info("could not announce to %s", account_id)
        await asyncio.sleep(0.05)
    log.info("patch announced to %d players", sent)


async def main() -> None:
    """Start polling. [ES] Qué hace: arranca el bot. La llaman: python -m adapters.telegram.bot. Si cambia, afecta: el arranque del bot."""
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    token = clean_token(os.environ.get("TELEGRAM_BOT_TOKEN", ""))
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")
    if not TOKEN_RE.match(token):
        log.error("TELEGRAM_BOT_TOKEN has a wrong format (length %d); copy it again from @BotFather", len(token))
    bot = Bot(token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    service = build_service()
    register(dp, service)
    me = await bot.get_me()
    log.info("running as @%s", me.username)
    render_module.BOT_USERNAME[0] = me.username or ""
    asyncio.create_task(notifier(bot, service))
    asyncio.create_task(announce_patch(bot, service))
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
