"""Muting the guild chat's notices and the players' global chat on the hero card (D-350, 0.63.1).

[ES]
Para qué sirve: prueba lo que pidió arkensaw203 (autorizado por el dueño el 31-oct-2026; sus dos intentos del 26 y el 28-oct
se revirtieron por romper el bot) y que se rehízo en la 0.63.1:
- 🛡️ Gremio → 📢 Chat tiene 🔕 Silenciar avisos: quien lo toca deja de recibir el aviso de cada mensaje del gremio, pero el
  mensaje queda en 📢 Chat, la pantalla lo recuerda y 🔔 Activar avisos lo vuelve a prender. Los demás siguen recibiendo;
  vale también con campamento y en inglés. Se guarda en "prefs" (campo "chat_mute").
- 👤 Héroe muestra al pie el enlace al 💬 chat global (balance.yaml community.global_chat_url); vacío, no sale.
- El botón "gmute" cuenta como contenido social en los informes.
Archivo: tests/test_chat_silenciado.py · Módulo: M15 Social, M2 Héroe · Prueba: engine/service/gremio.py (_chat_muted,
_guild_chat_mute, _guild_chat, _guild_chat_view), engine/service/game.py (_hero_view), engine/service/telemetry.py.
Si falla: alguien cambió el chat del gremio, la ficha del héroe o el enlace; ver D-350 en diseno/00-vision/decisiones.md.
"""

from conftest import make_hero
from test_camps import old_camp_at, place
from test_gremio_desde_el_inicio import join, new_gremio, pushes

from engine.service import telemetry


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def ids(view):
    return [action.id for action in view.actions]


def guild_of_two(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()                                                             # the join notices are not this test's
    return gid


def test_a_muted_member_gets_no_notice_but_the_message_stays_in_the_chat(service):
    gid = guild_of_two(service)
    chat = service.act("test:2", "gchat")
    assert "gmute" in ids(chat) and "🔕 Silenciar avisos" in [a.label for a in chat.actions]
    assert ids(chat)[-1] == "guild"                                            # ↩️ Volver stays last
    view = service.act("test:2", "gmute")
    assert view.kind == "guild_chat" and "ya no te llegan avisos" in view.notice
    assert "🔕 Tienes silenciados" in text(view) and "🔔 Activar avisos" in [a.label for a in view.actions]
    assert service.store.get("prefs", "test:2")["chat_mute"] is True

    sent = service.text("test:1", "Nos vemos en el bosque")
    assert "Enviado a tu gremio (1 compañero)" in sent.notice                 # it was sent: the mate can read it
    assert not pushes(service, "test:2", "gremio_message")                    # but no notice
    assert service.store.get("gremio", gid)["messages"][-1]["text"] == "Nos vemos en el bosque"
    assert "💬 Lyra: Nos vemos en el bosque" in text(service.act("test:2", "gchat"))

    back = service.act("test:2", "gmute")                                      # 🔔 on again
    assert "te vuelven a llegar" in back.notice and "🔕 Tienes silenciados" not in text(back)
    service.text("test:1", "Ya llegué")
    got = pushes(service, "test:2", "gremio_message")
    assert got and "💬 Lyra: Ya llegué" in got[0].body


def test_muting_is_personal_and_does_not_stop_what_you_send(service):
    guild_of_two(service)
    service.act("test:1", "gmute")                                             # the one who writes mutes
    service.text("test:1", "Hola")
    got = pushes(service, "test:2", "gremio_message")
    assert got and "💬 Lyra: Hola" in got[0].body                             # the others still get it
    service.text("test:2", "Hola Lyra")
    assert not pushes(service, "test:1", "gremio_message")


def test_muting_works_after_the_camp_is_founded(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    camp = service.store.get("camp", "6:0")
    camp["members"].append("test:2")
    service.store.put("camp", "6:0", camp)
    place(service, "test:2", 6, 0, camp="6:0")
    service.tick()
    service.act("test:2", "gmute")
    service.text("test:1", "Hay que reparar el muro")
    assert not pushes(service, "test:2", "gremio_message")
    assert "Hay que reparar el muro" in text(service.act("test:2", "gchat"))


def test_the_mute_reads_in_english(service):
    from test_idiomas import english_hero
    make_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()
    view = service.act("test:2", "gmute")
    assert "no longer reach you" in view.notice and "🔔 Turn notices on" in [a.label for a in view.actions]
    assert "You muted the chat notices" in text(view)
    assert not service.texts.fallbacks.get("en")


def test_the_hero_card_shows_the_global_chat_link(service):
    make_hero(service, "test:1", "Lyra")
    url = service.content.balance["community"]["global_chat_url"]
    assert url.startswith("https://t.me/")
    card = service.act("test:1", "hero")
    assert f"💬 Chat global de jugadores: {url}" in card.body
    service.content.balance["community"]["global_chat_url"] = ""             # empty: the line is not shown
    try:
        assert not any("Chat global" in line for line in service.act("test:1", "hero").body)
    finally:
        service.content.balance["community"]["global_chat_url"] = url


def test_the_mute_button_counts_as_social_content():
    assert telemetry.action_category("gmute") == "social"
