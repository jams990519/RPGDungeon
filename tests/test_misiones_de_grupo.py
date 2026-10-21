"""The camp's group missions (D-136, confirmed; how it was applied: D-332, provisional; 0.56): one shared goal per level-up.

[ES] Pruebas de las 🎯 misiones de grupo (el dueño: "para abrir cada nivel del campamento el grupo cumple misiones juntos:
farmear, recolectar, llenar la despensa; al terminarlas se abren el siguiente rango de misiones, el crecimiento y los
materiales"):
- al fundar empieza la 1.ª misión (vencer 20 monstruos para subir a nivel 2) y el fundador lee cuál es;
- ⏫ Siguiente nivel la muestra como una línea más ("🤝 Entre todos:") y traba la subida hasta cumplirla, aunque lo demás
  esté ✅; cumplida, ⏫ Subir; al subir empieza la siguiente;
- lo de cada miembro se suma, en cualquier lugar, y queda lo de cada uno; solo cuentan los miembros;
- al cumplirla, el 💰 fondo recibe un premio chico y a cada otro miembro le llega el aviso en su idioma (_push_each);
- los campamentos de antes de la 0.56 no quedan trabados: la subida en la que estaban no la pide; la siguiente sí (D-64);
- la meta crece poco con los miembros activos y queda fija al empezar;
- recolectar cuenta solo el recurso pedido, la despensa cuenta raciones y las peleas de oleada cuentan con 🛡️ Defender;
- 📜 Qué pide cada nivel y el 📜 Tablón la dicen; se lee en los dos idiomas.
Archivo: tests/test_misiones_de_grupo.py · Módulo: M9 Frontera y Fundación (con M10 Misiones) · Prueba:
engine/service/group_missions.py y sus ganchos en game.py (_create_camp, _lvlup_rows, _lvlup_view, _lvlup_all_view,
_level_up, _end_combat) y story.py (_story_event, _camp_task_lines)
"""

from conftest import make_hero, pass_group_mission
from engine.combat import make_combat
from test_camps import found_at, old_camp_at, place
from test_guilds import join, set_level
from test_guilds import win as quick_win
from test_idiomas import english_hero
from test_raids import win as raid_win

KEY = "6:0"
DAY = 24 * 3600


def ids(view):
    return [a.id for a in view.actions]


def camp(service):
    return service.store.get("camp", KEY)


def mission(service):
    return service.store.get("group_mission", KEY)


def build(service, *uids):
    data = service._upgrades(KEY)
    for uid in uids:
        data["built"][uid] = 0.0
    service.store.put("upgrades", KEY, data)


def new_camp(service, *names, level=1):
    """A camp at 6:0 founded by Lyra (test:1) after 0.56, of `level`: its mission starts with Lyra alone (goal of 1 active),
    then the other members (test:2…) join and stand at its center."""
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, level)
    service._gm_start(KEY, camp(service), service._load("test:1"))
    for n, name in enumerate(names, 2):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
        place(service, f"test:{n}", 6, 0)
    service.tick()


def everything_but_the_mission(service):
    """Build the works of the next level and give its materials (Lyra carries plenty): only the mission is left."""
    level = camp(service)["level"]
    build(service, *service._lvlup_works(level + 1))
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999})
    return service.act("test:1", "lvlgive")


def pushes(service, account, title=None):
    return [v for acc, v in service.tick() if acc == account and (title is None or v.title == title)]


def test_a_founded_camp_starts_its_first_mission(service):
    make_hero(service, "test:1", "Lyra")
    view = found_at(service, "test:1", 6, 0)
    assert "🎯 Nueva misión de grupo para subir a nivel 2: vencer 20 monstruos, entre todos los miembros." in view.notice
    record = mission(service)
    assert (record["to"], record["id"], record["n"], record["p"]) == (2, "gm_caza_2", 20, 0)
    body = service.act("test:1", "lvlup").body
    assert body[body.index("🤝 Entre todos:") + 1] == "▫️ 🎯 Misión de grupo: vencer 20 monstruos — 0 de 20 (faltan 20)"
    assert any(line.startswith("🎯 La misión de grupo suma lo que hace cada miembro") and "🪵 Madera ×6" in line for line in body)


def test_the_mission_blocks_the_level_until_it_is_done_and_the_next_one_starts(service):
    new_camp(service, "Bram")
    view = everything_but_the_mission(service)
    assert camp(service)["level"] == 1                                # the last material did not level it up
    assert "▫️ 🎯 Misión de grupo: vencer 20 monstruos — 0 de 20 (faltan 20)" in view.body
    assert ids(view) == ["improve"] and all(line.startswith("✅") for line in view.body if line.startswith(("✅", "▫️")) and "Misión" not in line)
    assert service.act("test:1", "lvlgo").notice == "Todavía falta algo de la lista." and camp(service)["level"] == 1
    for seed in range(19):
        quick_win(service, "test:2" if seed % 2 else "test:1", seed=seed)
    assert mission(service)["p"] == 19 and camp(service)["level"] == 1
    hero = service._load("test:1")
    edef = service.content.enemies["lobo_ceniciento"]
    state = make_combat("lobo_ceniciento", edef, edef["level_min"], service._kit(hero), 99)
    state["outcome"] = "victory"
    end = service._end_combat(hero, state)                            # the 20th win closes it
    service._save(hero)
    text = "\n".join(end.body)
    assert "🎯 ¡Misión de grupo cumplida en Roca Alta: vencer 20 monstruos! Tú pusiste 11 de 20." in text
    assert "⏫ Ya está toda la lista: cualquier miembro toca ⏫ Subir a nivel 2" in text
    view = service.act("test:2", "lvlup")
    assert "✅ 🎯 Misión de grupo: vencer 20 monstruos — cumplida" in view.body and ids(view) == ["lvlgo", "improve"]
    assert camp(service)["level"] == 1                                # it never levels up by itself
    view = service.act("test:2", "lvlgo")                             # Bram, a common member
    assert camp(service)["level"] == 2
    record = mission(service)
    assert record["to"] == 3 and record["id"] == "gm_madera_3" and record["p"] == 0
    assert record["n"] == 69                                          # 60 × (1 + 0.15 × 1): Lyra and Bram played this week
    assert "🎯 Nueva misión de grupo para subir a nivel 3: juntar 69 🪵 Madera, entre todos los miembros." in view.notice
    told = pushes(service, "test:1", "⏫ Tu campamento subió de nivel")
    assert told and "🎯 Nueva misión de grupo para subir a nivel 3" in told[0].body[-1]


def test_progress_is_summed_across_members_and_each_share_is_kept(service):
    new_camp(service, "Bram", "Cora")
    place(service, "test:3", 12, -3)                                  # far away: it counts wherever you are
    quick_win(service, "test:1", seed=1)
    for seed in range(3):
        quick_win(service, "test:2", seed=seed)
    quick_win(service, "test:3", seed=7)
    record = mission(service)
    assert record["p"] == 5 and record["by"] == {"test:1": 1, "test:2": 3, "test:3": 1}
    board = service.act("test:2", "board").body
    assert "▫️ 🎯 Misión de grupo (para subir a nivel 2): vencer 20 monstruos — 5 de 20 · tú: 3" in board
    body = service.act("test:1", "lvlup").body
    assert "▫️ 🎯 Misión de grupo: vencer 20 monstruos — 5 de 20 (faltan 15)" in body
    assert any("Tú llevas 1." in line for line in body)
    make_hero(service, "test:9", "Dax")                               # not a member: does not count
    place(service, "test:9", 6, 0)
    quick_win(service, "test:9", seed=3)
    assert mission(service)["p"] == 5


def test_completion_pays_the_fund_once_and_tells_every_other_member_in_their_language(service):
    new_camp(service, "Bram")
    english_hero(service, "test:3", "Ann")
    join(service, "test:3")
    place(service, "test:3", 6, 0)
    pushes(service, "test:2")
    fund_before = dict(service._upgrades(KEY)["fund"])
    record = mission(service)
    record["p"] = 19
    record["by"] = {"test:1": 10, "test:2": 6, "test:3": 3}
    service.store.put("group_mission", KEY, record)
    with service._speaking("test:2"):                                 # Bram closes it, in his language
        lines = service._story_event(service._load("test:2"), "win", enemy="lobo_ceniciento", biome="bosque", level=1)
    assert "🎯 ¡Misión de grupo cumplida en Roca Alta: vencer 20 monstruos! Tú pusiste 7 de 20. El 💰 fondo del campamento recibió 🪵 Madera ×6 · 🪨 Piedra ×4 · 🧵 Fibra ×2." in lines
    fund = dict(service._upgrades(KEY)["fund"])
    assert {k: fund.get(k, 0) - fund_before.get(k, 0) for k in ("madera", "piedra", "fibra")} == {"madera": 6, "piedra": 4, "fibra": 2}
    out = service.tick()
    lyra = [v for acc, v in out if acc == "test:1" and v.title == "🎯 Misión de grupo cumplida"]
    ann = [v for acc, v in out if acc == "test:3" and v.title == "🎯 Group mission done"]
    assert lyra and lyra[0].body[0] == ("🎯 Bram cerró la misión de grupo de Roca Alta: vencer 20 monstruos. Tú pusiste 10 de 20. "
                                        "El 💰 fondo recibió 🪵 Madera ×6 · 🪨 Piedra ×4 · 🧵 Fibra ×2.")
    assert ann and ann[0].body[0] == ("🎯 Bram closed Roca Alta's group mission: defeat 20 monsters. You put in 3 of 20. "
                                      "The 💰 fund got 🪵 Wood ×6 · 🪨 Stone ×4 · 🧵 Fiber ×2.")
    assert not [v for acc, v in out if acc == "test:2" and "🎯" in v.title]     # who closed it reads it on their screen
    service._story_event(service._load("test:1"), "win", enemy="lobo_ceniciento", biome="bosque", level=1)
    assert mission(service)["p"] == 20 and service._upgrades(KEY)["fund"] == fund     # paid once: nothing more counts


def test_existing_camps_are_not_blocked_retroactively(service):
    # [ES] D-332: un campamento de antes de la 0.56 (sin registro) no necesita la misión de la subida en la que estaba, aunque
    # ya tuviera toda la lista ✅ el día del parche; al subir, la siguiente sí la pide (D-64: nadie pierde nada)
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, 2)
    assert mission(service) is None
    build(service, *service._lvlup_works(3))
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999})
    view = service.act("test:1", "lvlup")
    waived = "✅ 🎯 Misión de grupo: esta subida no la pide (tu campamento ya iba en camino cuando llegaron las misiones); la primera llega al subir de nivel"
    assert waived in view.body
    assert "✅ 🎯 Misión de grupo: tu campamento no la necesita para subir a nivel 3; la primera llega al subir." in service.act("test:1", "board").body
    view = service.act("test:1", "lvlgive")                          # the last material levels it up, as before 0.56
    assert camp(service)["level"] == 3 and mission(service)["to"] == 4 and mission(service)["id"] == "gm_despensa_4"
    assert "🎯 Nueva misión de grupo para subir a nivel 4: llevar 20 raciones a la despensa" in view.notice
    service.store.put("pantry", KEY, {"rations": 30.0, "at": service.clock.now()})
    build(service, *service._lvlup_works(4))
    view = service.act("test:1", "lvlgive")
    assert camp(service)["level"] == 3 and "▫️ 🎯 Misión de grupo: llevar 20 raciones a la despensa — 0 de 20 (faltan 20)" in view.body
    # a record of another level (only possible when the level moved outside ⏫) does not block either
    record = mission(service)
    service.store.put("group_mission", KEY, dict(record, to=2))
    assert ids(service.act("test:1", "lvlup")) == ["lvlgo", "improve"]
    service.store.put("group_mission", KEY, record)
    assert ids(service.act("test:1", "lvlup")) == ["improve"]
    pass_group_mission(service, KEY)                                  # what old tests that climb several levels use
    assert ids(service.act("test:1", "lvlup")) == ["lvlgo", "improve"]
    # a castle has no next level and no mission (and keeps what it has)
    set_level(service, 9)
    assert not [line for line in service.act("test:1", "improve").body if "Misión" in line]


def test_the_goal_scales_gently_with_active_members_and_stays_fixed(service):
    assert [service._gm_target("gm_caza_2", a) for a in (1, 2, 5, 10, 25, 40, 100)] == [20, 23, 32, 47, 92, 137, 137]
    assert service._gm_target("gm_oleadas_5", 10) == 8 and service._gm_target("gm_caza_9", 40) == 548
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    for n, name in enumerate(("Bram", "Cora", "Dax", "Eda"), 2):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
        service.act(f"test:{n}", "hero")                              # played now (Hero.seen_at)
    hero = service._load("test:5")                                    # Eda has not played for 8 days: not active
    hero.seen_at = service.clock.now() - 8 * DAY
    service._save(hero)
    service._gm_start(KEY, camp(service), service._load("test:1"))
    assert (mission(service)["active"], mission(service)["n"]) == (4, 29)     # 20 × (1 + 0.15 × 3), rounded up
    make_hero(service, "test:6", "Fen")                               # someone new joins: the goal stays
    join(service, "test:6")
    service.act("test:6", "hero")
    assert mission(service)["n"] == 29
    assert "vencer 29 monstruos — 0 de 29" in "\n".join(service.act("test:1", "lvlup").body)
    every = service.act("test:1", "lvlall").body                      # the next ones: with today's actives (5)
    assert any(line.startswith("⏫ Nivel 3 (aldea)") and line.endswith("· 🎯 juntar 96 🪵 Madera") for line in every), every


def test_gather_feed_and_defend_count_only_what_they_ask(service):
    new_camp(service, "Bram", level=2)                                # to 3: gather 🪵 madera
    hero = service._load("test:2")
    service._story_event(hero, "gather", items={"madera": 5, "piedra": 3})
    service._story_event(hero, "win", enemy="lobo_ceniciento", biome="bosque", level=1)
    assert mission(service)["p"] == 5
    # to 4: 🌾 the pantry (real 🌾 Aportar comida)
    set_level(service, 3)
    service._gm_start(KEY, camp(service), service._load("test:1"))
    service.act("test:1", "claro")                                    # the pantry starts
    place(service, "test:1", 6, 0, backpack={"carne": 5})
    service.act("test:1", "campfeed")
    assert mission(service)["id"] == "gm_despensa_4" and mission(service)["p"] == 10    # 🍖 5 = 10 rations
    # to 5: ⚔️ wave fights won with 🛡️ Defender; an ordinary win does not count
    set_level(service, 4)
    service._gm_start(KEY, camp(service), service._load("test:1"))
    assert mission(service)["id"] == "gm_oleadas_5"
    quick_win(service, "test:1", seed=4)
    assert mission(service)["p"] == 0
    data = camp(service)
    service._open_raid(data, "raid", "test:1")
    service.store.put("camp", KEY, data)
    assert service.act("test:1", "defend").kind == "combat"
    raid_win(service, "test:1")
    assert mission(service)["p"] == 1 and mission(service)["by"] == {"test:1": 1}


def test_every_level_screen_and_the_board_name_the_missions(service):
    new_camp(service)
    every = service.act("test:1", "lvlall").body
    assert "⏫ Nivel 2 (campamento): construir 🔥 Fogón · 🪵 Empalizada · 🪵 Madera ×30 · 🪨 Piedra ×20 · 🧵 Fibra ×10 · 🎯 vencer 20 monstruos" in every
    assert any(line.startswith("⏫ Nivel 5 (pueblo)") and line.endswith("· 🎯 ganar 3 peleas de oleada") for line in every)
    assert any(line.startswith("⏫ Nivel 7 (ciudad)") and line.endswith("· 🎯 juntar 100 🪨 Piedra · 🪎 1 cofre") for line in every)
    improve = service.act("test:1", "improve").body
    assert "▫️ 🎯 Misión de grupo: vencer 20 monstruos — 0 de 20 (faltan 20)" in improve
    assert "⏫ Nivel 2: 0 de 6 listos (⬆️ Mejorar → ⏫ Siguiente nivel)." in service.act("test:1", "upgrades").body


def test_a_retired_mission_no_longer_asks_anything(service):
    new_camp(service)
    everything_but_the_mission(service)
    service.content.story["group_missions"]["gm_caza_2"]["retired"] = True
    view = service.act("test:1", "lvlup")
    assert not [line for line in view.body if "Misión" in line] and ids(view) == ["lvlgo", "improve"]


def test_it_reads_well_in_english(service):
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    service._gm_start(KEY, camp(service), service._load("test:1"))
    view = service.act("test:1", "lvlup")
    assert "🤝 All together:" in view.body and "▫️ 🎯 Group mission: defeat 20 monsters — 0 of 20 (20 to go)" in view.body
    assert any(line.startswith("🎯 The group mission adds up what every member does") for line in view.body)
    every = service.act("test:1", "lvlall").body
    assert any(line.endswith("· 🎯 gather 60 🪵 Wood") for line in every), every
    assert "▫️ 🎯 Group mission (to reach level 2): defeat 20 monsters — 0 of 20 · you: 0" in service.act("test:1", "board").body
    quick_win(service, "test:1", seed=2)
    for view in (service.act("test:1", a) for a in ("lvlup", "improve", "lvlall", "board", "upgrades")):
        assert "[" not in "\n".join([view.notice or ""] + view.body)
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
