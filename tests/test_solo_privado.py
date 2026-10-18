"""The game is played only in a private chat with the bot; the reports chat finds its real id (D-262, 0.33.1).

[ES] Pruebas de "se juega solo por privado" (pedido del dueño, 18-oct-2026: "no se permite enviar mensajes dentro de los
chats con el juego, porque si no todos van a estar jugando dentro de los chats"):
- en un grupo, un comando recibe solo el aviso "🔒 se juega por privado" con el botón al chat del bot, en el idioma del
  jugador; la charla del grupo no recibe nada; un botón viejo del juego en un grupo no juega; nada llega al motor;
- en el chat privado todo sigue igual;
- el chat de informes prueba el número configurado y su otra forma (-100… o sin -100) y recuerda el que sirvió;
- si el chat de informes no deja, el 💬 Feedback vuelve a la cola y nada se pierde.
Archivo: tests/test_solo_privado.py · Módulo: adaptador de Telegram, M20 Telemetría · Prueba: adapters/telegram/bot.py
(register, private_notice, in_group, report_chats, post_to_reports, send_reports), engine/service/game.py (say,
take_feedback, return_feedback).
"""

import asyncio
from datetime import datetime, timezone

import pytest
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import AnswerCallbackQuery, SendDocument, SendMessage
from aiogram.types import CallbackQuery, Chat, Message, Update, User
from conftest import make_hero

from adapters.telegram import bot as tg
from adapters.telegram import render

TOKEN = "123456789:" + "A" * 35


class FakeBot(Bot):
    """A bot that never talks to Telegram: it keeps every call; `refuse` lists the chat ids that answer "chat not found"."""

    def __init__(self, refuse=()):
        super().__init__(TOKEN)
        self.calls = []
        self.refuse = set(refuse)

    async def __call__(self, method, request_timeout=None):
        chat = getattr(method, "chat_id", None)
        if chat in self.refuse:
            raise TelegramBadRequest(method=method, message="Bad Request: chat not found")
        self.calls.append(method)
        return True


def user(lang="es"):
    return User(id=42, is_bot=False, first_name="Ana", language_code=lang)


def message(chat_type, text, chat_id=-100555):
    chat = Chat(id=chat_id if chat_type != "private" else 42, type=chat_type, title=None if chat_type == "private" else "Gremio")
    return Message(message_id=1, date=datetime.now(timezone.utc), chat=chat, from_user=user(), text=text)


def feed(service, update, fake=None):
    fake = fake or FakeBot()
    dp = Dispatcher()
    tg.register(dp, service)
    asyncio.run(dp.feed_update(fake, update))
    return fake


@pytest.fixture(autouse=True)
def bot_username():
    render.BOT_USERNAME[0] = "LostRealmsbot"
    tg._reports_chat[0] = None
    tg._report_failed_at[0] = float("-inf")
    yield
    render.BOT_USERNAME[0] = ""


def test_a_command_in_a_group_only_gets_the_private_notice(service):
    fake = feed(service, Update(update_id=1, message=message("supergroup", "/start")))
    assert len(fake.calls) == 1 and isinstance(fake.calls[0], SendMessage)
    sent = fake.calls[0]
    assert "por privado" in sent.text and sent.chat_id == -100555
    assert sent.reply_markup.inline_keyboard[0][0].url == "https://t.me/LostRealmsbot"
    assert service.players() == [] or "tg:42" not in service.players()      # nothing reached the engine


def test_plain_chat_in_a_group_gets_nothing(service):
    fake = feed(service, Update(update_id=1, message=message("group", "hola a todos")))
    assert fake.calls == []


def test_a_game_button_in_a_group_does_not_play(service):
    make_hero(service, "tg:42")
    hero = service._load("tg:42")
    before = (hero.x, hero.y, hero.energy, dict(hero.activity or {}))
    old = message("supergroup", "📍 Zona")
    query = CallbackQuery(id="q1", from_user=user("en"), chat_instance="c", message=old, data="explore")
    fake = feed(service, Update(update_id=2, callback_query=query))
    assert len(fake.calls) == 1 and isinstance(fake.calls[0], AnswerCallbackQuery)
    assert fake.calls[0].show_alert and "played in private" in fake.calls[0].text   # never chose a language: Telegram's
    hero = service._load("tg:42")
    assert (hero.x, hero.y, hero.energy, dict(hero.activity or {})) == before        # the button did not play


def test_the_private_chat_still_plays(service):
    fake = feed(service, Update(update_id=3, message=message("private", "/start")))
    assert any(isinstance(c, SendMessage) and c.text == "🌅 Lost Realms" for c in fake.calls)


def test_the_notice_speaks_the_players_language(service):
    assert "is played in private" in service.say("tg:7", "client.private_only", lang_hint="en")   # never chose: Telegram's
    assert "por privado" in service.say("tg:7", "client.private_only", lang_hint="xx")             # unknown: Spanish
    service.view("tg:8")
    service.act("tg:8", "lang:en")
    assert "is played in private" in service.say("tg:8", "client.private_only", lang_hint="es")    # chosen wins
    text, markup = tg.private_notice(service, user("en"))
    assert "private" in text and markup.inline_keyboard[0][0].text == "▶️ Play in private"


def test_the_reports_chat_tries_its_other_form_and_remembers_it(monkeypatch):
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "-1004365890113")
    assert tg.report_chats() == [-1004365890113, -4365890113]
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "-4365890113")
    assert tg.report_chats() == [-4365890113, -1004365890113]
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "no")
    assert tg.report_chats() == []
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "-1004365890113")
    fake = FakeBot(refuse={-1004365890113})
    asyncio.run(tg.post_to_reports(lambda chat: fake(SendMessage(chat_id=chat, text="hola"))))
    assert fake.calls[0].chat_id == -4365890113 and tg._reports_chat[0] == -4365890113


def test_the_report_and_feedback_wait_when_the_chat_refuses_and_go_out_later(service, monkeypatch):
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "-1004365890113")
    make_hero(service, "tg:42")
    service.act("tg:42", "fb")
    service.text("tg:42", "Me gusta la fogata")
    closed = FakeBot(refuse={-1004365890113, -4365890113})
    asyncio.run(tg.send_reports(closed, service))
    assert closed.calls == [] and tg._report_failed_at[0] > float("-inf")
    assert len([d for _, d in service.store.items("feedback") if not d.get("sent")]) == 1   # back in the queue
    tg._report_failed_at[0] = float("-inf")                                                 # an hour later
    open_chat = FakeBot(refuse={-1004365890113})
    asyncio.run(tg.send_reports(open_chat, service))
    kinds = [type(c) for c in open_chat.calls]
    assert kinds == [SendMessage, SendDocument] and all(c.chat_id == -4365890113 for c in open_chat.calls)
    assert "Me gusta la fogata" in open_chat.calls[0].text
    assert service.take_feedback() == []
