"""Player-facing text lookup. The engine uses keys; texts live in content/locales, one catalog per language.

The language of each lookup is the one set for the current request (`Texts.use(lang)`, a context variable), so the
engine never passes a language around: GameService sets it once per player at every entry point (D-250).

[ES]
Para qué sirve: que ningún texto que ve el jugador esté escrito en el código. El
motor pide "combat.victory" y aquí se busca la frase en el archivo del idioma del jugador.
Desde la 0.33 (D-250) hay un catálogo por idioma (español e inglés). El idioma de cada búsqueda es el que puso el
servicio para el jugador que está jugando (Texts.use, una variable de contexto): así ninguna de las miles de
llamadas a t.t(...) tuvo que cambiar. Si una clave falta en inglés, se muestra la española y se anota en
`fallbacks` (las pruebas exigen que quede vacío).
Documento de diseño: diseno/01-plataforma/idiomas.md; web-y-multiplataforma.md §3.3 regla 5; CLAUDE.md §4
Módulo: M1 Núcleo
Depende de: engine/core/content.py (Content.locales), content/locales/<idioma>*.yaml
Lo usan: engine/service/game.py (y sus mixins), engine/combat/engine.py, chain_round.py y auto.py (por ctx.texts),
    tools/sim.py, tools/balance_report.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Una clave que falta no rompe el juego: en otro idioma se muestra la española; si falta en todos, la clave
       entre corchetes.
    2. Singular y plural: en el texto, {n|vez|veces} pone "vez" si n vale 1 y "veces" si no (D-89). Igual en inglés:
       {n|time|times}.
    3. El idioma por defecto (el español) es la referencia: toda clave existe primero ahí.
Si cambias esto, revisa:
    - Textos: content/locales/es*.yaml y en*.yaml (tools/check_locales.py los compara)
    - Pruebas: tests/test_content.py (las claves usadas existen) y tests/test_idiomas.py (los dos idiomas completos)
    - engine/service/game.py: _speaking (pone el idioma del jugador en cada entrada del motor)
"""

from __future__ import annotations

import re
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator

# "{n|vez|veces}" -> "vez" when n == 1, else "veces" (singular and plural, D-89).
PLURAL = re.compile(r"\{(\w+)\|([^|{}]*)\|([^|{}]*)\}")

# The language of the request being served (None = the default one). [ES] El idioma de lo que se está atendiendo.
_CURRENT: ContextVar[str | None] = ContextVar("lost_realms_lang", default=None)


class Texts:
    """Dotted-key text catalogs, one per language, with str.format placeholders.

    [ES]
    Qué es: el diccionario de frases del juego, uno por idioma (D-250).
    Quién la usa: el servicio y el combate para armar las vistas.
    Si cambia, afecta: todo lo que se muestra.
    """

    def __init__(self, catalog: dict[str, Any], catalogs: dict[str, dict[str, Any]] | None = None,
                 default: str = "es") -> None:
        self.default = default
        self._catalogs: dict[str, dict[str, Any]] = dict(catalogs or {})
        self._catalogs[default] = catalog
        self._catalog = catalog
        self.missing: set[str] = set()
        self.fallbacks: dict[str, set[str]] = {}

    # ------------------------------------------------------------------ languages

    @property
    def languages(self) -> list[str]:
        """Available language codes, the default first. [ES] Los idiomas que hay, el español primero."""
        return [self.default] + sorted(lang for lang in self._catalogs if lang != self.default)

    @property
    def lang(self) -> str:
        """Language of the current request. [ES] El idioma de lo que se está atendiendo ahora."""
        current = _CURRENT.get()
        return current if current in self._catalogs else self.default

    @contextmanager
    def use(self, lang: str | None) -> Iterator[None]:
        """Serve everything inside the `with` in that language (unknown or None = the default).

        [ES]
        Qué hace: todo lo que se arma dentro del `with` sale en ese idioma.
        La llaman: GameService._speaking (cada entrada del motor y cada aviso para otro jugador).
        Si cambia, afecta: el idioma de todas las pantallas.
        """
        token = _CURRENT.set(lang if lang in self._catalogs else None)
        try:
            yield
        finally:
            _CURRENT.reset(token)

    # ------------------------------------------------------------------ lookup

    @staticmethod
    def _find(catalog: dict[str, Any], key: str) -> Any:
        node: Any = catalog
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        return node

    def _lookup(self, key: str, lang: str | None = None, record: bool = True) -> Any:
        lang = lang if lang in self._catalogs else self.lang
        node = self._find(self._catalogs[lang], key)
        if node is None and lang != self.default:
            node = self._find(self._catalogs[self.default], key)
            if node is not None and record:
                self.fallbacks.setdefault(lang, set()).add(key)
        return node

    def has(self, key: str) -> bool:
        """True if the key exists. [ES] Qué hace: dice si la frase existe. La llaman: pruebas. Si cambia, afecta: pruebas."""
        return self._lookup(key, record=False) is not None

    def all_languages(self, key: str) -> list[str]:
        """The text of a key in every language (for example, to recognize an old keyboard button in any language).

        [ES]
        Qué hace: da la frase en todos los idiomas. La llaman: el servicio y Telegram, para entender un botón del menú
        de abajo escrito en el idioma que tenía el jugador antes de cambiarlo. Si cambia, afecta: esos botones.
        """
        out = []
        for lang in self.languages:
            value = self._find(self._catalogs[lang], key)
            if isinstance(value, str) and value not in out:
                out.append(value)
        return out

    def list(self, key: str, lang: str | None = None) -> list[str]:
        """Return a list of texts (for example, name parts). [ES] Qué hace: da una lista de frases. La llaman: el mapa (nombres de zonas). Si cambia, afecta: los nombres generados."""
        value = self._lookup(key, lang)
        if not isinstance(value, list):
            self.missing.add(key)
            return []
        return [str(v) for v in value]

    def t(self, key: str, **values: Any) -> str:
        """Return the text for a key, formatted with values.

        [ES]
        Qué hace: da la frase lista para mostrar, en el idioma del jugador.
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
