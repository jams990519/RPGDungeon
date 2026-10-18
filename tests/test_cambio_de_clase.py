"""Changing class with a price that grows, and only the Explorer rising on its own (D-270, D-272).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026:
- 🔄 Cambiar de clase desde 🌟 Talentos o /cambiarclase: el 1.º gratis; después 🥈1, 🥈10, 🥈30 y 🥈50 para siempre; se
  conservan nivel, oficios, monedas y equipo; los puntos de nivel se reparten solos en el rol nuevo; se anota en el
  📔 Diario; sin monedas, ocupado o a la misma clase, no se cambia;
- solo el 🧭 Explorador sube solo: la recolección también se aprende (sin el oficio se recolectan igual los recursos base)
  y quien ya la practicaba la conserva aprendida.
Archivo: tests/test_cambio_de_clase.py · Módulo: M3 Personaje, M14 Oficios · Prueba: engine/service/game.py
(_class_change_view, _class_change_do, _class_change_price, _load, _knows, _learn_unlocks), content/balance.yaml
(class_change.prices), content/professions.yaml (learn: auto solo en el Explorador; grandfather).
"""

from conftest import make_hero


def ids(view):
    return [a.id for a in view.actions]


def give(service, account="test:1", **fields):
    hero = service._load(account)
    for key, value in fields.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def test_the_class_change_lives_in_talents_and_has_its_command(service):
    make_hero(service)
    assert "chcls" in ids(service.act("test:1", "talents")) and len(service.act("test:1", "talents").actions) <= 4
    view = service.text("test:1", "/cambiarclase")
    assert view.kind == "class_change" and "gratis" in "\n".join(view.body)
    assert "chgrp:guerrero" not in ids(view) and "chgrp:mago" in ids(view)       # your own class is not offered


def test_prices_grow_free_one_ten_thirty_then_fifty_for_ever(service):
    make_hero(service)
    assert service.content.balance["class_change"]["prices"] == [0, 100, 1000, 3000, 5000]
    hero = give(service, gold=20000)
    paid = []
    for target in ("mago_dps", "guerrero_dps", "mago_soporte", "guerrero_tanque", "mago_dps", "guerrero_dps"):
        before = service._load("test:1").gold
        view = service.act("test:1", f"chok:{target}")
        assert service._load("test:1").class_id == target, view.notice
        paid.append(before - service._load("test:1").gold)
    assert paid == [0, 100, 1000, 3000, 5000, 5000]
    assert service._load("test:1").class_changes == 6


def test_you_keep_level_professions_coins_and_gear_and_points_follow(service):
    make_hero(service)
    hero = give(service, level=12, gold=777, professions={"minero": 300}, learned=["minero", "herreria"])
    gear = dict(hero.gear)
    view = service.act("test:1", "chok:sacerdote_sanador")
    hero = service._load("test:1")
    assert hero.class_id == "sacerdote_sanador" and hero.level == 12 and hero.gold == 777
    assert hero.professions["minero"] == 300 and "herreria" in hero.learned and hero.gear == gear
    assert hero.talents == {"sacerdote_sanador": 11}                          # the level points sit in the new role
    assert hero.unlocked == [a["id"] for a in service.content.classes["sacerdote_sanador"]["abilities"]]
    assert "Fue gratis" in view.notice
    assert any(entry["k"] == "class_change" for entry in hero.journal)


def test_no_change_without_coins_while_busy_or_to_the_same_class(service):
    make_hero(service)
    service.act("test:1", "chok:mago_dps")                                     # the free one
    poor = service.act("test:1", "chok:guerrero_dps")
    assert "No te alcanza" in poor.notice and service._load("test:1").class_id == "mago_dps"
    give(service, gold=500)
    assert "Ya eres de esa clase" in service.act("test:1", "chok:mago_soporte").notice
    service.act("test:1", "go:e")
    assert service._load("test:1").activity
    busy = service.act("test:1", "chok:guerrero_dps")
    assert service._load("test:1").class_id == "mago_dps" and busy.notice


def test_only_the_explorer_rises_on_its_own_and_gathering_still_gives_base_resources(service):
    make_hero(service)
    hero = service._load("test:1")
    assert service._knows(hero, "explorador")
    for pid in ("minero", "herbolario", "lenador", "pescador"):
        assert not service._knows(hero, pid), pid
    view = service.text("test:1", "/minero")
    assert view.kind == "profession" and "recursos base" in "\n".join(view.body) and "learn:minero" in ids(view)
    assert service._prof_gain(hero, "minero", 10) == [] and not hero.professions.get("minero")   # no xp without it


def test_who_already_gathered_keeps_it_learned(service):
    make_hero(service)
    give(service, professions={"minero": 40, "herbolario": 0})
    hero = service._load("test:1")
    assert "minero" in hero.learned and service._knows(hero, "minero") and service._prof_rank(hero, "minero") >= 1
    assert "herbolario" not in hero.learned


def test_class_change_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    view = service.act("test:1", "chcls")
    assert view.title == "🔄 Change class" and "free" in "\n".join(view.body)
    assert not service.texts.fallbacks.get("en")
