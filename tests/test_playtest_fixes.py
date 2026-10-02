"""Bugs found playing the game as a new player (playtest of 0.9.2), one test each.

[ES] Fallos que salieron al jugar como un jugador nuevo (prueba de juego de la 0.9.2). Cada prueba
cuida que uno no vuelva: remedios gastados con la vida llena, posada cobrada sin necesidad, recolectar
sin espacio, el campamento que se fundaba solo con un texto suelto, la consola sin menú, etc.
"""

from conftest import make_hero
from engine.hero import hero_stats


def _max_hp(service, account="test:1"):
    hero = service._load(account)
    return hero_stats(service._kit(hero), hero.level)["max_hp"]


def test_a_remedy_is_not_wasted_with_full_health(service):
    make_hero(service)
    before = service.store.get("hero", "test:1")
    view = service.act("test:1", "use:pocion_vida")
    after = service.store.get("hero", "test:1")
    assert view.kind == "potions" and "llena" in view.notice
    assert after["belt"] == before["belt"] and after["backpack"] == before["backpack"]


def test_drinking_a_potion_ends_the_slow_recovery(service, clock):
    # D-83: falling means a slow recovery "until full health, a potion or the inn".
    make_hero(service)
    hero = service._load("test:1")
    hero.hp, hero.downed, hero.last_regen_at = 1, True, clock.now()
    service._save(hero)
    service.act("test:1", "use:venda")                      # a bandage heals, but is not a potion
    assert service._load("test:1").downed
    service.act("test:1", "use:pocion_vida")
    hero = service._load("test:1")
    assert not hero.downed and hero.hp < _max_hp(service)
    assert "Malherido" not in "\n".join(service.act("test:1", "hero").body)


def test_the_inn_does_not_charge_with_full_health(service):
    make_hero(service)
    gold = service.store.get("hero", "test:1")["gold"]
    view = service.act("test:1", "inn")
    hero = service.store.get("hero", "test:1")
    assert view.kind == "claro" and view.notice and hero["gold"] == gold and hero["activity"] is None


def test_gathering_with_a_full_backpack_spends_nothing(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.backpack["piedra"] = service._bag_cap() - service._bag_used(hero)
    service._save(hero)
    energy = hero.energy
    for action in ("gather", "do:gather:5"):
        view = service.act("test:1", action)
        assert view.kind == "explore_menu" and "mochila" in view.notice.lower()
    hero = service._load("test:1")
    assert hero.energy == energy and hero.activity is None


def test_gathering_a_depleted_zone_spends_nothing(service, clock):
    make_hero(service)
    service.store.put("stock", "0:0", {"levels": {"madera": 0.0, "fibra": 0.0}, "at": clock.now()})
    energy = service._load("test:1").energy
    view = service.act("test:1", "do:gather:5")
    assert view.kind == "explore_menu" and "agotada" in view.notice
    assert service._load("test:1").energy == energy


def test_hero_sheet_counts_the_backpack_like_the_space_line(service):
    make_hero(service)
    hero = service._load("test:1")
    line = next(x for x in service.act("test:1", "hero").body if x.startswith("🎒"))
    assert f"{service._bag_used(hero)}/{service._bag_cap()}" in line      # the belt does not take backpack space


def _camp_ready(service, account="test:1"):
    hero = service._load(account)
    hero.x, hero.y = 3, 0
    hero.known += ["3:0", "2:0", "4:0", "3:1", "3:-1"]
    hero.exploration["3:0"] = 100
    hero.backpack.update({"madera": 40, "piedra": 30, "fibra": 20})
    service._save(hero)


def test_leaving_the_camp_name_prompt_cancels_it(service):
    make_hero(service)
    _camp_ready(service)
    assert service.act("test:1", "found").expects_text
    service.act("test:1", "hero")                           # the player goes elsewhere...
    service.text("test:1", "hola")                          # ...and later writes anything
    assert service.store.get("camp", "3:0") is None
    assert service._load("test:1").backpack["madera"] == 40


def test_camp_grow_pages_say_zones_not_gear(service):
    make_hero(service)
    _camp_ready(service)
    service.act("test:1", "found")
    service.text("test:1", "Roble Alto")
    view = service.act("test:1", "grow")
    more = [a for a in view.actions if a.id.startswith("grow:")]
    assert more and "zonas" in more[0].label and "piezas" not in more[0].label


def test_menu_buttons_in_combat_say_why_nothing_happens(service):
    from engine.core import Rng
    make_hero(service)
    hero = service._load("test:1")
    service._start_combat(hero, service._zone(1, 0), Rng(5), "encounter.found")
    service._save(hero)
    view = service.act("test:1", "hero")
    assert view.kind == "combat" and "combate" in view.notice
    assert service.act("test:1", "back").notice is None      # closing the belt is not an error


def test_xp_shown_includes_the_boost(service, clock):
    # D-193: the guided path's step reward (it replaced the old tutorial's) shows the boosted experience
    make_hero(service)
    hero = service._load("test:1")
    hero.guide["done"] = ["move", "explore", "gather", "hunt"]
    hero.x = 1                                       # away from the Claro: "back home" does not chain in
    hero.xp_boost_until = clock.now() + 3600
    service._save(hero)
    view = service.act("test:1", "map")
    gained = service._load("test:1").xp
    reward = service.content.balance["guide"]["reward_xp"]
    assert gained == int(reward * 1.5) and f"+{gained} de experiencia" in view.notice


def test_console_shows_the_menu_and_shortcuts(service, monkeypatch, capsys):
    from adapters.cli import play
    make_hero(service)
    view = service.view("test:1")
    ids = [a.id for a in play.options(view, service)]
    assert "explore_menu" in ids and "hero" in ids               # from the zone you can reach every screen
    assert play.options(service.view("test:9"), service) == []    # no menu while creating the hero
    assert service.commands()["/doble"] == "dual"                 # the double spec is only linked as /doble
    play.draw(view, service)
    assert "🧭 Explorar" in capsys.readouterr().out
