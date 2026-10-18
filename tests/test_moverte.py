"""🔗 Moverte: add steps in any order and the hero walks them; an ambush on the way pauses the trip (D-244, 0.33).

[ES] Pruebas de 🔗 Moverte, el 5.º botón de 📍 Zona (pedido del dueño: "un botón extra que diga moverte" para elegir
cuántos pasos seguidos y en qué direcciones). Cada flecha suma un paso, ⌫ quita el último, ❌ Cancelar borra el camino y
✅ Terminar sale; el camino llega entero a donde se armó (también a tierra nueva) y hay un tope de travel.walk_max pasos.
Una emboscada a mitad de camino ya no tira el resto: si ganas, sigues; si huyes o caes, te quedas ahí. Vale también para
el viaje de 📒 Lugares. Todo en los dos idiomas.
Archivo: tests/test_moverte.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_zone_view, _walk_action,
_walk_view, _walk_start, _arrive, _resume_route, _end_combat), content/balance.yaml (travel.walk_max).
"""

from conftest import make_hero
from engine.core import Rng


def ids(view):
    return [a.id for a in view.actions]


def no_ambush(service):
    service.content.balance["explore"]["arrival_encounter_scale"] = 0.0


class AmbushRng(Rng):
    """Every chance() comes true: the arrival ambush always jumps (the rest is a normal seeded roll)."""

    def chance(self, probability):
        return probability > 0


def test_the_zone_has_a_fifth_wide_button_to_move(service):
    make_hero(service)
    view = service.act("test:1", "home")
    assert ids(view) == ["go:n", "go:s", "go:e", "go:w", "walk", "zmap"] and view.layout == [2, 2, 1, 1]   # 0.34: + 🗺️ Mapa
    assert view.actions[-2].label == "🔗 Moverte"


def test_steps_add_up_in_any_order_and_can_be_undone_or_cancelled(service):
    make_hero(service)
    view = service.act("test:1", "walk")
    assert view.kind == "walk" and ids(view) == ["wlk:n", "wlk:s", "wlk:e", "wlk:w", "wlk:cancel", "wlk:go"]
    for step in ("n", "n", "e", "w", "s", "s"):
        view = service.act("test:1", f"wlk:{step}")
    body = "\n".join(view.body)
    assert "⬆️×2 ➡️ ⬅️ ⬇️×2" in body and "6 pasos" in body and "(0, 0)" in body
    assert "wlk:undo" in ids(view) and view.layout == [4, 1, 2]
    view = service.act("test:1", "wlk:undo")
    assert "5 pasos" in "\n".join(view.body) and "(0, 1)" in "\n".join(view.body)
    assert service.act("test:1", "walk").kind == "walk" and "5 pasos" in "\n".join(service.act("test:1", "walk").body)
    view = service.act("test:1", "wlk:cancel")
    assert view.kind == "zone" and view.notice
    assert "wlk:undo" not in ids(service.act("test:1", "walk"))                  # the way was wiped
    assert service.act("test:1", "wlk:go").notice                                 # nothing to walk yet
    assert not service._load("test:1").activity
    assert not service.texts.missing


def test_the_walk_goes_step_by_step_to_new_land(service, clock):
    make_hero(service)
    no_ambush(service)
    for step in ("n", "n", "n", "e", "e"):
        service.act("test:1", f"wlk:{step}")
    view = service.act("test:1", "wlk:go")
    hero = service._load("test:1")
    assert view.kind != "walk" and hero.activity["kind"] == "travel" and hero.activity.get("walk")
    assert hero.activity["to"] == [0, 1] and hero.activity["goal"] == [2, 3] and len(hero.activity["path"]) == 4
    assert not hero.remembers(2, 3)                                               # a walk may end on uncharted land
    for _ in range(5):
        clock.advance(120)
        service.view("test:1")
    hero = service._load("test:1")
    assert (hero.x, hero.y) == (2, 3) and not hero.activity and hero.remembers(2, 3)
    assert not service.texts.missing


def test_there_is_a_cap_on_steps(service):
    make_hero(service)
    top = service.content.balance["travel"]["walk_max"]
    assert top == 50
    for _ in range(top):
        service.act("test:1", "wlk:n")
    view = service.act("test:1", "wlk:e")
    assert view.notice and f"{top} pasos" in "\n".join(view.body)


def test_an_ambush_on_the_way_won_lets_the_walk_go_on(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.x, hero.y = 0, 4                                       # outside the Claro's land: ambushes can happen
    service._save(hero)
    for step in ("n", "n", "n"):
        service.act("test:1", f"wlk:{step}")
    service.act("test:1", "wlk:go")
    hero = service._load("test:1")
    activity = dict(hero.activity)
    activity["until"] = service.clock.now()
    hero.activity = None
    notices = service._arrive(hero, activity, AmbushRng(3))
    service._save(hero)
    state = service.store.get("combat", "test:1")
    assert state and state["route"]["path"] == [[0, 6], [0, 7]] and state["route"]["walk"]
    assert any("Si le ganas" in line for line in notices)
    hero = service._load("test:1")
    state["outcome"] = "victory"
    end = service._end_combat(hero, state)
    service._save(hero)
    hero = service._load("test:1")
    assert hero.activity["kind"] == "travel" and hero.activity["to"] == [0, 6] and hero.activity["goal"] == [0, 7]
    assert hero.activity.get("walk") and any("Sigues tu camino" in line for line in end.body)
    assert not service.texts.missing


def test_fleeing_the_ambush_leaves_you_there(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.x, hero.y = 0, 4
    hero.known = sorted(set(hero.known) | {"0:4"})
    service._save(hero)
    hero = service._load("test:1")
    activity = {"kind": "travel", "to": [0, 5], "until": service.clock.now(), "dir": "n", "path": [[0, 6]], "goal": [0, 6]}
    service._arrive(hero, activity, AmbushRng(3))                 # a 📒 Lugares trip, not a walk: the same rule
    state = service.store.get("combat", "test:1")
    assert state["route"]["path"] == [[0, 6]] and not state["route"]["walk"]
    state["outcome"] = "fled"
    end = service._end_combat(hero, state)
    assert not hero.activity and (hero.x, hero.y) == (0, 5)
    assert any("se canceló" in line for line in end.body)


def test_moving_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    zone = service.act("test:1", "home")
    assert zone.actions[-2].label == "🔗 Move" and zone.actions[-1].label == "🗺️ Map"
    service.act("test:1", "wlk:n")
    view = service.act("test:1", "wlk:e")
    assert "2 steps" in "\n".join(view.body) and view.actions[-1].label == "✅ Finish"
    assert not service.texts.fallbacks.get("en")
