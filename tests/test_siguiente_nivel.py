"""⏫ Siguiente nivel (D-304, 0.41): a checklist of works that must be built, materials and 🪎 chests that fills in.

[ES] Pruebas del pedido del dueño del 20-oct-2026 ("ponme en el botón de mejorar dos opciones: una, siguiente nivel, y dos,
agrandar territorio… debes construir esto, esto y esto a tal nivel para pasar al siguiente nivel, más los recursos, en formato
de lista, y se va a ir completando a medida que va completándose"; y "cada mejora debe ser visible para todos los miembros"):
- 🏰 Gestionar tiene ⬆️ Mejorar campamento ("improve") con ⏫ Siguiente nivel y 🗺️ Agrandar territorio;
- la lista de 1 → 2 nombra 🔥 Fogón y 🪵 Empalizada (camps.level_up) y los 3 materiales con lo aportado (✅ / ▫️);
- se va llenando con los 🤲 de cualquier miembro (también uno común), el 💰 fondo pone primero, y con el último 🤲 sube solo;
- si lo último fue terminar una obra, cualquier miembro ve ⏫ Subir a nivel N; ocupado no aporta; sin nada, avisa qué falta;
- desde el nivel 6 pide 🪎 cofres; el paso a castillo (8 → 9) muestra el gremio, las 15 mejoras y la 🌙 Noche de prueba; la
  hambruna no deja subir; en castillo no hay otro nivel; los campamentos de antes conservan nivel y zonas; se lee en inglés.
Archivo: tests/test_siguiente_nivel.py · Módulo: M14 Construcción · Prueba: engine/service/game.py (_improve_view,
_lvlup_rows, _lvlup_view, _lvlup_give, _lvlup_go, _lvlup_trial, _level_up, _upgrades_view)
"""

from conftest import make_hero
from test_camps import old_camp_at, place
from test_guilds import join, set_level
from engine.service.game import button_cap
from engine.social import guilds as guild_rules

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def camp(service):
    return service.store.get("camp", KEY)


def record(service):
    return service._upgrades(KEY)


def build(service, *uids):
    data = record(service)
    for uid in uids:
        data["built"][uid] = 0.0
    service.store.put("upgrades", KEY, data)


def camp_with(service, *names, level=1):
    """An old camp at 6:0 founded by Lyra (test:1), of `level`, with the given members (test:2…), all at its center."""
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, level)
    for n, name in enumerate(names, 2):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
        place(service, f"test:{n}", 6, 0)
    service.tick()


def pushes(service, account, kind=None):
    return [v for acc, v in service.tick() if acc == account and (kind is None or v.kind == kind)]


def test_manage_has_improve_with_next_level_and_territory(service):
    camp_with(service)
    manage = service.act("test:1", "campmgmt")
    assert ids(manage)[0] == "improve" and "grow" not in ids(manage)
    assert any("⬆️ Mejorar: nivel 1 (campamento), territorio de 1 zona (hasta 3)" in line for line in manage.body)
    improve = service.act("test:1", "improve")
    assert improve.kind == "camp_improve" and ids(improve) == ["lvlup", "grow", "lvlall", "campmgmt"]
    assert [a.label for a in improve.actions[:3]] == ["⏫ Siguiente nivel", "🗺️ Agrandar territorio", "📜 Qué pide cada nivel"]
    # D-313 (the owner did not understand "1 de 3" nor "4 de 5 listos"): everything said in full, line by line
    assert improve.body[:8] == [
        "🏕️ Nivel 1 · campamento", "",
        "🗺️ Territorio: tu campamento ocupa 1 de las 3 zonas que permite la etapa campamento.",
        "Puedes sumarle 2 zonas más en 🗺️ Agrandar territorio.", "",
        "⏫ Para subir a nivel 2 (campamento) necesitas:",
        "▫️ 🔥 Fogón · ⏸️ sin activar: la activa el fundador o un 🤝 asistente en 🏘️ Servicios",
        "▫️ 🪵 Empalizada · ⏸️ sin activar: la activa el fundador o un 🤝 asistente en 🏘️ Servicios"]
    assert "▫️ 🪵 Madera: 0 de 30 (faltan 30)" in improve.body and "▫️ 🧵 Fibra: 0 de 10 (faltan 10)" in improve.body
    assert any(line.startswith("📦 Los materiales no llegan solos") for line in improve.body)


def test_level_one_checklist_names_the_works_and_the_resources(service):
    camp_with(service)
    view = service.act("test:1", "lvlup")
    assert view.kind == "camp_lvlup" and len(view.actions) <= button_cap(view.kind) == 4
    assert view.body[0] == "⏫ Para subir a nivel 2 (campamento) te falta:"
    assert "🏗️ Construir:" in view.body and "📦 Recursos:" in view.body
    assert "▫️ 🔥 Fogón · ⏸️ sin activar: la activa el fundador o un 🤝 asistente en 🏘️ Servicios" in view.body
    for line in ("▫️ 🪵 Madera: 0 de 30 (faltan 30)", "▫️ 🪨 Piedra: 0 de 20 (faltan 20)", "▫️ 🧵 Fibra: 0 de 10 (faltan 10)"):
        assert line in view.body, view.body
    assert ids(view) == ["lvlgive", "upgrades", "improve"]
    assert service._lvlup_works(2) == ["fogon", "empalizada"]
    assert service._lvlup_need(1) == {"madera": 30, "piedra": 20, "fibra": 10}
    assert service._lvlup_need(8) == {"madera": 240, "piedra": 160, "fibra": 80}


def test_a_state_per_work_and_a_retired_work_is_skipped(service):
    camp_with(service)
    data = record(service)
    data["active"] = ["fogon"]
    data["building"] = {"empalizada": {"need": 60, "done": 0, "at": 0.0, "floor": 10, "by": "test:1", "started": 0.0}}
    service.store.put("upgrades", KEY, data)
    body = service.act("test:1", "lvlup").body
    assert any(line.startswith("▫️ 🔥 Fogón · 🔨 activa: faltan 🪵 Madera ×20 · 🪨 Piedra ×15") for line in body), body
    assert "▫️ 🪵 Empalizada · 🏗️ en obra: termina en 1 min" in body     # D-313: when it ends (Lyra is there)
    service.content.balance["camps"]["level_up"][2] = ["fogon", "taller", "no_such_work"]   # taller is retired (D-288)
    assert service._lvlup_works(2) == ["fogon"]


def test_it_fills_in_as_any_member_gives_and_the_fund_goes_first(service):
    camp_with(service, "Bram")
    data = record(service)
    data["fund"] = {"madera": 10}
    service.store.put("upgrades", KEY, data)
    place(service, "test:2", 6, 0, backpack={"piedra": 5})          # Bram is a common member: he gives too
    merit = service._load("test:2").merit
    view = service.act("test:2", "lvlgive")
    assert "💰 El fondo puso 🪵 Madera ×10 en ⏫ Nivel 2." in view.notice
    assert "🤲 Aportaste 🪨 Piedra ×5 a ⏫ Nivel 2" in view.notice and "🏗️ Construcción +5" in view.notice
    assert "▫️ 🪵 Madera: 10 de 30 (faltan 20)" in view.body and "▫️ 🪨 Piedra: 5 de 20 (faltan 15)" in view.body
    assert record(service)["levelup"] == {"to": 2, "given": {"madera": 10, "piedra": 5}, "chests": 0}
    assert record(service)["fund"] == {} and service._load("test:2").backpack == {}
    assert service._load("test:2").merit > merit
    view = service.act("test:2", "lvlgive")                          # nothing left to give: it says what is missing
    assert view.notice == "No llevas nada de lo que falta: 🪵 Madera ×20 · 🪨 Piedra ×15 · 🧵 Fibra ×10."
    view = service.act("test:1", "lvlgive")                          # Lyra carries plenty: never more than missing
    assert all(line.startswith("✅") for line in view.body if " de " in line and line[2:4] in ("🪵", "🪨", "🧵") and ":" in line)
    hero = service._load("test:1")
    assert (hero.backpack["madera"], hero.backpack["piedra"], hero.backpack["fibra"]) == (160, 175, 90)
    assert camp(service)["level"] == 1                                # the works are still missing
    assert ids(view) == ["upgrades", "improve"]
    assert service.act("test:1", "lvlgive").notice == "Los materiales ya están: falta lo demás de la lista."


def test_the_last_give_levels_the_camp_up_at_once(service):
    camp_with(service, "Bram")
    build(service, "fogon", "empalizada")
    pushes(service, "test:2")
    view = service.act("test:1", "lvlgive")
    assert camp(service)["level"] == 2 and "levelup" not in record(service)
    assert "⏫ ¡Roca Alta subió a nivel 2 (campamento)!" in view.notice
    assert view.body[0] == "⏫ Para subir a nivel 3 (aldea) te falta:"
    assert any(line.startswith("▫️ 🗼 Torre de vigía · ⏸️ sin activar") for line in view.body)
    assert "▫️ 🪵 Madera: 0 de 60 (faltan 60)" in view.body
    told = pushes(service, "test:2", "camp_news")
    assert told and "Lyra subió Roca Alta a nivel 2 (campamento)" in told[0].body[0]
    assert service._members_cap(camp(service)) == 4                   # members_base 2 + 2 per level


def test_when_a_work_finishes_last_any_member_goes_up(service):
    camp_with(service, "Bram")
    service.act("test:1", "lvlgive")                                  # the materials first
    assert service.act("test:2", "lvlgo").notice == "Todavía falta algo de la lista."
    assert camp(service)["level"] == 1
    build(service, "fogon", "empalizada")                             # the last thing: the works got built
    view = service.act("test:2", "lvlup")
    assert view.body[0] == "⏫ ¡Todo listo para subir a nivel 2 (campamento)!"
    assert ids(view) == ["lvlgo", "improve"] and view.actions[0].label == "⏫ Subir a nivel 2"
    view = service.act("test:2", "lvlgo")                             # Bram, a common member
    assert camp(service)["level"] == 2 and "subió a nivel 2" in view.notice


def test_busy_members_do_not_give_and_only_at_the_camp(service, clock):
    camp_with(service)
    hero = service._load("test:1")
    hero.activity = {"kind": "explore", "until": clock.now() + 600}
    service._save(hero)
    view = service.act("test:1", "lvlgive")
    assert view.notice == service.texts.t("activity.busy") and "levelup" not in record(service)
    hero = service._load("test:1")
    hero.activity, hero.x = None, 9
    service._save(hero)
    assert service.act("test:1", "lvlup").kind != "camp_lvlup"


def test_chests_from_level_six(service):
    camp_with(service, level=6)
    view = service.act("test:1", "lvlup")
    assert "▫️ 🪎 Cofres 0/1" in view.body and any(line.startswith("🪎 Tienes 0 cofres") for line in view.body)
    place(service, "test:1", 6, 0, backpack={}, chests=3)
    view = service.act("test:1", "lvlgive")
    assert "🪎 Aportaste 1 cofre a ⏫ Nivel 7." in view.notice and service._load("test:1").chests == 2
    assert "✅ 🪎 Cofres 1/1" in view.body and record(service)["levelup"]["chests"] == 1
    assert service._grow_chests(8) == 3


def test_the_castle_step_lists_the_guild_the_upgrades_and_the_trial(service):
    camp_with(service, "Bram", level=8)
    view = service.act("test:1", "lvlup")
    body = view.body
    assert body[0] == "⏫ Para subir a nivel 9 (castillo) te falta:" and "🏰 Para pasar a castillo hace falta:" in body
    assert "▫️ Tener gremio" in body and "▫️ 🌙 Ganar la Noche de prueba" in body
    assert any(line.startswith("▫️ 🔨 15 mejoras construidas") for line in body)
    assert any(line.startswith("▫️ 🏹 Torres de arqueros · ⏸️ sin activar") for line in body) and "▫️ 🪎 Cofres 0/3" in body
    assert ids(view) == ["lvlgive", "upgrades", "guild", "improve"]
    # everything but the trial: the guild, 15 built with the two works, the materials and the chests
    cfg = service.content.balance["guild"]
    cfg["castle_min_members"] = 2
    service.store.put("guild", KEY, {"name": "Lobos Grises", "camp": KEY, "founder_id": "test:1",
                                     "level": cfg["castle_min_level"],
                                     "progress": {k: 0 for k in guild_rules.COUNTERS}, "created": 0.0})
    build(service, *list(service._upgrade_catalog())[:13], "torres_arqueros", "foso")
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999}, chests=5)
    view = service.act("test:1", "lvlgive")
    assert camp(service)["level"] == 8 and ids(view) == ["lvltrial", "improve"]     # only the 🌙 is left
    trial = service.act("test:1", "lvltrial")
    assert trial.kind == "camp_trial" and ids(trial) == ["trial", "lvlup"]
    data = camp(service)
    data["trial_won"] = True
    service.store.put("camp", KEY, data)
    view = service.act("test:1", "lvlup")
    assert "✅ 🌙 Ganar la Noche de prueba" in view.body and ids(view) == ["lvlgo", "improve"]
    view = service.act("test:2", "lvlgo")
    assert camp(service)["level"] == 9 and "castillo" in view.notice
    assert view.body == ["🏰 Tu campamento llegó a castillo: todavía no hay un nivel más."] and ids(view) == ["improve"]
    assert service.act("test:1", "lvlgive").kind == "camp_lvlup" and camp(service)["level"] == 9
    assert service.act("test:1", "lvltrial").kind == "camp_lvlup"


def test_an_empty_pantry_blocks_the_level(service):
    camp_with(service, level=3)
    service.store.put("pantry", KEY, {"rations": 0.0, "at": service.clock.now()})
    build(service, "refugio", "granero", "trampas")
    view = service.act("test:1", "lvlgive")
    assert camp(service)["level"] == 3 and "▫️ 🌾 Llenar la despensa: vacía, el campamento no sube" in view.body
    assert "campfeed" in ids(view) and "lvlgo" not in ids(view)
    service.store.put("pantry", KEY, {"rations": 30.0, "at": service.clock.now()})
    assert ids(service.act("test:1", "lvlup")) == ["lvlgo", "improve"]


def test_everyone_sees_the_checklist_and_the_progress_in_mejoras(service):
    camp_with(service, "Bram")
    member = service.act("test:2", "lvlup")                           # a common member sees the whole list
    assert member.kind == "camp_lvlup" and any(line.startswith("▫️ 🔥 Fogón · ⏸️ sin activar") for line in member.body)
    build(service, "fogon")
    mejoras = service.act("test:2", "upgrades")
    assert "⏫ Nivel 2: 1 de 5 listos (⬆️ Mejorar → ⏫ Siguiente nivel)." in mejoras.body
    improve = service.act("test:2", "improve").body                    # D-313: the whole list, not "1 de 5 listos"
    assert "✅ 🔥 Fogón" in improve and any(line.startswith("▫️ 🪵 Empalizada · ⏸️ sin activar") for line in improve)


def test_old_camps_keep_their_level_and_zones(service):
    camp_with(service, level=4)
    data = camp(service)
    data["zones"] = [[6, 0], [7, 0], [8, 0], [6, 1]]                  # level 4 with 4 zones, as growing left it before
    service.store.put("camp", KEY, data)
    service.act("test:1", "claro")
    service.act("test:1", "lvlup")
    assert camp(service)["level"] == 4 and len(camp(service)["zones"]) == 4
    assert service.act("test:1", "improve").body[:4] == [
        "🏕️ Nivel 4 · aldea", "", "🗺️ Territorio: tu campamento ocupa 4 de las 5 zonas que permite la etapa aldea.",
        "Puedes sumarle 1 zona más en 🗺️ Agrandar territorio."]


def test_the_screens_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    set_level(service, 6)
    screens = [service.act("test:1", action) for action in ("campmgmt", "improve", "lvlup", "lvlgive", "grow", "upgrades")]
    assert screens[1].actions[0].label == "⏫ Next level" and screens[1].actions[1].label == "🗺️ Expand territory"
    assert screens[2].body[0] == "⏫ To reach level 7 (city) you still need:"
    assert "▫️ 🪎 Chests 0/1" in screens[2].body
    for view in screens:
        assert "[" not in text(view), text(view)
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing


def fund_code(service, item_id):
    return f"/f{int(service.content.items[item_id]['code']):02d}"


def test_a_deposit_from_far_away_fills_the_next_level_and_levels_it_up(service):
    # [ES] D-313 (0.41.1, el dueño: "madera 11 de 30, lleva 40 minutos y no sé si está funcionando"): lo depositado con 💰
    # Depositar también llena ⏫ Siguiente nivel (después de las obras activas), y con lo último el campamento sube solo
    camp_with(service, "Bram")
    build(service, "fogon", "empalizada")
    place(service, "test:2", 12, -3, backpack={"madera": 35, "piedra": 20, "fibra": 10})      # far away
    pushes(service, "test:1")
    view = service.text("test:2", fund_code(service, "madera"))
    assert "💰 El fondo puso 🪵 Madera ×30 en ⏫ Nivel 2." in view.notice
    assert record(service)["levelup"]["given"] == {"madera": 30} and record(service)["fund"] == {"madera": 5}
    service.text("test:2", fund_code(service, "piedra"))
    view = service.text("test:2", fund_code(service, "fibra"))
    assert camp(service)["level"] == 2 and "⏫ ¡Roca Alta subió a nivel 2 (campamento)!" in view.notice
    assert "levelup" not in record(service) and record(service)["fund"] == {"madera": 5}       # nothing carried to level 3
    told = pushes(service, "test:1", "camp_news")
    assert told and "Bram subió Roca Alta a nivel 2 (campamento)" in told[0].body[0]


def test_every_level_screen_lists_what_each_step_up_asks(service):
    # [ES] D-313: 📜 Qué pide cada nivel, desde el tuyo hasta castillo (el dueño: "especifica mejor lo que hace falta para
    # cada subida de nivel")
    camp_with(service)
    view = service.act("test:1", "lvlall")
    assert view.kind == "camp_lvlall" and ids(view) == ["lvlup", "improve"]
    assert view.body[0] == "Tu campamento está en nivel 1 (campamento). Lo que pide cada subida:"
    assert ("⏫ Nivel 2 (campamento): construir 🔥 Fogón · 🪵 Empalizada · 🪵 Madera ×30 · 🪨 Piedra ×20 · 🧵 Fibra ×10"
            in view.body)
    assert any(line.startswith("⏫ Nivel 7 (ciudad): construir 🔥 Braseros") and line.endswith("· 🪎 1 cofre")
               for line in view.body), view.body
    assert sum(line.startswith("⏫ Nivel ") for line in view.body) == 8 and view.body[-1].startswith("🏰 Para castillo")
    from test_idiomas import english_hero
    english_hero(service, "test:9", "Ann")
    camp_record = camp(service)
    camp_record["members"].append("test:9")
    service.store.put("camp", KEY, camp_record)
    place(service, "test:9", 6, 0, camp=KEY)
    view = service.act("test:9", "lvlall")
    assert view.title == "📜 What each level needs" and not service.texts.fallbacks.get("en")
    assert any("📦 Materials do not arrive by themselves" in line for line in service.act("test:9", "improve").body)
