"""M14 Professions: chained professions, phase 1 (D-109): gather -> refine -> craft.

[ES]
Para qué sirve: los oficios encadenados de la fase 1: el rango de cada oficio (1 a 100), su título, qué oficio
produce cada material, las cuentas de las recetas, los beneficios de oficio (D-111), la ✒️ obra maestra (D-116,
rules.py), las cuentas del ✨ Encantamiento (D-115, fase 2: esencias, encantamiento por ranura, valor y costo), las de las
🎓 especializaciones (D-115, D-141: cuántas permite el rango, el dominio, lo que suma cada una, elegir o cambiar y su costo)
y, en la fase 2 (D-115), los beneficios de campamento y castillo (🎣 Pescador, 🍲 Cocina, 🗿 Cantería, 🏗️ Construcción),
que valen para el campamento con el mejor rango entre sus miembros (rules.py camp_perks). El catálogo está en
content/professions.yaml; la experiencia de oficio de cada héroe, en Hero.professions, y sus especializaciones en
Hero.prof_specs y Hero.spec_xp. Lo profundo (maestría por objeto, exámenes, calidad) es propuesta
(diseno/07-economia/profesiones.md §1 en adelante).
Documento de diseño: diseno/07-economia/profesiones.md §0; diseno/07-economia/red-de-oficios.md §3 (especializaciones) y §5
Módulo: M14 Oficios
Depende de: ninguno (los datos llegan de content/professions.yaml y content/balance.yaml, bloque professions)
Lo usan: engine/service/game.py y engine/core/content.py (las obras maestras derivadas, D-116)
Eventos que publica: ninguno (el servicio publica ItemCrafted y ProfessionRankUp)
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Sin tope duro de oficios (D-57): el freno es el costo natural (tiempo, materiales, estación).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (secciones "professions", "enchanting", "camp professions, phase 2" y
      "profession specializations")
    - Pruebas: tests/test_professions.py, tests/test_masterwork.py, tests/test_oficios_equipo.py,
      tests/test_oficios_campamento.py y tests/test_especializaciones.py
"""

from engine.professions.rules import (
    branches_of,
    disenchant_amount,
    disenchant_yield,
    enchant_cost,
    enchant_for_slot,
    enchant_value,
    gatherer_of,
    masterwork_chance,
    masterwork_id,
    masterwork_items,
    max_times,
    missing_for,
    rank_of,
    rank_title,
    source_of,
    spec_bonus,
    spec_choice,
    spec_finds,
    spec_held,
    spec_list,
    spec_owner,
    spec_share,
    spec_slots,
    switch_cost,
    xp_for_rank,
)

__all__ = ["branches_of", "disenchant_amount", "disenchant_yield", "enchant_cost", "enchant_for_slot", "enchant_value", "gatherer_of", "masterwork_chance", "masterwork_id", "masterwork_items", "max_times", "missing_for",
           "rank_of", "rank_title", "source_of", "spec_bonus", "spec_choice", "spec_finds", "spec_held", "spec_list", "spec_owner",
           "spec_share", "spec_slots", "switch_cost", "xp_for_rank"]
