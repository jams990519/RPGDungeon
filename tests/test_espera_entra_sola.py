"""Who waits in the guild gets into the camp by itself when there is room (D-323).

[ES] Pruebas de la orden del dueño del 21-oct-2026 ("verifica que los jugadores que están en cola de espera para entrar en el
campamento entren automáticamente cuando sube de nivel; si no pasa, hazlo ahora; garantiza que eso pase"): al subir de nivel
entran tantos como lugares, en orden de llegada, y el resto sigue esperando; sin lugar no entra nadie; quien acepta la espera
con lugar libre entra en el momento; los que esperaban desde antes del parche entran en el primer tick; el fundador y sus
asistentes reciben el aviso; y se lee bien en inglés.
Archivo: tests/test_espera_entra_sola.py · Módulo: M15 Social, M14 Construcción · Prueba: engine/service/gremio.py
(_tell_waiting_room, _waiting_sweep, _wait_invite_answer), engine/service/game.py (_level_up, tick, _guild_view).
"""

import pytest

from conftest import make_hero
from test_camps import old_camp_at, place
from test_guilds import join

KEY = "6:0"
# D-327 (0.51): these tests are about the waiting line, written with camps of 2 places at level 1 (2 more per level):
# they keep that old count in their test content (conftest.old_member_caps). [ES] El cupo por etapa (10, 15, 25…) y la
# fila que entra al pasar de etapa se prueban en tests/test_escalera_cupo_oficiales.py.
pytestmark = pytest.mark.usefixtures("old_member_caps")


def camp(service):
    return service.store.get("camp", KEY)


def wait(service, *accounts):
    """Put these heroes in the camp's waiting line, in this order (as an accepted invitation leaves them)."""
    data = camp(service)
    for account in accounts:
        data.setdefault("waiting", []).append(account)
        service.store.put("camp_wait", account, {"camp": KEY})
    service.store.put("camp", KEY, data)


def full_camp_with_line(service, line=("test:3", "test:4", "test:5")):
    """Lyra's old camp at level 1 (room for 2) with Bram in it, and a line of heroes waiting."""
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    for n, name in zip(range(3, 6), ("Cora", "Dario", "Eva")):
        make_hero(service, f"test:{n}", name)
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    wait(service, *line)
    service.tick()


def level_up(service):
    record = service._upgrades(KEY)
    record["built"].update({"fogon": 0.0, "empalizada": 0.0})
    record["levelup"] = {"to": 2, "given": {"madera": 30, "piedra": 20, "fibra": 10}, "chests": 0}
    service.store.put("upgrades", KEY, record)
    return service.act("test:1", "lvlgo")


def test_going_up_a_level_lets_in_as_many_as_fit_first_come_first_in(service):
    full_camp_with_line(service)
    assert service._camp_room(camp(service)) == 0
    level_up(service)                                                          # level 2: room for 4 → 2 more
    data = camp(service)
    assert data["level"] == 2 and data["members"][-2:] == ["test:3", "test:4"] and data["waiting"] == ["test:5"]
    assert service._load("test:3").camp == KEY and service._load("test:4").camp == KEY and not service._load("test:5").camp
    assert service.store.get("camp_wait", "test:5") == {"camp": KEY}
    out = service.tick()
    assert any(acc == "test:3" and v.kind == "camp_answer" for acc, v in out)
    told = [v for acc, v in out if acc == "test:1" and v.kind == "gremio_news"]
    assert told and "Cora" in told[0].body[0] and "Dario" in told[0].body[0] and "Eva" not in told[0].body[0]


def test_without_room_nobody_gets_in(service):
    full_camp_with_line(service)
    service._tell_waiting_room(KEY)
    assert camp(service)["waiting"] == ["test:3", "test:4", "test:5"] and len(camp(service)["members"]) == 2


def test_who_already_has_a_camp_leaves_the_line_without_taking_a_place(service):
    full_camp_with_line(service)
    data = service.store.get("hero", "test:3")
    data["camp"] = "9:9"
    service.store.put("hero", "test:3", data)
    level_up(service)
    assert camp(service)["members"][-2:] == ["test:4", "test:5"] and camp(service)["waiting"] == []


def test_those_waiting_from_before_the_patch_get_in_on_the_first_tick(service):
    full_camp_with_line(service, line=())
    data = camp(service)
    data["level"] = 2                                                          # room for 2 already, before the patch
    data["waiting"] = ["test:3"]
    service.store.put("camp", KEY, data)
    service.store.put("camp_wait", "test:3", {"camp": KEY})
    service._waiting_swept = False                                            # as if the bot just started
    service.tick()
    assert "test:3" in camp(service)["members"] and service._load("test:3").camp == KEY


def test_accepting_the_wait_with_room_free_joins_at_once(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:3", "Cora")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")                    # level 1: room for 2, only Lyra in
    data = camp(service)
    data.setdefault("wait_invites", []).append("test:3")
    service.store.put("camp", KEY, data)
    view = service.act("test:3", "cwait:6:0:y")
    assert "test:3" in camp(service)["members"] and service._load("test:3").camp == KEY
    assert "ya eres miembro del campamento Roca Alta" in view.notice


def test_the_notices_read_well_in_english(service):
    from test_idiomas import english_hero
    full_camp_with_line(service)
    english_hero(service, "test:3", "Cora")
    data = camp(service)
    data["waiting"] = ["test:3"]
    service.store.put("camp", KEY, data)
    level_up(service)
    out = service.tick()
    joined = [v for acc, v in out if acc == "test:3" and v.kind == "camp_answer"]
    assert joined and "You're now a member of the camp Roca Alta" in joined[0].body[0]
    assert not service.texts.fallbacks.get("en")
