"""Content loader: game data lives in content/*.yaml, not in code.

Classes, enemies, biomes, items, balance numbers and player-facing texts are
data (architecture rule 4). Adding a class or an enemy means editing YAML.

[ES]
Para qué sirve: leer los archivos de contenido (clases, enemigos, biomas, objetos,
números de balance y textos) para que el motor no tenga datos escritos a mano.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §1 regla 4; convenciones §4
Módulo: M1 Núcleo
Depende de: content/*.yaml, PyYAML
Lo usan: engine/service/game.py, engine/core/i18n.py, tests
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (solo lee)
Reglas que nunca se rompen:
    1. Los IDs de contenido son estables: solo se agregan; para retirar algo, retired: true.
Si cambias esto, revisa:
    - Todos los catálogos: engine/classes, engine/enemies, engine/world
    - Pruebas: tests/test_content.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONTENT_DIR = Path(__file__).resolve().parents[2] / "content"


@dataclass
class Content:
    """All loaded content files.

    Attributes:
        classes: content/classes.yaml as a dict keyed by class id.
        enemies: content/enemies.yaml keyed by enemy id.
        biomes: content/biomes.yaml keyed by biome id.
        items: content/items.yaml keyed by item id.
        balance: content/balance.yaml (tunable numbers).
        texts: content/locales/<lang>.yaml (player-facing texts).

    [ES]
    Qué es: todo el contenido del juego cargado en memoria.
    Quién la usa: el servicio del juego y los catálogos.
    Si cambia, afecta: a todo módulo que lea contenido.
    """

    classes: dict[str, Any]
    enemies: dict[str, Any]
    biomes: dict[str, Any]
    items: dict[str, Any]
    balance: dict[str, Any]
    texts: dict[str, Any]


def _read(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return {k: v for k, v in data.items() if not (isinstance(v, dict) and v.get("retired"))}


def load_content(content_dir: Path | None = None, lang: str = "es") -> Content:
    """Load every content file from a directory.

    Args:
        content_dir: folder with the YAML files; defaults to the repo's content/.
        lang: language code for the texts file.

    Returns:
        A Content object.

    [ES]
    Qué hace: lee todos los archivos de contenido.
    La llaman: el servicio del juego al arrancar, y las pruebas.
    Si cambia, afecta: el arranque del juego.
    """
    base = content_dir or DEFAULT_CONTENT_DIR
    return Content(
        classes=_read(base / "classes.yaml"),
        enemies=_read(base / "enemies.yaml"),
        biomes=_read(base / "biomes.yaml"),
        items=_read(base / "items.yaml"),
        balance=_read(base / "balance.yaml"),
        texts=_read(base / "locales" / f"{lang}.yaml"),
    )
