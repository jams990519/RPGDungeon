"""SQLite store keeps data across restarts. [ES] Prueba de que el guardado en disco no pierde datos."""

from adapters.storage import SqliteStore


def test_sqlite_roundtrip(tmp_path):
    path = tmp_path / "game.sqlite3"
    store = SqliteStore(path)
    store.put("hero", "tg:1", {"name": "Lyra", "hp": 10})
    store.put("hero", "tg:1", {"name": "Lyra", "hp": 20})
    reopened = SqliteStore(path)
    assert reopened.get("hero", "tg:1") == {"name": "Lyra", "hp": 20}
    assert dict(reopened.items("hero")) == {"tg:1": {"name": "Lyra", "hp": 20}}
    reopened.delete("hero", "tg:1")
    assert reopened.get("hero", "tg:1") is None
