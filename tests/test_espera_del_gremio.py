"""In the guild, waiting for room in the camp (D-294, 0.39): invited while the camp is full, everything of the guild, nothing of
the camp, joined by the founder or a helper when there is room.

[ES] Pruebas de lo que respondió el dueño el 19-oct-2026 ("quien va a entrar a tu territorio, puedes invitarlo si no tiene
campamento. Lo vas a invitar al gremio en sí. Cuando tengas más capacidad en el campamento, lo vas a unir al campamento. Hasta ese
momento no va a recibir los bonos del campamento. Pero como está en el gremio, va a poder depositar para el gremio"):
1. con el campamento lleno, el fundador o un ayudante invita al GREMIO a quien no tiene campamento (/inv_, la tarjeta de un
   jugador o el aviso de quien visita el territorio); si acepta, espera lugar (camp["waiting"]);
2. caben gremio.waiting_max esperando (10, número fijo del dueño);
3. cuando hay lugar, se avisa a quien espera y al fundador y sus ayudantes; lo une el fundador o un ayudante con un botón
   (🏕️ Unir al campamento), nunca solo;
4. mientras espera tiene todo lo del gremio (💰 depositar, 📢 chat de ida y vuelta, ⚔️ armería, 🗺️ zonas) y nada del campamento
   (servicios, estaciones, territorio, cupo); no funda ni entra a otro gremio, y puede salir del gremio;
5. 🛡️ Gremio lo muestra en su bloque "⏳ Esperando lugar en el campamento"; y todo se lee en inglés.
Además, el 🛡️ Gremio se abre directo desde el centro del campamento (el dueño: "el botón de gremio no se puede ver una vez ya
construiste el campamento… debería aparecer") y nunca pasa de 8 botones.
Archivo: tests/test_espera_del_gremio.py · Módulo: M15 Social · Prueba: engine/service/gremio.py (_waiting_key, _guild_camp,
_camp_or_wait_invite, _wait_invite_send, _wait_invite_answer, _camp_join_waiting, _waiting_leave, _tell_waiting_room,
_waiting_lines, _mates, _guild_chat, _camp_deposit, _armory_key) y engine/service/game.py (_guild_view, _visit_camp,
_camp_hub_actions, _ask_join).
"""

from conftest import make_hero
from engine.messaging import Action
from engine.service.game import HUB_BUTTONS
from test_camps import old_camp_at, place
from test_guilds import join

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def pushes(service, account, kind=None):
    return [v for acc, v in service.tick() if acc == account and (kind is None or v.kind == kind)]


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def full_camp(service):
    """Lyra's old camp at 6:0, level 1: room for 2, and Bram fills it. Cora has no camp nor guild."""
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cora")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    service.tick()


def waiting_cora(service):
    full_camp(service)
    service.text("test:1", f"/inv_{service.player_code('test:3')}")
    service.act("test:3", "cwait:6:0:y")
    service.tick()


def test_a_full_camp_invites_into_the_guild_and_they_show_in_their_own_block(service):
    full_camp(service)
    camp = service.store.get("camp", KEY)
    assert len(camp["members"]) == service._members_cap(camp) == 2
    view = service.text("test:1", f"/inv_{service.player_code('test:3')}")
    assert "esperará lugar" in view.notice
    invite = pushes(service, "test:3", "camp_wait_invite")
    assert invite and ids(invite[0]) == ["cwait:6:0:y", "cwait:6:0:n"] and "lleno" in invite[0].body[0]
    view = service.act("test:3", "cwait:6:0:y")
    camp = service.store.get("camp", KEY)
    assert camp["waiting"] == ["test:3"] and camp["members"] == ["test:1", "test:2"] and service._load("test:3").camp is None
    assert view.kind == "guild" and "esperando lugar" in text(view) and "gwleave" in ids(view) and "gfund" in ids(view)
    told = pushes(service, "test:1", "camp_answer")
    assert told and "espera lugar" in told[0].body[0]
    guild = service.act("test:1", "guild")
    body = text(guild)
    assert "⏳ Esperando lugar en el campamento (1/10):" in body
    assert any(line.startswith("/m3 ⏳ Cora") for line in guild.body)
    card = service.text("test:1", "/m3")
    assert card.kind == "gremio_member" and "lleno" in text(card) and not any(a.startswith("cwjoin:") for a in ids(card))
    assert "ya se respondió" in service.act("test:3", "cwait:6:0:y").notice


def test_the_waiting_cap_is_a_fixed_number(service):
    full_camp(service)
    assert service.content.balance["gremio"]["waiting_max"] == 10
    service.content.balance["gremio"]["waiting_max"] = 1
    service.text("test:1", f"/inv_{service.player_code('test:3')}")
    service.act("test:3", "cwait:6:0:y")
    make_hero(service, "test:4", "Dax")
    view = service.text("test:1", f"/inv_{service.player_code('test:4')}")
    assert "une a alguien al campamento primero" in view.notice and not pushes(service, "test:4", "camp_wait_invite")


def test_while_waiting_everything_of_the_guild_and_nothing_of_the_camp(service):
    waiting_cora(service)
    service.act("test:1", "upact:fogon")                                     # 20 madera + 15 piedra
    service.tick()
    set_hero(service, "test:3", x=9, y=-4, backpack={"madera": 8, "espada_2": 1})
    view = service.text("test:3", "/f01")                                    # 💰 deposits for the guild, from anywhere
    assert view.kind == "camp_fund" and service._upgrades(KEY)["works"]["fogon"] == {"madera": 8}
    assert "Cora" in text(service.act("test:1", "gfund"))                    # who gave what
    view = service.text("test:3", "Voy con madera")                         # 📢 the chat reaches the guild...
    assert "2 compañeros" in view.notice
    got = {acc for acc, v in service.tick() if v.kind == "gremio_message"}
    assert got == {"test:1", "test:2"}
    service.text("test:2", "Gracias")                                        # ...and the guild reaches them
    assert any("Gracias" in v.body[0] for v in pushes(service, "test:3", "gremio_message"))
    service.act("test:3", "garm")                                            # ⚔️ the armory
    assert "Dejaste" in service.text("test:3", "/a1").notice
    assert [e["item"] for e in service.store.get("armory", KEY)["items"]] == ["espada_2"]
    cora, lyra = service._load("test:3"), service._load("test:1")
    assert set(service._mates(cora)) == {"test:1", "test:2"} and "test:3" in service._mates(lyra)   # 🗺️ shared zones
    lyra.exploration["5:5"] = 70
    service._save(lyra)
    assert service._known_pct(service._load("test:3"), 5, 5) == 70
    place(service, "test:3", 6, 0)                                           # at the camp: none of the camp's things
    cora = service._load("test:3")
    assert service._camp_regen_mult(cora) == 1.0 and service._stations_here(cora) == ([], None)
    assert service.act("test:3", "upsvc").kind != "camp_services"
    here = service.act("test:3", "claro")                                    # the camp screen: no 🙋 Pedir unirme, 🛡️ instead
    assert "askjoin" not in ids(here) and "guild" in ids(here) and "esperando lugar" in text(here)
    camp = service.store.get("camp", KEY)
    assert "test:3" not in camp["members"] and len(camp["members"]) == service._members_cap(camp)
    assert "Ya tienes gremio" in service.act("test:3", "gnew").notice        # no other guild...
    make_hero(service, "test:4", "Dax")
    old_camp_at(service, "test:4", -6, 0, name="Otro Lado")
    place(service, "test:3", -6, 0)
    assert "Ya estás en un gremio" in service.act("test:3", "askjoin").notice   # ...nor another camp


def test_when_there_is_room_they_are_told_and_a_founder_or_helper_joins_them(service):
    waiting_cora(service)
    service.act("test:1", "claim:7:0")                                       # the camp grows: room for 4
    room = pushes(service, "test:3", "gremio_news")
    assert room and "Hay lugar en el campamento Roca Alta" in room[0].body[0]
    assert service.store.get("camp", KEY)["waiting"] == ["test:3"]           # never automatic
    told = [v for acc, v in service.tick() if acc == "test:1"]
    assert not told                                                          # the notice was already delivered
    assert "Hay 2 lugares" in text(service.act("test:1", "guild"))
    service.act("test:2", "guild")
    assert "cwjoin" not in " ".join(ids(service.text("test:2", "/m3")))      # a plain member cannot
    assert "fundador o un 🤝 ayudante" in service.act("test:2", "cwjoin:test:3").notice
    camp = service.store.get("camp", KEY)
    camp["helpers"] = ["test:2"]                                             # a helper can
    service.store.put("camp", KEY, camp)
    service.act("test:2", "guild")
    card = service.text("test:2", "/m3")
    assert "cwjoin:test:3" in ids(card)
    view = service.act("test:2", "cwjoin:test:3")
    camp = service.store.get("camp", KEY)
    assert "test:3" in camp["members"] and camp["waiting"] == [] and service._load("test:3").camp == KEY
    assert "ya es miembro" in view.notice and service.store.get("camp_wait", "test:3") is None
    joined = pushes(service, "test:3", "camp_answer")
    assert joined and "Ya eres miembro del campamento Roca Alta" in joined[0].body[0]


def test_leaving_the_guild_while_waiting(service):
    waiting_cora(service)
    assert service.act("test:3", "gwleave").kind == "gremio_confirm"
    view = service.act("test:3", "gwleave!")
    assert view.kind == "gremio_none" and "Saliste del gremio de Roca Alta" in view.notice
    assert service.store.get("camp", KEY)["waiting"] == [] and service._waiting_key("test:3") is None
    assert pushes(service, "test:1", "gremio_news")
    set_hero(service, "test:3", gold=100)
    assert service.act("test:3", "gnew").kind == "name_gremio"               # free again


def test_a_visitor_with_no_camp_can_be_invited_from_the_visit_notice(service):
    full_camp(service)
    visitor = service._load("test:3")
    visitor.x, visitor.y = 6, 0
    service._visit_camp(visitor)
    out = service.tick()
    lyra = [v for acc, v in out if acc == "test:1" and v.kind == "camp_visit"]
    bram = [v for acc, v in out if acc == "test:2" and v.kind == "camp_visit"]
    assert lyra and ids(lyra[0])[-1] == "ginvite:test:3"                     # the founder can invite...
    assert bram and "ginvite:test:3" not in ids(bram[0])                     # ...a plain member cannot
    view = service.act("test:1", "ginvite:test:3")
    assert "esperará lugar" in view.notice and pushes(service, "test:3", "camp_wait_invite")


def test_the_guild_is_on_the_camp_hub_and_the_hub_keeps_eight(service, monkeypatch):
    full_camp(service)
    view = service.act("test:1", "claro")
    assert "guild" in ids(view) and len(view.actions) <= HUB_BUTTONS
    assert "gfund" in ids(service.act("test:1", "guild"))
    from test_camp_upgrades import build
    from test_guilds import set_level
    set_level(service, 7)
    build(service, "biblioteca")
    view = service.act("test:1", "claro")
    assert ids(view) == ["cook", "research", "oficios", "trainer", "upsvc", "guild", "campmgmt", "dudas"]   # 📜 in /encargos
    monkeypatch.setattr(service, "_defend_action", lambda camp, hero: Action(id="defend", label="🛡️"))
    view = service.act("test:1", "claro")
    assert ids(view) == ["defend", "cook", "research", "oficios", "upsvc", "guild", "campmgmt", "dudas"]   # 🧑‍🏫 in /entrenador


def test_waiting_reads_well_in_english(service):
    from test_idiomas import english_hero
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    english_hero(service, "test:3", "Cora")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    join(service, "test:2")
    service.text("test:1", f"/inv_{service.player_code('test:3')}")
    invite = pushes(service, "test:3", "camp_wait_invite")
    assert invite and invite[0].title == "✉️ Guild invitation"
    view = service.act("test:3", "cwait:6:0:y")
    assert "waiting for room" in text(view) and "[" not in text(view)
    assert "[" not in text(service.act("test:3", "gfund")) and "[" not in text(service.act("test:3", "garm"))
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
