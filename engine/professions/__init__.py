"""M14 Professions: chained professions, phase 1 (D-109): gather -> refine -> craft.

[ES]
Para qué sirve: los oficios encadenados de la fase 1: el rango de cada oficio (1 a 100), su título, qué oficio
produce cada material, las cuentas de las recetas, los beneficios de oficio (D-111) y la ✒️ obra maestra (D-116,
rules.py). El catálogo está en content/professions.yaml; la
experiencia de oficio de cada héroe, en Hero.professions. Lo profundo (especializaciones, maestría por objeto,
exámenes, calidad) es propuesta (diseno/07-economia/profesiones.md §1 en adelante).
Documento de diseño: diseno/07-economia/profesiones.md §0
Módulo: M14 Oficios
Depende de: ninguno (los datos llegan de content/professions.yaml y content/balance.yaml, bloque professions)
Lo usan: engine/service/game.py y engine/core/content.py (las obras maestras derivadas, D-116)
Eventos que publica: ninguno (el servicio publica ItemCrafted y ProfessionRankUp)
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Sin tope duro de oficios (D-57): el freno es el costo natural (tiempo, materiales, estación).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (sección "professions")
    - Pruebas: tests/test_professions.py
"""

from engine.professions.rules import (
    branches_of,
    gatherer_of,
    masterwork_chance,
    masterwork_id,
    masterwork_items,
    max_times,
    missing_for,
    rank_of,
    rank_title,
    source_of,
    xp_for_rank,
)

__all__ = ["branches_of", "gatherer_of", "masterwork_chance", "masterwork_id", "masterwork_items", "max_times", "missing_for",
           "rank_of", "rank_title", "source_of", "xp_for_rank"]
