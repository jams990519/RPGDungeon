"""Full backpack (D-90) and the 🪎 chest (D-92), both provisional.

[ES] Pruebas de la mochila llena y del cofre. Lo que encuentras nunca se pierde (hallazgos de explorar y botín entran
aunque la mochila pase de 60), pero con la mochila llena no se recolecta ni se compra hasta vender o usar cosas.
El cofre se arma solo en el Claro con 10 bolsas, madera y metal, y paga el crecimiento de los campamentos desde el
nivel 6 (1 cofre de 6 a 7, 2 de 7 a 8, 3 de 8 a 9). También: la ficha del héroe muestra 🪎, los héroes viejos
cargan con 0 cofres, la billetera del Claro tiene 4 botones y la etapa del campamento se lee bien.
"""

from conftest import make_hero
from engine.combat import make_combat
from engine.hero import Hero
from test_camps import found_at, place


class StubRng:
    """Always the same roll: an exploration in the Claro that finds the first item of its list."""

    def random(self):
        return 0.5

    def uniform(self, low, high):
        return low

    def pick_weighted(self, options, weights):
        return options[0]

    def chance(self, probability):
        return False


def fill(service, account="test:1", extra=0, **more):
    """Leave the backpack at its space (plus `extra`) with stone, and whatever else is asked."""
    hero = service._load(account)
    hero.backpack = {"piedra": service._bag_cap() + extra, **more}
    service._save(hero)
    return hero


def test_exploration_finds_go_in_beyond_the_space(service):
    make_hero(service)
    hero = fill(service)
    activity = {"log": [], "got": {}}
    assert service._explore_step(hero, service._zone(0, 0), StubRng(), activity) is None
    assert hero.backpack["hierba_curativa"] == 1 and activity["got"] == {"hierba_curativa": 1}
    assert service._bag_used(hero) == service._bag_cap() + 1        # never lost, even over the space


def test_combat_loot_goes_in_beyond_the_space(service):
    make_hero(service)
    edef = service.content.enemies["lobo_ceniciento"]
    for seed in range(60):
        hero = fill(service)
        state = make_combat("lobo_ceniciento", edef, edef["level_min"], service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        if hero.backpack.get("carne"):
            break
    assert hero.backpack["carne"] >= 1 and service._bag_used(hero) > service._bag_cap()


def test_gathering_is_refused_with_a_full_or_overfull_backpack(service):
    make_hero(service)
    for extra in (0, 3):
        fill(service, extra=extra)
        energy = service._load("test:1").energy
        cap = service._bag_cap()
        for action in ("gather", "do:gather:5"):
            view = service.act("test:1", action)
            assert view.kind == "explore_menu"
            assert view.notice == f"🎒 Mochila llena ({cap + extra}/{cap}): vende o usa cosas para volver a recolectar o comprar."
        hero = service._load("test:1")
        assert hero.energy == energy and hero.activity is None      # nothing spent for nothing


def test_buying_is_refused_when_full_and_selling_frees_space(service):
    make_hero(service)
    hero = fill(service, madera=2)
    hero.gold = 100
    service._save(hero)
    view = service.act("test:1", "shop")
    assert any("Mochila llena" in line for line in view.body) and len(view.actions) <= 4
    view = service.act("test:1", "buy:pocion_vida")
    hero = service._load("test:1")
    assert "Mochila llena (62/60)" in view.notice
    assert hero.gold == 100 and hero.backpack == {"piedra": service._bag_cap(), "madera": 2}   # never charged
    service.act("test:1", "sell:all")
    hero = service._load("test:1")
    assert hero.backpack == {} and hero.gold > 100
    gold = hero.gold
    view = service.act("test:1", "buy:pocion_vida")
    hero = service._load("test:1")
    assert "Mochila llena" not in (view.notice or "") and hero.gold == gold - service.content.items["pocion_vida"]["price"]
    assert not any("Mochila llena" in line for line in view.body)


def test_bag_view_shows_the_space_or_the_full_line(service):
    make_hero(service)
    hero = service._load("test:1")
    view = service.act("test:1", "bag")
    assert f"🎒 Espacio en la mochila: {service._bag_used(hero)}/{service._bag_cap()}" in view.body
    fill(service, extra=3)
    view = service.act("test:1", "bag")
    assert any(line.startswith("🎒 Mochila llena (63/60)") for line in view.body) and len(view.actions) <= 4
    assert "🎒 Mochila: 63/60 — /inv" in service.act("test:1", "hero").body   # the hero sheet counts the same


def test_chest_is_assembled_only_in_the_claro(service):
    make_hero(service)
    place(service, "test:1", 3, 0, bags=10, backpack={"madera": 10, "pieza_metal": 5})
    view = service.act("test:1", "wallet")
    assert not any(a.id == "chest" for a in view.actions)
    assert "💰 Las bolsas se cosen y los 🪎 cofres se arman en el Claro, o en el 🧵 Taller de tu campamento." in view.body   # D-101
    view = service.act("test:1", "chest")
    hero = service._load("test:1")
    assert view.notice and hero.chests == 0 and hero.bags == 10 and hero.backpack["madera"] == 10

    place(service, "test:1", 0, 0, bags=9, backpack={"madera": 12, "pieza_metal": 5})
    view = service.act("test:1", "wallet")
    assert [a.id for a in view.actions] == ["sew", "chest", "gems", "bag"]      # 4 buttons at most (D-75)
    assert "🪎 Cofres: 0" in view.body
    view = service.act("test:1", "chest")
    hero = service._load("test:1")
    assert "necesitas 10 💰 bolsas (tienes 9)" in view.notice and hero.chests == 0 and hero.bags == 9
    place(service, "test:1", 0, 0, bags=11)
    view = service.act("test:1", "chest")
    hero = service._load("test:1")
    assert hero.chests == 1 and hero.bags == 1
    assert hero.backpack == {"madera": 2}                                   # 10 wood and 5 metal used
    assert "🪎 Cofres: 1" in view.body and "1" in view.notice
    assert service.act("test:1", "chest").notice.startswith("Para armar un cofre")   # nothing left: refused


def _camp_at_level(service, level, chests=0):
    make_hero(service)
    found_at(service, "test:1", 6, 0)
    camp = service.store.get("camp", "6:0")
    camp["level"] = level
    camp["zones"] = [[6 + i, 0] for i in range(level)]
    service.store.put("camp", "6:0", camp)
    place(service, "test:1", 6, 0, chests=chests, backpack={"madera": 500, "piedra": 500, "fibra": 500})


def test_chest_cost_by_level(service):
    assert [service._grow_chests(level) for level in (1, 5, 6, 7, 8, 9)] == [0, 0, 1, 2, 3, 4]
    assert "🪎" not in service._grow_cost_text(5)
    assert service._grow_cost_text(6).endswith("🪎 Cofre ×1")


def test_growing_from_level_five_needs_no_chest(service):
    _camp_at_level(service, 5)
    view = service.act("test:1", "claim:6:1")
    assert service.store.get("camp", "6:0")["level"] == 6 and "creció" in view.notice


def test_growing_from_level_six_needs_one_chest(service):
    _camp_at_level(service, 6)
    view = service.act("test:1", "grow")
    assert view.kind == "camp_grow" and "🪎 Cofre ×1" in view.body[0] and len(view.actions) <= 4
    assert "🪎 Tienes 0 cofres. Se arman en el Claro, en 💰 Monedas (/monedas)." in view.body
    view = service.act("test:1", "claim:6:1")
    hero = service._load("test:1")
    assert service.store.get("camp", "6:0")["level"] == 6                  # refused: nothing paid
    assert "🪎 Cofre ×1" in view.notice and "tienes 0 de 1" in view.notice
    assert hero.backpack["madera"] == 500
    place(service, "test:1", 6, 0, chests=1)
    view = service.act("test:1", "claim:6:1")
    hero = service._load("test:1")
    assert service.store.get("camp", "6:0")["level"] == 7 and hero.chests == 0
    assert hero.backpack["madera"] == 500 - 15 * 6 and len(view.actions) <= 4


def test_growing_from_level_seven_needs_two_chests(service):
    _camp_at_level(service, 7, chests=1)
    view = service.act("test:1", "claim:6:1")
    assert service.store.get("camp", "6:0")["level"] == 7 and "tienes 1 de 2" in view.notice
    assert service._load("test:1").chests == 1
    place(service, "test:1", 6, 0, chests=3)
    service.act("test:1", "claim:6:1")
    assert service.store.get("camp", "6:0")["level"] == 8 and service._load("test:1").chests == 1


def test_empty_pantry_still_blocks_growth_before_chests(service):
    _camp_at_level(service, 6, chests=5)
    service.store.put("pantry", "6:0", {"rations": 0.0, "at": service.clock.now()})
    view = service.act("test:1", "claim:6:1")
    assert "despensa" in view.notice.lower() and service._load("test:1").chests == 5
    assert service.store.get("camp", "6:0")["level"] == 6


def test_hero_card_shows_chests_and_old_heroes_load(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("chests", None)                                         # a hero saved before the patch
    service.store.put("hero", "test:1", data)
    assert Hero.from_dict(data).chests == 0
    body = service.act("test:1", "hero").body
    assert any("💰 0" in line and "🪎 0" in line and "💎 0" in line for line in body)
    place(service, "test:1", 0, 0, chests=2)
    assert any("🪎 2" in line for line in service.act("test:1", "hero").body)


def test_camp_stage_line_reads_well(service):
    make_hero(service)
    found_at(service, "test:1", 6, 0)
    body = service.act("test:1", "claro").body
    assert "🏰 Etapa: campamento. Al crecer pasa a aldea, pueblo, ciudad y castillo." in body
    assert not any("Es un" in line for line in body)


def test_the_backpack_explains_its_buttons_and_does_not_list_everything(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.backpack.update({"madera": 7, "fibra": 3, "carne": 2})
    service._save(hero)
    view = service.act("test:1", "bag")
    body = "\n".join(view.body)
    assert [a.id for a in view.actions] == ["gear", "potions", "wallet", "resources"]
    for word in ("🛡️ Equipo", "🧪 Pociones", "💰 Monedas", "📦 Recursos"):
        assert word in body
    assert "Madera" not in body                                  # the hub never lists what you carry


def test_resources_screen_lists_materials_and_food_by_pages(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.backpack.update({"madera": 7, "fibra": 3, "carne": 2, "pocion_vida": 1, "espada_2": 1})
    service._save(hero)
    view = service.act("test:1", "resources")
    body = "\n".join(view.body)
    assert view.kind == "resources" and [a.id for a in view.actions] == ["bag"]
    assert "Madera ×7" in body and "agrandar campamentos" in body and "2 raciones" in body
    assert "Poción" not in body and "Espada" not in body           # potions and gear have their own buttons
    assert not service.texts.missing
    per = service.content.balance["resources"]["per_page"]
    many = [i for i, it in service.content.items.items() if it.get("kind") in ("material", "food")]
    hero = service._load("test:1")
    hero.backpack = {i: 1 for i in many}
    service._save(hero)
    first = service.act("test:1", "resources")
    if len(many) > per:
        assert [a.id for a in first.actions] == ["res:1", "bag"]
        second = service.act("test:1", "res:1")
        assert second.kind == "resources" and len(second.actions) <= 4
