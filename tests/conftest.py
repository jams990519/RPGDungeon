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


@pytest.fixture
def clock():
    return FixedClock()


@pytest.fixture
def service(content, clock):
    return GameService(content, MemoryStore(), clock, world_seed=12345, time_scale=1.0)


def make_hero(service, account="test:1", name="Lyra", class_id="guerrero"):
    service.view(account)
    service.text(account, name)
    return service.act(account, f"cls:{class_id}")
