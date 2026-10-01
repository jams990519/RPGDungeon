"""Hero record and derived stats.

[ES]
Para qué sirve: guardar al héroe y calcular sus estadísticas según clase y nivel.
Documento de diseño: diseno/03-personaje/progresion.md; diseno/03-personaje/balance.md
Módulo: M2 Héroe
Depende de: content/classes.yaml, content/balance.yaml (hero.xp_curve)
Lo usan: engine/service/game.py, engine/combat/engine.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "hero" del almacén (clave = id de cuenta)
Reglas que nunca se rompen:
    1. to_dict() y from_dict() van juntos: un campo nuevo necesita valor por defecto
       para que los héroes ya guardados sigan cargando.
Si cambias esto, revisa:
    - Almacén: héroes guardados en SQLite (campos nuevos con valor por defecto)
    - Números: classes.yaml base/per_level, balance.yaml hero.xp_curve
    - Pruebas: tests/test_service.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Hero:
    """A player's hero.

    Attributes:
        id: account id given by the client adapter (the engine does not parse it).
        name: hero name.
        class_id: id in content/classes.yaml.
        level, xp, gold: progression.
        hp: current health (max is derived).
        x, y: zone coordinates on the infinite map; (0, 0) is the Claro.
        activity: None or {"kind": "travel"|"explore", "until": ts, ...}.
        belt, backpack: item id -> count.
        last_regen_at: timestamp of the last passive health regeneration.
        known: zones this hero has visited, as "x:y" (its own map memory, D-61).

    [ES]
    Qué es: el héroe del jugador (en el diseño, "héroe").
    Quién la usa: el servicio lo crea, lo guarda y lo pasa al combate.
    Si cambia, afecta: los héroes guardados y todas las vistas.
    """

    id: str
    name: str
    class_id: str
    level: int = 1
    xp: int = 0
    gold: int = 0
    hp: int = 1
    x: int = 0
    y: int = 0
    activity: dict[str, Any] | None = None
    belt: dict[str, int] = field(default_factory=dict)
    backpack: dict[str, int] = field(default_factory=dict)
    last_regen_at: float = 0.0
    kills: int = 0
    zones_discovered: int = 0
    known: list[str] = field(default_factory=lambda: ["0:0"])

    def remembers(self, x: int, y: int) -> bool:
        """True if this hero has been in zone (x, y). [ES] Qué hace: dice si el héroe recuerda esa zona. La llaman: el servicio (mapa, rutas, lugares). Si cambia, afecta: qué ve cada héroe en su mapa."""
        return f"{x}:{y}" in self.known

    def remember(self, x: int, y: int) -> None:
        """Add zone (x, y) to the hero's memory. [ES] Qué hace: el héroe anota la zona en su memoria. La llaman: el servicio al llegar. Si cambia, afecta: el mapa personal."""
        key = f"{x}:{y}"
        if key not in self.known:
            self.known.append(key)

    def to_dict(self) -> dict[str, Any]:
        """Serialize for storage. [ES] Qué hace: lo convierte en datos guardables. La llaman: el servicio. Si cambia, afecta: el guardado."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Hero":
        """Load from storage, ignoring unknown fields. [ES] Qué hace: lo reconstruye desde lo guardado. La llaman: el servicio. Si cambia, afecta: la carga de héroes viejos."""
        known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**known)


def hero_stats(class_def: dict[str, Any], level: int) -> dict[str, float]:
    """Derived combat stats for a class at a level.

    Returns:
        dict with max_hp, attack, armor and initiative.

    [ES]
    Qué hace: calcula vida máxima, ataque, armadura e iniciativa.
    La llaman: el servicio (vista del héroe) y el combate.
    Si cambia, afecta: el balance de todas las clases.
    """
    base = class_def["base"]
    per = class_def.get("per_level", {})
    lv = max(1, level) - 1
    return {
        "max_hp": int(base["hp"] + per.get("hp", 0) * lv),
        "attack": float(base["attack"] + per.get("attack", 0) * lv),
        "armor": float(base.get("armor", 0.0)),
        "initiative": float(base.get("initiative", 10)),
    }


def xp_for_level(formula: dict[str, float], level: int) -> int:
    """Total xp needed to reach a level: base × (level − 1) ^ exponent. No level cap.

    [ES]
    Qué hace: dice cuánta experiencia total pide un nivel; crece rápido y no tiene tope (niveles infinitos).
    La llaman: el servicio al dar experiencia y en la vista del héroe.
    Si cambia, afecta: el ritmo de subida de nivel de todo el juego (balance.yaml hero.xp_formula).
    """
    if level <= 1:
        return 0
    return int(round(formula["base"] * (level - 1) ** formula["exponent"]))
