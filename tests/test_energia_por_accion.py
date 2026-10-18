"""What each action outside a fight costs in ⚡, measured in play (the owner's check, 18-oct-2026).

[ES] El dueño pidió verificar que explorar (no moverse), hacer misiones, entrar a las mazmorras y minar gastan energía. Esta
prueba juega cada acción con la energía sin recuperarse y mira cuánto bajó:
- moverse: 0 (D-190: solo tiempo), también con /ir y 🔗 Moverte;
- explorar y recolectar (minar, talar, recoger): 1 ⚡ por vuelta (energy.per_explore, per_gather), solo las vueltas hechas;
- cazar: 2 ⚡ por presa (hunt.energy); 🔭 reconocer: 2 (recon.energy);
- mazmorra chica: 2 ⚡ por pelea; profunda: 2 por entrar y 2 por pelea (dungeons.*.fight_energy, enter_energy);
- campamento enemigo: 2 ⚡ por pelea del asalto; 🕵️ infiltrarse: 3 (ecamps.fight_energy, infiltrate.energy);
- lo que no se puede hacer (sin rango, sin energía) no cobra nada;
- las misiones no cobran por sí mismas: cobran sus pasos (explorar, recolectar, cazar…); hablar, vender o viajar no.
Archivo: tests/test_energia_por_accion.py · Módulo: M3 Personaje (energía) · Prueba: engine/service/game.py (_spend_energy,
_step_cost, los lotes, la caza, las mazmorras, los campamentos enemigos y el reconocimiento), content/balance.yaml (energy).
"""

import pytest
from conftest import make_hero
from test_camps import place
from test_enemy_camps import rank_xp

A = "test:1"


@pytest.fixture
def service(content, clock):
    from engine.core import MemoryStore
    from engine.service import GameService
    content.balance["explore"]["arrival_encounter_scale"] = 0.0    # no ambush on the way
    content.balance["explore"]["encounter"] = 0.0                   # no fight while exploring
    content.balance["gather"]["encounter_scale"] = 0.0              # nor while gathering
    content.balance["energy"]["per_day"] = 1e-9                     # no regeneration: what is spent shows as is
    return GameService(content, MemoryStore(), clock, world_seed=12345, time_scale=1.0)


def energy(service):
    return service._load(A).energy


def setup(service, x, y, **extra):
    service.store.delete("combat", A)                               # the fight of the step before is not this test's
    place(service, A, x, y, known=[f"{x}:{y}", "0:0"], energy=200, level=30, **extra)


def finish(service, clock):
    for _ in range(600):
        if not service._load(A).activity:
            return
        clock.advance(60)
        service.act(A, "home")


def spent(service, action, *more):
    before = energy(service)
    service.act(A, action)
    for extra in more:
        service.act(A, extra)
    return before - energy(service)


def test_moving_is_free_exploring_and_gathering_cost_one_per_round(service, clock):
    make_hero(service)
    setup(service, 0, 0, learned=["explorador", "minero", "lenador", "herbolario"])
    before = energy(service)
    service.act(A, "go:e")
    finish(service, clock)
    service.text(A, "/ir 3 0")
    service.act(A, "wlk:go")
    finish(service, clock)
    assert energy(service) == before and (service._load(A).x, service._load(A).y) == (3, 0)
    before = energy(service)
    service.act(A, "do:explore:5")
    finish(service, clock)
    assert before - energy(service) == 5
    before = energy(service)
    service.act(A, "do:gather:5")
    finish(service, clock)
    assert before - energy(service) == 5


def test_hunting_recon_dungeons_and_enemy_camps(service):
    make_hero(service)
    setup(service, 3, 0)
    assert spent(service, "hunt", "prey") == service.content.balance["hunt"]["energy"] == 2
    small = next((x, y) for x in range(-20, 21) for y in range(-20, 21) if service._dng_kind(x, y) == "small")
    setup(service, *small)
    assert spent(service, "dungeon", "dgo") == 2                                   # one room fight
    deep = next((x, y) for x in range(-30, 31) for y in range(-30, 31) if service._dng_kind(x, y) == "deep")
    setup(service, *deep)
    assert spent(service, "dungeon", "dgo") == 4                                   # going down (2) + the first fight (2)
    camp = next((x, y) for x in range(-30, 31) for y in range(-30, 31) if service._ecamp_standing(x, y))
    setup(service, *camp)
    assert spent(service, "assault") == 2
    setup(service, *camp)
    assert spent(service, "infiltrate") == 0                                       # rank 30 of 🧭 Explorador needed: free
    setup(service, *camp, professions={"explorador": rank_xp(service, 40)})
    assert spent(service, "infiltrate") == 3
    setup(service, camp[0] + 1, camp[1], professions={"explorador": rank_xp(service, 40)})
    target = next(a.id for a in service.act(A, "recon").actions if a.id.startswith("rcn:"))
    assert spent(service, target) == 2


def test_quests_cost_through_their_steps_and_talking_is_free(service):
    make_hero(service)
    before = energy(service)
    for action in ("claro", "npcs", "board", "journal"):
        service.act(A, action)
    assert energy(service) == before                                              # looking and talking cost nothing
