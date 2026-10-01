"""SQLite implementation of the engine's Store, with numbered migrations.

[ES]
Para qué sirve: guardar el juego en un archivo SQLite para que nada se pierda al
reiniciar el bot. Más adelante se puede cambiar por PostgreSQL con la misma interfaz.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §7 (base de datos, migraciones desde el día uno)
Módulo: adaptadores (almacenamiento)
Depende de: engine.core.Store, sqlite3 (biblioteca estándar)
Lo usan: adapters/telegram/bot.py, adapters/cli/play.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: el archivo de base de datos (RPG_DB_PATH)
Reglas que nunca se rompen:
    1. Las migraciones solo se agregan al final de MIGRATIONS; nunca se edita una ya aplicada.
Si cambias esto, revisa:
    - Datos de jugadores ya guardados (hacer una migración nueva, no editar las viejas)
    - Pruebas: tests/test_storage.py
"""

from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any, Iterator

from engine.core.store import Store

MIGRATIONS: list[str] = [
    "CREATE TABLE IF NOT EXISTS kv (namespace TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, PRIMARY KEY (namespace, key))",
]


class SqliteStore(Store):
    """Key-value store on one SQLite file.

    [ES]
    Qué es: el guardado en disco.
    Quién la usa: el bot de Telegram y la consola.
    Si cambia, afecta: los datos guardados de todos los jugadores.
    """

    def __init__(self, path: str | Path) -> None:
        path = Path(path)
        if str(path) != ":memory:":
            path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._migrate()

    def _migrate(self) -> None:
        with self._lock, self._conn:
            self._conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)")
            row = self._conn.execute("SELECT MAX(version) FROM schema_version").fetchone()
            current = row[0] or 0
            for number, sql in enumerate(MIGRATIONS, start=1):
                if number > current:
                    self._conn.execute(sql)
                    self._conn.execute("INSERT INTO schema_version (version) VALUES (?)", (number,))

    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute("SELECT value FROM kv WHERE namespace=? AND key=?", (namespace, key)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, namespace: str, key: str, value: dict[str, Any]) -> None:
        data = json.dumps(value, ensure_ascii=False)
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO kv (namespace, key, value) VALUES (?, ?, ?) "
                "ON CONFLICT(namespace, key) DO UPDATE SET value=excluded.value",
                (namespace, key, data),
            )

    def delete(self, namespace: str, key: str) -> None:
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM kv WHERE namespace=? AND key=?", (namespace, key))

    def items(self, namespace: str) -> Iterator[tuple[str, dict[str, Any]]]:
        with self._lock:
            rows = self._conn.execute("SELECT key, value FROM kv WHERE namespace=?", (namespace,)).fetchall()
        for key, value in rows:
            yield key, json.loads(value)
