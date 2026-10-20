"""💱 Comercio is locked for now: it will be redefined for the caravans (D-298).

[ES] Prueba de la orden del dueño (20-oct-2026): "la profesión de comerciante va a cambiar, va a estar bloqueada por ahora; va a
estar definida para las caravanas que se van a definir luego":
- no aparece en 📚 Aprender oficios ni se puede aprender, ni con su código /comercio;
- vender al mercader ya no le da experiencia ni su beneficio (+% al vender), ni el de sus 🎓 especializaciones;
- quien ya tenía rango lo conserva guardado (el progreso no se pierde, D-64); y vender sigue funcionando para todos.
Archivo: tests/test_comercio_bloqueado.py · Módulo: M7 Economía y oficios · Prueba: engine/service/game.py (_prof_catalog,
_pspec_catalog, _perks, _prof_gain), content/professions.yaml (comercio: locked).
"""

from conftest import make_hero
from test_camps import place


def test_commerce_is_not_learnable_nor_listed(service):
    make_hero(service)
    assert "comercio" not in service._prof_catalog()
    learn = service.act("test:1", "learn")
    assert not any("Comercio" in line for line in learn.body) and not any("comercio" in a.id for a in learn.actions)
    view = service.text("test:1", "/comercio")
    assert "Comercio" not in (view.title or "")


def test_selling_gives_no_commerce_xp_or_bonus_but_keeps_the_old_rank(service):
    make_hero(service)
    place(service, "test:1", 0, 0, professions={"comercio": 5000}, learned=["comercio"],
          prof_specs={"comercio": ["comercio_abastecedor"]}, spec_xp={"comercio_abastecedor": 10**6})
    hero = service._load("test:1")
    assert service._perks(hero)["sell"] == 0                                # the +% when selling is paused
    total, lines = service._merchant_sale(hero, 100, "goods")
    assert total == 100 and not lines                                       # no bonus, no specialization, no rank up
    assert hero.professions["comercio"] == 5000                             # no xp, and nothing lost
