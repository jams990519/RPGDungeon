"""Player time zones (D-124, confirmed; how it was applied: D-334, provisional; 0.58): every player sees clock times in the
zone they chose, while every rule (waves, the board's reset, the world clock, the Braseros' night) keeps one clock for
everyone (UTC seconds, as the engine always stored them).

A zone id is either a preset of balance.yaml time_zones.presets (an IANA zone such as "Europe/Madrid", with its summer
time when the server knows the zone, and a fixed offset to fall back on) or a fixed offset: "utc", "utc-5", "utc+1"
(whole hours from time_zones.offsets[0] to offsets[1]). The zone of the player being served lives in a context variable,
like the language of engine/core/i18n.py: GameService._speaking sets both for every entry point and every notice.

[ES]
Para qué sirve: que cada jugador vea las horas en su zona horaria (D-124, confirmada por el dueño: "cada jugador elige su
    zona horaria para ver las horas, pero los horarios de combate y de eventos son los mismos para todos"). Aquí solo hay
    cuentas puras: qué zonas existen, cuántos segundos le suma cada una a UTC en un instante (con el horario de verano si
    el servidor conoce la zona; si no, sus horas fijas), cómo se escribe una hora ("14:32") o una fecha ("23/10") y cómo se
    corre una hora para los botones ➖ 1 h / ➕ 1 h. Las reglas nunca pasan por aquí: siguen en segundos UTC.
Documento de diseño: diseno/02-mundo/mundo-vivo-y-viaje.md §2.1 (D-124, D-334); diseno/01-plataforma/web-y-multiplataforma.md
    (las horas llegan en UTC y cada uno las ve en su zona)
Módulo: M1 Núcleo (el reloj y lo que se muestra de él)
Depende de: zoneinfo de Python (si falta la zona, usa las horas fijas del preset); los datos llegan de content/balance.yaml,
    bloque time_zones (default, presets, offsets)
Lo usan: engine/service/game.py (_speaking fija la zona de quien juega o recibe un aviso) y engine/service/world_time.py
    (_clock, _tz_label, la pantalla 🕐 Zona horaria)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (la zona elegida se guarda en el espacio "prefs" del almacén, clave la cuenta = el héroe,
    campo "tz", como el idioma; la guarda engine/service/world_time.py)
Reglas que nunca se rompen:
    1. Solo cambia lo que se ve: ninguna regla del juego lee la zona de un jugador (D-124; el motor no sabe desde qué cliente
       ni desde qué país juega nadie, D-40, D-41).
    2. Una zona que no se conoce (borrada, mal escrita o de un preset retirado que ya no carga) nunca rompe una pantalla:
       vale la zona por defecto. Un preset retirado (retired: true) sigue convirtiendo para quien ya lo eligió (D-64).
    3. Los ids de los presets son estables (se guardan en "prefs"): solo se agregan; para sacar uno, retired: true.
Si cambias esto, revisa:
    - Servicio: engine/service/world_time.py (_clock, _tz_label, _tz_view, _tz_action) y engine/service/game.py (_speaking)
    - Datos: content/balance.yaml time_zones; textos tz.* en content/locales/es_dia_y_hora.yaml y en_dia_y_hora.yaml
    - Pruebas: tests/test_zona_horaria_y_dia.py
"""

from __future__ import annotations

import re
import time
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from functools import lru_cache
from typing import Any, Iterator, Mapping

try:                                    # Python 3.9+; the "tzdata" package fills it in where the system has no zone files
    from zoneinfo import ZoneInfo
except ImportError:                     # pragma: no cover - very old Python: presets fall back to their fixed offset
    ZoneInfo = None  # type: ignore[assignment]

UTC_ID = "utc"
FIXED_RE = re.compile(r"^utc([+-])(\d{1,2})$")
DEFAULT_RANGE = (-12, 14)

# The zone of the request being served (None = the default one). [ES] La zona de lo que se está atendiendo.
_CURRENT: ContextVar[str | None] = ContextVar("lost_realms_tz", default=None)


def current() -> str | None:
    """The zone id chosen by the player being served, or None. [ES] Qué hace: da la zona de quien se está atendiendo (None
    = nunca eligió). La llaman: engine/service/world_time.py. Si cambia, afecta: todas las horas que se muestran."""
    return _CURRENT.get()


@contextmanager
def use(zone_id: str | None) -> Iterator[None]:
    """Show every clock time built inside the `with` in that zone (None = the default zone).

    [ES]
    Qué hace: todo lo que se arma dentro del `with` muestra las horas en esa zona (como Texts.use con el idioma).
    La llaman: GameService._speaking (cada entrada del motor y cada aviso para otro jugador) y _tz_action (la pantalla de
    después de elegir ya muestra la hora nueva).
    Si cambia, afecta: las horas de todas las pantallas.
    """
    token = _CURRENT.set(zone_id or None)
    try:
        yield
    finally:
        _CURRENT.reset(token)


def offset_range(cfg: Mapping[str, Any]) -> tuple[int, int]:
    """The whole-hour offsets a player may pick with ➖ / ➕ (time_zones.offsets, default UTC−12 to UTC+14)."""
    raw = list(cfg.get("offsets") or DEFAULT_RANGE)
    low, high = int(raw[0]), int(raw[-1])
    return (min(low, high), max(low, high))


def fixed_id(hours: int) -> str:
    """The id of a fixed offset: 0 → "utc", −5 → "utc-5", 1 → "utc+1". [ES] El id de una hora fija."""
    hours = int(hours)
    return UTC_ID if hours == 0 else f"utc{hours:+d}"


def parse_fixed(zone_id: str | None) -> int | None:
    """Hours of a fixed-offset id ("utc" → 0, "utc-5" → −5), or None if it is not one. [ES] Lee un id de hora fija."""
    if zone_id == UTC_ID:
        return 0
    match = FIXED_RE.match(zone_id or "")
    if not match:
        return None
    hours = int(match.group(2))
    return -hours if match.group(1) == "-" else hours


def presets(cfg: Mapping[str, Any], include_retired: bool = False) -> list[dict[str, Any]]:
    """The one-tap zones, in data order (time_zones.presets); retired ones only if asked. [ES] Los botones de un toque."""
    return [dict(p) for p in cfg.get("presets") or [] if isinstance(p, Mapping) and p.get("id")
            and (include_retired or not p.get("retired"))]


def preset(cfg: Mapping[str, Any], zone_id: str | None) -> dict[str, Any] | None:
    """The preset with that id (also a retired one: whoever chose it keeps its clock, D-64), or None."""
    for entry in presets(cfg, include_retired=True):
        if entry["id"] == zone_id:
            return entry
    return None


def known(cfg: Mapping[str, Any], zone_id: str | None) -> bool:
    """True if the id is a preset or a fixed offset inside time_zones.offsets. [ES] Dice si la zona existe."""
    if not zone_id:
        return False
    if preset(cfg, zone_id) is not None:
        return True
    hours = parse_fixed(zone_id)
    low, high = offset_range(cfg)
    return hours is not None and low <= hours <= high


def resolve(cfg: Mapping[str, Any], zone_id: str | None) -> str:
    """The zone that applies: the chosen one if it exists, else time_zones.default, else "utc".

    [ES]
    Qué hace: la zona que vale para mostrar las horas: la elegida si existe; si no (nunca eligió o ya no existe), la de
    time_zones.default; y si esa tampoco, UTC.
    La llaman: offset_seconds y la pantalla 🕐 Zona horaria. Si cambia, afecta: lo que ven quienes nunca eligieron.
    """
    if known(cfg, zone_id):
        return str(zone_id)
    default = cfg.get("default", UTC_ID)
    return str(default) if known(cfg, default) else UTC_ID


@lru_cache(maxsize=64)
def _zoneinfo(name: str) -> Any:
    """The IANA zone, or None if this Python or this server does not know it (then the preset's fixed offset)."""
    if ZoneInfo is None or not name:
        return None
    try:
        return ZoneInfo(name)
    except Exception:       # unknown name, or no zone files and no tzdata package on the server
        return None


def offset_seconds(cfg: Mapping[str, Any], zone_id: str | None, when: float) -> int:
    """Seconds the zone adds to UTC at the instant `when` (summer time included when the server knows the zone).

    [ES]
    Qué hace: cuántos segundos le suma la zona a UTC en ese momento: una hora fija da siempre lo mismo; un preset usa su
    zona IANA (con el horario de verano: España +1 en invierno y +2 en verano) y, si el servidor no la conoce, sus horas
    fijas ("offset").
    La llaman: engine/service/world_time.py (_clock, _tz_label, los botones ➖ / ➕). Si cambia, afecta: todas las horas.
    """
    zid = resolve(cfg, zone_id)
    hours = parse_fixed(zid)
    if hours is not None:
        return hours * 3600
    entry = preset(cfg, zid) or {}
    zone = _zoneinfo(str(entry.get("tz") or ""))
    if zone is not None:
        try:
            delta = datetime.fromtimestamp(float(when), zone).utcoffset()
            if delta is not None:
                return int(delta.total_seconds())
        except (OverflowError, OSError, ValueError):
            pass
    return int(round(float(entry.get("offset", 0)) * 3600))


def local_time(when: float, offset: int) -> time.struct_time:
    """The wall clock of a zone at `when`, given its offset in seconds. [ES] La hora de pared en esa zona."""
    return time.gmtime(float(when) + int(offset))


def clock_text(when: float, offset: int) -> str:
    """"14:32": the hour and minutes in that zone (24-hour clock, the same in every language). [ES] La hora escrita."""
    stamp = local_time(when, offset)
    return f"{stamp.tm_hour:02d}:{stamp.tm_min:02d}"


def date_text(when: float, offset: int) -> str:
    """"23/10": the day and month in that zone (as the 📔 Diario always wrote it). [ES] La fecha escrita."""
    stamp = local_time(when, offset)
    return f"{stamp.tm_mday:02d}/{stamp.tm_mon:02d}"


def same_day(a: float, b: float, offset: int) -> bool:
    """True if both instants fall on the same calendar day in that zone. [ES] Dice si dos momentos son el mismo día allí."""
    one, two = local_time(a, offset), local_time(b, offset)
    return (one.tm_year, one.tm_yday) == (two.tm_year, two.tm_yday)


def offset_parts(offset: int) -> tuple[str, str]:
    """("−", "5") or ("+", "5:30") for an offset in seconds; ("", "") for UTC itself. [ES] Las partes de "UTC−5"."""
    if offset == 0:
        return "", ""
    sign = "−" if offset < 0 else "+"
    minutes = abs(int(offset)) // 60
    hours, rest = divmod(minutes, 60)
    return sign, f"{hours}" if not rest else f"{hours}:{rest:02d}"


def step(cfg: Mapping[str, Any], zone_id: str | None, when: float, delta: int) -> str:
    """The fixed zone one hour (delta) away from what the zone shows now, inside time_zones.offsets.

    [ES]
    Qué hace: el botón ➖ 1 h / ➕ 1 h: toma la hora que el jugador ve ahora (redondeada a horas enteras), le suma o resta
    una hora y devuelve esa hora fija ("utc-4"), sin salir de time_zones.offsets (de UTC−12 a UTC+14).
    La llama: engine/service/world_time.py (_tz_action). Si cambia, afecta: a qué zona llevan esos botones.
    """
    low, high = offset_range(cfg)
    hours = int(round(offset_seconds(cfg, zone_id, when) / 3600)) + int(delta)
    return fixed_id(max(low, min(high, hours)))
