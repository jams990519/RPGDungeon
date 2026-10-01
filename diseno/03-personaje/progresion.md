# Progresión: por qué alguien sigue jugando dos años después

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Talentos](talentos.md), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md), [Profesiones](../07-economia/profesiones.md) · **Alimenta a:** [Balance](balance.md), [Equipamiento](equipamiento.md), [Temporadas y social](../08-social/README.md) · **Estado:** §1 y §2 están en el juego (0.9.2); §3 en adelante es propuesta

El dueño pidió que quien encuentre algo que le guste pueda avanzar **más de dos años**. Eso no sale de un número de nivel alto. Sale de **varias escaleras paralelas**, cada una para un tipo de jugador, y ninguna obligatoria. La primera ya está en el juego: **100 niveles lentos** con **1 punto de talento por nivel** (D-68, D-78).

---

## 1. Niveles: 100 y lentos (en el juego)

- **Hay 100 niveles por ahora** (`hero.max_level`). Al llegar al 100 se deja de subir.
- **Experiencia total para llegar al nivel N = 120 × (N − 1)^2,35** (`hero.xp_formula`, D-78).
- **No hay Techo de la Frontera.** La experiencia nunca se corta por ir adelante del resto. La idea vieja se retiró (ver §9).
- **El freno es la energía,** no el nivel: 50 ⚡ como máximo y 40 por día. Moverse, explorar y recolectar gastan 1 cada uno. Pelear no gasta (D-78).

| Nivel | Experiencia total | Con toda la energía cada día |
|---|---|---|
| 2 | 120 | El primer día |
| 6 | 5.269 | Unos días. Es el nivel de Raigambre (D-82) |
| 10 | 20.973 | Unos 18 días |
| 20 | 121.409 | Unos 70 días |
| 47 | 969.755 | Cerca de un año (estimado) |
| 100 | 5.873.865 | Unos 2,5 años |

Quien juega menos tarda más, y está bien: cada nivel cuenta.

### 1.1 De dónde sale la experiencia hoy

| Fuente | Cuánto | Dónde se ajusta |
|---|---|---|
| **Ganar una pelea** | La experiencia del enemigo, +15 % por cada nivel del enemigo sobre el 1 | `content/enemies.yaml` (`xp`) |
| **Vencer a Raigambre** | Su experiencia, con la misma regla | `content/enemies.yaml` (`raigambre`) |
| ~~Aportar a la obra común del Claro~~ | Quitado en la 0.11 (D-98): el Claro no crece | — |
| **Aportar comida a la despensa de tu campamento** | 2 de experiencia por ración | `pantry.xp_per_ration` |
| **Explorar** (D-104) | 3 de experiencia por vuelta y 15 al dejar una zona al 100 % | `explore.xp_per_step`, `explore.xp_full_zone` |
| **Tutorial** | 20 por cada paso cumplido | `tutorial.reward_xp` |
| **⭐ Acelerador** (con 💎 diamantes) | +50 % de experiencia durante 7 días | `currency.gem_shop.xp_boost` (D-43, D-80) |

Explorar y recolectar no dan experiencia directa. Dan los encuentros que sí la dan, y los materiales que se aportan.

## 2. Talentos: 1 punto por nivel (en el juego)

- **Cada nivel da 1 punto,** desde el nivel 2. Al nivel 100 se tienen 99 puntos (D-68).
- Los puntos van a cualquiera de las 3 especializaciones de tu clase. La que tiene más puntos es la principal ⭐.
- **8 habilidades por especialización,** que se abren con 1, 3, 6, 10, 16, 24, 34 y 46 puntos (D-79). Con todo en una sola, la 4.ª llega al nivel 11, la 5.ª al 17, la 6.ª al 25, la 7.ª al 35 y la 8.ª al 47.
- **Mejora pasiva:** cada punto suma alrededor de 1 % según el rol (ataque, vida o repartido), con un tope de 50 puntos por especialización (`talents.passive`, `talents.passive_cap`). Los números son bajos a propósito: crecer se nota durante los 100 niveles.
- **Reiniciar** cuesta 10 🥉 por nivel (D-74). **Doble especialización:** 10 puntos en la principal y 3 💰 bolsas (D-88).
- El detalle está en [Talentos](talentos.md).

## 3. Las escaleras (propuesta, salvo nivel y talentos)

| Escalera | Qué sube | Techo | Estado | De dónde sale |
|---|---|---|---|---|
| **Nivel** | 1 a 100 | 100 por ahora (D-78) | En el juego | WoW |
| **Talentos** | 8 habilidades por especialización y mejoras pasivas | 99 puntos | En el juego | WoW |
| **Equipo** | 7 ranuras, 4 rarezas, piezas con nivel (D-77, D-83) | Se renueva con cada anillo | En el juego (capa simple) | WoW, Albion |
| **Campamento** | Nivel del campamento y zonas de territorio | Castillo al nivel 9, y sigue creciendo (D-87) | En el juego | Ashes of Creation |
| **Maestría de armas y armaduras** | Bonos pequeños por usar cada tipo | Muy largo, con rendimientos decrecientes | Propuesta | Albion |
| **Oficios** | 1 a 100 por oficio, especializaciones, maestrías | Años (ver [Profesiones](../07-economia/profesiones.md)) | Propuesta | RuneScape, Albion, WoW |
| **Renombre** | Puntos después del nivel máximo, para bonos horizontales | Sin techo, con rendimientos decrecientes | Propuesta | Diablo (Paragon) |
| **Reputaciones** | Con campamentos, comunidades y órdenes | Por facción | Propuesta | WoW |
| **Conocimiento** | Bestiario: movimientos de jefes, debilidades, partes | Todo el bestiario | Propuesta | Monster Hunter, Souls |
| **Colecciones** | Apariencias, monturas, mascotas, cicatrices, recetas | Cientos de piezas | Propuesta | WoW |
| **Rangos de temporada** | Mítica+, arena, ligas | Se reinicia cada temporada | Propuesta | WoW, Path of Exile |
| **Prestigio social** | Pionero, títulos, mérito en la obra común | — | En parte: Pionero del Claro (D-82) y mérito del Claro | SAO, WoW |
| **Casa y seguidores** | Vivienda, granja, mesa de misiones | Largo (ver [Casa propia](../09-construccion/casa-propia.md)) | Propuesta | WoW, Albion |

## 4. Experiencia: más fuentes (propuesta)

- **Se gana de todo.** Más adelante también fabricar, curar a otros, completar misiones y ganar en PvP. Es la "fama" de Albion, que sube haciendo cualquier cosa.
- **Descanso:** dormir en la posada o en tu casa acumularía **experiencia descansada**, que duplica la de combate hasta gastarse. Es el "descanso" de WoW. En Telegram es clave: quien juega poco no se queda atrás.
- **Viento de Cola:** las regiones muy por detrás de la Frontera darían más experiencia, para que quien llega tarde alcance al resto (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §2).
- **Carriles:** cada tipo de contenido lidera en algo distinto. Por ejemplo, las mazmorras en experiencia, las expediciones en materiales y el PvP en monedas. TowerWars trabaja con esta idea y funciona.

## 5. Maestría de armas y armaduras (propuesta)

- Cada tipo de arma (espada, daga, arco, bastón) y de armadura (tela, cuero, malla, placas) tendría su maestría, que sube al usarla.
- Da bonos pequeños (un poco más de crítico con ese tipo, menos desgaste) con rendimientos decrecientes fuertes: llegar al 80 % lleva semanas; el último 20 %, meses.
- Nunca supera el 5 % de poder total: es identidad, no una brecha imposible de alcanzar.

## 6. Renombre (propuesta)

Al llegar al nivel máximo del momento, la experiencia se convertiría en **Renombre**. Cada punto se invierte en bonos horizontales: más espacio en la mochila, menos tiempo de viaje, más energía guardada, cosméticos. **Nunca daño.** Así quien va adelante sigue progresando sin romper el balance.

## 7. Reputaciones, logros y colecciones (propuesta)

- **Reputaciones** con el Claro, con cada campamento grande, con las comunidades PNJ del Colapso (D-45) y con órdenes (cazadores, eruditos, sanadores, mercaderes). Niveles: Hostil, Neutral, Amistoso, Honorable, Reverenciado, Exaltado. Dan recetas, apariencias y misiones.
- **Logros** para cada sistema, incluidos los raros: "Vencer a un Guardián sin recibir heridas", "Explorar 100 zonas al 100 %".
- **Títulos** junto al nombre: "Pionero del Claro" ya existe (D-82). Más adelante, "el Cartógrafo" o "Fundador de [campamento]".
- **Colecciones** compartidas por cuenta: apariencias, monturas, mascotas, piezas de arqueología, recetas descubiertas.
- **Cicatrices como trofeo:** el perfil lista tus cicatrices con el jefe y la zona (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)).

## 8. Temporadas, ligas y progreso de cuenta (propuesta)

- **Temporadas de 3-4 meses** para Mítica+ y arena, con recompensas cosméticas y títulos.
- **Ligas opcionales:** un mundo paralelo con economía desde cero y una regla especial. Al terminar, los personajes pasan al mundo normal. El mundo normal **nunca se reinicia** (D-64).
- **Juramento de Hierro** con ranking propio (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)).
- **Progreso de cuenta:** colecciones, reputaciones y bestiario compartidos entre personajes; banco de cuenta; experiencia extra para el segundo personaje hasta donde llegó el primero. Los oficios **no** se comparten.

## 9. Lo que se retiró

- **Techo de la Frontera** (antes, Techo del Piso): bajaba la experiencia al 10 % si tu nivel pasaba en 5 al de la Frontera. D-78 fijó 100 niveles lentos y no lo incluyó. El ritmo ya lo frenan la energía y la fórmula. Si algún día hace falta, vuelve como pregunta nueva, no como regla.
- **Niveles sin tope** (D-64): D-78 los cambió por 100 niveles por ahora.

## 10. Metas por horizonte de tiempo

Qué tiene para hacer un jugador en cada escala de tiempo. Si una fila queda vacía, el juego se queda sin razones para volver.

| Horizonte | Hoy en el juego | Más adelante (propuesta) |
|---|---|---|
| **Hoy** (varios toques) | Gastar la energía explorando o recolectando, aportar a la obra común, ganar peleas | Encargos, curar heridas, una mazmorra, fabricar |
| **Esta semana** | Desafiar a Raigambre (cada 24 horas), agrandar tu campamento, explorar una región al 100 % | Jefe semanal, bandas, asedio del gremio |
| **Este mes** | Subir 10 niveles, abrir una habilidad nueva, llevar el Claro a la siguiente etapa | Un rango de oficio, una reputación, un logro difícil |
| **Esta temporada** (3-4 meses) | Doble especialización, campamento en pueblo o ciudad | Rango de Mítica+ o arena, una liga |
| **Este año** | Las 8 habilidades de una especialización (nivel 47), un campamento castillo | Cruzar una Gran Barrera, Gran Maestro de un oficio |
| **Dos años o más** | Nivel 100 | La Lejanía profunda, maestrías completas, un nombre en la historia del servidor |

## 11. Para que el veterano no se aleje del nuevo

- Las mejoras pasivas son de ~1 % por punto, con tope (D-79). Un veterano es más fuerte, pero no imposible de seguir.
- El poder vertical se comprime por anillos (ver [Balance](balance.md)).
- El Viento de Cola acelera a quien llega tarde (propuesta).
- El Renombre y las maestrías dan horizontal, no vertical (propuesta).
- Los veteranos ganan **prestigio y comodidad**, no una ventaja imposible de alcanzar.

## 12. De dónde sale

- **World of Warcraft:** niveles con talentos, especializaciones, descanso, reputaciones, logros y colecciones de cuenta.
- **Albion Online:** la fama que sube haciendo cualquier cosa y el tablero de destino (maestrías).
- **Diablo:** el Paragon (Renombre) después del nivel máximo.
- **RuneScape:** habilidades de 1 a 99 que llevan años.
- **Path of Exile:** temporadas y ligas.
- **Juegos de energía de Telegram** (TowerWars, Chat Wars): la energía por día como freno justo para quien juega poco.

## 13. Preguntas

- P-16 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md): ya sin efecto (D-58, D-78).
