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
    assert {k: v for k, v in need(service, "curtiduria").items() if k != "coins"} == base(service, "curtiduria")
