"""What camp works cost after 0.45 and how fast a camp gets to castle (D-319, 0.45.1).

[ES] Pruebas del recálculo de costos y beneficios de los edificios que pidió el dueño el 21-oct-2026, después de la 0.45
(D-317: los edificios de oficio con lo de su oficio; D-318: desde el nivel 5 se mezclan oficios):
- ninguna obra que pide ⏫ Siguiente nivel (balance.yaml camps.level_up) pide algo que solo hace un rango alto: todo lo
  fabricado sale con rango 10 o menos (15 en el paso a castillo), sin 🎓 especialización, sin 📚 libro y sin título comprado;
  así un campamento no se traba meses en un nivel esperando a un carpintero (en la 0.45 pedían rango 70 y dos 🎓);
- la piel solo la piden los oficios del cuero (🪣 Curtiduría y 🦺 Peletería): es lo más caro de juntar;
- las obras que cambiaron siguen guardando en cost_before lo de antes de la 0.45 (las activadas antes lo siguen pidiendo)
  y una obra activada hoy guarda su costo nuevo;
- el ritmo hasta castillo de tools/camp_costs.py queda en la misma franja que antes de la 0.45 (un poco más largo), con
  menos piel que en la 0.45, y el artesano dedicado llega a tiempo a cada nivel.
Archivo: tests/test_costos_edificios.py · Módulo: M24 Construcción · Prueba: content/camp_upgrades.yaml,
content/professions.yaml (literas_roble, armero_roble), balance.yaml camps.level_up, engine/service/game.py (_work_base,
_freeze_mult, _upgrade_need), tools/camp_costs.py.
"""

import sys
from pathlib import Path

import pytest

from test_camp_upgrades import KEY
from test_servicios_por_tipo import two

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import camp_costs  # noqa: E402

BEFORE_045 = {   # [ES] lo que pedían antes de la 0.45 (cost_before no se toca nunca)
    "muralla": {"piedra": 260, "madera": 60, "arcilla": 40},
    "huerto": {"madera": 80, "fibra": 60, "hierba_curativa": 50, "arcilla": 40},
    "forja": {"piedra": 80, "madera": 50, "pieza_metal": 40},
}


@pytest.fixture(scope="module")
def model():
    return camp_costs.Model()


def crafted_needs(content, item, out):
    """Every recipe behind a good (the one without variant with the lowest rank): (recipe id, recipe) into `out`."""
    recipes = {rid: r for rid, r in content.professions["recipes"].items() if not r.get("retired")}
    options = [(rid, r) for rid, r in recipes.items() if item in (r.get("output") or {}) and not r.get("variant")]
    if not options:
        return
    rid, rdef = min(options, key=lambda o: (bool(o[1].get("spec")), int(o[1].get("min_rank", 1)), o[0]))
    out.append((rid, rdef))
    for inner in rdef.get("inputs") or {}:
        crafted_needs(content, inner, out)


def test_level_up_works_never_wait_for_a_high_rank(content):
    """D-319: what ⏫ asks is made with rank ≤ 10 (≤ 15 for the castle), no 🎓, no 📚 book, no title to buy."""
    catalog = content.camp_upgrades["upgrades"]
    books = min(int(b["rank"]) for b in content.balance["recipe_tiers"]["books"])
    first_cap = min(int(r["from"]) for r in content.professions["ranks"] if int(r["from"]) > 1) - 1   # 20: the Oficial
    top = max(int(k) for k in content.balance["camps"]["level_up"])
    checked = 0
    for target, works in content.balance["camps"]["level_up"].items():
        limit = 15 if int(target) == top else 10
        for uid in works:
            for item in catalog[uid]["cost"]:
                needs = []
                crafted_needs(content, item, needs)
                for rid, rdef in needs:
                    rank = int(rdef.get("min_rank", 1))
                    assert not rdef.get("spec"), (uid, rid)                      # one 🎓 per hero until rank 75
                    assert rank <= limit and rank < books and rank <= first_cap, (uid, rid, rank)
                    checked += 1
    assert checked >= 20                                                         # the refined and crafted goods of 7 works


def test_the_hospital_still_asks_carpentry_medicine_and_tailoring(content):
    """D-318 kept: the 🏥 Enfermería asks 🪑 Literas, ointments and bandages; the 🏹 Torres a 🪑 Armero (now ranks 10 and 15)."""
    catalog = content.camp_upgrades["upgrades"]
    recipes = content.professions["recipes"]
    assert {"literas_roble", "unguento", "venda"} <= set(catalog["enfermeria"]["cost"])
    assert "armero_roble" in catalog["torres_arqueros"]["cost"]
    assert (recipes["literas_roble"]["min_rank"], recipes["armero_roble"]["min_rank"]) == (10, 15)
    for uid in ("muralla", "huerto"):                                            # the 🎓 furniture left the level-up works
        assert not {"paveses_roble", "carro_viveres"} & set(catalog[uid]["cost"]), uid
    assert recipes["paveses_roble"]["spec"] and recipes["carro_viveres"]["spec"]   # still made, still exclusive


def test_only_the_leather_trades_ask_hide(content):
    """D-319: 🦌 hide is the dearest raw (hunted outside the territory): only the Curtiduría and the Peletería ask leather."""
    catalog = content.camp_upgrades["upgrades"]
    leather = {uid for uid, u in catalog.items() if not u.get("retired") and ({"cuero_curtido", "piel"} & set(u["cost"]))}
    assert leather == {"curtiduria", "peleteria"}
    assert catalog["forja"]["cost"] == {"lingote": 75, "madera": 10, "piedra": 10}


def test_changed_works_keep_the_cost_from_before_045(content):
    catalog = content.camp_upgrades["upgrades"]
    for uid, old in BEFORE_045.items():
        assert dict(catalog[uid]["cost_before"]) == old, uid
    for uid, cost in camp_costs.COST_045.items():                                # the tool's 0.45 photo is not today's cost
        assert dict(catalog[uid]["cost"]) != cost, uid


def test_works_activated_before_keep_their_cost_and_new_ones_freeze_today(service):
    """A Muralla activated before 0.45 (no frozen cost) asks cost_before; one frozen in 0.45 keeps it; a new one asks today's."""
    two(service, 5)
    catalog = service._upgrade_catalog()
    record = service._upgrades(KEY)
    record["active"] = ["muralla"]                                               # activated before 0.45: no frozen cost
    record["cost"] = {"huerto": dict(camp_costs.COST_045["huerto"])}             # activated during 0.45: its cost frozen
    record["active"].append("huerto")
    service.store.put("upgrades", KEY, record)
    camp = service.store.get("camp", KEY)
    perks = service._camp_perks(camp, service._load("test:1"))

    def need(uid):
        return {k: v for k, v in service._upgrade_need(catalog[uid], perks, service._upgrades(KEY), uid).items() if k != "coins"}

    assert need("muralla") == BEFORE_045["muralla"]
    assert need("huerto") == camp_costs.COST_045["huerto"]                       # nobody changes a price half-way
    service.act("test:1", "upact:forja")                                         # activated now: today's cost, frozen
    assert {k: v for k, v in service._upgrades(KEY)["cost"]["forja"].items() if k != "coins"} == dict(catalog["forja"]["cost"])
    assert need("forja") == dict(catalog["forja"]["cost"])


def test_pace_to_castle_stays_in_the_band(model):
    """tools/camp_costs.py: the list path (D-304) costs a bit more energy than before 0.45, never a wall."""
    before = model.total(model.path("before", False))
    now = model.total(model.path("now", False))
    assert 1.0 <= now.energy / before.energy <= 1.25                              # same ballpark, slightly longer
    assert 0.97 <= now.raw_total / before.raw_total <= 1.05
    days = sum(step["days"] for step in model.path("now", False))
    assert 12 <= days <= 25                                                      # 5 → 10 members, 75 % of their ⚡
    full_before = model.total(model.path("before", True))
    full_045 = model.total(model.path("045", True))
    full_now = model.total(model.path("now", True))
    assert full_now.energy <= full_045.energy and full_now.energy / full_before.energy <= 1.4
    assert full_now.raw.get("piel", 0) <= 0.75 * full_045.raw.get("piel", 0)       # less hide than 0.45
    assert full_now.raw.get("pieza_metal", 0) <= 2.5 * full_before.raw.get("pieza_metal", 0)   # 0.42 tripled its regrowth


def test_a_dedicated_crafter_arrives_in_time(model):
    """Each level's highest rank is reached by a crafter who starts on day one before the camp gets to that level."""
    day = 0.0
    for step in model.path("now", False):
        day += step["days"]
        pid, rank, spec, reach = camp_costs.top_need(model, step["acc"])
        if pid:
            assert not spec and reach is not None and reach[0] <= day, (step["level"], pid, rank, reach, day)
    assert camp_costs.same_trade_specs(model.total(model.path("now", True))) == 0
    old = model.total(model.path("045", False))                                  # 0.45: 🎓 Escudos and 🎓 Mobiliario
    assert camp_costs.same_trade_specs(old) == 2


def test_the_tool_prints_its_tables(capsys):
    assert camp_costs.main([]) == 0
    out = capsys.readouterr().out
    assert "antes de la 0.45" in out and "| hoy |" in out and "nivel por nivel" in out
