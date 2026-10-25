"""💬 Feedback for the team: the player picks a type, the card brings the @, priority and steps with buttons (D-275).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026 ("que los feedback vengan con el arroba, una descripción clasificada de
acuerdo al tipo de problema y las notas del jugador para yo darle prioridad; botones de acción… hasta cerrar el feedback
como resuelto"):
- el jugador elige el tipo (🐞 💡 ⚖️ ❓ 💬); si escribe directo, el tipo sale de sus palabras;
- cada feedback tiene su número, su @, su prioridad según el tipo y el paso 🆕 Nuevo;
- la tarjeta del chat de informes trae tipo, prioridad, paso, @, héroe, lugar, versión, texto e historial;
- los botones mueven el paso (👀 → ✅ → 🔧 → ✔️), cambian la prioridad, descartan y reabren; al resolver, el jugador recibe
  un gracias en su idioma; solo valen en el chat de informes.
Archivo: tests/test_feedback_equipo.py · Módulo: M20 Telemetría y administración · Prueba: engine/service/game.py
(_feedback_view, _feedback_classify, _save_feedback, set_handle, feedback_update), adapters/feedback_desk.py,
adapters/telegram/bot.py (send_reports, on_desk_button).
"""

import asyncio

import pytest
from aiogram.methods import AnswerCallbackQuery, EditMessageText
from aiogram.types import CallbackQuery, Update
from conftest import make_hero
from test_solo_privado import FakeBot, feed, message, user

from adapters import feedback_desk
from adapters.telegram import bot as tg

REPORTS = -1001234567890


def ids(view):
    return [a.id for a in view.actions]


def send(service, text, kind=None, account="test:1"):
    service.act(account, "fb")
    if kind:
        service.act(account, f"fbk:{kind}")
    return service.text(account, text)


@pytest.fixture(autouse=True)
def reports_chat(monkeypatch):
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", str(REPORTS))
    tg._reports_chat[0] = None
    tg._report_failed_at[0] = float("-inf")


def test_the_player_picks_a_type_or_the_words_pick_it(service):
    make_hero(service)
    view = service.act("test:1", "fb")
    assert ids(view)[:5] == ["fbk:bug", "fbk:idea", "fbk:balance", "fbk:confusing", "fbk:other"] and view.expects_text
    assert "🐞 Error" in "\n".join(service.act("test:1", "fbk:bug").body)
    assert "Gracias" in service.text("test:1", "Todo bien por acá").notice
    send(service, "No entiendo cómo se aprende un oficio")
    send(service, "Sería bueno agregar monturas")
    notes = service.take_feedback()
    assert [n["kind"] for n in notes] == ["bug", "confusing", "idea"]
    assert [n["id"] for n in notes] == [1, 2, 3] and [n["priority"] for n in notes] == ["high", "mid", "low"]
    assert all(n["status"] == "new" for n in notes)


def test_the_card_brings_the_at_the_hero_the_place_and_the_version(service):
    make_hero(service)
    service.set_handle("test:1", "@lyra")
    send(service, "La mochila no carga", "bug")
    note = service.take_feedback()[0]
    card = feedback_desk.card(note)
    assert "🐞 Error" in card and "🔴 Alta" in card and "🆕 Nuevo" in card and "#fb1" in card
    assert "@lyra" in card and "Lyra" in card and "nivel 1" in card and "(0, 0)" in card and "La mochila no carga" in card
    assert f"v{list(service.content.patches.values())[-1]['version']}" in card
    service.set_handle("test:1", "")
    send(service, "otra cosa", "other")
    assert 'tg://user?id=' not in feedback_desk.card(service.take_feedback()[0])   # a test account is not "tg:"


def test_the_buttons_walk_the_steps_and_resolving_thanks_the_player(service):
    make_hero(service)
    send(service, "La mochila no carga", "bug")
    service.take_feedback()
    assert feedback_desk.buttons(service.feedback_note("1"))[1][0] == ("👀 Visto", "fbo:1:next")
    steps = [service.feedback_update("1", "next", "@dueno")["status"] for _ in range(4)]
    assert steps == ["seen", "approved", "fixing", "resolved"]
    assert service.feedback_update("1", "next", "@dueno") is None                 # closed: nothing further
    assert feedback_desk.buttons(service.feedback_note("1")) == [[("↩️ Reabrir", "fbo:1:reopen")]]
    outbox = service.store.get("outbox", "test:1")["items"]
    assert any("quedó resuelto" in line for item in outbox for line in item["body"])
    assert service.feedback_update("1", "reopen", "@dueno")["status"] == "seen"
    assert service.feedback_update("1", "p:low", "@dueno")["priority"] == "low"
    assert service.feedback_update("1", "discard", "@dueno")["status"] == "discarded"
    history = service.feedback_note("1")["history"]
    assert len(history) == 7 and all(h["by"] == "@dueno" for h in history)
    assert feedback_desk.parse("fbo:1:p:high") == ("1", "p:high") and feedback_desk.parse("fbk:bug") is None


def test_the_bot_posts_the_card_and_the_team_moves_it_only_in_the_reports_chat(service):
    make_hero(service)
    send(service, "La mochila no carga", "bug")
    poster = FakeBot()
    asyncio.run(tg.send_reports(poster, service))
    card = poster.calls[0]
    assert card.chat_id == REPORTS and "🐞 Error" in card.text and card.reply_markup.inline_keyboard[1][0].callback_data == "fbo:1:next"
    msg = message("supergroup", "card", chat_id=REPORTS)
    query = CallbackQuery(id="d1", from_user=user(), chat_instance="c", message=msg, data="fbo:1:next")
    fake = feed(service, Update(update_id=10, callback_query=query))
    assert any(isinstance(c, EditMessageText) and "👀 Visto" in c.text for c in fake.calls)
    assert service.feedback_note("1")["status"] == "seen"
    elsewhere = message("supergroup", "card", chat_id=-100777)
    query = CallbackQuery(id="d2", from_user=user(), chat_instance="c", message=elsewhere, data="fbo:1:next")
    fake = feed(service, Update(update_id=11, callback_query=query))
    assert service.feedback_note("1")["status"] == "seen" and all(isinstance(c, AnswerCallbackQuery) for c in fake.calls)


def test_feedback_types_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    view = service.act("test:1", "fb")
    assert [a.label for a in view.actions][:2] == ["🐞 Bug", "💡 Idea"]
    service.text("test:1", "The game crashes when I open the map")
    assert service.take_feedback()[0]["kind"] == "bug"
    assert not service.texts.fallbacks.get("en")
