"""Player-facing text lookup. The engine uses keys; texts live in content/locales.

[ES]
Para qué sirve: que ningún texto que ve el jugador esté escrito en el código. El
motor pide "combat.victory" y aquí se busca la frase en el archivo de idioma.
Documento de diseño: diseno/01-plataforma/web-y-multiplataforma.md §3.3 regla 5; CLAUDE.md §4
Módulo: M1 Núcleo
Depende de: engine/core/content.py, content/locales/es.yaml
Lo usan: engine/service/game.py, engine/combat/engine.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Una clave que falta no rompe el juego: se muestra la clave entre corchetes.
    2. Singular y plural: en el texto, {n|vez|veces} pone "vez" si n vale 1 y "veces" si no (D-89).
Si cambias esto, revisa:
    - Textos: content/locales/es.yaml
    - Pruebas: tests/test_content.py (comprueba que las claves usadas existan)
"""

from __future__ import annotations

import re
from typing import Any

# "{n|vez|veces}" -> "vez" when n == 1, else "veces" (singular and plural, D-89).
PLURAL = re.compile(r"\{(\w+)\|([^|{}]*)\|([^|{}]*)\}")


class Texts:
    """Dotted-key text catalog with str.format placeholders.

    [ES]
    Qué es: el diccionario de frases del juego.
    Quién la usa: el servicio y el combate para armar las vistas.
    Si cambia, afecta: todo lo que se muestra.
    """

    def __init__(self, catalog: dict[str, Any]) -> None:
        self._catalog = catalog
        self.missing: set[str] = set()

    def has(self, key: str) -> bool:
        """True if the key exists. [ES] Qué hace: dice si la frase existe. La llaman: pruebas. Si cambia, afecta: pruebas."""
        return self._lookup(key) is not None

    def _lookup(self, key: str) -> Any:
        node: Any = self._catalog
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        return node

    def list(self, key: str) -> list[str]:
        """Return a list of texts (for example, name parts). [ES] Qué hace: da una lista de frases. La llaman: el mapa (nombres de zonas). Si cambia, afecta: los nombres generados."""
        value = self._lookup(key)
        if not isinstance(value, list):
            self.missing.add(key)
            return []
        return [str(v) for v in value]

    def t(self, key: str, **values: Any) -> str:
        """Return the text for a key, formatted with values.

        [ES]
        Qué hace: da la frase lista para mostrar.
        La llaman: el servicio y el combate.
        Si cambia, afecta: todo el texto del juego.
        """
        text = self._lookup(key)
        if not isinstance(text, str):
            self.missing.add(key)
            return f"[{key}]"
        text = PLURAL.sub(lambda m: m.group(2) if values.get(m.group(1)) == 1 else m.group(3), text)
        try:
            return text.format(**values)
        except (KeyError, IndexError):
            return text
