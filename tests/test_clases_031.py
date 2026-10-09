"""The six classes of the 0.31 patch (D-225, D-230, D-232): two roles each, the mother rule, old heroes and the second role.

[ES] Pruebas de las clases nuevas: hay exactamente 6 clases (desde la 0.32, D-233: Guerrero y Paladín de placa, Druida y
Cazador de cuero, Sacerdote y Mago de tela, en ese orden y de 2 en 2 al crear el héroe; el Chamán pasa a Paladín) con sus 2
roles del parche; las clases de un mismo rol comparten el esqueleto (la misma vida, ataque, armadura e iniciativa, base y por
nivel: regla madre); la esquiva del Druida tiene los mismos números que el aguante del Guerrero; la Sanación superior cuesta 6
como todo gastador; la Marea de sanación (hoy la Luz del alba) no escala con la cadena; las 48 especializaciones viejas quedan retiradas y un héroe
guardado con una de ellas pasa a la nueva con su nivel, experiencia, equipo y monedas; al crear el héroe se elige el primer
rol y el segundo se abre al nivel 5; la pantalla de combate tiene a lo sumo 6 botones con su costo. Ningún texto falta.
Archivo: tests/test_clases_031.py · Módulo: M3 Clases y talentos · Prueba: content/classes.yaml (system: chain),
engine/classes/talents.py (ensure_talents, sync_chain, switch_role, kit), engine/service/game.py (creación, talentos, combate).
"""

import pytest

from conftest import make_hero
from engine.classes import specs_of, switch_role
from engine.combat import chain
from engine.core import load_content
from engine.hero import Hero

PATCH = {                                                   # 0.32 (D-233): the Paladín took the Chamán's place
    "guerrero": {"guerrero_tanque": "defensa", "guerrero_dps": "ataque"},
    "paladin": {"paladin_sanador": "curacion", "paladin_dps": "ataque"},
    "druida": {"druida_tanque": "defensa", "druida_dps": "ataque"},
    "cazador": {"cazador_soporte": "soporte", "cazador_dps": "ataque"},
    "sacerdote": {"sacerdote_sanador": "curacion", "sacerdote_dps": "ataque"},
    "mago": {"mago_soporte": "soporte", "mago_dps": "ataque"},
}
ARMOR = {"guerrero": "placas", "paladin": "placas", "druida": "cuero", "cazador": "cuero", "sacerdote": "tela", "mago": "tela"}


@pytest.fixture(scope="module")
def content():
    return load_content()


def test_six_classes_with_the_two_roles_of_the_patch(content):
    active = {cid: c for cid, c in content.classes.items() if not c.get("retired")}
    groups = {}
    for cid, cdef in active.items():
        groups.setdefault(cdef["group"], {})[cid] = cdef["role"]
    assert groups == PATCH
    for group, armor in ARMOR.items():
        assert content.balance["gear"]["armor_by_group"][group] == armor
    for cdef in active.values():
        assert cdef["system"] == "chain" and cdef["attack"]["link"] == "B"
        assert [a["link"] for a in cdef["abilities"]] == ["H1", "H2", "H3"]          # 4 buttons: Básico + 3
        assert cdef["resource_start"] == content.balance["chain"]["energy"]["start"]


def test_the_mother_rule_same_role_same_numbers(content):
    by_role = {}
    for cid, cdef in content.classes.items():
        if cdef.get("system") == "chain":
            by_role.setdefault(cdef["role"], []).append(cdef)
    for role, specs in by_role.items():
        assert len({str(s["base"]) for s in specs}) == 1, role                       # same skeleton
        assert len({str(s["per_level"]) for s in specs}) == 1, role
    # The Druid's dodge is the Warrior's endurance in numbers (only the name changes).
    w = {a["link"]: a for a in content.classes["guerrero_tanque"]["abilities"]}
    d = {a["link"]: a for a in content.classes["druida_tanque"]["abilities"]}
    for link in ("H2", "H3"):
        assert (w[link]["value"], w[link]["rounds"]) == (d[link]["value"], d[link]["rounds"])
        assert (w[link]["style"], d[link]["style"]) == ("aguante", "esquiva")


def test_every_spender_costs_six_and_the_tide_ignores_the_chain(content):
    assert chain.cost_of("H3", content.balance) == 6
    marea = next(a for a in content.classes["paladin_sanador"]["abilities"] if a["link"] == "H3")     # the old Marea
    assert marea.get("chain_free") and marea.get("group")
    superior = next(a for a in content.classes["sacerdote_sanador"]["abilities"] if a["link"] == "H3")
    assert superior["kind"] == "heal" and not superior.get("chain_free")


def test_old_classes_are_retired_and_old_heroes_move_with_everything(service, content):
    old = [cid for cid, c in content.classes.items() if c.get("retired")]
    assert len(old) == 48                                      # 46 before the patch + the Chamán's 2 roles (0.32)
    for cid in old:
        target = content.classes[cid]["migrate_to"]
        assert target in content.classes and not content.classes[target].get("retired")
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.update(class_id="picaro", level=12, xp=345, gold=999, talents={"picaro": 11}, points=0, bar=["evasion"],
                gear={"arma": "daga_1"})
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.class_id == "druida_dps" and hero.level == 12 and hero.xp == 345 and hero.gold == 999
    assert hero.gear == {"arma": "daga_1"} and hero.talents == {"druida_dps": 11} and hero.points == 0
    view = service.act("test:1", "talents")
    assert any("Druida · DPS" in line for line in view.body)
    assert not service.texts.missing


def test_creating_a_hero_chooses_the_first_role(service):
    service.view("test:9")
    service.text("test:9", "Ayla")
    view = service.act("test:9", "grp:guerrero")
    ids = [a.id for a in view.actions]
    assert ids[:2] == ["cls:guerrero_tanque", "cls:guerrero_dps"] and ids[-1] == "grp:"
    service.act("test:9", "cls:guerrero_dps")
    hero = service._load("test:9")
    assert hero.class_id == "guerrero_dps" and "Guerrero · DPS" in service._hero_title(hero)
    assert not service.texts.missing


def test_the_second_role_opens_at_level_five(service, content):
    make_hero(service)
    hero = service._load("test:1")
    hero.level = 4
    assert not switch_role(content.classes, content.balance, hero, "guerrero_dps")
    view = service.act("test:1", "tal:guerrero_dps")
    assert not any(a.id.startswith("role:") for a in view.actions) and any("nivel 5" in line for line in view.body)
    hero = service._load("test:1")
    hero.level = 5
    service._save(hero)
    view = service.act("test:1", "tal:guerrero_dps")
    assert "role:guerrero_dps" in [a.id for a in view.actions]
    view = service.act("test:1", "role:guerrero_dps")
    hero = service._load("test:1")
    assert hero.class_id == "guerrero_dps" and hero.talents == {"guerrero_dps": 4} and "Ahora juegas" in view.notice
    assert specs_of(content.classes, "guerrero") == ["guerrero_tanque", "guerrero_dps"]
    assert not service.texts.missing


def test_the_fight_screen_shows_the_chain_with_six_buttons_at_most(service):
    make_hero(service)
    hero = service._load("test:1")
    from engine.core import Rng
    service._start_combat(hero, service._zone(1, 0), Rng(5), "encounter.ambush")
    service._save(hero)
    view = service.view("test:1")
    assert view.kind == "combat" and len(view.actions) <= 6
    labels = [a.label for a in view.actions]
    assert labels[0].startswith("⚔️") and "(+1)" in labels[0] and "(2)" in labels[1] and "(3)" in labels[2] and "(6)" in labels[3]
    assert view.actions[4].id == "dodge" and view.actions[5].id == "bag"
    assert any(line.startswith("🔷 Energía: 5") for line in view.body) and any(line.startswith("🔗 Tu cadena:") for line in view.body)
    bag = service.act("test:1", "bag")
    assert "flee" in [a.id for a in bag.actions]
    service.act("test:1", "back")
    for _ in range(30):                                       # a whole fight: every text exists
        state = service.store.get("combat", "test:1")
        if not state:
            break
        hero = service._load("test:1")
        hero.hp = 999
        service._save(hero)
        service.act("test:1", ("atk", "ab:1", "ab:0", "ab:2")[state["round"] % 4])
    assert not service.texts.missing


def test_old_heroes_without_combo_shapes_load(content):
    hero = Hero.from_dict({"id": "x", "name": "X", "class_id": "guerrero"})
    assert hero.combo_shapes == []


def test_two_classes_per_armor_in_this_order(service, content):
    """0.32 (D-233): Guerrero and Paladín (plate), Druida and Cazador (leather), Sacerdote and Mago (cloth)."""
    assert service._class_groups() == ["guerrero", "paladin", "druida", "cazador", "sacerdote", "mago"]
    armor = content.balance["gear"]["armor_by_group"]
    assert [armor[g] for g in service._class_groups()] == ["placas", "placas", "cuero", "cuero", "tela", "tela"]


def test_shaman_heroes_become_paladins_with_everything(service, content):
    make_hero(service)
    for old, new in (("chaman_sanador", "paladin_sanador"), ("chaman_dps", "paladin_dps"), ("chaman_restauracion", "paladin_sanador")):
        data = service.store.get("hero", "test:1")
        data.update(class_id=old, level=7, xp=500, gold=321, talents={old: 6}, points=0)
        service.store.put("hero", "test:1", data)
        hero = service._load("test:1")
        assert hero.class_id == new and hero.level == 7 and hero.xp == 500 and hero.gold == 321, old
        assert hero.talents == {new: 6}
    assert not service.texts.missing


def test_the_creation_pages_show_one_armor_each(service):
    """0.32 (D-233): two classes per page, so each armor pair stays together."""
    service.view("test:9")
    view = service.text("test:9", "Pares")
    pages = []
    for _ in range(3):
        pages.append([a.id[4:] for a in view.actions if a.id.startswith("grp:")])
        view = service.act("test:9", next(a.id for a in view.actions if a.id.startswith("page:")))
    assert pages == [["guerrero", "paladin"], ["druida", "cazador"], ["sacerdote", "mago"]]
    service.act("test:9", "grp:cazador")
    back = service.act("test:9", "grp:")                                  # back returns to the leather page
    assert [a.id for a in back.actions if a.id.startswith("grp:")] == ["grp:druida", "grp:cazador"]
    assert not service.texts.missing
