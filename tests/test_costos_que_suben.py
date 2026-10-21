"""Every new camp work costs more than the one before (D-295).

[ES] Prueba de lo que pidió el dueño el 19-oct-2026 ("aumentar los costos a medida que se va subiendo"), cuando los 13
edificios de oficio (D-288) dejaban el castillo a menos de la mitad de las obras de antes:
- sin obras construidas, cada obra pide lo de base;
- con N obras construidas, una obra nueva pide × (1 + upgrades.cost_growth × N), redondeado hacia arriba;
- el precio queda fijo al activarla: si se termina otra obra, lo que falta no sube;
- una obra con materiales dados antes de esta regla sigue pidiendo lo de base (no se le pide más a lo empezado);
- 🏘️ Servicios dice cuánto más cuesta hoy cada obra nueva.
Archivo: tests/test_costos_que_suben.py · Módulo: M14 Construcción · Prueba: engine/service/game.py (_upgrade_need,
_growth_mult, _work_mult, _freeze_mult, _activate_work, _service_type_view), content/balance.yaml (upgrades.cost_growth).
"""

import math

from test_camp_upgrades import KEY, build
from test_servicios_por_tipo import two


def need(service, uid):
    record = service._upgrades(KEY)
    camp = service.store.get("camp", KEY)
    return service._upgrade_need(service._upgrade_catalog()[uid], service._camp_perks(camp, service._load("test:1")), record, uid)


def base(service, uid):
    return dict(service._upgrade_catalog()[uid]["cost"])


def test_no_works_built_costs_the_base(service):
    two(service, 2)
    assert {k: v for k, v in need(service, "curtiduria").items() if k != "coins"} == base(service, "curtiduria")


def test_each_built_work_raises_the_next_and_activation_fixes_the_price(service):
    two(service, 2)
    growth = service.content.balance["upgrades"]["cost_growth"]
    build(service, "fogon", "empalizada")                                   # 2 built: ×(1 + 2 × growth)
    mult = 1 + 2 * growth
    expected = {k: math.ceil(n * mult - 1e-9) for k, n in base(service, "curtiduria").items()}
    assert {k: v for k, v in need(service, "curtiduria").items() if k != "coins"} == expected
    assert "un 30 % más" in "\n".join(service.act("test:1", "svc:oficio").body)
    service.act("test:1", "upact:curtiduria")                               # ▶️ activate: the price is fixed
    assert service._upgrades(KEY)["mult"]["curtiduria"] == mult
    build(service, "pozo", "torre_vigia")                                   # two more get built later
    assert {k: v for k, v in need(service, "curtiduria").items() if k != "coins"} == expected   # it did not go up
    assert need(service, "aserradero")["madera"] == math.ceil(base(service, "aserradero")["madera"] * (1 + 4 * growth) - 1e-9)


def test_a_work_started_before_the_rule_keeps_its_base_price(service):
    two(service, 2)
    build(service, "fogon", "empalizada", "pozo")
    record = service._upgrades(KEY)
    record["works"]["curtiduria"] = {"madera": 5}                          # given before 0.39, no fixed price yet
    service.store.put("upgrades", KEY, record)
    old = dict(service._upgrade_catalog()["curtiduria"]["cost_before"])   # D-317: begun before 0.45, it keeps its old cost
    assert {k: v for k, v in need(service, "curtiduria").items() if k != "coins"} == old


def test_profession_buildings_ask_their_goods_and_open_works_keep_the_old_cost(service):
    """D-317 (0.45): the 13 profession buildings ask ~90 % of their profession's goods; works begun before keep the old cost."""
    from engine.professions import rules as profession_rules
    two(service, 2)
    catalog = service._upgrade_catalog()
    raw = profession_rules.refined_from(service.content.professions["professions"], service.content.professions["recipes"])
    changed = [uid for uid, udef in catalog.items() if udef.get("cost_before") and udef.get("kind") == "oficio"]
    assert len(changed) == 13
    for uid in changed:
        cost = catalog[uid]["cost"]
        value = {k: n * raw.get(k, (k, 1))[1] for k, n in cost.items()}
        basic = value.get("madera", 0) + value.get("piedra", 0)
        assert basic <= 0.15 * sum(value.values()), uid                     # just a little wood and stone
    record = service._upgrades(KEY)
    record["active"] = ["curtiduria"]                                       # activated before the patch: no frozen cost
    service.store.put("upgrades", KEY, record)
    assert {k: v for k, v in need(service, "curtiduria").items() if k != "coins"} == dict(catalog["curtiduria"]["cost_before"])
    service.act("test:1", "upact:alambique")                                # activated now: the new cost, frozen
    assert service._upgrades(KEY)["cost"]["alambique"] == {**catalog["alambique"]["cost"], "coins": catalog["alambique"]["coins"]}
    assert {k: v for k, v in need(service, "alambique").items() if k != "coins"} == dict(catalog["alambique"]["cost"])


def test_from_level_5_buildings_mix_goods_of_other_professions(service):
    """D-318 (0.45): from camp level 5 the buildings that are not of a profession ask goods refined or made by others."""
    catalog = service._upgrade_catalog()
    recipes = service.content.professions["recipes"]
    made = {item for rdef in recipes.values() if not rdef.get("retired") for item in (rdef.get("output") or {})}
    for uid, udef in catalog.items():
        if udef.get("retired") or udef.get("kind") == "oficio" or udef["level"] < 5:
            continue
        others = [item for item in udef["cost"] if item in made]
        assert others, uid                                                  # at least one good from a profession
    assert {"literas_roble", "unguento", "venda"} <= set(catalog["enfermeria"]["cost"])   # the hospital: carpentry, medicine, tailoring
