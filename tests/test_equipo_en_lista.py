"""🔁 Equipar as a list of what you don't wear, and 🔽 Desequipar to take pieces off (D-299).

[ES] Pruebas de lo que pidió el dueño el 20-oct-2026: "en héroe, mochila, equipo, dentro de equipar, que salga en formato lista y
solamente lo que no está equipado, porque se ve lo que ya tienes equipado y se forma la confusión; y un segundo botón en el menú
anterior de equipar, un botón de desequipar":
- 🛡️ Equipo tiene 🔁 Equipar y, al lado, 🔽 Desequipar;
- 🔁 Equipar lista solo las piezas de la mochila, una por renglón con su código /e1 (lo puesto no sale); /e1 abre la pieza;
- 🔽 Desequipar lista lo puesto con su código /q1, y /q1 lo quita y lo deja en la mochila;
- con muchas piezas hay páginas; un código que no está en la lista avisa; y se lee bien en inglés.
Archivo: tests/test_equipo_en_lista.py · Módulo: M3 Personaje (equipo) · Prueba: engine/service/game.py (_worn_view,
_gear_view, _unequip_view, _gear_code), content/balance.yaml (gear.list_per_page).
"""

from conftest import make_hero


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def with_bag(service, *items):
    make_hero(service, class_id="guerrero")
    hero = service._load("test:1")
    for item_id in items:
        hero.backpack[item_id] = 1
    service._save(hero)
    return hero


def test_equip_lists_only_what_you_dont_wear_and_the_code_opens_it(service):
    hero = with_bag(service, "espada_2", "tela_1")
    worn = set(hero.gear.values())
    view = service.act("test:1", "gear:0")
    codes = [line for line in view.body if line.startswith("/e")]
    assert len(codes) == 2 and view.title == "🔁 Equipar"
    assert not any(service._gear_name(i) in line for i in worn for line in codes)      # nothing you wear
    piece = service.text("test:1", "/e1")
    assert piece.kind == "item" and any(a.id.startswith("equip:") for a in piece.actions)
    assert "no está en la lista" in service.text("test:1", "/e9").notice


def test_unequip_lists_what_you_wear_and_the_code_takes_it_off(service):
    hero = with_bag(service)
    weapon = hero.gear["arma"]
    assert "unequipl" in [a.id for a in service.act("test:1", "gear").actions]
    view = service.act("test:1", "unequipl")
    assert view.kind == "gear_unequip" and any(line.startswith("/q1") for line in view.body)
    done = service.text("test:1", "/q1")
    hero = service._load("test:1")
    assert "arma" not in hero.gear and hero.backpack.get(weapon) == 1 and "Te quitaste" in done.notice
    assert all(not line.startswith("/q") or service._gear_name(weapon) not in line for line in done.body)


def test_many_pieces_have_pages_and_english_reads_well(service):
    from test_idiomas import english_hero
    english_hero(service)
    hero = service._load("test:1")
    gear = [i for i, d in service.content.items.items() if d.get("kind") == "gear" and not d.get("retired")][:12]
    for item_id in gear:
        hero.backpack[item_id] = 1
    service._save(hero)
    view = service.act("test:1", "gear:0")
    assert view.title == "🔁 Equip" and sum(1 for l in view.body if l.startswith("/e")) == service.content.balance["gear"]["list_per_page"]
    assert "gear:1" in [a.id for a in view.actions]
    assert service.act("test:1", "unequipl").title == "🔽 Unequip"
    assert not service.texts.fallbacks.get("en")
