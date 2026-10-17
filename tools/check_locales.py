"""Compare two languages of the player texts: every key, placeholder, plural group, list length and HTML tag must match.

Usage:
    python tools/check_locales.py                 # content/locales: es (reference) against every other language
    python tools/check_locales.py es_part.yaml en_part.yaml   # two single files (used while translating)

[ES]
Para qué sirve: que ninguna traducción se quede corta. Compara el español (el idioma de referencia) con cada otro idioma
    (hoy el inglés, D-250): las mismas claves, los mismos huecos {nombre} y {n|uno|varios}, las mismas etiquetas HTML y
    el mismo largo en las listas que el motor usa por posición (los nombres de zona y las salas de mazmorra). Avisa,
    sin fallar, de los textos que quedaron iguales al español o con letras del español (á, ñ, ¿…).
Documento de diseño: diseno/01-plataforma/idiomas.md
Módulo: herramientas (M1 Núcleo, textos)
Depende de: engine/core/content.py (_read_texts), content/locales/*.yaml
Lo usan: tests/test_idiomas.py (las comprobaciones que fallan), quien traduce (a mano o con agentes)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (solo lee)
Reglas que nunca se rompen:
    1. El español manda: una clave nueva se escribe primero en es y en el mismo cambio en cada otro idioma.
    2. Las listas de POSITION_LISTS tienen el mismo largo en todos los idiomas (el motor elige por índice).
Si cambias esto, revisa: tests/test_idiomas.py y diseno/01-plataforma/idiomas.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from engine.core.content import _read_texts  # noqa: E402

# Lists the engine reads by position: same length in every language. [ES] Listas que el motor lee por posición.
POSITION_LISTS = {"world.name_first", "world.name_second", "dungeon.rooms", "dungeon.boss_rooms"}
# Lists of words that are matched against what the player types: free length. [ES] Palabras que se comparan con lo escrito.
FREE_LISTS = {"dudas.stopwords", "story.bio_clear_words", "story.journal_show_words"}

FIELD = re.compile(r"\{(\w+)(?:[:!][^{}|]*)?\}")
PLURAL = re.compile(r"\{(\w+)\|[^|{}]*\|[^|{}]*\}")
TAG = re.compile(r"</?([a-z]+)[^>]*>")
SPANISH = re.compile(r"[áéíóúñÁÉÍÓÚÑ¿¡]")


def flatten(node: Any, prefix: str = "") -> dict[str, Any]:
    """Dotted key -> leaf (str or list). [ES] Aplana el catálogo: "combat.victory" -> texto."""
    out: dict[str, Any] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            out.update(flatten(value, f"{prefix}.{key}" if prefix else str(key)))
    else:
        out[prefix] = node
    return out


def _shape(text: str) -> tuple[set[str], set[str], list[str]]:
    plurals = set(PLURAL.findall(text))
    fields = set(FIELD.findall(PLURAL.sub("", text)))
    return fields, plurals, sorted(TAG.findall(text))


def compare(ref: dict[str, Any], other: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) of `other` against the reference catalog. [ES] Errores (fallan) y avisos (no fallan)."""
    a, b = flatten(ref), flatten(other)
    errors: list[str] = []
    warnings: list[str] = []
    for key in sorted(a.keys() - b.keys()):
        errors.append(f"falta: {key}")
    for key in sorted(b.keys() - a.keys()):
        errors.append(f"sobra: {key}")
    for key in sorted(a.keys() & b.keys()):
        x, y = a[key], b[key]
        if isinstance(x, list) or isinstance(y, list):
            if not (isinstance(x, list) and isinstance(y, list)):
                errors.append(f"tipo distinto: {key}")
            elif key in POSITION_LISTS and len(x) != len(y):
                errors.append(f"largo distinto ({len(x)} y {len(y)}): {key}")
            elif key not in POSITION_LISTS and key not in FREE_LISTS and len(x) != len(y):
                warnings.append(f"lista de largo distinto ({len(x)} y {len(y)}): {key}")
            continue
        if not isinstance(x, str) or not isinstance(y, str):
            if type(x) is not type(y):
                errors.append(f"tipo distinto: {key}")
            continue
        fx, px, tx = _shape(x)
        fy, py, ty = _shape(y)
        if fx != fy:
            errors.append(f"huecos distintos {sorted(fx)} y {sorted(fy)}: {key}")
        if px != py:
            errors.append(f"plurales distintos {sorted(px)} y {sorted(py)}: {key}")
        if tx != ty:
            errors.append(f"etiquetas HTML distintas: {key}")
        if SPANISH.search(y):
            warnings.append(f"letras del español: {key}: {y[:60]}")
        elif x == y and re.search(r"[a-z]{4}", x) and len(x) > 12:
            warnings.append(f"igual al español: {key}: {y[:60]}")
    return errors, warnings


def languages(folder: Path) -> list[str]:
    """Languages with a main file (<lang>.yaml) in the folder. [ES] Los idiomas que tienen archivo principal."""
    return sorted(p.stem for p in folder.glob("*.yaml") if "_" not in p.stem)


def main(argv: list[str]) -> int:
    """Print the report; exit code 1 if there are errors. [ES] Imprime el informe; sale con 1 si hay errores."""
    if len(argv) == 2:
        load = lambda p: yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}   # noqa: E731
        pairs = [(f"{argv[0]} → {argv[1]}", load(argv[0]), load(argv[1]))]
    else:
        folder = ROOT / "content" / "locales"
        ref = _read_texts(folder, "es")
        pairs = [(f"es → {lang}", ref, _read_texts(folder, lang)) for lang in languages(folder) if lang != "es"]
    failed = False
    for name, ref, other in pairs:
        errors, warnings = compare(ref, other)
        print(f"== {name}: {len(errors)} errores, {len(warnings)} avisos")
        for line in errors:
            print("  ERROR", line)
        for line in warnings[:200]:
            print("  aviso", line)
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
