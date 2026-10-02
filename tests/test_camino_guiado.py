"""The guided path (D-190 confirmed, D-193 provisional): one step at a time, in the owner's order, and one-time tips.

[ES] Pruebas del 🧭 camino guiado: al crear el héroe sale "dónde estás" (el Claro, la antorcha) con las 4 rutas; después, un
solo paso a la vez y en el orden del dueño (moverte, explorar, recolectar, cazar, el mapa, volver al Claro, el campamento, el
entrenador y el héroe), cada uno con su premio chico una sola vez; el tutorial de fundar campamento solo empieza al salir del
Claro y después de moverse (D-190), y termina con el tutorial corto del campamento; los avisos salen una vez y como mucho uno
por pantalla; los héroes de antes se ponen al día sin premio (E-133); /guia y /origen (E-131); no falta ningún texto.
"""

import re

from conftest import make_hero
from engine.hero import Hero, hero_stats

ACC = "test:1"


def hero_of(service, account=ACC):
    return Hero.from_dict(service.store.get("hero", account))


def put(service, hero):
    service.store.put("hero", hero.id, hero.to_dict())


def done(service, account=ACC):
    return service.store.get("hero", account)["guide"]["done"]


def heal(service, account=ACC):
    hero = service._load(account)
    hero.hp = hero_stats(service._kit(hero), hero.level)["max_hp"]
    hero.downed = False
    service._save(hero)


def win(service, account=ACC):
    """Finish the current fight with a victory (the enemy at 1 health before each attack, the hero always healed)."""
    view = service.view(account)
    for _ in range(12):
        state = service.store.get("combat", account)
        if state is None:
            break
        state["enemy"]["hp"] = 1
        service.store.put("combat", account, state)
        heal(service, account)
        view = service.act(account, "atk")
    assert service.store.get("combat", account) is None
    return view


def settle(service, clock, seconds=3600, account=ACC):
    """Let time pass, deliver the pushes and finish any fight that came up; returns every notice seen."""
    clock.advance(seconds)
    seen = [view.notice or "" for acc, view in service.tick() if acc == account]
    if service.store.get("combat", account) is not None:
        seen.append(win(service, account).notice or "")
    heal(service, account)
    return "\n".join(seen)


def wild_direction(service):
    """A route from the Claro to a zone with prey (a biome with danger, not the lair)."""
    for direction, (x, y) in (("e", (1, 0)), ("n", (0, 1)), ("w", (-1, 0)), ("s", (0, -1))):
        zone = service._zone(x, y)
        if service.content.biomes[zone.biome]["danger"] > 0 and not service._is_lair(x, y):
            return direction
    raise AssertionError("no wild zone next to the Claro")


def basic_ids(service):
    return service._guide_basic()


def test_creation_ends_in_where_you_are_with_the_four_routes(service):
    # [ES] D-190: nombre y clase, y enseguida "dónde estás" (el Claro, la antorcha) y cómo moverte, con las 4 rutas
    view = make_hero(service)
    assert view.kind == "guide" and "Claro" in view.title
    text = "\n".join(view.body)
    assert "🔥" in text and "terreno" in text and "Cómo moverte" in text and "monstruos" in text
    assert "🧭 Ahora:" in text and "Paso 1 de" in text
    assert sorted(a.id for a in view.actions) == ["go:e", "go:n", "go:s", "go:w"]
    hero = service.store.get("hero", ACC)
    assert hero["guide"]["done"] == [] and hero["guide"]["v"] == 1
    assert service.act(ACC, "home").kind == "zone"            # never blocking: the menu goes on playing


def test_moving_text_follows_the_energy_number(service):
    # [ES] D-190 dice que moverse no gasta energía; hoy energy.per_move es 1 (D-78, E-135): el texto dice el número real
    view = make_hero(service)
    text = "\n".join(view.body)
    cost = service.content.balance["energy"]["per_move"]
    assert ("no gasta energía" in text) == (cost == 0)
    assert (f"gasta {cost} ⚡" in text) == (cost > 0)


def test_a_new_hero_walks_the_whole_path_in_order(service, clock):
    # [ES] el orden del dueño, una acción por paso; cada paso se cumple con su acción exacta y paga una sola vez
    make_hero(service)
    order = [sid for sid, _ in service._guide_steps()]
    assert order[:9] == ["move", "explore", "gather", "hunt", "map", "return", "camp", "trainer", "hero"]
    reward = service.content.balance["guide"]["reward_gold"]
    gold = hero_of(service).gold

    direction = wild_direction(service)
    service.act(ACC, f"go:{direction}")
    seen = settle(service, clock, 600)
    assert done(service) == ["move"] and "Paso 1 de" in seen and "Explorar" in seen

    view = service.act(ACC, "explore_menu")
    assert any("🧭 Ahora: explora" in line for line in view.body)
    service.act(ACC, "do:explore:1")
    seen = settle(service, clock)
    assert done(service) == ["move", "explore"] and "Recolectar" in seen

    service.act(ACC, "do:gather:1")
    settle(service, clock)
    assert done(service) == ["move", "explore", "gather"]

    assert service.act(ACC, "hunt").kind == "hunt"
    fight = service.act(ACC, "prey")
    assert fight.kind == "combat"
    end = win(service)
    assert done(service)[-1] == "hunt" and any("El mapa" in line for line in end.body)

    view = service.act(ACC, "map")
    assert done(service)[-1] == "map" and "Cómo leer el mapa" in view.notice and "👑" in view.notice

    places = service.act(ACC, "places")
    assert "goto:0:0" in [a.id for a in places.actions]
    service.act(ACC, "goto:0:0")
    settle(service, clock, 1800)
    hero = hero_of(service)
    assert (hero.x, hero.y) == (0, 0) and done(service)[-1] == "return"

    view = service.act(ACC, "claro")
    assert done(service)[-1] == "camp" and "Entrenador" in view.notice and "Dudas" in view.notice
    view = service.act(ACC, "trainer")                         # the 🧑‍🏫 screen is the camp's (D-191); the step is the button
    assert done(service)[-1] == "trainer" and "más oficios" in view.notice
    view = service.act(ACC, "hero")
    assert done(service)[-1] == "hero" and "Talentos" in view.notice and "Dudas" in view.notice
    assert done(service) == order[:9]
    assert hero_of(service).gold >= gold + 9 * reward
    assert not service.texts.missing


def test_only_one_task_at_a_time_and_buttons_out_of_order_do_nothing(service, clock):
    # [ES] nunca más de una tarea: tocar el mapa, el campamento o el héroe antes de tiempo no cumple nada
    make_hero(service)
    for action in ("map", "claro", "hero", "trainer", "explore_menu"):
        service.act(ACC, action)
    assert done(service) == []
    service.act(ACC, "do:explore:1")                           # exploring in the Claro before moving: not the "move" step
    settle(service, clock)
    assert done(service) == []
    view = service.act(ACC, "home")
    assert sum("🧭 Ahora:" in line for line in view.body) == 1
    assert service.store.get("hero", ACC)["tutorial"] == 0     # the old tutorial no longer advances (D-193)


def test_rewards_are_paid_once(service):
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = ["move", "explore", "gather", "hunt"]
    hero.x = 1                                                 # away: "back home" does not chain in right after
    service._save(hero)
    before = hero_of(service)
    service.act(ACC, "map")
    after = hero_of(service)
    cfg = service.content.balance["guide"]
    assert after.gold == before.gold + cfg["reward_gold"] and after.xp == before.xp + cfg["reward_xp"]
    service.act(ACC, "map")
    again = hero_of(service)
    assert (again.gold, again.xp) == (after.gold, after.xp) and done(service).count("map") == 1


def test_the_reward_shows_the_xp_boost(service, clock):
    # [ES] el premio dice la experiencia real, con el acelerador de 💎 (×1,5)
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = ["move", "explore", "gather", "hunt"]
    hero.x = 1
    hero.xp_boost_until = clock.now() + 3600
    service._save(hero)
    view = service.act(ACC, "map")
    gained = service._load(ACC).xp
    assert gained == int(service.content.balance["guide"]["reward_xp"] * 1.5) and f"+{gained} de experiencia" in view.notice


def test_back_home_completes_when_you_are_already_there(service):
    # [ES] si ya estás en el Claro cuando llega "volver", se da por hecho enseguida (sin pedir un viaje inútil)
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = ["move", "explore", "gather", "hunt"]
    service._save(hero)
    view = service.act(ACC, "map")
    assert done(service)[-2:] == ["map", "return"] and "El campamento" in view.notice


def test_founding_guide_starts_only_after_leaving_the_claro_and_moving(service, clock):
    # [ES] D-190: sin tutorial de fundar mientras estás en el Claro; al salir, 1 o 2 movimientos y "encontraste un buen lugar"
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = list(basic_ids(service))
    service._save(hero)
    view = service.act(ACC, "home")
    assert not any("🧭 Ahora:" in line for line in view.body)
    guide = service.act(ACC, "guide")
    assert guide.kind == "guide" and any("Cuando salgas del Claro" in line for line in guide.body)
    service.act(ACC, "go:e")
    seen = settle(service, clock, 600)
    assert "Tu propio campamento" in seen and "found_spot" not in done(service)
    assert service.store.get("hero", ACC)["guide"]["away"] == 1
    service.act(ACC, "go:e")
    seen = settle(service, clock, 600)
    hero = hero_of(service)
    assert service._zone(hero.x, hero.y).lejania >= service.content.balance["camps"]["min_lejania"]
    assert "found_spot" in done(service) and "buen lugar para tu propio campamento" in seen
    assert "Fundar tu campamento" in seen and "▫️" in seen         # what founding still needs here
    view = service.act(ACC, "home")
    assert any("🧭 Ahora: funda tu campamento" in line for line in view.body)
    assert any("Te falta" in line for line in view.body)


def test_moving_during_the_basic_path_does_not_count_for_founding(service, clock):
    make_hero(service)
    service.act(ACC, "go:e")
    settle(service, clock, 600)
    assert service.store.get("hero", ACC)["guide"]["away"] == 0


def test_founding_completes_the_last_step_with_the_camp_tutorial(service):
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = list(basic_ids(service)) + ["found_spot"]
    hero.x, hero.y = 3, 0
    hero.known = ["0:0", "3:0", "2:0", "4:0", "3:1", "3:-1"]
    hero.exploration = {"3:0": 100}
    hero.backpack = {"madera": 30, "piedra": 10}
    service._save(hero)
    gold = hero_of(service).gold
    assert service.act(ACC, "found").kind == "name_camp"
    view = service.text(ACC, "Roca Alta")
    assert service.store.get("camp", "3:0")["name"] == "Roca Alta"
    assert "found" in done(service) and "botón de mejora" in view.notice and "más oficios" in view.notice
    assert hero_of(service).gold == gold + service.content.balance["guide"]["reward_gold"]
    assert service._guide_current(service._load(ACC)) is None
    assert service.act(ACC, "guide").body[0].startswith("✅")


def test_joining_a_camp_skips_the_search_and_completes_founding(service):
    # [ES] si entras al campamento de otro, no hace falta buscar lugar: el paso de fundar se da por hecho
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = list(basic_ids(service))
    hero.camp = "5:5"
    service._save(hero)
    view = service.act(ACC, "home")
    assert "found_spot" in done(service) and "found" in done(service) and "botón de mejora" in (view.notice or "")


def test_tips_show_once_and_one_per_screen(service):
    # [ES] D-190: los avisos llegan de a uno y una sola vez (energía baja y mochila llena a la vez: uno por pantalla)
    make_hero(service)
    hero = service._load(ACC)
    hero.energy = 3
    hero.backpack["madera"] = service._bag_cap(hero) + 5
    service._save(hero)
    first = [line for line in service.act(ACC, "home").body if line.startswith("💡")]
    second = [line for line in service.act(ACC, "home").body if line.startswith("💡")]
    third = [line for line in service.act(ACC, "home").body if line.startswith("💡")]
    assert len(first) == 1 and len(second) == 1 and first != second and third == []
    seen = service.store.get("hero", ACC)["guide"]["tips"]
    assert "energy_low" in seen and "bag_full" in seen


def test_first_fight_tip_shows_in_the_combat_screen_once(service):
    make_hero(service)
    hero = service._load(ACC)
    x, y = {"e": (1, 0), "n": (0, 1), "w": (-1, 0), "s": (0, -1)}[wild_direction(service)]
    hero.x, hero.y = x, y
    service._save(hero)
    fight = service.act(ACC, "prey")
    assert fight.kind == "combat" and any("Tu primera pelea" in line for line in fight.body)
    heal(service)
    nxt = service.act(ACC, "atk")
    assert not any("Tu primera pelea" in line for line in nxt.body)


def test_unlocked_tips_wait_for_their_step(service):
    # [ES] el aviso de ⚙️ Opciones espera al paso 🏹 Cazar; el del 🎭 origen, al final del camino básico (E-131)
    make_hero(service)
    hero = service._load(ACC)
    hero.kills = 10
    service._save(hero)
    assert not any("Peleas automáticas" in line for line in service.act(ACC, "home").body)
    hero = service._load(ACC)
    hero.guide["done"] = list(basic_ids(service))
    service._save(hero)
    lines = service.act(ACC, "home").body + service.act(ACC, "home").body
    assert any("Peleas automáticas" in line for line in lines) and any("/origen" in line for line in lines)
    assert service.text(ACC, "/origen").kind == "origin"


def test_old_heroes_are_brought_up_to_date_without_rewards(service):
    # [ES] E-133: con el tutorial viejo terminado o nivel 5+, el camino básico queda hecho sin premio; los demás empiezan en
    # el primer paso que no hicieron a la vista; los avisos de lo que ya conocen quedan vistos
    steps = len(service.content.balance["tutorial"]["steps"])
    service.store.put("hero", "old:1", {"id": "old:1", "name": "Viejo", "class_id": "guerrero", "tutorial": steps,
                                         "level": 3, "kills": 4, "gold": 100})
    service.store.put("hero", "old:2", {"id": "old:2", "name": "Alto", "class_id": "guerrero", "tutorial": 1, "level": 5,
                                         "gold": 100})
    service.store.put("hero", "old:3", {"id": "old:3", "name": "Afuera", "class_id": "guerrero", "tutorial": 2, "level": 1,
                                         "x": 1, "y": 0, "known": ["0:0", "1:0"], "exploration": {"1:0": 40}, "gold": 100})
    service.store.put("hero", "old:4", {"id": "old:4", "name": "Quieto", "class_id": "guerrero", "level": 1, "gold": 100})
    basic = basic_ids(service)
    for account in ("old:1", "old:2", "old:3", "old:4"):
        service.view(account)
    assert done(service, "old:1") == basic and done(service, "old:2") == basic
    assert done(service, "old:3") == ["move", "explore", "gather"]
    assert done(service, "old:4") == []
    for account in ("old:1", "old:2", "old:3", "old:4"):
        hero = service.store.get("hero", account)
        assert hero["gold"] == 100 and hero["guide"]["v"] == 1
    assert service.store.get("hero", "old:1")["tutorial"] == steps         # stored data is kept (D-64)
    assert "fight" in service.store.get("hero", "old:1")["guide"]["tips"]
    assert "level_up" in service.store.get("hero", "old:1")["guide"]["tips"]


def test_old_tutorial_finished_means_basic_path_done(service):
    # [ES] quien tiene el tutorial viejo al final (también si se pone después) tiene el camino básico hecho
    make_hero(service)
    hero = service._load(ACC)
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    service._save(hero)
    service.view(ACC)
    assert done(service) == basic_ids(service)


def test_guide_command_shows_the_current_step_with_its_button(service):
    make_hero(service)
    hero = service._load(ACC)
    hero.guide["done"] = ["move", "explore", "gather", "hunt"]
    service._save(hero)
    view = service.text(ACC, "/guia")
    assert view.kind == "guide" and [a.id for a in view.actions] == ["map"] and len(view.actions) <= 4
    assert any("Paso 5 de" in line for line in view.body)


def test_every_step_and_tip_has_its_texts(service, content):
    hero = make_hero(service) and service._load(ACC)
    values = service._guide_values(hero)
    values["needs"] = "x"
    for sid, step in service._guide_steps():
        for part in ("name", "task", "intro"):
            assert service.texts.has(f"guide.step.{sid}.{part}"), (sid, part)
            text = service.texts.t(f"guide.step.{sid}.{part}", **values)
            assert not re.search(r"\{\w+\}", text), (sid, part, text)
        if step.get("go") and step["go"] != "routes":
            assert service.texts.has(f"guide.go.{step['go']}"), sid
    for tid, _ in service._guide_tips():
        for part in ("name", "text"):
            assert service.texts.has(f"guide.tip.{tid}.{part}"), (tid, part)
            assert not re.search(r"\{\w+\}", service.texts.t(f"guide.tip.{tid}.{part}", **values)), tid
    assert not service.texts.missing


def test_step_and_tip_ids_are_unique_and_known(content):
    # [ES] IDs estables (C-18, C-29): pasos y avisos con su condición conocida
    steps = content.guide["steps"]
    tips = content.guide["tips"]
    assert len(set(steps) | set(tips)) == len(steps) + len(tips)
    events = {"arrive", "explore", "gather", "fight", "camp"}
    for sid, step in steps.items():
        rule = step["done"]
        assert rule.get("event") in events or rule.get("action"), sid
    whens = {"in_combat", "downed", "level_up", "energy_low", "bag_full", "cave", "ecamp", "node", "rank_up", "raid", "kills",
             "path_done"}
    assert all(tip["when"] in whens for tip in tips.values())
    assert 8 <= len(tips) <= 12
