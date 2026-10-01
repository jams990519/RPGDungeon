"""Storage port: the engine saves plain dicts by namespace and key.

The engine depends on this small interface, not on a database. MemoryStore
is for tests; adapters/storage/sqlite_store.py persists to disk; a
PostgreSQL store can replace it later without touching the rules.

[ES]
Para qué sirve: guardar y leer datos del juego (héroes, combates, zonas) sin que
el motor sepa qué base de datos hay detrás.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §7 (base de datos)
Módulo: M1 Núcleo
Depende de: ninguno
Lo usan: engine/service/game.py; adapters/storage/sqlite_store.py implementa la interfaz
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (cada módulo es dueño de su espacio de nombres)
Reglas que nunca se rompen:
    1. Lo que se guarda es JSON simple (dict, list, str, número, bool, None).
Si cambias esto, revisa:
    - Almacenamiento: adapters/storage/sqlite_store.py — debe cumplir la misma interfaz
    - Pruebas: tests/test_storage.py
"""

from __future__ import annotations

import copy
from typing import Any, Iterator


class Store:
    """Key-value storage grouped by namespace.

    Namespaces in use: "hero" (key = account id), "combat" (key = hero id),
    "zone" (key = "x:y", only zones changed by players), "meta".

    [ES]
    Qué es: la interfaz de guardado.
    Quién la usa: el servicio del juego.
    Si cambia, afecta: todos los almacenes (memoria, SQLite, el futuro PostgreSQL).
    """

    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        raise NotImplementedError

    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        raise NotImplementedError

    def delete(self, namespace: str, key: str) -> None:
        raise NotImplementedError

    def items(self, namespace: str) -> Iterator[tuple[str, dict[str, Any]]]:
        raise NotImplementedError


class MemoryStore(Store):
    """In-memory store for tests and the console client. [ES] Qué es: un guardado que se borra al cerrar. Quién la usa: pruebas. Si cambia, afecta: pruebas."""

    def __init__(self) -> None:
        self._data: dict[str, dict[str, dict[str, Any]]] = {}

    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        value = self._data.get(namespace, {}).get(key)
        return copy.deepcopy(value) if value is not None else None

    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        self._data.setdefault(namespace, {})[key] = copy.deepcopy(value)

    def delete(self, namespace: str, key: str) -> None:
        self._data.get(namespace, {}).pop(key, None)

    def items(self, namespace: str) -> Iterator[tuple[str, dict[str, Any]]]:
        for key, value in list(self._data.get(namespace, {}).items()):
            yield key, copy.deepcopy(value)
