"""Content loader: game data lives in content/*.yaml, not in code.

Classes, enemies, biomes, items, balance numbers and player-facing texts are
data (architecture rule 4). Adding a class or an enemy means editing YAML.

[ES]
Para qué sirve: leer los archivos de contenido (clases, enemigos, biomas, objetos,
números de balance y textos) para que el motor no tenga datos escritos a mano.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §1 regla 4; convenciones §4
Módulo: M1 Núcleo
Depende de: content/*.yaml, PyYAML; engine/professions/rules.py (masterwork_items: las ✒️ obras maestras que se
    derivan de cada pieza de artesano al cargar los objetos, D-116; ese módulo no importa nada del motor)
Lo usan: engine/service/game.py, engine/core/i18n.py, tests
    (content/camp_upgrades.yaml → Content.camp_upgrades: mejoras y conocimiento de los campamentos, D-101)
    (content/story.yaml → Content.story: orígenes, campaña, personajes, facciones y encargos, D-117)
    (content/guide.yaml → Content.guide: pasos del 🧭 camino guiado y avisos de una sola vez, D-190/D-193)
    (content/dungeons.yaml → Content.dungeons: familias de enemigos que llenan las mazmorras para uno, D-164/D-170)
    (content/faq.yaml → Content.faq: las preguntas de ❓ Dudas con su código, tema, palabras clave y relacionadas, D-191/D-192)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (solo lee)
Reglas que nunca se rompen:
    1. Los IDs de contenido son estables: solo se agregan; para retirar algo, retired: true.
    2. Las obras maestras (D-116) se derivan siempre igual de items.yaml y balance.yaml masterwork: mismo id
       (<pieza>_obra), así las que guardan los héroes siguen cargando. Una escrita a mano en items.yaml gana.
Si cambias esto, revisa:
    - Todos los catálogos: engine/classes, engine/enemies, engine/world, engine/professions (D-109), engine/story (D-117)
    - Obra maestra (D-116): Content.items trae también las piezas "<id>_obra" (source: masterwork); quien recorre todos
      los objetos las ve (nunca salen en el botín ni en el equipo inicial: tienen "source")
    - Pruebas: tests/test_content.py, tests/test_masterwork.py
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
        items: content/items.yaml keyed by item id, plus the masterwork twin of every crafted gear piece ("<id>_obra",
            source: masterwork, D-116), derived from balance.yaml "masterwork".
        balance: content/balance.yaml (tunable numbers).
        texts: content/locales/<lang>.yaml merged with <lang>_*.yaml (player-facing texts).
        guide: content/guide.yaml (the guided path, D-190/D-193: "steps" in order and one-time "tips"), read with retired
            entries kept (engine/service/guide.py leaves retired ones out; heroes keep the ids they have done).
        patches: content/patches.yaml (patch notes, D-67).
        camp_upgrades: content/camp_upgrades.yaml ("upgrades" and "knowledge" of player camps, D-101),
            read with retired entries kept (a built improvement keeps counting).
        professions: content/professions.yaml (chained professions, phase 1, D-109: "ranks", "professions",
            "stations" and "recipes"), read with retired entries kept (the service hides retired recipes).
        story: content/story.yaml (story and roleplay, D-117: "factions", "rank_rewards", "npcs", "origins",
            "chapters", "quests", "daily" and "camp_tasks"), read with retired entries kept (the service hides them).
        dungeons: content/dungeons.yaml (solo dungeons, D-164/D-170: "families" of enemies that fill a dungeon each day),
            read with retired entries kept (the service leaves retired families out).
        faq: content/faq.yaml (❓ Dudas, D-191/D-192: "topics", "popular" and "questions" with stable codes d01, d02...),
            read with retired entries kept (the service hides retired questions).

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
    guide: dict[str, Any] | None = None
    patches: dict[str, Any] | None = None
    camp_upgrades: dict[str, Any] | None = None
    professions: dict[str, Any] | None = None
    story: dict[str, Any] | None = None
    dungeons: dict[str, Any] | None = None
    faq: dict[str, Any] | None = None


def _read(path: Path, keep_retired: bool = False) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if keep_retired:
        return data
    return {k: v for k, v in data.items() if not (isinstance(v, dict) and v.get("retired"))}


def load_content(content_dir: Path | None = None, lang: str = "es") -> Content:
    """Load every content file from a directory.

    Args:
        content_dir: folder with the YAML files; defaults to the repo's content/.
        lang: language code for the texts file.

    Returns:
        A Content object.

    [ES]
    Qué hace: lee todos los archivos de contenido y agrega a los objetos las ✒️ obras maestras de cada pieza de
    artesano (D-116, engine/professions/rules.py masterwork_items).
    La llaman: el servicio del juego al arrancar, y las pruebas.
    Si cambia, afecta: el arranque del juego.
    """
    from engine.professions.rules import masterwork_items     # pure helper, no engine imports (no cycle)

    base = content_dir or DEFAULT_CONTENT_DIR
    items = _read(base / "items.yaml")
    balance = _read(base / "balance.yaml")
    items.update(masterwork_items(items, balance.get("masterwork")))     # D-116: ✒️ the masterwork twins
    return Content(
        classes=_read(base / "classes.yaml", keep_retired=True),
        enemies=_read(base / "enemies.yaml"),
        biomes=_read(base / "biomes.yaml"),
        items=items,
        balance=balance,
        texts=_read_texts(base / "locales", lang),
        guide=_read(base / "guide.yaml", keep_retired=True) if (base / "guide.yaml").exists() else {},
        patches=_read(base / "patches.yaml") if (base / "patches.yaml").exists() else {},
        camp_upgrades=_read(base / "camp_upgrades.yaml", keep_retired=True) if (base / "camp_upgrades.yaml").exists() else {},
        professions=_read(base / "professions.yaml", keep_retired=True) if (base / "professions.yaml").exists() else {},
        story=_read(base / "story.yaml", keep_retired=True) if (base / "story.yaml").exists() else {},
        dungeons=_read(base / "dungeons.yaml", keep_retired=True) if (base / "dungeons.yaml").exists() else {},
        faq=_read(base / "faq.yaml", keep_retired=True) if (base / "faq.yaml").exists() else {},
    )


def _merge(into: dict[str, Any], extra: dict[str, Any]) -> None:
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(into.get(key), dict):
            _merge(into[key], value)
        else:
            into[key] = value


def _read_texts(folder: Path, lang: str) -> dict[str, Any]:
    """Merge locales/<lang>.yaml with every locales/<lang>_*.yaml (for example es_clases.yaml)."""
    texts = _read(folder / f"{lang}.yaml")
    for extra in sorted(folder.glob(f"{lang}_*.yaml")):
        _merge(texts, _read(extra))
    return texts
