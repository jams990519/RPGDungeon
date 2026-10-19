"""🏘️ Servicios by type of building, one building per profession and works that the founder or a helper activates (0.39).

[ES] Pruebas de lo que pidió el dueño el 19-oct-2026 ("dentro de los servicios, botones de acuerdo a los tipos de construcciones…
que todos los miembros puedan entrar y ver qué es lo que se necesita… si un jugador quiere construir la refinería para el cuero,
yo lo activo o mi ayudante… una vez yo lo pongo todos pueden ver lo que falta"; "si hay algo que no está para tu nivel, no lo vas
a mostrar"; "un edificio por profesión"):
- 🏘️ Servicios muestra un botón por tipo (🏠 Casas, ⚒️ Oficios, 🛡️ Defensas, 📚 Saber) solo si ese jugador puede ver algo ahí, más
  💰 Depositar y ↩️ Volver; nada de niveles que el campamento no tiene (D-287, D-288);
- cada tipo lista lo construido con sus botones de uso, las obras activas con lo que falta y su 🤲 y las obras de este nivel
  sin activar: el fundador (o un ayudante) con ▶️ Activar; un miembro común las ve "⏸️ sin activar" (el dueño: "las mejoras
  tienen que ser visibles para los jugadores… no van a tener derecho a elegir cuál mejora, pero sí aportar a las mejoras
  existentes"), no activa nada y no puede aportar a una obra que no está activa (D-291);
- al activar se avisa a todos; ⏹️ Quitar solo mientras nadie le dio nada; sin tope de obras activas;
- un campamento de antes de la 0.39 con materiales dados sigue con esa obra activa; el 🧵 Taller y la 🔨 Herrería quedan retirados
  pero quien los construyó conserva todas sus estaciones (y uno a medias se puede terminar); cada edificio nuevo abre su estación;
- las pantallas no pasan de 8 botones y se leen en inglés.
Archivo: tests/test_servicios_por_tipo.py · Módulo: M14 Construcción · Prueba: engine/service/game.py (_services_view,
_service_type_view, _activate_work, _stop_work, _give_to_work, _active_works, _open_works), content/camp_upgrades.yaml (kind,
retired, los 13 edificios de oficio) y content/professions.yaml stations.camp.
"""

import pytest

from conftest import make_hero
from engine.service.game import CAMP_KINDS, HUB_BUTTONS, HUB_KINDS
from test_camp_upgrades import build, camp_at, set_hero
from test_camps import place
from test_guilds import join, set_level

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def pushes(service, account, kind=None):
    return [v for acc, v in service.tick() if acc == account and (kind is None or v.kind == kind)]


def two(service, level):
    """Lyra founds a camp at 6:0 of `level`; Bram is a plain member; both at its center."""
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, level)
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    service.tick()


def all_pages(service, account, kind):
    """Every button and line of a type's screen, walking its ➡️ pages."""
    buttons, lines, page = [], [], 0
    for _ in range(12):
        view = service.act(account, f"svc:{kind}:{page}")
        check_buttons(view)
        buttons += ids(view)
        lines += view.body
        more = [a.id for a in view.actions if a.id.startswith(f"svc:{kind}:")]
        if not more or more[0].endswith(":0"):
            break
        page = int(more[0].rsplit(":", 1)[1])
    return buttons, "\n".join(lines)


def check_buttons(view):
    assert view.kind in HUB_KINDS and len(view.actions) <= HUB_BUTTONS, (view.kind, ids(view))
    assert view.layout and view.layout[-1] == 1 and sum(view.layout) == len(view.actions), view.layout


def test_the_hub_shows_one_button_per_type_the_player_can_see(service):
    two(service, 3)
    build(service, "fogon", "refugio")
    hub = service.act("test:1", "upsvc")
    check_buttons(hub)
    assert hub.kind == "camp_services" and ids(hub)[-2:] == ["gfund:svc", "claro"]
    assert ids(hub)[:-2] == ["svc:casa", "svc:oficio", "svc:defensa"]        # 📚 Saber opens at level 7: not shown (D-287)
    assert "Biblioteca" not in text(hub) and "nivel 7" not in text(hub)
    assert any(line.startswith("🏠 Casas: ✅ 1") and "▶️" in line for line in hub.body)   # the founder sees what to activate
    member = service.act("test:2", "upsvc")                                # Bram sees every work of this level...
    assert ids(member)[:-2] == ["svc:casa", "svc:oficio", "svc:defensa"]
    assert "▶️" not in text(member) and "⏸️" in text(member)               # ...but does not choose which one
    assert all(kind in ("casa", "oficio", "defensa", "saber") for kind in CAMP_KINDS)


def test_the_founder_activates_and_every_member_sees_what_is_missing(service):
    two(service, 2)
    buttons, lines = all_pages(service, "test:1", "oficio")
    assert "upact:curtiduria" in buttons and "upact:fogon" in buttons      # level 2: the tannery is there
    assert "upact:carpinteria" not in buttons and "Carpintería" not in lines   # level 3: hidden (D-287)
    # the owner: "las mejoras tienen que ser visibles para los jugadores; no van a tener derecho a elegir cuál mejora, pero sí
    # aportar a las mejoras existentes": Bram sees the works of this level read-only (⏸️), no ▶️ and no 🤲 until one is active
    buttons, lines = all_pages(service, "test:2", "oficio")
    assert "⏸️ 🪣 Curtiduría · nivel 2 · sin activar" in lines and "Pide:" in lines
    assert not any(b.startswith(("upact:", "upg:")) for b in buttons)
    assert "Carpintería" not in lines                                       # level 3: hidden for everyone (D-287)
    set_hero(service, "test:2", backpack={"madera": 40, "piedra": 20, "piel": 10}, gold=100)
    view = service.act("test:2", "upg:curtiduria:s")                       # not active: Bram cannot give to it
    assert "todavía no está activa" in view.notice and service._load("test:2").backpack["madera"] == 40
    assert "fundador o un 🤝 ayudante" in service.act("test:2", "upact:curtiduria").notice
    assert "curtiduria" not in service._upgrades(KEY)["active"]
    view = service.act("test:1", "upact:curtiduria")                       # ▶️ the founder activates the tannery
    assert "Activaste" in view.notice and service._upgrades(KEY)["active"] == ["curtiduria"]
    told = pushes(service, "test:2", "camp_news")
    assert told and "Lyra activó" in told[0].body[0] and "Curtiduría" in told[0].body[0] and "falta" in told[0].body[0]
    assert ids(told[0]) == ["gfund"]                                       # 💰 Depositar from wherever they are
    member = service.act("test:2", "svc:oficio")                           # now Bram sees it with its bars and 🤲
    assert "upg:curtiduria:s" in ids(member) and "Madera: 0/30" in text(member)
    set_hero(service, "test:2", backpack={"madera": 12, "fibra": 3}, gold=0)
    view = service.act("test:2", "upg:curtiduria:s")
    assert view.kind == "camp_type" and "Aportaste" in view.notice
    assert service._upgrades(KEY)["works"]["curtiduria"] == {"madera": 12}
    assert service._load("test:2").backpack == {"fibra": 3}               # never what it does not ask


def test_stop_only_while_nothing_was_given_and_no_limit_on_active_works(service):
    two(service, 2)
    for uid in ("aserradero", "tejeduria", "canteria", "fogon", "empalizada", "pozo"):
        service.act("test:1", f"upact:{uid}")
    assert len(service._upgrades(KEY)["active"]) == 6                      # no hard limit
    view = service.act("test:1", "svc:oficio")
    assert "upstop:aserradero" in ids(view)
    view = service.act("test:1", "upstop:aserradero")
    assert "Quitaste" in view.notice and "aserradero" not in service._upgrades(KEY)["active"]
    set_hero(service, "test:2", backpack={"fibra": 5})
    service.act("test:2", "upg:tejeduria:s")                               # Bram gives a little
    assert "no se puede quitar" in service.act("test:1", "upstop:tejeduria").notice
    assert "tejeduria" in service._upgrades(KEY)["active"]
    assert "fundador o un 🤝 ayudante" in service.act("test:2", "upstop:canteria").notice


def test_old_buttons_a_founder_giving_activates_and_pages_stay_under_eight(service):
    two(service, 5)
    set_hero(service, "test:1", backpack={"madera": 5})
    view = service.act("test:1", "upg:aserradero")                         # an old 🤲 of the founder activates the work
    assert "Activaste" in view.notice and "aserradero" in service._upgrades(KEY)["active"]
    seen = set(all_pages(service, "test:1", "oficio")[0])
    assert {"upact:forja", "upact:joyeria", "upact:sastreria", "upg:aserradero:s"} <= seen
    assert not any(a.startswith(("upact:taller", "upact:herreria", "upact:braseros")) for a in seen)   # retired / level 6


def test_a_camp_of_before_keeps_its_half_built_works_active(service):
    two(service, 3)
    service.store.put("upgrades", KEY, {"built": {"fogon": 0.0}, "works": {"refugio": {"madera": 10}, "trueque": {}}, "tech": {}})
    record = service._upgrades(KEY)
    assert service._active_works(service.store.get("camp", KEY), record) == ["refugio"]   # materials given: active by itself
    view = service.act("test:2", "svc:casa")                               # a plain member sees it and can give
    assert "upg:refugio:s" in ids(view) and "Madera: 10/70" in text(view)
    set_hero(service, "test:2", backpack={"madera": 5})
    service.act("test:2", "upg:refugio:s")
    assert service._upgrades(KEY)["works"]["refugio"]["madera"] == 15


def test_old_taller_and_herreria_keep_their_stations_and_a_half_built_one_can_be_finished(service):
    two(service, 6)
    build(service, "taller")
    stations, where = service._stations_here(service._load("test:1"))
    assert where == "camp" and len(stations) == 10 and "canteria" in stations    # D-288: nothing lost
    assert "upact:taller" not in ids(service.act("test:1", "svc:oficio"))       # retired: not built again
    record = service._upgrades(KEY)
    record["works"]["herreria"] = {"piedra": 100}                              # a Herrería half built before 0.39
    service.store.put("upgrades", KEY, record)
    camp = service.store.get("camp", KEY)
    assert "herreria" in service._active_works(camp, service._upgrades(KEY))  # what was given is never lost
    set_hero(service, "test:2", backpack={"piedra": 5})
    service.act("test:2", "upg:herreria")                                      # any member can go on giving to it
    assert service._upgrades(KEY)["works"]["herreria"]["piedra"] == 105


@pytest.mark.usefixtures("instant_works", "every_profession_known")
def test_each_new_building_opens_its_station_and_the_old_services(service):
    two(service, 5)
    assert service._stations_here(service._load("test:1")) == ([], None)
    build(service, "curtiduria")
    assert service._stations_here(service._load("test:1")) == (["curtiduria"], "camp")
    build(service, "botica", "alambique", "forja")
    stations, _ = service._stations_here(service._load("test:1"))
    assert {"medicina", "destilacion", "herreria"} <= set(stations) and "joyeria" not in stations
    recipe = service.content.balance["currency"]["bag_recipe"]                 # 🪡 Sastrería: bags and chests, like the Taller
    set_hero(service, "test:1", backpack=dict(recipe), gold=500, bags=0)
    assert service.act("test:1", "ctaller").kind != "camp_workshop"
    build(service, "sastreria")
    view = service.act("test:1", "svc:oficio")
    assert "ctaller" in ids(view) and "Sastrería" in text(view)
    service.act("test:1", "tsew")
    assert service._load("test:1").bags == 1
    worn = set(service._load("test:1").gear.values())                         # 🔨 Forja: sells the gear you do not use
    piece = next(i for i, item in service.content.items.items() if item.get("kind") == "gear" and item.get("price") and i not in worn)
    set_hero(service, "test:1", backpack={piece: 1}, gold=0)
    assert f"sellg:{piece}" in ids(service.act("test:1", f"item:{piece}"))
    assert "Forja" in text(service.act("test:1", "svc:oficio"))


def test_the_type_screens_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    camp_at(service, 3)
    build(service, "refugio")
    service.act("test:1", "upact:fogon")
    for action in ("upsvc", "svc:casa", "svc:oficio", "svc:defensa", "upgrades", "upw", "gfund:svc"):
        view = service.act("test:1", action)
        assert "[" not in text(view), (action, text(view))
    assert service.act("test:1", "upsvc").actions[0].label == "🏠 Homes"
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
    set_level(service, 7)
    build(service, "biblioteca")
    assert "svc:saber" in ids(service.act("test:1", "upsvc"))
