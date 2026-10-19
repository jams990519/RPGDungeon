"""Health comes back by itself in 30 minutes, also after falling; healing is always faster (D-284).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026: "la recuperación de la vida total a 30 minutos únicamente, sin
contar pociones; con pociones es más rápido" (y, al caer, "también 30 minutos"); y "si te curas, sea menos de 30 min":
- sola, de 0 a llena en 30 minutos; malherido (caíste), igual;
- una poción o una venda cura al instante su parte de la vida;
- la posada llena la vida en menos de 30 minutos (7,5 con la vida en 0, nunca menos de 5);
- en el territorio de tu campamento con 🔥 Fogón, la vida sola vuelve más rápido que 30 minutos.
Archivo: tests/test_vida_30_minutos.py · Módulo: M5 Salud · Prueba: engine/service/game.py (_hp_full_minutes,
_hp_refill_seconds, _use_out_of_combat, _inn_seconds, _camp_regen_mult), content/balance.yaml (regen, inn).
"""

from conftest import make_hero
from engine.hero import hero_stats

A = "test:1"


def hurt(service, hp=1, downed=False):
    hero = service._load(A)
    hero.hp, hero.downed = hp, downed
    service._save(hero)
    return hero


def max_hp(service):
    hero = service._load(A)
    return int(hero_stats(service._kit(hero), hero.level)["max_hp"])


def test_alone_full_in_thirty_minutes_also_after_falling(service):
    make_hero(service)
    assert service.content.balance["regen"]["hp_full_minutes"] == 30
    assert service.content.balance["regen"]["downed_full_minutes"] == 30
    for downed in (False, True):
        hero = hurt(service, hp=0, downed=downed)
        assert service._hp_full_minutes(hero) == 30
        assert abs(service._hp_refill_seconds(hero, max_hp(service)) - 30 * 60) < 1


def test_healing_is_faster_than_thirty_minutes(service):
    make_hero(service)
    hurt(service, hp=1)
    before = service._load(A).hp
    service.act(A, "use:pocion_vida")                                              # a potion: at once
    assert service._load(A).hp > before
    hero = hurt(service, hp=1)
    assert service._inn_seconds(hero) < 30 * 60                                   # the inn: well under 30 minutes
    assert service._inn_seconds(hero) <= 7.5 * 60 + 1


def test_the_hearth_in_your_camp_makes_it_faster_still(service):
    from test_camps import old_camp_at
    make_hero(service)
    old_camp_at(service, A, 6, 0)                                                 # standing at its own camp
    record = service._upgrades("6:0")
    record["built"]["fogon"] = service.clock.now()                               # with a 🔥 Fogón built
    service.store.put("upgrades", "6:0", record)
    hero = hurt(service, hp=0)
    assert service._camp_regen_mult(hero) > 1 and service._hp_full_minutes(hero) < 30
