# Simulación de los oficios (18-oct-2026)

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Profesiones](profesiones.md), [Red de oficios](red-de-oficios.md), `content/professions.yaml`, `content/balance.yaml` · **Alimenta a:** las preguntas P-232 a P-235 ([Preguntas abiertas](../00-vision/preguntas-abiertas.md)), el [registro de balance](../03-personaje/balance.md) · **Estado:** revisión del código (lo que hay hoy) y propuesta (§8); nada de esto está decidido todavía

El dueño pidió (18-oct-2026) "un chequeo masivo de todas las profesiones": cuántos recursos pide cada una para aprender y para subir, qué hay que hacer en cada rango, y una simulación del progreso continuo, porque "las profesiones tienen que ser un camino lento, pero que se vea la progresión, que puedas vender lo que tienes, que lo que tienes te sirva para vender a otras clases". Este documento es esa revisión, hecha solo con lo que ya está en el código. Los scripts que la calculan quedaron fuera del repositorio (en la copia de trabajo de la sesión); los números se pueden recalcular con el motor.

## De dónde sale

- **World of Warcraft:** los colores de receta (naranja, amarillo, verde, gris) y los tramos de recetas por rango.
- **Albion Online:** la maestría por línea (hacer N piezas de un tramo para pasar al siguiente), §8.3.
- **El propio código de Lost Realms:** todos los números de hoy salen de `content/*.yaml` y del motor.

## 0. En pocas palabras

1. **Hoy cada oficio se sube al 100 repitiendo su receta más barata de rango 1.** La experiencia de cada receta es fija (12 por
   pieza de 2 ⚡, 6 por refinado de 1 ⚡) y no baja cuando tu rango pasa la receta. Herrería al 100 = **7.351 dagas forjadas**;
   Sastrería = 14.702 vendas; Alquimia = 14.702 tandas de pociones de vida. Fabricar siempre lo más nuevo cuesta 2,5 a 4,6 veces más
   energía para la misma experiencia (Herrería: 8.034 días frente a 2.246), así que el juego no da ningún motivo para hacerlo.
2. **La progresión casi no se ve.** Los oficios de equipo abren recetas en los rangos 1, 25 y 50 y después cada 5 rangos del 55 al
   100. Del rango 2 al 24 y del 26 al 49 no se abre nada, y hasta el rango 54 la pieza que sale es de nivel 3, 5 u 8 (un héroe pasa
   el nivel 10 en ~18 días). Los 6 oficios de refinado tienen **una sola receta en 100 rangos**; Alquimia y Medicina no tienen
   nada después del 50.
3. **El "1 año al 100" del diseño cuenta solo la energía de fabricar.** Con los materiales en la mochila, cualquier oficio de
   fabricación o refinado llega al 25 en 22 días, al 50 en 90 y al 100 en 368 (40 ⚡ al día; Alquimia, 281). Si el mismo jugador junta, caza y
   refina lo suyo, el 100 tarda **2,3 a 9,2 años** (Fundición 2,3; Sastrería 3,9; Herrería 6,2; Curtiduría 8,6; Peletería 9,2).
4. **El cuello de botella es la 🦌 piel:** sale solo del botín de bestias, ~4,4 ⚡ por piel (cazar = 2 ⚡ por presa, 0,45 pieles por
   presa en las mejores zonas). En la Herrería es el 47 % de toda la energía; en la Peletería el 60 %; en la Curtiduría el 88 %.
5. **Tres oficios casi no pueden subir:** 🏗️ Construcción (todas las obras del catálogo juntas dan 5.015 de experiencia: rango
   24 como máximo, aunque un solo jugador aportara todo), 🔪 Desollador (0,53 por ⚡: 9,6 años al 100) y 🎣 Pescador (0,66 peces por ⚡: 7,7
   años). ✨ Encantamiento depende de conseguir piezas: ~0,4 de experiencia por ⚡ si salen del botín.
6. **Lo que se fabrica no se le puede vender a otro jugador:** no hay mercado ni forma de pasar objetos. Pociones, vendas,
   ungüentos y botiquines tampoco se le venden al mercader (y el mercader vende la poción de vida y la venda). En el mercader, una
   pieza de rango 1 vale la mitad que lo crudo que lleva; desde el rango 55 vale unas 2 veces.
7. **La línea de malla de la 🦺 Peletería (67 recetas) hace equipo que ninguna clase activa usa** (D-208 quitó la malla) y es justo
   la receta más barata para subir la Peletería (la simulación la elige: 7.351 almófares de aprendiz).
8. **La regla nueva del dueño ("solo el 🧭 Explorador automático")** no cambia el ritmo una vez aprendido el oficio, pero quien
   recolecta sin aprenderlo no guarda experiencia (el código la tira), no saca la unidad de más ni los raros: 💠 gemas y 🌸 flores
   de luna solo saldrían de los nodos (5 % por vuelta). La Joyería sin el Minero pasa de 4,4 a 11,3 años.
9. **Recomendación principal:** tramos cada 5 rangos en todos los oficios (con nivel de pieza = rango), colores de receta (la
   experiencia cae cuando tu rango pasa la receta, como en WoW), experiencia que crece con el tramo, ingredientes intermedios por
   tramo (acero, tablón noble, tela fina, cuero grueso) y, primero que todo, el mercado entre jugadores. Detalle y números en el §8.

## 1. Cómo se hizo y de dónde sale cada número

| Qué | Valor | Dónde está |
|---|---|---|
| Experiencia total para el rango r | 9 × (r − 1)²; rango 25: 5.184 · 50: 21.609 · 100: 88.209 | `balance.yaml` professions.rank_formula, `engine/professions/rules.py` xp_for_rank |
| Energía | 40 por día (tope 50) | `balance.yaml` energy.per_day |
| Recolectar | 1 ⚡ por vuelta; (2 + nivel de zona ÷ 3) unidades en promedio, cada una sorteada entre los recursos de la zona según riqueza × lo que queda | `balance.yaml` gather.amount, energy.per_gather; `game.py` _gather_step |
| Cuánto sale de UN recurso | Medido con el motor (8 semillas de mundo, todas las zonas hasta Lejanía 12): en la mejor zona hasta Lejanía 6 salen ~1,4 a 1,5 unidades por ⚡ del recurso que buscas (madera 1,54 · metal 1,37 · fibra 1,50 · hierba 1,47 · piedra 1,54; los propios de terreno ~1,0 a 1,1; pescado 0,66). Fuera del Claro (madera 56 %, fibra 44 %), ningún recurso pasa del ~45 % de lo que da una vuelta | `world_stats.py` → `world_stats.json` (usa `_zone_resources`, `_zone`, `_zone_enemies`) |
| Unidad de más por rango | +0,3 % por rango al recolectar, desollar o refinar (rango 100: +30 %) | `balance.yaml` professions.rank_yield; `game.py` _trade_gather, _trade_loot, _make |
| Raros | 💠 gema (Minero) y 🌸 flor de luna (Herbolario) desde el rango 10: 5 % + 0,15 % por rango, por vuelta; nodos de su terreno: 5 % por vuelta | professions.rare_chance, rare_per_rank; `biomes.yaml` node_rare; nodes.rare_chance |
| Piel y carne | Solo de bestias. Cazar = 2 ⚡ por presa. Mejores zonas: 0,45 pieles y 0,60 carnes por presa (medido; la carne tiene 10 puntos más de probabilidad que la piel, 1 o 2 unidades) | hunt.energy; `enemies.yaml` loot; `items.yaml` loot_amount |
| Refinar y fabricar | Energía y experiencia fijas de cada receta | `professions.yaml` recipes |
| Vender al mercader | Mitad del precio, hacia abajo, al menos 1 por unidad; el equipo igual | shop.sell_ratio; `game.py` _sell_price, _sellable, _sell_gear |
| Clases y armaduras | 6 clases activas: guerrero y paladín (placas), druida y cazador (cuero), sacerdote y mago (tela) | `classes.yaml` (retired), `balance.yaml` gear.armor_by_group, weapons_by_group |

**Supuestos de la simulación:** gana todas las peleas, la zona tiene el recurso lleno, no viaja (moverse no gasta ⚡), sin 🎓
especialización, sin bono de origen, en el Claro (sin el +10 % del campamento). Aprende todos los oficios que usa (🥉20 cada uno).
Al recolectar cuenta solo lo que sirve para la receta: lo demás que sale en la vuelta (otros recursos, ~1 🥉 cada uno) no se usa,
así que la "cadena" es un techo. **Codiciosa** = en cada rango hace la receta disponible con más experiencia del oficio por ⚡ total
(fabricar + refinar + recolectar + cazar). **Lo más nuevo** = siempre la receta del rango más alto que tiene. La energía de los
raros se cuenta junto con la del mismo recolector (una vuelta de minería da metal y, a veces, gema): se toma la mayor de las dos.

## 2. Los oficios: cómo suben y qué abre cada tramo

### 2.1 Catálogo

| Oficio | Rama | ¿Se aprende hoy? | Cómo gana experiencia (código) | Recetas por rango (sin 🎓) | 🎓 exclusivas | Primera receta → lo que pide |
|---|---|---|---|---|---|---|
| 🪓 lenador | gather | no (auto) | 1 por unidad recolectada (gather_xp_per_unit) | — | — | — |
| ⛏️ minero | gather | no (auto) | 1 por unidad recolectada (gather_xp_per_unit) | — | — | — |
| 🌿 herbolario | gather | no (auto) | 1 por unidad recolectada (gather_xp_per_unit) | — | — | — |
| 🔪 desollador | gather | sí, 🥉20 | 1 por 🍖 carne o 🦌 piel del botín de bestias (_trade_loot) | — | — | — |
| 🧭 explorador | explore | no (auto) | 5 por vuelta de exploración + 6 al dejar una zona al 100 % (explorer.*); 12 por 🔭 reconocer (2 ⚡) | — | — | — |
| 🪚 aserradero | refine | sí, 🥉20 | 6 por vez que refinas (1 ⚡) | r1: 1 | — | tablon → madera ×3 |
| 🔥 fundicion | refine | sí, 🥉20 | 6 por vez que refinas (1 ⚡) | r1: 3 | — | lingote → pieza_metal ×2 |
| 💧 destilacion | refine | sí, 🥉20 | 6 por vez que refinas (1 ⚡) | r1: 2 | — | extracto → hierba_curativa ×3 |
| 🧶 tejeduria | refine | sí, 🥉20 | 6 por vez que refinas (1 ⚡) | r1: 3 | — | tela → fibra ×3 |
| 🪣 curtiduria | refine | sí, 🥉20 | 6 por vez que refinas (1 ⚡) | r1: 2 | — | cuero → piel ×2 |
| 🪑 carpinteria | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 2, r25: 2, r40: 1, r50: 2, r55: 2, r60: 2, r65: 2, r70: 3, r75: 2, r80: 2, r85: 2, r90: 2, r95: 2, r100: 2 | r25: 2, r50: 1, r100: 1 | baston_roble → tablon ×3, tela_tejida ×1 |
| 🔨 herreria | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 7, r25: 7, r50: 7, r55: 7, r60: 7, r65: 7, r70: 7, r75: 7, r80: 7, r85: 7, r90: 7, r95: 7, r100: 7 | r25: 2, r100: 2 | espada_forjada → lingote ×3, cuero_curtido ×1 |
| ⚗️ alquimia | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 3, r25: 3, r50: 1 | — | pocion_vida → extracto ×1, arcilla ×1 |
| 🪡 sastreria | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 6, r25: 5, r50: 5, r55: 5, r60: 5, r65: 5, r70: 5, r75: 5, r80: 5, r85: 5, r90: 5, r95: 5, r100: 5 | r25: 1, r100: 1 | vendas → tela_tejida ×1, hierba_curativa ×1 |
| 🦺 peleteria | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 10, r25: 10, r50: 10, r55: 10, r60: 10, r65: 10, r70: 10, r75: 10, r80: 10, r85: 10, r90: 10, r95: 10, r100: 10 | r25: 2, r100: 2 | jubon_cuero → cuero_curtido ×4, tela_tejida ×1 |
| 🩺 medicina | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 3, r25: 2, r50: 1 | — | unguento → extracto ×1, tela_tejida ×1 |
| 💍 joyeria | craft | sí, 🥉20 | xp fija de la receta (12 por pieza de 2 ⚡; 6 las de 1 ⚡; 24 los muebles de 4 ⚡) | r1: 1, r25: 1, r50: 1, r55: 1, r60: 1, r65: 1, r70: 1, r75: 1, r80: 1, r85: 1, r90: 1, r95: 1, r100: 1 | r25: 2, r100: 2 | anillo_engarzado → lingote ×1, gema_bruta ×1 |
| 💱 comercio | service | sí, 🥉20 | 1 por cada 🥉 de venta base al mercader, trueque o equipo (trade_xp_per_coin) | — | — | — |
| ✨ encantamiento | enchant | sí, 🥉20 | 6 por pieza desencantada (1 ⚡) y 12 por encantamiento (2 ⚡) | — | — | — |
| 🎣 pescador | gather | no (auto) | 1 por unidad recolectada (gather_xp_per_unit) | — | — | — |
| 🍲 cocina | craft | sí, 🥉20 | xp de la receta (6 por ⚡) | r1: 6, r25: 3, r50: 2, r75: 2, r100: 1 | — | racion_campamento → carne ×1, hierba_curativa ×1 |
| 🗿 canteria | refine | sí, 🥉20 | 6 por vez que refinas (1 ⚡) | r1: 3 | — | sillar → piedra ×3 |
| 🏗️ construccion | service | sí, 🥉20 | 1 por material crudo aportado a una obra o reparación (un tablón o sillar = 3) | — | — | — |

**Qué abre cada tramo (sin contar las 🎓 exclusivas):**

- 🔨 **Herrería** (7 por tramo): rango 1, espada, daga y peto forjados y 4 piezas de placas de nivel 3; 25, lo mismo "templado" (nivel 5);
  50, "del artesano" (nivel 8, con 💠 gema); del 55 al 100, cada 5 rangos, espada, daga, peto y las 4 piezas chicas del nivel 10, 20 … 100.
- 🦺 **Peletería** (10 por tramo): jubón y cota y 4 piezas de cuero y 4 de **malla** en cada tramo, mismos rangos que la Herrería.
- 🪡 **Sastrería**: rango 1, vendas, túnica y 4 piezas de tela; después 5 por tramo (túnica + 4 piezas), mismos rangos.
- 🪑 **Carpintería**: bastón y arco en cada tramo (1, 25, 50, 55 … 100); muebles 🛏️ literas (rango 40) y 🗄️ armero (70).
- 💍 **Joyería**: 1 receta por tramo (anillo, collar, amuleto y joyas del nivel 10 al 100). La primera ya pide 💠 gema.
- ⚗️ **Alquimia**: poción de vida (rango 1, con 2 variantes de terreno), poción mayor (25, con 2 variantes), pociones mayores ×2 (50). Nada más.
- 🩺 **Medicina**: ungüento (1, con 2 variantes), botiquín (25, con 1), vendaje de maestro (50). Nada más.
- 🍲 **Cocina**: ración y pescado asado (1, con 4 variantes), guiso (25), conservas (50), festín (75), banquete (100).
- 🪚 🔥 💧 🧶 🪣 🗿 **Refinado**: una receta (y sus variantes de terreno) desde el rango 1. Nunca otra.
- Todos: 🎓 primera especialización al 25 y segunda al 75 (`balance.yaml` specs.slots_at); sus recetas exclusivas piden 25 % de dominio
  (1.800 de experiencia del oficio con la especialización puesta, ~150 piezas) y el rango 25 o 100. ✒️ Obra maestra: hasta 5 % al rango
  100 (Carpintería 15 %). El beneficio de cada oficio crece parejo con el rango.

**Rango del oficio y nivel de la pieza que fabrica** (igual en Herrería, Peletería, Sastrería, Carpintería y Joyería):

| Rango del oficio | 1 | 25 | 50 | 55 | 60 | 65 | 70 | 75 | 80 | 85 | 90 | 95 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nivel de la pieza que sale | 3 | 5 | 8 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |

### 2.2 Tramos sin nada nuevo (rangos seguidos en los que no se abre ninguna receta)

| Oficio | Rangos con recetas nuevas | Tramo vacío más largo | Recetas (y xp) para llegar al primer tramo nuevo |
|---|---|---|---|
| aserradero | 1 | 99 rangos | nunca hay otra receta |
| fundicion | 1 | 99 rangos | nunca hay otra receta |
| destilacion | 1 | 99 rangos | nunca hay otra receta |
| tejeduria | 1 | 99 rangos | nunca hay otra receta |
| curtiduria | 1 | 99 rangos | nunca hay otra receta |
| carpinteria | 1, 25, 40, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100 | 23 rangos | rango 25: 5.184 xp = 432 veces la primera receta |
| herreria | 1, 25, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100 | 24 rangos | rango 25: 5.184 xp = 432 veces la primera receta |
| alquimia | 1, 25, 50 | 50 rangos | rango 25: 5.184 xp = 864 veces la primera receta |
| sastreria | 1, 25, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100 | 24 rangos | rango 25: 5.184 xp = 864 veces la primera receta |
| peleteria | 1, 25, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100 | 24 rangos | rango 25: 5.184 xp = 432 veces la primera receta |
| medicina | 1, 25, 50 | 50 rangos | rango 25: 5.184 xp = 864 veces la primera receta |
| joyeria | 1, 25, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100 | 24 rangos | rango 25: 5.184 xp = 432 veces la primera receta |
| cocina | 1, 25, 50, 75, 100 | 24 rangos | rango 25: 5.184 xp = 864 veces la primera receta |
| canteria | 1 | 99 rangos | nunca hay otra receta |

### 2.3 La curva (balance.yaml professions.rank_formula: 9 × (rango − 1)²)

| Rango | xp total | xp de este rango al siguiente | Piezas de 12 xp (total) | Refinados de 6 xp (total) |
|---|---|---|---|---|
| 2 | 9 | 27 | 1 | 2 |
| 5 | 144 | 81 | 12 | 24 |
| 10 | 729 | 171 | 61 | 122 |
| 20 | 3.249 | 351 | 271 | 542 |
| 25 | 5.184 | 441 | 432 | 864 |
| 40 | 13.689 | 711 | 1.141 | 2.282 |
| 50 | 21.609 | 891 | 1.801 | 3.602 |
| 55 | 26.244 | 981 | 2.187 | 4.374 |
| 60 | 31.329 | 1.071 | 2.611 | 5.222 |
| 75 | 49.284 | 1.341 | 4.107 | 8.214 |
| 90 | 71.289 | 1.611 | 5.941 | 11.882 |
| 100 | 88.209 | — | 7.351 | 14.702 |

## 3. Materiales: de dónde sale cada cosa y cuánto crudo lleva cada receta

- Los 6 recursos de base (madera, piedra, fibra, hierba, metal y arcilla) salen en manchas por todo el mapa; el terreno solo los
  favorece ("más en"). Los propios de terreno salen sobre todo en los terrenos de su lista ("propio de").
- **Ningún material está sin fuente** (todas las entradas de todas las recetas se pueden conseguir hoy), **no hay ciclos** (ningún
  refinado vuelve sobre sí mismo) y todas las salidas existen en `items.yaml`.
- **Solo botín:** 🦌 piel y 🍖 carne (bestias). **Solo con agua:** 🐟 pescado. **Raros con rango o nodo:** 💠 gema en bruto (Minero 10 o
  nodo de colinas, montaña, desierto, tundra, ruinas, volcán o cañón) y 🌸 flor de luna (Herbolario 10 o nodo de pradera, bosque,
  pantano, selva, sabana, bosque oscuro o lago). **Casi de un solo terreno:** 🖤 obsidiana (volcán; 30 % de las veces un propio sale
  de otro catálogo, D-185). En ~12 nodos hasta Lejanía 6 por mundo, ~4,6 son de gema y ~7,1 de flor de luna (medido).
- **Oficios con recetas solo de rango 1:** los 6 de refinado (Aserradero, Fundición, Destilación, Tejeduría, Curtiduría, Cantería).

### 3.1 Fuentes de cada material

| Material | Precio (venta al mercader) | Fuentes en el juego hoy | Bandera |
|---|---|---|---|
| arcilla | 2 (1) | recolección minero (más en: canon, lago); botín de 3 enemigos |  |
| arena | 2 (1) | recolección minero (propio de: desierto, ruinas, volcan, canon, lago) |  |
| bayas | 2 (1) | recolección herbolario (propio de: pradera, bosque, colinas, tundra, selva, sabana, canon, bosque_oscuro, lago) |  |
| cactus | 3 (1) | recolección herbolario (propio de: desierto, sabana, canon) |  |
| carbon | 3 (1) | recolección minero (propio de: colinas, montana, tundra, ruinas, volcan, canon, bosque_oscuro) |  |
| carne | 2 (1) | botín de bestias (desollador) | solo botín |
| chatarra | 3 (1) | recolección minero (propio de: desierto, ruinas, canon) |  |
| corteza | 2 (1) | recolección lenador (propio de: bosque, colinas, pantano, tundra, ruinas, selva, bosque_oscuro) |  |
| cuarzo | 5 (2) | recolección minero (propio de: colinas, montana, desierto, ruinas, volcan, canon) |  |
| cuero_curtido | 7 (3) | refinado: cuero, cuero_corteza |  |
| datiles | 3 (1) | recolección herbolario (propio de: desierto, selva, sabana) |  |
| extracto | 10 (5) | refinado: extracto, extracto_raiz |  |
| fibra | 2 (1) | recolección herbolario (más en: claro, pradera, bosque, pantano, desierto, selva, sabana, bosque_oscuro, lago); botín de 27 enemigos |  |
| flor_escarcha | 4 (2) | recolección herbolario (propio de: montana, tundra) |  |
| flor_luna | 12 (6) | raro de herbolario desde rango 10; nodos de pradera, bosque, pantano, selva, sabana, bosque_oscuro, lago (5 %/vuelta) | raro, con rango |
| gema_bruta | 15 (7) | raro de minero desde rango 10; nodos de colinas, montana, desierto, tundra, ruinas, volcan, canon (5 %/vuelta) | raro, con rango |
| hielo | 2 (1) | recolección minero (propio de: montana, tundra) |  |
| hierba_curativa | 3 (1) | recolección herbolario (más en: pradera, bosque, pantano, selva, bosque_oscuro, lago); botín de 32 enemigos; hallazgo al explorar |  |
| juncos | 2 (1) | recolección herbolario (propio de: pantano, lago) |  |
| lingote | 13 (6) | refinado: lingote, lingote_carbon, lingote_chatarra |  |
| lino | 2 (1) | recolección herbolario (propio de: pradera, pantano, sabana, lago) |  |
| madera | 2 (1) | recolección lenador (más en: claro, bosque, colinas, tundra, selva, sabana, bosque_oscuro); botín de 8 enemigos |  |
| mazorca | 2 (1) | recolección herbolario (propio de: pradera, colinas, sabana) |  |
| miel | 4 (2) | recolección herbolario (propio de: pradera, bosque, selva, sabana, bosque_oscuro) |  |
| musgo | 2 (1) | recolección herbolario (propio de: bosque, pantano, montana, tundra, ruinas, selva, volcan, bosque_oscuro, lago) |  |
| nenufar | 4 (2) | recolección herbolario (propio de: pantano, lago) |  |
| obsidiana | 5 (2) | recolección minero (propio de: volcan) | solo 🌋 volcán (o 30 % ajeno) |
| pescado | 2 (1) | recolección pescador (zonas con agua: pradera, bosque, pantano, selva, sabana, canon, bosque_oscuro, lago) | solo agua |
| piedra | 2 (1) | recolección minero (más en: pradera, colinas, montana, desierto, tundra, ruinas, sabana, volcan, canon); botín de 21 enemigos |  |
| piel | 3 (1) | botín de bestias (desollador) | solo botín |
| pieza_metal | 6 (3) | recolección minero (más en: colinas, montana, desierto, tundra, ruinas, volcan, canon); botín de 45 enemigos; hallazgo al explorar |  |
| raiz_amarga | 3 (1) | recolección herbolario (propio de: pradera, bosque, pantano, ruinas, selva, bosque_oscuro, lago) |  |
| resina | 3 (1) | recolección lenador (propio de: bosque, pantano, montana, tundra, selva, sabana, volcan, bosque_oscuro) |  |
| sal | 3 (1) | recolección minero (propio de: colinas, montana, desierto, volcan, canon) |  |
| setas | 3 (1) | recolección herbolario (propio de: pradera, bosque, pantano, ruinas, selva, bosque_oscuro, lago) |  |
| tablon | 7 (3) | refinado: tablon |  |
| tela_tejida | 7 (3) | refinado: tela, tela_lino, tela_juncos |  |
| tomillo | 3 (1) | recolección herbolario (propio de: pradera, colinas, montana, desierto, sabana, volcan, canon) |  |

### 3.2 Cuánto crudo pide una pieza, tramo por tramo

Con la receta de refinado de siempre (tablón = 3 maderas, lingote = 2 metales, tela = 3 fibras, cuero = 2 pieles, extracto = 3 hierbas).
La tabla completa, receta por receta (las 373 recetas de fabricación, con la energía de refinar), está en `anexo-recetas-a-crudo.md`.

| Línea | Lo crudo que pide una pieza en cada tramo (rango: crudo + raros) |
|---|---|
| 🔨 Espada (Herrería) | r1: 6 metal + 2 piel · r25: 10 metal + 4 piel · r50: 16 metal + 6 piel + 1 💠 · r55: 18 metal + 6 piel + 1 💠 · r75: 26 metal + 10 piel + 2 💠 · r100: 36 metal + 16 piel + 4 💠 |
| 🔨 Peto de placas (Herrería) | r1: 8 metal + 4 piel · r25: 14 metal + 6 piel · r50: 20 metal + 8 piel + 6 fibra · r55: 22 metal + 8 piel + 6 fibra · r75: 30 metal + 12 piel + 9 fibra + 1 💠 · r100: 40 metal + 18 piel + 15 fibra + 3 💠 |
| 🪑 Bastón (Carpintería) | r1: 9 madera + 3 fibra · r25: 15 madera + 6 fibra · r50: 24 madera + 9 fibra + 1 💠 · r55: 27 madera + 9 fibra + 1 💠 · r75: 39 madera + 15 fibra + 2 💠 + 1 🌸 · r100: 63 madera + 24 fibra + 4 💠 + 2 🌸 |
| 🪑 Arco (Carpintería) | r1: 9 madera + 2 piel · r25: 15 madera + 4 piel · r50: 24 madera + 6 piel + 3 fibra · r55: 27 madera + 6 piel + 3 fibra · r75: 45 madera + 10 piel + 6 fibra + 1 💠 · r100: 66 madera + 16 piel + 12 fibra + 3 💠 |
| 🪡 Túnica (Sastrería) | r1: 12 fibra + 2 piel · r25: 18 fibra + 3 hierba · r50: 27 fibra + 6 hierba + 1 🌸 · r55: 30 fibra + 6 hierba + 1 🌸 · r75: 45 fibra + 12 hierba + 2 🌸 · r100: 72 fibra + 21 hierba + 4 🌸 |
| 🦺 Jubón de cuero (Peletería) | r1: 8 piel + 3 fibra · r25: 12 piel + 6 fibra · r50: 18 piel + 9 fibra + 3 hierba · r55: 20 piel + 9 fibra + 3 hierba · r75: 28 piel + 15 fibra + 6 hierba + 1 💠 · r100: 42 piel + 24 fibra + 12 hierba + 3 💠 |
| 💍 Joya (Joyería) | r1: 2 metal + 1 💠 · r25: 4 metal + 2 💠 · r50: 6 metal + 3 💠 · r55: 6 metal + 3 💠 · r75: 12 metal + 6 💠 + 1 🌸 · r100: 16 metal + 11 💠 + 3 🌸 |
| ⚗️ Pociones (Alquimia) | r1: 3 hierba + 1 arcilla · r25: 6 hierba + 1 arcilla + 1 🌸 · r50: 9 hierba + 2 arcilla + 1 🌸 |
| 🩺 Remedios (Medicina) | r1: 3 hierba + 3 fibra · r25: 6 hierba + 3 fibra + 2 piel · r50: 6 hierba + 6 fibra + 1 🌸 |
| 🍲 Platos (Cocina) | r1: 1 carne + 1 hierba · r25: 2 carne + 2 pescado + 1 hierba · r50: 3 carne + 3 pescado + 1 arcilla + 3 hierba · r75: 4 carne + 4 pescado + 2 hierba + 1 🌸 · r100: 6 carne + 6 pescado + 6 hierba + 2 🌸 |

Una pieza del nivel 100 pide 6 a 10 veces el crudo de la de rango 1, pero da **la misma experiencia** (12). Por eso nadie sube con lo nuevo.

## 4. Simulación del avance

### 4.1 Resumen: días hasta el rango 25, 50 y 100 (40 ⚡ al día, todo a ese oficio)


"Solo su ⚡" = la cuenta del diseño (los materiales ya están en la mochila). "Cadena" = recolectar, cazar y refinar uno mismo. Cerca = Lejanía ≤ 3; media = ≤ 6; lejos = ≤ 12. "Lo más nuevo" = siempre la receta del rango más alto que tiene.

| Oficio | Solo su ⚡: r25 / r50 / r100 | Cadena media (codicioso): r25 / r50 / r100 | Cadena cerca | Cadena lejos | Cadena media, siempre lo más nuevo: r25 / r50 / r100 | Cadena media sin aprender la recolección |
|---|---|---|---|---|---|---|
| aserradero | 22 / 90 / 368 | 62 / 254 / 994 | 82 / 335 / 1.307 | 48 / 198 / 782 | 62 / 254 / 994 | 64 / 265 / 1.082 |
| fundicion | 22 / 90 / 368 | 52 / 215 / 850 | 66 / 271 / 1.069 | 42 / 172 / 686 | 52 / 215 / 850 | 53 / 222 / 905 |
| destilacion | 22 / 90 / 368 | 64 / 262 / 1.027 | 90 / 364 / 1.417 | 49 / 200 / 790 | 64 / 262 / 1.027 | 66 / 274 / 1.119 |
| tejeduria | 22 / 90 / 368 | 63 / 258 / 1.012 | 89 / 360 / 1.402 | 49 / 199 / 787 | 63 / 258 / 1.012 | 65 / 270 / 1.102 |
| curtiduria | 22 / 90 / 368 | 206 / 827 / 3.154 | 206 / 827 / 3.154 | 206 / 827 / 3.154 | 206 / 827 / 3.154 | 214 / 890 / 3.635 |
| carpinteria | 22 / 90 / 368 | 140 / 552 / 2.041 | 181 / 709 / 2.601 | 114 / 450 / 1.679 | 140 / 952 / 8.910 | 143 / 573 / 2.186 |
| herreria | 22 / 90 / 368 | 144 / 582 / 2.246 | 162 / 656 / 2.524 | 131 / 531 / 2.051 | 144 / 937 / 8.034 | 147 / 604 / 2.412 |
| alquimia | 22 / 73 / 281 | 103 / 411 / 1.561 | 137 / 546 / 2.057 | 80 / 320 / 1.223 | 103 / 547 / 2.285 | 105 / 425 / 1.659 |
| sastreria | 22 / 90 / 368 | 96 / 382 / 1.435 | 128 / 508 / 1.890 | 77 / 308 / 1.169 | 96 / 672 / 5.175 | 98 / 398 / 1.549 |
| peleteria | 22 / 90 / 368 | 222 / 886 / 3.352 | 242 / 970 / 3.668 | 207 / 827 / 3.130 | 222 / 948 / 8.491 | 228 / 934 / 3.705 |
| medicina | 22 / 90 / 368 | 119 / 430 / 1.590 | 160 / 565 / 2.063 | 92 / 337 / 1.261 | 119 / 430 / 2.086 | 122 / 451 / 1.728 |
| joyeria | 22 / 90 / 368 | 161 / 506 / 1.615 | 173 / 548 / 1.697 | 147 / 457 / 1.550 | 161 / 724 / 7.508 | 243 / 1.013 / 4.131 |
| cocina | 22 / 90 / 368 | 99 / 404 / 1.587 | 115 / 469 / 1.843 | 72 / 294 / 1.158 | 99 / 506 / 3.303 | 101 / 421 / 1.719 |
| canteria | 22 / 90 / 368 | 60 / 245 / 968 | 88 / 361 / 1.418 | 44 / 181 / 720 | 60 / 245 / 968 | 61 / 254 / 1.036 |

Lectura: "solo su ⚡" es la cuenta del diseño (y la de un especialista que recibe los materiales de otros); la "cadena" es lo que
tarda quien lo hace todo solo. La distancia entre las dos columnas es la energía que la economía tiene que poner en recolectar,
cazar y refinar para que un artesano llegue al 100: para la Herrería, ~75.000 ⚡ de otros (unos 5 años de un jugador a tiempo
completo); para la Peletería, ~119.000 ⚡ (de ellas 80.000 cazando).

### 4.2 Detalle por oficio (cadena, Lejanía ≤ 6, estrategia codiciosa)

Cada tabla: la receta que conviene en ese rango, cuántas veces se hizo en total, el crudo gastado, la energía (y en qué se fue) y
los rangos que de paso subieron los demás oficios.

#### aserradero

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | tablon | 24 (tablon 24) | madera 72 | — | 70 | 0 / 24 / 46 / 0 | 2 | 4 | lenador 3 |
| 10 | tablon | 122 (tablon 122) | madera 366 | — | 356 | 0 / 122 / 234 / 0 | 9 | 18 | lenador 7 |
| 25 | tablon | 864 (tablon 864) | madera 2.592 | — | 2.486 | 0 / 864 / 1.622 / 0 | 62 | 124 | lenador 17 |
| 50 | tablon | 3.602 (tablon 3.602) | madera 10.806 | — | 10.143 | 0 / 3.602 / 6.541 / 0 | 254 | 507 | lenador 35 |
| 75 | tablon | 8.214 (tablon 8.214) | madera 24.642 | — | 22.661 | 0 / 8.214 / 14.447 / 0 | 567 | 1.133 | lenador 53 |
| 100 | tablon | 14.702 (tablon 14.702) | madera 44.106 | — | 39.779 | 0 / 14.702 / 25.077 / 0 | 994 | 1.989 | lenador 71 |

#### fundicion

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | lingote | 24 (lingote 24) | pieza_metal 48 | — | 59 | 0 / 24 / 35 / 0 | 1 | 3 | minero 3 |
| 10 | lingote | 122 (lingote 122) | pieza_metal 244 | — | 298 | 0 / 122 / 176 / 0 | 7 | 15 | minero 6 |
| 25 | lingote | 864 (lingote 864) | pieza_metal 1.728 | — | 2.092 | 0 / 864 / 1.228 / 0 | 52 | 105 | minero 14 |
| 50 | lingote | 3.602 (lingote 3.602) | pieza_metal 7.204 | — | 8.582 | 0 / 3.602 / 4.980 / 0 | 215 | 429 | minero 29 |
| 75 | lingote | 8.214 (lingote 8.214) | pieza_metal 16.428 | — | 19.273 | 0 / 8.214 / 11.059 / 0 | 482 | 964 | minero 43 |
| 100 | lingote | 14.702 (lingote 14.702) | pieza_metal 29.404 | — | 33.993 | 0 / 14.702 / 19.291 / 0 | 850 | 1.700 | minero 58 |

#### destilacion

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | extracto | 24 (extracto 24) | hierba_curativa 72 | — | 73 | 0 / 24 / 49 / 0 | 2 | 4 | herbolario 3 |
| 10 | extracto | 122 (extracto 122) | hierba_curativa 366 | — | 368 | 0 / 122 / 246 / 0 | 9 | 18 | herbolario 7 |
| 25 | extracto | 864 (extracto 864) | hierba_curativa 2.592 | — | 2.570 | 0 / 864 / 1.706 / 0 | 64 | 129 | herbolario 17 |
| 50 | extracto | 3.602 (extracto 3.602) | hierba_curativa 10.806 | — | 10.482 | 0 / 3.602 / 6.880 / 0 | 262 | 524 | herbolario 35 |
| 75 | extracto | 8.214 (extracto 8.214) | hierba_curativa 24.642 | — | 23.409 | 0 / 8.214 / 15.195 / 0 | 585 | 1.170 | herbolario 53 |
| 100 | extracto | 14.702 (extracto 14.702) | hierba_curativa 44.106 | — | 41.077 | 0 / 14.702 / 26.375 / 0 | 1.027 | 2.054 | herbolario 71 |

#### tejeduria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | tela | 24 (tela 24) | fibra 72 | — | 72 | 0 / 24 / 48 / 0 | 2 | 4 | herbolario 3 |
| 10 | tela | 122 (tela 122) | fibra 366 | — | 363 | 0 / 122 / 241 / 0 | 9 | 18 | herbolario 7 |
| 25 | tela | 864 (tela 864) | fibra 2.592 | — | 2.532 | 0 / 864 / 1.668 / 0 | 63 | 127 | herbolario 17 |
| 50 | tela | 3.602 (tela 3.602) | fibra 10.806 | — | 10.326 | 0 / 3.602 / 6.724 / 0 | 258 | 516 | herbolario 35 |
| 75 | tela | 8.214 (tela 8.214) | fibra 24.642 | — | 23.065 | 0 / 8.214 / 14.851 / 0 | 577 | 1.153 | herbolario 53 |
| 100 | tela | 14.702 (tela 14.702) | fibra 44.106 | — | 40.480 | 0 / 14.702 / 25.778 / 0 | 1.012 | 2.024 | herbolario 71 |

#### curtiduria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | cuero | 24 (cuero 24) | piel 48 | — | 236 | 0 / 24 / 0 / 212 | 6 | 12 | desollador 4 |
| 10 | cuero | 122 (cuero 122) | piel 244 | — | 1.189 | 0 / 122 / 0 / 1.067 | 30 | 59 | desollador 8 |
| 25 | cuero | 864 (cuero 864) | piel 1.728 | — | 8.227 | 0 / 864 / 0 / 7.363 | 206 | 411 | desollador 22 |
| 50 | cuero | 3.602 (cuero 3.602) | piel 7.204 | — | 33.066 | 0 / 3.602 / 0 / 29.464 | 827 | 1.653 | desollador 44 |
| 75 | cuero | 8.214 (cuero 8.214) | piel 16.428 | — | 72.836 | 0 / 8.214 / 0 / 64.622 | 1.821 | 3.642 | desollador 66 |
| 100 | cuero | 14.702 (cuero 14.702) | piel 29.404 | — | 126.153 | 0 / 14.702 / 0 / 111.451 | 3.154 | 6.308 | desollador 88 |

#### carpinteria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | baston_roble | 12 (baston_roble 12) | madera 107, fibra 36 | — | 164 | 24 / 48 / 93 / 0 | 4 | 8 | aserradero 5, lenador 4, tejeduria 3, herbolario 2 |
| 10 | baston_roble | 61 (baston_roble 61) | madera 537, fibra 181 | — | 823 | 122 / 239 / 462 / 0 | 21 | 41 | aserradero 11, lenador 8, tejeduria 7, herbolario 5 |
| 25 | baston_roble | 432 (baston_roble 432) | madera 3.678, fibra 1.253 | — | 5.612 | 864 / 1.644 / 3.104 / 0 | 140 | 281 | aserradero 29, lenador 21, tejeduria 17, herbolario 12 |
| 50 | baston_roble | 1.801 (baston_roble 1.801) | madera 14.546, fibra 5.059 | — | 22.070 | 3.602 / 6.535 / 11.933 / 0 | 552 | 1.103 | aserradero 57, lenador 41, tejeduria 34, herbolario 24 |
| 75 | baston_roble | 4.107 (baston_roble 4.107) | madera 31.632, fibra 11.192 | — | 47.770 | 8.214 / 14.274 / 25.281 / 0 | 1.194 | 2.388 | aserradero 84, lenador 60, tejeduria 50, herbolario 36 |
| 100 | baston_roble | 7.351 (baston_roble 7.351) | madera 54.320, fibra 19.468 | — | 81.644 | 14.702 / 24.596 / 42.346 / 0 | 2.041 | 4.082 | aserradero 100, lenador 78, tejeduria 66, herbolario 47 |

#### herreria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | daga_forjada | 12 (daga_forjada 12) | pieza_metal 36, piel 18, carbon 12, corteza 6 | — | 164 | 24 / 18 / 43 / 79 | 4 | 8 | minero 3, desollador 3, fundicion 3, curtiduria 2 |
| 10 | daga_forjada | 61 (daga_forjada 61) | pieza_metal 182, piel 91, carbon 61, corteza 30 | — | 828 | 122 / 91 / 215 / 401 | 21 | 41 | fundicion 7, minero 6, desollador 5, curtiduria 5, lenador 2 |
| 25 | daga_forjada | 432 (daga_forjada 432) | pieza_metal 1.274, piel 640, carbon 425, corteza 213 | — | 5.756 | 864 / 638 / 1.482 / 2.772 | 144 | 288 | fundicion 17, minero 14, desollador 13, curtiduria 12, lenador 5 |
| 50 | daga_forjada | 1.801 (daga_forjada 1.801) | pieza_metal 5.223, piel 2.636, carbon 1.741, corteza 879 | — | 23.281 | 3.602 / 2.620 / 5.932 / 11.128 | 582 | 1.164 | fundicion 35, minero 28, desollador 27, curtiduria 25, lenador 10 |
| 75 | daga_forjada | 4.107 (daga_forjada 4.107) | pieza_metal 11.717, piel 5.941, carbon 3.906, corteza 1.980 | — | 51.583 | 8.214 / 5.886 / 13.009 / 24.473 | 1.290 | 2.579 | fundicion 52, minero 42, desollador 40, curtiduria 37, lenador 15 |
| 100 | daga_forjada | 7.351 (daga_forjada 7.351) | pieza_metal 20.643, piel 10.512, carbon 6.881, corteza 3.504 | — | 89.820 | 14.702 / 10.385 / 22.431 / 42.303 | 2.246 | 4.491 | fundicion 68, minero 56, desollador 53, curtiduria 49, lenador 20 |

#### alquimia

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | pocion_vida_resina | 24 (pocion_vida_resina 24) | hierba_curativa 71, resina 24 | — | 119 | 24 / 24 / 71 / 0 | 3 | 6 | destilacion 4, herbolario 3, lenador 2 |
| 10 | pocion_vida_resina | 122 (pocion_vida_resina 122) | hierba_curativa 360, resina 122 | — | 598 | 122 / 120 / 356 / 0 | 15 | 30 | destilacion 9, herbolario 7, lenador 4 |
| 25 | pocion_vida_resina | 864 (pocion_vida_resina 864) | hierba_curativa 2.475, resina 864 | — | 4.116 | 864 / 825 / 2.427 / 0 | 103 | 206 | destilacion 24, herbolario 17, lenador 10 |
| 50 | pocion_vida_resina | 3.602 (pocion_vida_resina 3.602) | hierba_curativa 9.871, resina 3.602 | — | 16.450 | 3.602 / 3.290 / 9.557 / 0 | 411 | 822 | destilacion 47, herbolario 34, lenador 21 |
| 75 | pocion_vida_resina | 8.214 (pocion_vida_resina 8.214) | hierba_curativa 21.620, resina 8.214 | — | 36.112 | 8.214 / 7.207 / 20.691 / 0 | 903 | 1.806 | destilacion 70, herbolario 50, lenador 31 |
| 100 | pocion_vida_resina | 14.702 (pocion_vida_resina 14.702) | hierba_curativa 37.275, resina 14.702 | — | 62.423 | 14.702 / 12.425 / 35.296 / 0 | 1.561 | 3.121 | destilacion 92, herbolario 65, lenador 41 |

#### sastreria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | vendas | 24 (vendas 24) | fibra 71, hierba_curativa 24 | — | 111 | 24 / 24 / 63 / 0 | 3 | 6 | herbolario 4, tejeduria 4 |
| 10 | vendas | 122 (vendas 122) | fibra 360, hierba_curativa 122 | — | 560 | 122 / 120 / 318 / 0 | 14 | 28 | tejeduria 9, herbolario 8 |
| 25 | vendas | 864 (vendas 864) | fibra 2.475, hierba_curativa 864 | — | 3.841 | 864 / 825 / 2.152 / 0 | 96 | 192 | tejeduria 24, herbolario 20 |
| 50 | vendas | 3.602 (vendas 3.602) | fibra 9.871, hierba_curativa 3.602 | — | 15.267 | 3.602 / 3.290 / 8.374 / 0 | 382 | 763 | tejeduria 47, herbolario 39 |
| 75 | vendas | 8.214 (vendas 8.214) | fibra 21.620, hierba_curativa 8.214 | — | 33.350 | 8.214 / 7.207 / 17.930 / 0 | 834 | 1.668 | tejeduria 70, herbolario 58 |
| 100 | vendas | 14.702 (vendas 14.702) | fibra 37.275, hierba_curativa 14.702 | — | 57.396 | 14.702 / 12.425 / 30.270 / 0 | 1.435 | 2.870 | tejeduria 92, herbolario 76 |

#### peleteria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | artesano_cabeza_malla_1 | 12 (artesano_cabeza_malla_1 12) | pieza_metal 36, piel 36, corteza 12, carbon 12 | — | 255 | 24 / 24 / 48 / 158 | 6 | 13 | desollador 4, minero 3, fundicion 3, curtiduria 3, lenador 2 |
| 10 | artesano_cabeza_malla_1 | 61 (artesano_cabeza_malla_1 61) | pieza_metal 182, piel 182, corteza 61, carbon 61 | — | 1.284 | 122 / 121 / 244 / 797 | 32 | 64 | desollador 7, fundicion 7, curtiduria 7, minero 6, lenador 3 |
| 25 | artesano_cabeza_malla_1 | 432 (artesano_cabeza_malla_1 432) | pieza_metal 1.274, piel 1.274, corteza 425, carbon 425 | — | 8.861 | 864 / 849 / 1.684 / 5.463 | 222 | 443 | desollador 19, fundicion 17, curtiduria 17, minero 14, lenador 7 |
| 50 | artesano_cabeza_malla_1 | 1.801 (artesano_cabeza_malla_1 1.801) | pieza_metal 5.223, piel 5.223, corteza 1.741, carbon 1.741 | — | 35.442 | 3.602 / 3.482 / 6.742 / 21.616 | 886 | 1.772 | desollador 37, fundicion 35, curtiduria 35, minero 28, lenador 14 |
| 75 | artesano_cabeza_malla_1 | 4.107 (artesano_cabeza_malla_1 4.107) | pieza_metal 11.717, piel 11.717, corteza 3.906, carbon 3.906 | — | 77.733 | 8.214 / 7.811 / 14.789 / 46.918 | 1.943 | 3.887 | desollador 56, fundicion 52, curtiduria 52, minero 42, lenador 21 |
| 100 | artesano_cabeza_malla_1 | 7.351 (artesano_cabeza_malla_1 7.351) | pieza_metal 20.643, piel 20.643, corteza 6.881, carbon 6.881 | — | 134.086 | 14.702 / 13.762 / 25.501 / 80.122 | 3.352 | 6.704 | desollador 74, fundicion 68, curtiduria 68, minero 56, lenador 28 |

#### medicina

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | unguento_cactus | 24 (unguento_cactus 24) | fibra 71, cactus 48 | — | 138 | 24 / 24 / 90 / 0 | 3 | 7 | herbolario 4, tejeduria 4 |
| 10 | unguento_cactus | 122 (unguento_cactus 122) | fibra 360, cactus 244 | — | 693 | 122 / 120 / 451 / 0 | 17 | 35 | herbolario 9, tejeduria 9 |
| 25 | unguento_cactus | 864 (unguento_cactus 864) | fibra 2.475, cactus 1.728 | — | 4.755 | 864 / 825 / 3.066 / 0 | 119 | 238 | tejeduria 24, herbolario 22 |
| 50 | botiquin_miel | 2.233 (botiquin_miel 1.369, unguento_cactus 864) | fibra 6.230, hierba_curativa 3.876, miel 2.738, cactus 1.728 | — | 17.196 | 3.602 / 3.369 / 10.225 / 0 | 430 | 860 | herbolario 41, tejeduria 38, destilacion 30 |
| 75 | botiquin_miel | 4.539 (botiquin_miel 3.675, unguento_cactus 864) | fibra 12.316, hierba_curativa 10.062, miel 7.350, cactus 1.728 | — | 37.036 | 8.214 / 7.459 / 21.362 / 0 | 926 | 1.852 | herbolario 60, tejeduria 53, destilacion 48 |
| 100 | botiquin_miel | 7.783 (botiquin_miel 6.919, unguento_cactus 864) | fibra 20.549, hierba_curativa 18.385, miel 13.838, cactus 1.728 | — | 63.587 | 14.702 / 12.978 / 35.908 / 0 | 1.590 | 3.179 | herbolario 78, tejeduria 68, destilacion 64 |

#### joyeria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | anillo_engarzado | 12 (anillo_engarzado 12) | pieza_metal 18, carbon 6 | gema_bruta 12 | 270 | 24 / 6 / 240 / 0 | 7 | 13 | minero 10, fundicion 2 |
| 10 | anillo_engarzado | 61 (anillo_engarzado 61) | pieza_metal 91, carbon 30 | gema_bruta 61 | 1.244 | 122 / 30 / 1.091 / 0 | 31 | 62 | minero 21, fundicion 5 |
| 25 | anillo_engarzado | 432 (anillo_engarzado 432) | pieza_metal 640, carbon 213 | gema_bruta 432 | 6.445 | 864 / 213 / 5.367 / 0 | 161 | 322 | minero 46, fundicion 12 |
| 50 | anillo_engarzado | 1.801 (anillo_engarzado 1.801) | pieza_metal 2.636, carbon 879 | gema_bruta 1.801 | 20.233 | 3.602 / 879 / 15.752 / 0 | 506 | 1.012 | minero 81, fundicion 25 |
| 75 | anillo_engarzado | 4.107 (anillo_engarzado 4.107) | pieza_metal 5.941, carbon 1.980 | gema_bruta 4.107 | 39.040 | 8.214 / 1.980 / 28.846 / 0 | 976 | 1.952 | minero 100, fundicion 37 |
| 100 | anillo_engarzado | 7.351 (anillo_engarzado 7.351) | pieza_metal 10.512, carbon 3.504 | gema_bruta 7.351 | 64.587 | 14.702 / 3.504 / 46.381 / 0 | 1.615 | 3.229 | minero 100, fundicion 49 |

#### cocina

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | pescado_asado | 24 (pescado_asado 24) | pescado 48, madera 24 | — | 112 | 24 / 0 / 88 / 0 | 3 | 6 | pescador 3, lenador 2 |
| 10 | pescado_asado | 122 (pescado_asado 122) | pescado 244, madera 122 | — | 566 | 122 / 0 / 444 / 0 | 14 | 28 | pescador 6, lenador 4 |
| 25 | pescado_asado | 864 (pescado_asado 864) | pescado 1.728, madera 864 | — | 3.958 | 864 / 0 / 3.094 / 0 | 99 | 198 | pescador 14, lenador 10 |
| 50 | pescado_asado | 3.602 (pescado_asado 3.602) | pescado 7.204, madera 3.602 | — | 16.165 | 3.602 / 0 / 12.563 / 0 | 404 | 808 | pescador 29, lenador 21 |
| 75 | pescado_asado | 8.214 (pescado_asado 8.214) | pescado 16.428, madera 8.214 | — | 36.148 | 8.214 / 0 / 27.934 / 0 | 904 | 1.807 | pescador 43, lenador 31 |
| 100 | pescado_asado | 14.702 (pescado_asado 14.702) | pescado 29.404, madera 14.702 | — | 63.492 | 14.702 / 0 / 48.790 / 0 | 1.587 | 3.175 | pescador 58, lenador 41 |

#### canteria

| Rango | Receta que hace | Veces (acum.) | Crudo consumido (acum.) | Raros | ⚡ total | ⚡: fabricar / refinar / recolectar / cazar | Días (100 %) | Días (50 %) | Otros oficios que subió |
|---|---|---|---|---|---|---|---|---|---|
| 5 | sillar_obsidiana | 24 (sillar_obsidiana 24) | piedra 24, obsidiana 24 | — | 67 | 0 / 24 / 43 / 0 | 2 | 3 | minero 3 |
| 10 | sillar_obsidiana | 122 (sillar_obsidiana 122) | piedra 122, obsidiana 122 | — | 341 | 0 / 122 / 219 / 0 | 9 | 17 | minero 6 |
| 25 | sillar_obsidiana | 864 (sillar_obsidiana 864) | piedra 864, obsidiana 864 | — | 2.392 | 0 / 864 / 1.528 / 0 | 60 | 120 | minero 14 |
| 50 | sillar_obsidiana | 3.602 (sillar_obsidiana 3.602) | piedra 3.602, obsidiana 3.602 | — | 9.798 | 0 / 3.602 / 6.196 / 0 | 245 | 490 | minero 29 |
| 75 | sillar_obsidiana | 8.214 (sillar_obsidiana 8.214) | piedra 8.214, obsidiana 8.214 | — | 21.974 | 0 / 8.214 / 13.760 / 0 | 549 | 1.099 | minero 43 |
| 100 | sillar_obsidiana | 14.702 (sillar_obsidiana 14.702) | piedra 14.702, obsidiana 14.702 | — | 38.705 | 0 / 14.702 / 24.003 / 0 | 968 | 1.935 | minero 58 |

### 4.3 Si siempre fabrica lo más nuevo que tiene (hasta el rango 100, cadena media)


| Oficio | Veces | Crudo consumido (lo principal) | 💠 gemas | 🌸 flores | ⚡ total | Días (100 %) |
|---|---|---|---|---|---|---|
| aserradero | 14.702 | madera 44.106 | 0 | 0 | 39.779 | 994 |
| fundicion | 14.702 | pieza_metal 29.404 | 0 | 0 | 33.993 | 850 |
| destilacion | 14.702 | hierba_curativa 44.106 | 0 | 0 | 41.077 | 1.027 |
| tejeduria | 14.702 | fibra 44.106 | 0 | 0 | 40.480 | 1.012 |
| curtiduria | 14.702 | piel 29.404 | 0 | 0 | 126.153 | 3.154 |
| carpinteria | 6.753 | madera 195.127, fibra 62.831, piel 11.049, corteza 3.683 | 9.882 | 4.654 | 356.387 | 8.910 |
| herreria | 7.351 | pieza_metal 89.314, piel 41.628, carbon 29.771, fibra 17.786 | 9.904 | 0 | 321.344 | 8.034 |
| alquimia | 8.468 | hierba_curativa 53.323, arcilla 11.100, flor_escarcha 4.108, cuarzo 2.054 | 0 | 5.550 | 91.388 | 2.285 |
| sastreria | 7.783 | fibra 171.145, hierba_curativa 51.205 | 0 | 10.553 | 207.018 | 5.175 |
| peleteria | 7.351 | pieza_metal 74.462, piel 47.096, fibra 36.795, carbon 24.821 | 5.839 | 0 | 339.654 | 8.491 |
| medicina | 7.783 | fibra 34.040, hierba_curativa 31.979, miel 2.738, cactus 1.728 | 0 | 5.550 | 83.428 | 2.086 |
| joyeria | 7.351 | pieza_metal 44.973, carbon 14.991 | 40.093 | 7.673 | 300.308 | 7.508 |
| cocina | 7.783 | pescado 24.360, carne 22.632, miel 6.488, bayas 6.488 | 0 | 0 | 132.105 | 3.303 |
| canteria | 14.702 | piedra 14.702, obsidiana 14.702 | 0 | 0 | 38.705 | 968 |

### 4.4 Oficios de recolección


Una vuelta de recolección = 1 ⚡. Unidades de ese oficio por vuelta en su mejor zona (medido): lenador 2,45 (≤6) / 1,55 (≤3); minero 3,49 (≤6) / 2,46 (≤3); herbolario 3,73 (≤6) / 2,65 (≤3); pescador 0,66 (≤6) / 0,45 (≤3). Desollador: por presa (2 ⚡) 0,45 piel + 0,60 carne en las mejores zonas. Más 0,3 % de unidad extra por rango.

| Oficio | Rango 10 (unid. / días) | Rango 25 | Rango 50 | Rango 100 | Qué abre |
|---|---|---|---|---|---|
| lenador | 729 / 7 d | 5.184 / 50 d | 21.609 / 201 d | 88.209 / 754 d | nada propio (sin raro); 🎓 al 25 y al 75; +10 mochila al 100 |
| minero | 729 / 5 d | 5.184 / 35 d | 21.609 / 141 d | 88.209 / 529 d | 💠 gema desde el 10 (5 % por vuelta, +0,15 %/rango); 🎓 al 25 y al 75; +5 % vida al 100 |
| herbolario | 729 / 5 d | 5.184 / 33 d | 21.609 / 132 d | 88.209 / 495 d | 🌸 flor de luna desde el 10; 🎓 al 25 y al 75; +20 % regeneración al 100 |
| pescador | 729 / 27 d | 5.184 / 187 d | 21.609 / 745 d | 88.209 / 2.795 d | nada propio; 🎓 al 25 y al 75; +30 % pescado en la despensa (beneficio de campamento) |
| desollador | 729 / 34 d | 5.184 / 235 d | 21.609 / 937 d | 88.209 / 3.514 d | nada propio; 🎓 al 25 y al 75; +4 % ataque al 100 |

**Según dónde recolecta** (días hasta los rangos 10 / 25 / 50 / 100; el Desollador no cambia: depende de las presas, no de la zona):

| Oficio | Unidades por ⚡ (≤3 · ≤6 · ≤12) | Lejanía ≤ 3: r10 / r25 / r50 / r100 (días) | Lejanía ≤ 6 | Lejanía ≤ 12 |
|---|---|---|---|---|
| lenador | 1,55 · 2,45 · 3,55 | 12 / 80 / 317 / 1.190 | 7 / 50 / 201 / 754 | 5 / 35 / 139 / 520 |
| minero | 2,46 · 3,49 · 5,55 | 7 / 50 / 200 / 751 | 5 / 35 / 141 / 529 | 3 / 22 / 89 / 332 |
| herbolario | 2,65 · 3,73 · 5,77 | 7 / 47 / 185 / 695 | 5 / 33 / 132 / 495 | 3 / 21 / 85 / 320 |
| pescador | 0,45 · 0,66 · 1,02 | 40 / 274 / 1.093 / 4.100 | 27 / 187 / 745 / 2.795 | 17 / 121 / 481 / 1.804 |
| desollador | 0,53 · 0,53 · 0,53 | 34 / 235 / 937 / 3.514 | 34 / 235 / 937 / 3.514 | 34 / 235 / 937 / 3.514 |

- El diseño dice que un recolector dedicado llega al 100 en 9 a 11 meses: se cumple para Minero (11 meses) y Herbolario (10,5) recolectando
  hasta Lejanía 12 (zonas de nivel ~10). El Leñador tarda la mitad más (en cada zona sus recursos son menos de la mitad). El
  🎣 Pescador y el 🔪 Desollador quedan fuera de toda escala.
- **Stock:** cada recurso de cada zona se vacía con ~42 unidades y vuelve ~24 por día (`balance.yaml` stock); un recolector dedicado tiene
  que rotar 3 o 4 zonas por recurso. El stock es de la zona, compartido por todos: cerca del Claro van a competir.

### 4.5 Exploración, servicio y artes arcanas

#### 🧭 Explorador (automático)

Rinde ~6,2 xp por ⚡ explorando (5 por vuelta + 6 por zona completa; una zona pide ~4,9 vueltas). Días hasta el rango: r5 1, r10 3, r25 21, r50 86, r75 195, r100 347 (40 ⚡ al día). Abre: tiempos de viaje y 🔭 reconocer al 10, campamentos cercanos al 25, 🕵️ infiltrarse y reconocer a 2 zonas al 30, todo el mapa y 3 zonas al 50, la fuerza de los campamentos al 75, título al 100 (balance.yaml explorer.ranks).

#### 💱 Comercio (se aprende)

1 xp por 🥉 de venta base. Vender todo lo que se recolecta da 7,29 🥉 por vuelta en la mejor zona (Lejanía ≤ 6; mediana 4,1; ≤ 12: 11,06). Con 7 🥉 por ⚡: rango 25 en 18 días, 50 en 74, 100 en 302 (vendiendo todo lo que se junta, sin gastar ⚡ extra: sube solo al jugar). Vender equipo fabricado suma mucho de una vez (una pieza de nivel 100 paga ~280 🥉 = 280 xp).

#### 🏗️ Construcción (se aprende; solo miembros de campamento)

1 xp por material crudo aportado. **Todas** las mejoras del catálogo (content/camp_upgrades.yaml) piden juntas 5.015 unidades de crudo (contando tablón y sillar como 3). Aunque un solo jugador aportara todo, llegaría al rango 24. Reparar defensas: 12 crudo por punto dañado, 1 o 2 puntos por oleada semanal (12 a 24 xp por semana para todo el campamento). El rango 100 (88.209 xp) equivale a ~17,6 campamentos enteros construidos por una sola persona: **hoy es inalcanzable**. Además el propio beneficio de la Construcción baja lo que piden las obras.

#### ✨ Encantamiento (se aprende)

Desencantar: 6 xp por 1 ⚡, pero hace falta una pieza. Del botín: 15 % por victoria (nivel < 10; 10 % desde el 10), una presa = 2 ⚡ → ~13,3 ⚡ de caza por pieza → ~0,42 xp por ⚡. Fabricando la pieza más barata (🗡️ daga forjada: 2 lingotes + 1 cuero, cadena media) cuesta ~13,7 ⚡ + 1 ⚡ al desencantar → ~0,41 xp por ⚡ (más 12 de Herrería). Encantar da 12 xp por 2 ⚡ pero pide 3+ esencias (1,6 por pieza común del botín) y un material. Rango 100 desencantando botín: ~14.702 piezas.

## 5. Economía: ¿vale la pena lo que se fabrica?


Venta al mercader = mitad del precio, redondeado hacia abajo, al menos 1 por unidad (GameService._sell_price; el equipo igual, _sell_gear). Pociones, vendas, ungüentos y botiquines **no se pueden vender** (no son material ni comida: _sellable).

| Receta | Rango | Sale (venta) | Lo refinado que entra (venta) | Lo crudo que entra (venta) | Venta salida ÷ venta crudo | ⚡ cadena media | 🥉 de más por ⚡ frente a vender lo crudo | Quién lo usa (clases activas) |
|---|---|---|---|---|---|---|---|---|
| tablon (aserradero) | 1 | tablon: 3 | 3 | 3 | 1,00 | 2,7 | 0,00 | — |
| lingote (fundicion) | 1 | lingote: 6 | 6 | 6 | 1,00 | 2,3 | 0,00 | — |
| extracto (destilacion) | 1 | extracto: 5 | 3 | 3 | 1,67 | 2,8 | 2,00 | — |
| tela (tejeduria) | 1 | tela_tejida: 3 | 3 | 3 | 1,00 | 2,7 | 0,00 | — |
| cuero (curtiduria) | 1 | cuero_curtido: 3 | 2 | 2 | 1,50 | 8,7 | 1,00 | — |
| baston_roble (carpinteria) | 1 | artesano_baston_1: 10 | 12 | 12 | 0,83 | 11,4 | -0,37 | druida, mago, paladin, sacerdote |
| baston_labrado (carpinteria) | 25 | artesano_baston_2: 25 | 21 | 21 | 1,19 | 18,5 | 0,49 | druida, mago, paladin, sacerdote |
| baculo_artesano (carpinteria) | 50 | artesano_baston_3: 50 | 40 | 40 | 1,25 | 36,9 | 0,86 | druida, mago, paladin, sacerdote |
| espada_forjada (herreria) | 1 | artesano_espada_1: 10 | 21 | 20 | 0,50 | 13,4 | -2,59 | guerrero, paladin |
| espada_templada (herreria) | 25 | artesano_espada_2: 25 | 36 | 34 | 0,74 | 23,1 | -1,71 | guerrero, paladin |
| espada_artesano (herreria) | 50 | artesano_espada_3: 50 | 64 | 61 | 0,82 | 34,5 | -1,55 | guerrero, paladin |
| pocion_vida (alquimia) | 1 | pocion_vida: no se vende | 6 | 4 | — | 4,3 | — | todos |
| pocion_mayor (alquimia) | 25 | pocion_mayor: no se vende | 17 | 13 | — | 12,7 | — | todos |
| pociones_mayores (alquimia) | 50 | pocion_mayor: no se vende | 23 | 17 | — | 15,5 | — | todos |
| vendas (sastreria) | 1 | venda: no se vende | 4 | 4 | — | 4,0 | — | todos |
| tunica_tenida (sastreria) | 25 | artesano_tela_2: 25 | 23 | 21 | 1,19 | 18,7 | 0,49 | mago, sacerdote |
| tunica_artesano (sastreria) | 50 | artesano_tela_3: 50 | 43 | 39 | 1,28 | 28,2 | 0,95 | mago, sacerdote |
| jubon_cuero (peleteria) | 1 | artesano_cuero_1: 10 | 15 | 11 | 0,91 | 29,4 | -0,21 | cazador, druida |
| jubon_reforzado (peleteria) | 25 | artesano_cuero_2: 25 | 24 | 18 | 1,39 | 44,3 | 1,07 | cazador, druida |
| jubon_artesano (peleteria) | 50 | artesano_cuero_3: 50 | 41 | 30 | 1,67 | 67,8 | 2,07 | cazador, druida |
| anillo_engarzado (joyeria) | 1 | artesano_joya_1: 10 | 13 | 13 | 0,77 | 11,6 | -1,22 | cazador, druida, guerrero, mago, paladin, sacerdote |
| collar_gemas (joyeria) | 25 | artesano_joya_2: 25 | 26 | 26 | 0,96 | 21,1 | -0,34 | cazador, druida, guerrero, mago, paladin, sacerdote |
| amuleto_artesano (joyeria) | 50 | artesano_joya_3: 50 | 39 | 39 | 1,28 | 30,7 | 3,24 | cazador, druida, guerrero, mago, paladin, sacerdote |
| unguento (medicina) | 1 | unguento: no se vende | 8 | 6 | — | 5,8 | — | todos |
| botiquin (medicina) | 25 | botiquin: no se vende | 16 | 11 | — | 15,5 | — | todos |
| vendaje_maestro (medicina) | 50 | vendaje_maestro: no se vende | 22 | 18 | — | 14,6 | — | todos |
| espada_nivel_10 (herreria) | 55 | artesano_espada_4: 75 | 70 | 67 | 1,12 | 36,2 | 1,06 | guerrero, paladin |
| espada_nivel_50 (herreria) | 75 | artesano_espada_8: 167 | 107 | 102 | 1,64 | 57,5 | 6,27 | guerrero, paladin |
| espada_nivel_100 (herreria) | 100 | artesano_espada_13: 282 | 160 | 152 | 1,86 | 96,8 | 9,22 | guerrero, paladin |
| arco_nivel_10 (carpinteria) | 55 | artesano_arco_4: 75 | 39 | 36 | 2,08 | 44,2 | 3,23 | cazador |
| arco_nivel_50 (carpinteria) | 75 | artesano_arco_8: 167 | 73 | 68 | 2,46 | 82,2 | 5,18 | cazador |
| arco_nivel_100 (carpinteria) | 100 | artesano_arco_13: 282 | 123 | 115 | 2,45 | 140,3 | 5,89 | cazador |
| tunica_nivel_10 (sastreria) | 55 | artesano_tela_4: 75 | 46 | 42 | 1,79 | 30,6 | 2,65 | mago, sacerdote |
| tunica_nivel_50 (sastreria) | 75 | artesano_tela_8: 167 | 77 | 69 | 2,42 | 47,4 | 5,29 | mago, sacerdote |
| tunica_nivel_100 (sastreria) | 100 | artesano_tela_13: 282 | 131 | 117 | 2,41 | 76,0 | 5,70 | mago, sacerdote |
| jubon_nivel_10 (peleteria) | 55 | artesano_cuero_4: 75 | 44 | 32 | 2,34 | 74,1 | 4,25 | cazador, druida |
| jubon_nivel_50 (peleteria) | 75 | artesano_cuero_8: 167 | 74 | 56 | 2,98 | 115,4 | 7,60 | cazador, druida |
| jubon_nivel_100 (peleteria) | 100 | artesano_cuero_13: 282 | 128 | 99 | 2,85 | 189,3 | 8,24 | cazador, druida |
| joya_nivel_10 (joyeria) | 55 | artesano_joya_4: 75 | 39 | 39 | 1,92 | 30,7 | 10,60 | cazador, druida, guerrero, mago, paladin, sacerdote |
| joya_nivel_50 (joyeria) | 75 | artesano_joya_8: 167 | 84 | 84 | 1,99 | 68,4 | 17,33 | cazador, druida, guerrero, mago, paladin, sacerdote |
| joya_nivel_100 (joyeria) | 100 | artesano_joya_13: 282 | 143 | 143 | 1,97 | 133,0 | 24,30 | cazador, druida, guerrero, mago, paladin, sacerdote |
| sillar (canteria) | 1 | sillar: 3 | 3 | 3 | 1,00 | 2,7 | 0,00 | — |
| racion_campamento (cocina) | 1 | racion_campamento: 1 | 2 | 2 | 0,50 | 4,5 | -1,00 | — |
| guiso_cazador (cocina) | 25 | guiso_cazador: 5 | 5 | 5 | 1,00 | 11,0 | 0,00 | — |
| conserva (cocina) | 50 | conserva: 9 | 12 | 10 | 0,90 | 17,9 | -0,35 | — |
| festin (cocina) | 75 | festin: 13 | 16 | 16 | 0,81 | 28,0 | -1,50 | — |
| banquete (cocina) | 100 | banquete: 22 | 34 | 30 | 0,73 | 47,2 | -2,14 | — |

De 341 recetas de equipo, en 59 la pieza vale en el mercader **menos** que lo crudo que lleva.

**Lo que dice la tabla:**

- Refinar casi no cambia el valor (tablón, lingote, tela y sillar valen lo mismo que lo crudo; extracto y cuero algo más por el redondeo).
- Las piezas de equipo de rango 1 se venden por 0,5 a 0,9 veces lo crudo que llevan (se pierde); las de rango 25 y 50, entre 0,7 y 1,7; desde el
  rango 55, entre 1,1 y 3 veces (se gana, sobre todo en Joyería, Peletería y Carpintería). La prueba de D-113 ("se vende por menos que sus
  materiales", `tests/test_balance_d110.py`) compara con el precio de compra de los materiales, no con lo que el mercader paga por ellos.
- Pociones, vendas, ungüentos y botiquines no se pueden vender (no son material ni comida). Lo cocinado sí se le vende al mercader (es comida
  con código), aunque `items.yaml` dice que no; vale menos que lo crudo.
- **Lo fabricado es mejor que el botín del mismo nivel**, pero poco: hasta el nivel 8 es la misma pieza con un bono chico (+1 % de vida en el
  arma, +1 % de ataque en la armadura); del nivel 10 al 100, 🟣 épica con ~10 % más que la 🔵 rara del botín (ej. peto del 100: vida 0,44 y
  defensa 0,07 frente a 0,40 y 0,06). El botín suelta pieza en 10-15 % de las victorias.

### 5.1 Para quién es lo que se fabrica (clases activas y su armadura, balance.yaml gear)

| Tipo | Clases activas que lo usan entero | Oficio | Recetas (pecho + cabeza/manos/piernas/pies + 🎓) |
|---|---|---|---|
| baston | druida, mago, paladin, sacerdote | carpinteria | 13 |
| arco | cazador | carpinteria | 15 |
| espada | guerrero, paladin | herreria | 15 |
| daga | cazador, druida | herreria | 13 |
| placas | guerrero, paladin | herreria | 67 |
| tela | mago, sacerdote | sastreria | 67 |
| cuero | cazador, druida | peleteria | 67 |
| malla | **ninguna** (rinde la mitad para cualquiera: gear.off_type_factor 0,5) | peleteria | 67 |
| joya | cazador, druida, guerrero, mago, paladin, sacerdote | joyeria | 17 |

- **Para otras clases:** hoy un jugador no puede darle ni venderle nada a otro. Quien sube la Herrería hace placas para guerreros y paladines
  que nunca le van a llegar; si su clase no usa placas, solo puede venderlas al mercader. El objetivo del dueño ("que lo que haces valga para
  venderlo, sobre todo a otras clases") necesita el mercado entre jugadores (2.ª tanda de la economía, D-109/D-113, todavía sin hacer).
- Cada armadura tiene 2 clases clientes; la malla, ninguna. El arco, 1 (cazador). La joya, las 6.

## 6. Diseño frente a código: lo que no coincide

| # | Documento | Qué dice | Qué hace el código o los datos |
|---|---|---|---|
| 1 | `profesiones.md` §0.1, `balance.yaml` professions | Rango 25 en ~3 semanas, 50 en ~3 meses, 100 en ~1 año | Cierto solo contando la energía de fabricar o refinar. Con la cadena propia: 2,3 a 9,2 años (§4.1) |
| 2 | `profesiones.md` §0.1 | Un recolector dedicado llega al 100 en 9 a 11 meses | Minero y Herbolario sí (lejos); Leñador 17 a 39 meses; Pescador 5 a 11 años; Desollador 9,6 años (§4.4) |
| 3 | `profesiones.md` §0.4, `balance.yaml` camp_professions | 🏗️ Construcción al 100 en ~1 a 1,5 años | Las obras tienen tope: todo el catálogo da 5.015 de experiencia (rango 24). Inalcanzable (§4.5) |
| 4 | D-208, `oficios-repaso-2-oct.md` | Ya no hay malla | 67 recetas de malla, `espec_malla_*`, la 🎓 ⛓️ Malla ligera de la Peletería, su beneficio `armor_type: [cuero, malla]` y la 🎓 Aleaciones de la Fundición (obra maestra en malla) siguen activos |
| 5 | `items.yaml` (comidas) y `profesiones.md` §0.4 | El mercader no compra lo cocinado | `_sellable` lo compra (comida con código, D-261); solo el trueque del campamento no |
| 6 | D-113, `profesiones.md` §0.1 | El equipo fabricado se vende por menos que sus materiales | Por menos que su precio de compra; frente a lo que el mercader paga por los materiales, desde el rango 55 se gana ~2 veces (§5) |
| 7 | `profesiones.md` §0.1 (tabla de cómo sube) | Minero: piedra, metal o arcilla | También carbón, sal, cuarzo, arena, hielo, chatarra y obsidiana (D-183); Herbolario y Leñador igual |
| 8 | `profesiones.md` §0.4 | En el pantano ~1 de cada 4 unidades es pescado | Medido: el pescado es como mucho ~15-18 % de una vuelta (1 de cada 6) |
| 9 | `profesiones.md` §0.0, D-257 | Recolección y exploración suben solas | Correcto hoy; el dueño ya decidió que solo el Explorador (todavía no está en el código ni registrado como decisión; el próximo número libre es D-264) |
| 10 | `oficios-repaso-2-oct.md` (D-194) | Refinar pasa a ser estructura del asentamiento; gemas refinadas por la Joyería (D-198); ranuras de gemas (D-199) | Nada de eso está en el código (el documento lo dice: "solo diseño") |

## 7. La regla nueva: solo el 🧭 Explorador sube solo

Lo que pidió el dueño: la recolección también se aprende (🪓 Leñador, ⛏️ Minero, 🌿 Herbolario, 🎣 Pescador, como ya el 🔪 Desollador);
sin el oficio, recolectar da igual los recursos de base.

**Cómo queda con el código de hoy si solo se quita `learn: auto` de esos 4 oficios en `content/professions.yaml`:**

- Recolectar sin el oficio da los recursos de siempre (eso ya funciona así: `_gather_step` no mira el oficio), pero **sin la unidad de más,
  sin experiencia y sin raros**: `_prof_rank` da 0, `_prof_gain` no suma nada y el raro pide rango 10. Lo que juntes antes de aprender
  **no cuenta después** (la experiencia no se guarda). Recomiendo guardarla como "práctica" hasta un tope (por ejemplo, hasta el rango 5) o
  avisar en la primera recolección "aprende ⛏️ Minero para que esto cuente".
- 💠 gemas y 🌸 flores de luna: sin Minero o Herbolario en rango 10, solo de los nodos (5 % por vuelta; ~4,6 nodos de gema y ~7,1 de flor
  hasta Lejanía 6). La Joyería (su primera receta pide una gema), las piezas desde el rango 50, las pociones mayores, la túnica y el vendaje
  del 50, el festín y el banquete dependen de eso. Simulado: Joyería al 100 pasa de 1.615 a 4.131 días.
- Los jugadores de hoy no pierden nada: `_learn_price` cobra 0 a quien ya tiene experiencia en el oficio (D-64).
- Los beneficios de esos oficios (Leñador +10 de mochila, Minero +5 % de vida, Herbolario +20 % de regeneración, Pescador +30 % de pescado
  en la despensa del campamento) y sus 🎓 especializaciones solo valen aprendiéndolos.
- El origen ⛏️ Minero y el 🌿 Herbolario (`story.yaml`, +15 % de experiencia de ese oficio) no sirven hasta aprenderlo: conviene decirlo al
  elegir el origen, o que el origen regale el oficio.
- El aviso del camino guiado "tu primer oficio subió de rango" (`guide.yaml` rank_up) seguirá saliendo con el 🧭 Explorador.
- Hay que agregar los textos `learn.unlocks_lenador`, `_minero`, `_herbolario` y `_pescador` en `es_menus.yaml` y su `en_*.yaml` (hoy solo
  existen los de Desollador, Comercio, Encantamiento y Construcción), y revisar `tests/test_aprender_oficios.py`, las notas de
  `engine/hero/hero.py` y `game.py` (`_knows`, `_prof_auto`), `profesiones.md` §0.0 y D-257.
- Precio: con 🥉20 (P-231) aprender es casi gratis (lo que da vender ~3 a 6 vueltas de recolección). Si se quiere que aprender sea una
  decisión, ver el §8.

## 8. Recomendaciones para lo que pidió el dueño

Las metas: camino **lento**, progreso **visible**, "que no sea tan fácil", **muchas recetas de rango 1 antes de las siguientes**, recetas
mejoradas, **ingredientes intermedios fabricados**, y que lo fabricado **valga para venderlo, sobre todo a otras clases**.

### 8.1 Que se vea el progreso: un tramo cada 5 rangos en todos los oficios

- Hoy: 3 tramos en los primeros 54 rangos de los oficios de equipo; 1 solo tramo en el refinado; nada después del 50 en Alquimia y Medicina.
- Propuesta: **20 tramos (1, 5, 10 … 95, 100) en todos los oficios**, y **nivel de pieza = rango** (rango 30 → pieza de nivel 30), en vez de 3, 5 y
  8 hasta el 54. Así el artesano de rango 30 hace lo que necesita un héroe de nivel 30, que es quien se lo puede comprar. Hoy las piezas
  de nivel 10 llegan recién al rango 55 (2.187 piezas hechas), cuando los héroes ya pasaron ese nivel.
- Para no multiplicar las 387 recetas de hoy: un tramo puede ser una receta de cada línea (como ya pasa del 55 al 100).

### 8.2 Que no sea tan fácil: colores de receta (la experiencia cae)

Como en WoW: con d = tu rango − rango de la receta, **naranja** (experiencia completa), **amarillo** (la mitad), **verde** (un cuarto) y
**gris** (nada). Con tramos cada 5 rangos, recomiendo: d < 5 naranja, 5-9 amarillo, 10-14 verde, 15 o más gris. Así hay que hacer
muchas del tramo para pasar al siguiente, y después dejarlas.

Simulado con las recetas de hoy (como hoy los tramos están cada 25, se usó d < 10 / 10-19 / 20-29 / 30+):

Variante B: colores y además la experiencia de cada receta crece con su rango (× (1 + rango de la receta ÷ 50): la de rango 50 da el doble, la de 100 el triple).

| Oficio | Solo su ⚡ hoy: r25 / r50 / r100 | Solo su ⚡ con colores | Cadena media hoy | Cadena media con colores | Cadena media, colores + xp que crece (B) | Veces hasta el 100 (hoy → colores → B) | Crudo hasta el 100 (hoy → colores → B) |
|---|---|---|---|---|---|---|---|
| carpinteria | 22 / 90 / 368 | 53 / 135 / 412 | 140 / 552 / 2.041 | 331 / 1.243 / 8.500 | 325 / 894 / 4.133 | 7.351 → 7.361 → 3.991 | 73.788 → 269.531 → 126.956 |
| herreria | 22 / 90 / 368 | 53 / 203 / 480 | 144 / 582 / 2.246 | 345 / 2.009 / 8.385 | 338 / 1.466 / 4.247 | 7.351 → 9.603 → 5.334 | 41.539 → 195.187 → 95.161 |
| alquimia | 22 / 73 / 281 | 53 / 165 / nunca / (se traba en el rango 80) | 103 / 411 / 1.561 | 245 / 1.166 / nunca / (se traba en el rango 80) | 240 / 866 / nunca / (se traba en el rango 80) | 14.702 → — → — | 51.977 → — → — |
| sastreria | 22 / 90 / 368 | 53 / 203 / 480 | 96 / 382 / 1.435 | 228 / 1.403 / 5.456 | 224 / 1.029 / 2.724 | 14.702 → 10.656 → 6.385 | 51.977 → 230.768 → 111.934 |
| peleteria | 22 / 90 / 368 | 53 / 203 / 480 | 222 / 886 / 3.352 | 528 / 2.048 / 8.967 | 518 / 1.546 / 4.588 | 7.351 → 9.603 → 5.324 | 55.047 → 204.280 → 98.103 |
| medicina | 22 / 90 / 368 | 53 / 203 / nunca / (se traba en el rango 80) | 119 / 430 / 1.590 | 282 / 935 / nunca / (se traba en el rango 80) | 277 / 717 / nunca / (se traba en el rango 80) | 7.783 → — → — | 54.499 → — → — |
| joyeria | 22 / 90 / 368 | 53 / 203 / 480 | 161 / 506 / 1.615 | 330 / 1.407 / 7.519 | 325 / 1.059 / 3.543 | 7.351 → 10.713 → 5.611 | 14.016 → 67.641 → 31.564 |
| cocina | 22 / 90 / 368 | 53 / 203 / 784 | 99 / 404 / 1.587 | 238 / 1.115 / 6.713 | 234 / 823 / 3.356 | 14.702 → 16.731 → 9.202 | 44.106 → 141.318 → 68.096 |

- Con colores, el especialista (solo su ⚡) tarda un 30 % más (368 → 480 días) y el que lo hace todo solo, casi 4 veces más (Herrería 2.246 →
  8.385 días), porque las recetas nuevas piden mucho más material por la misma experiencia. Se gasta 3 a 5 veces más material: más demanda
  para los recolectores.
- Alquimia y Medicina **se traban en el rango 80** con colores: no tienen recetas después del 50. Necesitan tramos hasta el 100.
- **Variante B** (la experiencia crece con el tramo: × (1 + rango de la receta ÷ 50)) deja la cadena en la mitad que solo con colores
  (Herrería 4.247 días) y hace que fabricar lo nuevo sea lo que conviene. El especialista bajaría a 264 días: si se quiere mantener
  ~1 año, que la energía de las piezas también suba con el tramo (2 ⚡ hasta el 50, 3 ⚡ del 55 al 80, 4 ⚡ del 85 al 100).

**La propuesta completa** (colores + experiencia que crece con el tramo + energía de las piezas que crece con el tramo), con y sin
arreglar la piel (×2,5 pieles por presa), días hasta el 25 / 50 / 100 (`propuesta_combinada.py`):

| Oficio | Solo su ⚡ hoy | Solo su ⚡ con la propuesta | Cadena hoy | Cadena hoy con piel ×2,5 | Cadena con la propuesta | Cadena con la propuesta y piel ×2,5 |
|---|---|---|---|---|---|---|
| herreria | 22 / 90 / 368 | 52 / 152 / 324 | 144 / 582 / 2.246 | 102 / 416 / 1.618 | 338 / 1.466 / 4.317 | 241 / 1.026 / 3.078 |
| peleteria | 22 / 90 / 368 | 52 / 152 / 324 | 222 / 886 / 3.352 | 140 / 565 / 2.170 | 518 / 1.546 / 4.649 | 329 / 1.021 / 3.232 |
| sastreria | 22 / 90 / 368 | 52 / 152 / 324 | 96 / 382 / 1.435 | 96 / 382 / 1.435 | 224 / 1.029 / 2.785 | 224 / 1.029 / 2.785 |
| carpinteria | 22 / 90 / 368 | 52 / 103 / 264 | 140 / 552 / 2.041 | 140 / 552 / 2.041 | 325 / 894 / 4.170 | 325 / 858 / 3.706 |
| joyeria | 22 / 90 / 368 | 52 / 152 / 324 | 161 / 506 / 1.615 | 161 / 506 / 1.615 | 325 / 1.059 / 3.622 | 325 / 1.059 / 3.622 |

- El especialista queda en ~11 meses al 100 (hoy 12), pero tiene que fabricar lo nuevo para subir: el progreso se ve.
- Quien lo hace todo solo tarda el doble que hoy (Herrería 6,2 → 11,8 años; con la piel arreglada, 8,4): la economía tiene que poner
  ~2,3 veces más material por artesano. Es la parte "lenta" que pidió el dueño; si parece demasiado, la palanca es la curva
  (`rank_formula.base`) o cuánto crece la experiencia por tramo.

### 8.3 "Muchas recetas de rango 1 para aprender las siguientes"

- Hoy el rango 2 sale con 1 receta, el 5 con 12 y el 10 con 61 (la curva empieza muy suave: 9 × (r − 1)²).
- Opción A (más simple): con tramos cada 5 y colores, ya hay que hacer ~12 recetas para el rango 5, ~50 más para el 10, etc.
- Opción B (lo que dijo el dueño, literal): además del rango, **cada tramo pide haber hecho N recetas del tramo anterior** (por ejemplo 20
  en los primeros tramos, 40 desde el 50). Es la "maestría por línea" de Albion (`profesiones.md` §6) en su capa más simple.

### 8.4 Ingredientes intermedios y recetas mejoradas

- Hoy hay un solo paso intermedio (tablón, lingote, tela, cuero, extracto, sillar), igual del rango 1 al 100.
- Propuesta: **un refinado mejor cada 25 rangos** que piden los tramos altos de fabricación: 🔩 acero (lingote ×2 + carbón) al 25, plata y oro
  al 50 (ya están como especializaciones en `red-de-oficios.md` §2.2: Metales preciosos, Aleaciones); 🟫 tablón noble (madera + resina),
  🧣 tela fina (lino o tela + tinte), 🟤 cuero grueso (cuero + corteza), 🧴 extracto concentrado. Da recetas nuevas a los 6 oficios de
  refinado (hoy 100 rangos con una receta) y cumple lo de "ingredientes intermedios fabricados". Encaja con la idea de D-194 (refinado en
  estructuras) si se programa después.

### 8.5 Costos de aprender

- Hoy 🥉20 por oficio (P-231): menos que vender lo que dan 3 a 6 vueltas de recolección.
- Propuesta: **oficios de fabricación 1 🥈 (100 🥉), recolección y refinado 🥉50**, y un **libro de recetas por tramo** en el
  🧑‍🏫 Entrenador (por ejemplo 2 🥈 al 25, 10 🥈 al 50, 25 🥈 al 75): saca monedas del juego y hace que subir de tramo se sienta.
  Sigue gratis para quien ya practicaba el oficio (D-64).

### 8.6 Los cuellos de botella

- **🦌 Piel (Curtiduría, Peletería, Herrería, arcos):** hoy ~4,4 ⚡ por piel; un recurso común cuesta ~0,7 ⚡. Llevarla a ~1,5-2 ⚡: que las
  bestias suelten 1 a 3 pieles (`loot_amount`) o que el 🔪 Desollador saque una piel más por bestia. Un peletero al 100 necesita ~20.600
  pieles: hoy son ~6 años de un cazador a tiempo completo.
- **🔪 Desollador (0,53 por ⚡):** que dé experiencia por bestia desollada (por ejemplo +3 por bestia, además de 1 por unidad), para
  quedar en ~2 por ⚡ como los demás.
- **🎣 Pescador (0,66 por ⚡):** un botón **🎣 Pescar** en las zonas con agua que solo saque pescado (como 🏹 Cazar solo pelea), o subir
  `camp_professions.fish.richness` de 0,5 a ~1,5.
- **🏗️ Construcción (tope en el rango 24):** necesita algo que se repita: mantenimiento semanal de lo construido, obras del
  Claro o del reino que se reabren, o más experiencia por material (×3 llega al ~40 con un campamento entero).
- **✨ Encantamiento:** depende de piezas para desencantar (13 ⚡ de caza por pieza del botín). Con mercado, las miles de piezas que hacen
  los artesanos al subir (7.351 por oficio) son su materia prima natural: un artesano al 100 da para medio encantador. Mientras tanto,
  que desencantar dé más experiencia con el nivel de la pieza.
- **💍 Joyería:** la primera receta pide una 💠 gema: el joyero necesita el Minero en 10 (729 unidades) o un nodo de gemas (20 vueltas por
  gema). Con la regla nueva, conviene una primera receta sin gema.

### 8.7 Que valga la pena venderlo

- **Mercado entre jugadores primero** (está en el plan como 2.ª tanda): sin él, nada de lo fabricado le llega a otra clase.
- Mientras tanto: que el mercader compre pociones y remedios a poco (hoy no los compra y vende pociones de vida y vendas), y retirar o
  convertir la malla (D-208, E-176: las 67 recetas con `retired: true`, sin borrar ids).
- Con nivel de pieza = rango (§8.1), lo que hace el artesano coincide con lo que necesitan los héroes que juegan ahora.

### 8.8 Recolectar con intención

- Hoy una vuelta reparte al azar entre 4 a 6 recursos: en la mejor zona, el recurso que buscas es ~30-45 % de lo que sale. Propuesta para la
  capa profunda: desde un rango del recolector (por ejemplo 25), elegir qué recurso buscar (sube su peso en la vuelta).

### 8.9 Para decidir con el dueño (con mi recomendación)

1. Tramos cada 5 rangos y nivel de pieza = rango. **Recomiendo sí**: es lo que hace visible el progreso.
2. Colores de receta (d < 5 / 5-9 / 10-14 / 15+). **Recomiendo sí, junto con la experiencia y la energía que crecen con el tramo**: el
   especialista sigue en ~1 año y quien lo hace todo solo tarda ~2 veces más que hoy (8 a 12 años en los oficios con piel). Medirlo en la beta.
3. ¿Cada tramo pide además N recetas del anterior? **Recomiendo empezar sin eso** (los colores ya lo piden) y medir.
4. Costos: 1 🥈 los de fabricación, 🥉50 los demás, libros por tramo. **Recomiendo** probarlo con el informe diario (P-231).
5. Piel, Pescador, Desollador y Construcción: **recomiendo arreglarlos antes de la beta**, son los que hoy no avanzan.
6. Lo que se recolecta antes de aprender el oficio: **recomiendo guardarlo hasta el rango 5** y avisar.

## 9. Lo que no se pudo determinar

- El ritmo real de los jugadores (cuánta energía ponen en cada cosa): sale del informe diario (D-260), no del código.
- El nivel de héroe que tiene un artesano en cada momento (la experiencia de héroe al fabricar depende del menor entre nivel y rango):
  no se simuló; se tomó del diseño "nivel 10 en ~18 días, 20 en ~70" (`balance.yaml` hero).
- Las peleas: se supuso que se ganan todas. Las derrotas y el tiempo de viaje alargan todo lo que pide piel, carne o zonas lejanas.
- El agotamiento por muchos jugadores en la misma zona y el efecto de los nodos que doblan un recurso (se tomó la zona llena, sin nodo).
- Las 🎓 especializaciones (hasta +15-20 % de rendimiento) y el +10 % de las estaciones del campamento: no se sumaron.

## 10. Archivos de la simulación (fuera del repositorio)

- `informe-oficios.md`: este informe.
- `anexo-recetas-a-crudo.md`: las 373 recetas de fabricación, cada una bajada hasta lo crudo.
- `world_stats.py` → `world_stats.json`: lo medido del mundo con el motor (recursos por zona, presas, nodos).
- `sim_oficios.py` → `tablas_generadas.md`, `resultados.json`, `simulacion_detalle.json`: catálogo, simulación y economía.
- `gather_scen.py`: recolección por distancia. `propuesta_combinada.py`: la propuesta del §8.2. `build_report.py`: arma este informe.
