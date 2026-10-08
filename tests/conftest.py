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
