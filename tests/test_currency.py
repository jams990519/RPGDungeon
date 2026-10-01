"""Five currencies (D-80): bronze, silver and gold earned; bags sewn in the Claro; gems bought.

[ES] Prueba las monedas: cómo se muestran (100 de una = 1 de la siguiente), coser bolsas en el
Claro (gasta fibra, metal y monedas) y la tienda de gemas (experiencia +50 % y estandarte único).
"""

from conftest import make_hero


def test_money_shows_gold_silver_bronze(service):
    assert service._money(0) == "🥉0"
    assert service._money(45) == "🥉45"
    assert service._money(12345) == "🥇1 🪙23 🥉45"
    assert service._money(10000) == "🥇1"


def test_sew_a_bag_in_the_claro(service):
    make_hero(service)
    hero = service._load("test:1")
    view = service.act("test:1", "sew")
    assert "necesitas" in (view.notice or "") and service._load("test:1").bags == 0
    hero.backpack.update({"fibra": 5, "pieza_metal": 1})
    hero.gold = 150
    service._save(hero)
    view = service.act("test:1", "sew")
    hero = service._load("test:1")
    assert hero.bags == 1 and hero.gold == 50 and hero.backpack.get("fibra") == 1 and "pieza_metal" not in hero.backpack
    assert view.kind == "wallet" and len(view.actions) <= 4


def test_gem_shop_boost_and_banner(service, clock):
    make_hero(service)
    view = service.act("test:1", "gem:xp_boost")
    assert "diamantes" in (view.notice or "").lower()
    hero = service._load("test:1")
    hero.gems = 300
    service._save(hero)
    service.act("test:1", "gem:xp_boost")
    service.act("test:1", "gem:banner")
    hero = service._load("test:1")
    assert hero.gems == 50 and hero.banner == "beta"
    assert service._xp_mult(hero) == 1.5
    assert "🚩[Beta] Lyra" in "\n".join(service.act("test:1", "hero").body)
    view = service.act("test:1", "gems")
    assert not any(a.id == "gem:banner" for a in view.actions)      # only one banner
    clock.advance(8 * 86400)
    assert service._xp_mult(service._load("test:1")) == 1.0
