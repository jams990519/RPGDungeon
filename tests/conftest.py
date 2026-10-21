"""Shared test fixtures. [ES] Piezas comunes de las pruebas: un servicio con reloj fijo y guardado en memoria."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.core import FixedClock, MemoryStore, load_content  # noqa: E402
from engine.service import GameService  # noqa: E402


@pytest.fixture
def content():
    return load_content()


def legacy_content():
    """The content as it was before the 0.31 class patch: the 46 old specs active and the 12 chain specs retired.

    [ES] Para las pruebas del sistema viejo de talentos y barra (D-79), que sigue en el código para las especializaciones
    retiradas: se les quita el retiro a las viejas y se retiran las nuevas, solo en memoria (content/classes.yaml no cambia).
    """
    content = load_content()
    for cdef in content.classes.values():
        cdef.pop("migrate_to", None)
        if cdef.get("retired_in") == "0.31":
            cdef.pop("retired", None)
        elif cdef.get("system") == "chain":
            cdef["retired"] = True
    return content


@pytest.fixture
def clock():
    return FixedClock()


@pytest.fixture
def service(content, clock):
    return GameService(content, MemoryStore(), clock, world_seed=12345, time_scale=1.0)


def make_hero(service, account="test:1", name="Lyra", class_id="guerrero"):
    from engine.classes import default_spec, specs_of
    service.view(account)
    service.text(account, name)
    cdef = service.content.classes[class_id]
    if cdef.get("retired") and cdef.get("migrate_to"):      # 0.31: an old class id stands for the new class it maps to
        class_id = cdef["migrate_to"]
    group = service.content.classes[class_id].get("group", class_id)
    service.act(account, f"grp:{group}")
    specs = specs_of(service.content.classes, group)
    return service.act(account, f"cls:{class_id if class_id in specs else default_spec(service.content.classes, group)}")

@pytest.fixture
def every_profession_known(monkeypatch):
    """Tests about crafting itself (D-109 to D-141): every profession counts as learned.

    [ES] Desde la 0.33 los oficios se aprenden (D-257, con sus propias pruebas en test_aprender_oficios.py). Las pruebas de
    cómo se fabrica, se refina, se encanta o se especializa usan este arreglo para que todo oficio cuente como aprendido.
    Desde la 0.44 (D-306) las recetas de rango 25, 50 y 75 o más piden su 📚 libro de recetas: este arreglo también da todos
    los libros por comprados (los libros tienen sus propias pruebas en tests/test_tramos_de_recetas.py).
    """
    monkeypatch.setattr(GameService, "_knows", lambda self, hero, pid: True)
    monkeypatch.setattr(GameService, "_book_missing", lambda self, hero, rdef: [])


@pytest.fixture
def weak_wild_monsters(content):
    """Old tests where a strong hero (level 30) beats every monster outside: since 0.34 monsters match the hero (D-266).

    [ES] Desde la 0.34 los monstruos de afuera salen del nivel del héroe (balance.yaml wild_level). Las pruebas viejas que
    usan un héroe de nivel 30 para ganar seguro (lotes con peleas automáticas, cacería) bajan a los monstruos al nivel 1,
    solo en su contenido de prueba, para seguir probando lo mismo que antes.
    """
    content.balance["wild_level"] = {"below": 1000, "above": -1000}


@pytest.fixture
def auto_fights_on(content):
    """Tests of the automatic fights, switched off in the game since 0.33 (D-258): they turn them back on.

    [ES] Las peleas automáticas se apagaron (balance.yaml auto_fight.enabled: false) pero el código queda para volver; sus
    pruebas las prenden en su contenido de prueba para seguir cuidándolo.
    """
    content.balance["auto_fight"]["enabled"] = True


@pytest.fixture
def instant_works(content):
    """Tests of what a camp improvement costs and gives (not of its time): built the moment its materials are complete.

    [ES] Desde la 0.36 cada mejora, con sus materiales completos, se construye con el tiempo y los miembros presentes en el
    territorio (D-269.4, balance.yaml works.minutes_per_level). Las pruebas de costos y beneficios de las obras la ponen en 0,
    solo en su contenido de prueba: la obra queda construida al completarse, como antes. El tiempo de las obras se prueba en
    tests/test_gremio_desde_el_inicio.py.
    """
    content.balance["works"]["minutes_per_level"] = 0


@pytest.fixture
def old_member_caps(content):
    """Tests of the waiting line written with small camps (room for 2 at level 1, 2 more per level): that old count.

    [ES] Desde la 0.51 (D-253.1, D-327) el cupo es el de la etapa (balance.yaml camps.members_by_stage: campamento 10…). Las
    pruebas de la fila de espera del gremio (D-294, D-323), escritas con campamentos de 2 lugares, vacían esa tabla solo en su
    contenido de prueba: sin etapa en la tabla, el cupo vuelve a ser la cuenta de antes (camps.members_base +
    members_per_level, o el del gremio). El cupo por etapa se prueba en tests/test_escalera_cupo_oficiales.py.
    """
    content.balance["camps"]["members_by_stage"] = {}


def listed_recipes(service, account="test:1", branch="craft", every_page=True):
    """The recipe ids the 🪚 / 🛠️ / 🍲 list shows, in order, page by page (D-321: a list with /rN codes, not buttons).

    [ES] Para las pruebas de los oficios: lee el orden que guardó _station_view (gremio_codes "recipes") en cada página de
    la estación; con every_page=False, solo la primera página.
    """
    import re
    rids, page, total = [], 0, 1
    while page < total:
        view = service.act(account, f"est:{branch}:{page}")
        found = re.search(r"página \d+ de (\d+)|page \d+ of (\d+)", "\n".join(view.body))
        if page == 0 and found and every_page:
            total = int(next(g for g in found.groups() if g))
        rids += [code.split("|")[0] for code in (service.store.get("gremio_codes", account) or {}).get("recipes", [])]
        page += 1
    return rids


def pass_castle_waves(service, key="6:0"):
    """The camp at `key` passed the castle's 🌊 growing waves (D-122, D-329), straight in the store.

    [ES] Desde la 0.53 el paso a castillo pide también las oleadas crecientes (balance.yaml ladder.castle_waves: ganar 3 de 5).
    Las pruebas viejas que llegan a castillo, y que no prueban las oleadas, las dan por superadas con esto, como ya daban por
    ganada la 🌙 Noche de prueba ("trial_won"). Las oleadas tienen sus propias pruebas en
    tests/test_oleadas_crecientes_castillo.py.
    """
    need = int(service.content.balance["ladder"]["castle_waves"]["pass_wins"])
    camp = service.store.get("camp", key)
    camp["castle_waves"] = {"won": need, "lost": 0, "passed": True, "tries": 1}
    service.store.put("camp", key, camp)
