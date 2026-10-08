# Talentos

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Clases](clases-y-especializaciones.md), [Balance](balance.md) · **Estado:** propuesta (la capa simple de §5 ya está en el juego: D-68, D-79)

> ⚠️ **8-oct-2026 (D-225, D-230):** en las clases nuevas los puntos de nivel van solos al rol activo, los 4 botones están siempre abiertos y el segundo rol se aprende al nivel 5. Las 8 habilidades por especialización y su desbloqueo por puntos quedan para las clases retiradas. Ver [Combate en cadena](../04-combate/combate-en-cadena.md).


**De dónde sale.** WoW desde *Dragonflight* (2022): un árbol de clase más un árbol de especialización. Desde *The War Within* (2024) se suman los **talentos de héroe**: cada spec elige 1 de 2 árboles, y cada árbol lo comparten dos specs de la clase. Desde *Midnight* (2026), un **talento Ápice** de remate de cuatro rangos.

---

## 1. Los cuatro árboles

| Árbol | Desde | Qué contiene | Puntos |
|---|---|---|---|
| **Clase** | Nivel 10 | Utilidad, defensivos, movilidad, el aporte de grupo | 1 por nivel par |
| **Especialización** | Nivel 10 | La rotación, la firma de la spec, variantes de sus habilidades | 1 por nivel impar |
| **Héroe** | Nivel 50 | Dos caminos por spec. Por ejemplo, un Paladín Protección elige *Templario* o *Heraldo del Sol*, y cada camino lo comparten dos specs | 1 cada 2 niveles |
| **Ápice** | Nivel 90 | Un nodo de 4 rangos que remata la identidad de la spec | 1 cada 2 niveles |

Con el nivel ligado a la Frontera (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)), los árboles crecen a su ritmo: el árbol de héroe llega cuando el servidor cruza la Gran Barrera del anillo V.

## 2. Reglas

- **Nodos de elección**: en ciertos puntos del árbol se elige entre dos talentos. Es donde está la personalización real.
- **Configuraciones guardadas**: hasta 5 por spec (por ejemplo, "banda", "mazmorra", "PvP", "solitario").
- **Cambiar es gratis en cualquier asentamiento.** Castigar la experimentación desalienta a probar cosas; en WoW Clásico el cambio de talentos costaba oro y la gente jugaba siempre lo mismo.
- **Cambiar de spec** también es gratis dentro de la clase, fuera de combate y en un asentamiento.
- **Cambiar de clase** no existe: se crea otro personaje. El progreso de cuenta (ver [Progresión](progresion.md)) hace que un alt avance rápido.
- **Las habilidades del árbol entran en la barra de 8** a elección del jugador (4 casillas de clase; ver [Clases](clases-y-especializaciones.md)).

## 3. Cómo se equilibra un árbol

- Cada nodo tiene un **costo en el presupuesto** de la spec (ver [Balance](balance.md)).
- Dos nodos de una misma elección deben tener valor parecido **en contextos distintos**: uno sirve contra un objetivo, el otro contra varios. Así no hay una opción "obligatoria".
- El simulador corre todas las configuraciones populares y avisa si alguna se aleja más de un 3 % de las demás en su contexto.

## 4. Además de los talentos

La progresión horizontal (maestrías de arma, renombre, conocimiento del bestiario) está en [Progresión](progresion.md). La regla es la misma: **permanente, nunca prestada**.

## 5. Lo que ya está en el juego (D-68, D-79)

Lo de arriba es el diseño completo, para más adelante. La versión jugable usa una capa simple (D-44):

- **1 punto por nivel** (100 niveles por ahora, D-78). Cada punto va a una especialización de tu clase. Tu especialización principal ⭐ es la que tiene más puntos.
- **8 habilidades por especialización.** Se abren con puntos en esa especialización:

| Habilidad | 1.ª | 2.ª | 3.ª | 4.ª | 5.ª | 6.ª | 7.ª | 8.ª |
|---|---|---|---|---|---|---|---|---|
| Puntos en la especialización | 1 | 3 | 6 | 10 | 16 | 24 | 34 | 46 |
| Nivel, con todo en una sola | 2 | 4 | 7 | 11 | 17 | 25 | 35 | 47 |

  Con los 99 puntos del nivel 100 se pueden abrir dos especializaciones completas, o una completa y repartir el resto.
- **Mejora pasiva pequeña:** cada punto suma alrededor de un 1 % según el rol de la especialización (Ataque: +1 % de ataque; Defensa: +1,25 % de vida y +0,2 de armadura; Curación: +0,85 % de vida y +0,4 % de ataque; Soporte: +0,5 % de ataque y +0,6 % de vida; desde la pasada de D-110, ver [Balance](balance.md) §7). Cuentan hasta 50 puntos por especialización. Al nivel 5 es un +4 o +5 %.
- **Barra de combate de 3 (D-46), elegible:** en 🌟 Talentos → 🎛️ Barra de combate.
  - Casilla 1: una **respuesta** al aviso (🛡 bloquear, 💨 esquivar o 🫧 escudo). Nunca queda sin respuesta.
  - Casillas 2 y 3: cualquier otra habilidad que ya abriste, también de otra especialización de tu clase.
  - Si no eliges, la barra **se arma sola**: tu respuesta más nueva, tu golpe más nuevo (golpe, remate o daño en el tiempo) y tu otra habilidad más nueva; en las de 🛡 Defensa, la casilla 3 es su curación más nueva, si ya abrió alguna (D-110).
  - Cada habilidad muestra una línea corta de qué hace, sacada de sus números (por ejemplo, "golpe ×1,3 · te cura 15 % del daño · +15 de Ira").
- **Reiniciar la especialización** cuesta 10 💰 por nivel (D-74): devuelve los puntos y vacía la barra elegida.
- **Los héroes guardados no pierden nada:** conservan sus habilidades, y al entrar ganan las que sus puntos ya pagan con la tabla nueva.

**Registro de balance (D-79), antes → después:**

| Número | Antes | Después | Por qué |
|---|---|---|---|
| `talents.unlock` | 1, 3, 6 | 1, 3, 6, 10, 16, 24, 34, 46 | 8 habilidades repartidas en 100 niveles lentos |
| `talents.passive` (Ataque / Defensa) | 3 % por punto | 1 % por punto | El dueño pidió porcentajes bajos; con 100 niveles, 3 % daba hasta +60 % |
| `talents.passive` (Curación / Soporte) | 2 % + 1 % | 0,6 % + 0,4 % | Igual, repartido |
| `talents.passive_cap` | 20 puntos | 50 puntos | Tope de +50 % para 100 niveles |
| "Pegas más" de las primeras habilidades: *Estandarte de Guerra*, *Dados del Destino*, *Tótem de Ventarrón*, *Desborde Arcano*, *Entregar Alma*, *Fuerza Prestada*, *Allegro* y *Apuntar* | 60 % | 50 % | Porcentajes más bajos al inicio; las nuevas van de 30 a 35 % |
| *Distracción* (Forajido) | 35 % | 40 % | Compensa la baja de *Dados del Destino* (el simulador bajó a 92 % de victorias contra el Oso de las cumbres; con 40 % vuelve a 98 %) |

Medición: `python3 tools/sim.py --summary` (todas las especializaciones ≥ 95 % de victorias contra los enemigos de nivel 1 a 3 con sus 3 primeras habilidades) y `python3 tools/sim.py --bars --level=11|25|47` (todas las barras posibles de cada especialización: ninguna queda más de 12 puntos de vida restante por encima de la mediana de su rol).

Ajustes posteriores de números por especialización (vida base, segunda habilidad, curación): ver el registro en [Balance](balance.md) §7.

## Doble especialización (en el juego desde 0.9.1, D-88)

- **Cuándo:** cuando tienes 10 puntos en tu especialización principal ("te dedicaste a ella") y pagas 3 💰 bolsas (`talents.dual`).
- **Qué da:** dos configuraciones de talentos. Cada una guarda sus puntos, sus habilidades abiertas, su especialización principal y su barra. Cambias entre ellas con /doble fuera de combate y sin estar haciendo nada.
- **Puntos:** salen de tu nivel. Cada configuración tiene nivel − 1 puntos para repartir. La segunda empieza con todos libres.
- **Reiniciar** (🔄) solo afecta a la configuración que estás usando.

