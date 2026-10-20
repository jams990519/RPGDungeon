"""/inv_ and the player code: invite someone to your guild, or to your camp once founded, from anywhere (D-280).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026 ("el formato para invitar a jugadores al gremio: /inv_ y el código de
jugador"):
- cada jugador tiene su código de 8 cifras, que no cambia y se ve en 👤 Héroe, en su tarjeta (/j1) y en 🛡️ Gremio sin gremio;
- el líder o un oficial invita con /inv_<código> desde cualquier lugar; al otro le llega ✅ / ❌; un miembro común no puede;
- un código que no es de nadie o el tuyo propio solo avisan; un jugador que nunca miró su código igual se encuentra;
- con el campamento ya fundado invita su fundador: el jugador entra al campamento (y a su gremio) si hay lugar;
- /inv solo sigue abriendo la 🎒 Mochila; y todo se lee en inglés.
Archivo: tests/test_invitar_con_codigo.py · Módulo: M15 Social · Prueba: engine/service/gremio.py (player_code,
_account_by_code, _invite_code, _gremio_invite_send, _camp_invite_send, _camp_invite_answer), engine/service/game.py (text()).
"""

from conftest import make_hero
from test_camps import old_camp_at
from test_gremio_desde_el_inicio import join, new_gremio


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def last_push(service, account):
    items = (service.store.get("outbox", account) or {}).get("items", [])
    return items[-1] if items else None


def test_every_player_has_a_stable_code_shown_in_hero_card_and_guild(service):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    code = service.player_code("test:1")
    assert code.isdigit() and len(code) == 8 and service.player_code("test:1") == code
    assert service.player_code("test:2") != code
    assert f"/inv_{code}" in text(service.act("test:1", "hero"))
    assert f"/inv_{code}" in text(service.act("test:1", "guild"))                  # no guild yet: your code
    assert f"/inv_{service.player_code('test:2')}" in text(service._player_card(service._load("test:1"), "test:2"))


def test_the_leader_invites_with_the_code_from_anywhere(service):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    gid, created = new_gremio(service)
    assert "/inv_" in created.notice
    hero = service._load("test:1")
    hero.x, hero.y = 5, -4                                                         # far from the bonfire
    service._save(hero)
    view = service.text("test:1", f"/inv_{service.player_code('test:2')}")
    assert "Invitaste a Bram" in view.notice
    push = last_push(service, "test:2")
    assert [a["id"] for a in push["actions"]] == [f"ginv:{gid}:y", f"ginv:{gid}:n"]
    service.act("test:2", f"ginv:{gid}:y")
    assert "test:2" in service.store.get("gremio", gid)["members"]
    assert "/inv_" in text(service.act("test:1", "gmembers"))                      # the leader sees how to invite (D-302: in 👥 Miembros)


def test_unknown_own_or_without_rights_only_explain(service):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cira")
    assert "No hay ningún jugador" in service.text("test:1", "/inv_12345678").notice
    assert "tu propio código" in service.text("test:1", f"/inv_{service.player_code('test:1')}").notice
    assert "líder u oficial" in service.text("test:1", f"/inv_{service.player_code('test:2')}").notice
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    assert "Solo el líder o un oficial" in service.text("test:2", f"/inv_{service.player_code('test:3')}").notice   # a plain member
    service.act("test:1", "goff:test:2")                                           # now an officer
    assert "Invitaste a Cira" in service.text("test:2", f"/inv_{service.player_code('test:3')}").notice


def test_a_player_who_never_looked_at_the_code_is_found(service):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    new_gremio(service)
    code = service.player_code("test:2")
    service.store.delete("player_code", code)                                     # as if never asked for
    service.store.delete("player_code_of", "test:2")
    assert "Invitaste a Bram" in service.text("test:1", f"/inv_{code}").notice


def test_the_camp_founder_invites_into_the_camp(service):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cira")
    make_hero(service, "test:4", "Dax")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")                       # a level-1 camp: room for 2
    view = service.text("test:1", f"/inv_{service.player_code('test:2')}")
    assert "Invitaste a Bram" in view.notice
    push = last_push(service, "test:2")
    assert push["actions"][0]["id"] == "cinv:6:0:y" and "(6, 0)" in "\n".join(push["body"])
    service.text("test:1", f"/inv_{service.player_code('test:3')}")
    service.act("test:3", "cinv:6:0:n")
    assert service._load("test:3").camp is None
    assert "no entró" in "\n".join(last_push(service, "test:1")["body"])
    answer = service.act("test:2", "cinv:6:0:y")
    assert "Entraste al campamento Roca Alta" in answer.notice
    assert service._load("test:2").camp == "6:0" and "test:2" in service.store.get("camp", "6:0")["members"]
    assert "ya se respondió" in service.act("test:2", "cinv:6:0:y").notice
    assert "lleno" in service.text("test:1", f"/inv_{service.player_code('test:4')}").notice   # the camp is full now
    assert "líder u oficial" in service.text("test:2", f"/inv_{service.player_code('test:4')}").notice   # only the founder


def test_inv_alone_is_still_the_backpack(service):
    make_hero(service)
    assert service.text("test:1", "/inv").kind == service.act("test:1", "bag").kind


def test_inviting_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    assert "/inv_" in text(service.act("test:1", "hero"))
    assert "No player has the code" in service.text("test:1", "/inv_12345678").notice
    assert not service.texts.fallbacks.get("en")
