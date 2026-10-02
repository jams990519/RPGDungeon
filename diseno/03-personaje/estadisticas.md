# Estadísticas, armaduras y clases (la reforma del 2-oct-2026)

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Decisiones](../00-vision/decisiones.md) (D-44, D-46, D-77, D-83, D-110, D-199, D-208 a D-211, D-214), [Clases y especializaciones](clases-y-especializaciones.md), [Equipamiento](equipamiento.md) · **Alimenta a:** [Combate](../04-combate/README.md), [Botín](botin.md), [Talentos](talentos.md), los oficios que fabrican equipo ([Repaso de oficios](../07-economia/oficios-repaso-2-oct.md)) · **Estado:** lo que dijo el dueño es decisión confirmada (D-208 a D-210 y D-214); el resto es **propuesta de Claude** (D-211, provisional) que espera las preguntas E-170 a E-176 y E-182 a E-186. **Solo diseño: el código no se toca hasta que el dueño apruebe la propuesta.**

## 1. Lo que pidió el dueño

El 2-oct-2026 el dueño dijo por voz (transcripción ordenada; ver [Entrevista de voz](../00-vision/entrevista-de-voz.md)):

- "¿Dónde está el resto de estadísticas de World of Warcraft que te permiten sumar beneficios de algún tipo? Está dando muy pocas estadísticas. En WoW hay como 40 estadísticas diferentes."
- "Cómo podemos definir para que dos o tres clases compartan algunas cosas, para que las clases se equipen con ese equipamiento."
- "Vamos a dejar únicamente tres tipos: placa, cuero y tela. No va a haber malla. Hay que corregir las clases y lo demás." (D-208)
- "Vamos a mantener únicamente cuatro habilidades por especialización, no más que eso." (D-209)
- "Vamos a reformular todo. Básate en el World of Warcraft en todas sus versiones, teniendo en cuenta todas las estadísticas y todas las cosas que se pueden mejorar dentro de las clases." (D-210)

**Por qué hoy hay tan pocas.** El juego arrancó con la capa simple (D-44, "amplio pero ligero"): solo ❤️ vida, ⚔️ ataque, 🛡️ armadura y ⚡ iniciativa, más un 10 % de crítico igual para todos (`balance.yaml combat.crit_chance`). El diseño completo ya nombraba afijos como Crítico, Celeridad, Maestría y Versatilidad ([Equipamiento](equipamiento.md) §3), pero nunca se programaron. Esta reforma los trae.

## 2. Todas las estadísticas del WoW, versión por versión

Clásico (1.x), The Burning Crusade (TBC), Wrath of the Lich King (WotLK), Cataclysm (Cata), Mists of Pandaria (MoP), Warlords of Draenor (WoD), Legion, Battle for Azeroth (BfA), Shadowlands (SL), Dragonflight (DF) y The War Within (TWW).

| # | Estadística (WoW) | Versiones | Qué hacía | En Lost Realms |
|---|---|---|---|---|
| 1 | Fuerza | Todas | Poder de ataque cuerpo a cuerpo; en Clásico, valor de bloqueo y parada | ✅ Principal (§3) |
| 2 | Agilidad | Todas | Poder de ataque, crítico y esquiva | ✅ Principal |
| 3 | Intelecto | Todas | Poder con hechizos, maná y (en Clásico) crítico de hechizos | ✅ Principal |
| 4 | Aguante (Stamina) | Todas | Vida máxima | ✅ Como ❤️ **Vitalidad** (reemplaza a la "vida" de hoy; "Aguante" ya nombra la barra de reacciones del diseño de combate) |
| 5 | Espíritu | Clásico a WoD | Regeneración de vida y maná fuera de combate; en sanadores, maná en combate | ❌ Se funde en Intelecto y Celeridad (WoW lo quitó en Legion) |
| 6 | Poder de ataque | Clásico a MoP en el equipo | Daño físico | ➖ Sale de la principal (como desde Cata) |
| 7 | Poder de ataque a distancia | Clásico a MoP | Daño a distancia | ➖ Igual que el 6 |
| 8 | Poder con hechizos | TBC a MoP en el equipo (antes, daño y curación por separado) | Daño y curación mágicos | ➖ Sale del Intelecto |
| 9 | Bonificación de curación | Clásico y TBC | Solo curación | ➖ Igual que el 8 |
| 10 | Golpe (Hit) | Clásico a MoP | Probabilidad de no fallar | ❌ WoW lo quitó en WoD: obligaba a llegar a un tope aburrido |
| 11 | Pericia (Expertise) | TBC a MoP | Que no te esquiven ni paren | ❌ Mismo motivo |
| 12 | Crítico | Todas | Golpes y curas que valen más | ✅ Secundaria |
| 13 | Celeridad (Haste) | TBC en adelante | Lanzar y atacar más rápido; más recurso | ✅ Secundaria (adaptada a turnos, §4) |
| 14 | Maestría | Cata en adelante | Un bono distinto para cada especialización | ✅ Secundaria |
| 15 | Versatilidad | WoD en adelante | Más daño y curación hechos, menos daño recibido | ✅ Secundaria |
| 16 | Golpe múltiple (Multistrike) | Solo WoD | Golpes extra pequeños | ❌ WoW lo quitó en Legion |
| 17 | Penetración de armadura | TBC a WotLK | Ignorar armadura | ❌ WoW lo quitó en Cata; desequilibraba |
| 18 | Penetración de hechizos | TBC a WotLK | Ignorar resistencias | ❌ Igual |
| 19 | Habilidad con arma | Clásico | Fallar menos con un tipo de arma | ❌ Ya lo cubre la clase (armas de tu clase rinden más, D-83) |
| 20 | Daño y velocidad del arma | Todas | El golpe base del arma | ✅ Ya existe: el arma da el ataque base |
| 21 | Armadura | Todas | Menos daño físico | ✅ Se queda (tope 60 %) |
| 22 | Armadura adicional | Solo WoD | Armadura extra para tanques | ❌ La cubre la Maestría de los tanques |
| 23 | Defensa | Clásico a WotLK | Tope contra críticos y golpes de jefes | ❌ WoW la quitó en Cata |
| 24 | Esquiva | Todas (en el equipo hasta MoP) | Evitar golpes | ➖ Sale de la Agilidad y de las respuestas 💨 |
| 25 | Parada | TBC en adelante (en el equipo hasta MoP) | Desviar golpes cuerpo a cuerpo | ➖ Sale de la Fuerza y de las respuestas 🛡 |
| 26 | Bloqueo | Todas | Frenar parte del golpe con el escudo | ➖ Ya existe como respuesta 🛡; la Maestría de algunos tanques lo sube |
| 27 | Valor de bloqueo | Clásico a WotLK | Cuánto frena el bloqueo | ❌ Se funde en el bloqueo |
| 28 | Resiliencia | TBC a WoD | Menos daño de otros jugadores | ⏳ Cuando llegue el PvP (capa profunda) |
| 29 | Poder JcJ | Solo MoP | Más daño a otros jugadores | ❌ |
| 30-35 | Resistencias: fuego, escarcha, naturaleza, sombra, arcano (y sagrado) | Clásico a Cata | Menos daño de ese elemento | ✅ Capa profunda: se cruzan con el bestiario, el clima y las enfermedades |
| 36 | Maná cada 5 s (MP5) | Clásico a Cata | Regenerar maná | ❌ Se funde en Celeridad |
| 37 | Vida cada 5 s (HP5) | Clásico y TBC | Regenerar vida | ❌ La vida ya vuelve sola (D-103) |
| 38 | Robo de vida (Leech) | WoD en adelante | Te curas una parte de lo que haces | ✅ Terciaria |
| 39 | Evasión (Avoidance) | WoD en adelante | Menos daño de golpes en área | ✅ Terciaria |
| 40 | Velocidad (Speed) | WoD en adelante | Moverte más rápido | ⏳ Terciaria, solo si E-161 permite acortar el viaje |
| 41 | Indestructible | WoD en adelante | El equipo se gasta menos | ✅ Terciaria (cuando llegue el desgaste, E-70) |
| 42 | Nivel de objeto, engarces y bono de engarce | TBC en adelante | Cuánto vale una pieza; gemas | ✅ Ya decidido: gemas en armaduras y armas (D-199) |
| 43 | Efectos al equipar y al usar, bonos de conjunto | Todas | Efectos especiales | ✅ Capa profunda (§7) |
| 44 | Corrupción | Solo BfA 8.3 | Efectos fuertes con un castigo | ❌ |

**Lo que muestra la tabla.** WoW llegó a tener más de 40 estadísticas, pero en cada versión quitó las que solo servían para llegar a un tope (golpe, pericia, defensa, penetración). Las que sobrevivieron hasta hoy son **3 principales, Aguante (aquí Vitalidad), Armadura, 4 secundarias y 4 terciarias**. Esa es la base de la propuesta.

## 3. La propuesta: qué estadísticas tiene Lost Realms (D-211, provisional)

**Capa simple: 9 estadísticas, siempre a la vista en cada pieza.**

| Estadística | Qué hace en una pelea por turnos | Dónde sale |
|---|---|---|
| 💪 Fuerza | Sube el daño de los golpes; un poco de parada | Placa y armas pesadas |
| 🏹 Agilidad | Sube el daño de los golpes; un poco de esquiva | Cuero, dagas y arcos |
| 🔮 Intelecto | Sube el daño de los hechizos y las curas, y el maná | Tela, piezas de intelecto y bastones |
| ❤️ Vitalidad | Vida máxima (el Aguante del WoW) | Todas las piezas |
| 🛡️ Armadura | Menos daño de golpes (nunca más de 60 %) | Según el tipo: placa mucha, cuero media, tela poca |
| 🎯 Crítico | Probabilidad de que un golpe o una cura valga ×1,5 (hoy todos tienen 10 %) | Secundaria |
| ⚡ Celeridad | Actúas antes en la ronda, tus habilidades con espera vuelven antes y ganas un poco más de recurso por ronda | Secundaria |
| 🌀 Maestría | El bono propio de tu especialización (ver abajo) | Secundaria |
| 🔄 Versatilidad | Más daño y curación hechos, y la mitad de eso menos daño recibido | Secundaria |

**Capa profunda: 10 más, en piezas raras, gemas, encantamientos, comida y adornos de artesano.**

- **Terciarias:** 🩸 Robo de vida, 💨 Evasión (menos daño en área), 🔒 Indestructible (el equipo se gasta menos) y 👟 Velocidad (solo si E-161 permite acortar el viaje de 1 minuto por cuadro, D-197).
- **Resistencias:** 🔥 fuego, ❄️ frío, 🌿 naturaleza, 🌑 sombra, ✨ arcano y ☀️ sagrado. Bajan el daño de ese elemento y la probabilidad de sus estados (quemadura, congelación, veneno, enfermedad). Se cruzan con el bestiario, el clima y las enfermedades.
- **Resiliencia:** cuando llegue el PvP (E-76).

**Maestría: una por especialización.** Cada especialización tiene la suya, como en WoW desde Cataclysm. Ejemplos:

| Especialización | Su Maestría |
|---|---|
| 🏰 Guerrero · Protección | Bloqueas más (las respuestas 🛡 frenan más) |
| 💢 Guerrero · Furia | Más daño mientras tienes ira alta |
| 😇 Sacerdote · Sagrado | Tus curas dejan una cura extra la ronda siguiente |
| 📿 Sacerdote · Disciplina | Tus escudos 🫧 son más grandes |
| 🐍 Pícaro · Asesinato | Tus venenos y sangrados pegan más |
| ☄️ Mago · Fuego | Las quemaduras duran y pegan más |

Las 46 se escriben con el código, una línea cada una, en `content/classes.yaml`.

**Cómo se suman los puntos.** Como en WoW: cada pieza da **puntos**, y los puntos se vuelven porcentaje según tu nivel (a más nivel, hacen falta más puntos para el mismo 1 %). Así una pieza vieja no rompe el juego cuando subes. Los números exactos se fijan con las herramientas de balance (§9).

**Lo que no entra, y por qué.** Golpe, Pericia, Defensa, Penetración, Golpe múltiple, Armadura adicional, Valor de bloqueo, Espíritu y MP5: WoW los quitó porque solo obligaban a llegar a un tope o porque se volvieron confusos. El poder de ataque y el poder con hechizos salen de la estadística principal, como en WoW desde Cataclysm.

### 3.1 Cómo funcionan de verdad en el WoW (lo investigado)

- **Puntos que se vuelven porcentaje.** El equipo da "puntos" de una secundaria y el juego los convierte en porcentaje según el nivel. Ejemplo del WoW de hoy: 1320 puntos de Celeridad dan +2 %.
- **Dos secundarias por pieza.** Cada pieza trae dos de las cuatro (Crítico, Celeridad, Maestría, Versatilidad); los abalorios son la excepción. Por eso dos piezas del mismo nivel no valen lo mismo para todos.
- **Rendimiento decreciente.** Pasado un 30 % en una secundaria, cada punto rinde menos, y hay un tope. Así conviene repartir y no apilar una sola.
- **Qué hace cada una:**
  - **Crítico:** en el WoW de hoy dobla el golpe o la cura; aquí vale ×1,5.
  - **Celeridad:** acelera todo: lanzamientos, recarga de algunas habilidades, efectos que pegan por tiempo y recursos.
  - **Maestría:** distinta para cada especialización, potencia lo que mejor hace.
  - **Versatilidad:** sube el daño y la curación, y baja el daño recibido en la mitad de ese porcentaje.
- **Prioridades por especialización.** Cada especialización tiene un orden de estadísticas que más le rinden. Los foros y las guías publican ese orden para cada una.
- **"Afinidad" (WoW Warlords of Draenor).** Cada especialización estaba "afinada" a una secundaria y recibía +5 % extra de ella. Es justo la idea del dueño (§3.2).
- **Especialización de armadura.** Si llevas todas tus piezas del tipo de tu clase, ganas +5 % de tu principal.
- **Del WoW clásico, para comparar:**
  - 1 punto de Aguante daba 10 de vida.
  - En algunas clases, 20 de Agilidad daban 1 % de crítico y 1 % de esquiva.
  - La Fuerza daba poder de ataque y bloqueo; el Espíritu, regeneración.
- **La ficha de personaje** (y los complementos que la amplían) agrupa todo así:
  - **Atributos:** principal, Aguante y armadura.
  - **Mejoras:** Crítico, Celeridad, Maestría y Versatilidad.
  - **Terciarias:** Robo de vida, Evasión y Velocidad.
  - **Defensa:** esquiva, parada y bloqueo.

  La ficha "📊 Estadísticas" de Lost Realms seguiría ese orden.

**Fuentes consultadas:** [Wowhead: rendimiento decreciente de las secundarias](https://www.wowhead.com/tw/guide/diminishing-returns-on-secondary-stats-in-world-of-warcraft), [warcraft.wiki: estadística secundaria](https://warcraft.wiki.gg/wiki/Secondary_stat), [warcraft.wiki: estadística principal](https://warcraft.wiki.gg/wiki/Primary_stat), [foro oficial: "Secondary Stats: The Illusion of Choice"](https://us.forums.blizzard.com/en/wow/t/secondary-stats-the-illusion-of-choice/2010037), [Blizzard Watch: las estadísticas en Warlords](https://blizzardwatch.com/2015/02/18/explaining-stats-in-warlords-of-draenor/), [RankedBoost: estadísticas del clásico](https://rankedboost.com/world-of-warcraft/classic-stats/), [Icy Veins: prioridad de estadísticas del Guerrero Protección](https://www.icy-veins.com/wow/protection-warrior-pve-tank-stat-priority) y fichas ampliadas de complementos como [DejaCharacterStats](https://www.curseforge.com/wow/addons/dejacharacterstats).

### 3.2 Afinidades: lo que hace mejor a tu clase (D-214, propuesta)

El dueño, el 2-oct: "todos los jugadores tienen esas estadísticas, pero el aumento específico de una hace mejor a tu personaje que el resto".

- **Todos tienen todas las estadísticas.** Cualquier héroe puede llevar Crítico o Fuerza.
- **Cada clase tiene 2 afinidades y cada especialización 1 más.** Lo que sumas en una estadística afín vale +10 % (E-183). Es la "afinidad" del WoW Warlords (+5 %), algo más marcada para que se note en un juego de texto.
- **Ejemplos** (con las clases de hoy, que se van a rehacer):

| Clase | Afinidades de la clase | Una especialización y su afinidad extra |
|---|---|---|
| Guerrero | Fuerza, Armadura | Protección: Versatilidad |
| Pícaro | Agilidad, Crítico | Asesinato: Maestría (venenos) |
| Mago | Intelecto, Crítico | Fuego: Celeridad |
| Sacerdote | Intelecto, Vitalidad | Sagrado: Maestría (curas extra) |

- **Por qué así:** con el mismo equipo, un Pícaro saca más Crítico que un Guerrero, y el Guerrero aguanta más. El equipo se comparte entre las 2 o 3 clases de una familia (§4), pero cada una lo aprovecha distinto. Eso le da sentido al mercado y a las prioridades.

### 3.3 Clases personalizadas (D-214)

El dueño: "vamos a crear clases personalizadas; no va a ser específicamente la del World of Warcraft; la del WoW era para que tuvieras una idea de cómo funcionaría".

- **Las 15 clases de hoy son el punto de partida, no el final.** La propuesta (E-182) es que Claude arme un juego de clases propias, de unas 8 a 10 con 3 especializaciones cada una. Cada clase tendría nombre propio, tipo de armadura (placa, cuero o tela), afinidades y sus 4 habilidades por especialización.
- **Quién decide:** el dueño elige y cambia antes de programar.
- **Los jugadores de hoy:** conservan nivel, equipo y oficios, y cambian de clase gratis una vez cuando lleguen las nuevas (E-186).

## 4. Las tres armaduras y las clases (D-208)

**Sin malla, las clases que la usaban pasan a otro tipo.** Propuesta (E-171):

| Clase | Antes | Ahora (propuesta) | Por qué |
|---|---|---|---|
| 🏹 Cazador | Malla | **Cuero** | En el WoW clásico usaba cuero hasta el nivel 40; es de Agilidad, como el Pícaro |
| 🌊 Chamán | Malla | **Placa** | Queda como el Paladín, un híbrido pesado de Intelecto con escudo; así placa no se queda con solo 3 clases |
| 🐲 Evocador | Malla | **Tela** | Lanza hechizos y cura con Intelecto, como el Mago y el Sacerdote |

**Las familias de equipo: quién comparte qué.** La estadística principal de una pieza **se adapta a quien la lleva** (como en el WoW moderno, E-170): una pieza de placa da Fuerza al Guerrero e Intelecto al Paladín Sagrado. Así cada pieza sirve a 2 o 3 clases o más, como pidió el dueño.

| Familia | Clases (especializaciones) | Cuántas clases |
|---|---|---|
| 🛡️ Placa · 💪 Fuerza | Guerrero (todas), Caballero de la Muerte (todas), Paladín (Reprensión y Protección) | 3 |
| 🛡️ Placa · 🔮 Intelecto | Paladín (Sagrado), Chamán (todas) | 2 |
| 🦺 Cuero · 🏹 Agilidad | Pícaro, Cazador, Cazador de demonios (todas); Monje (Viajero del Viento, Maestro Cervecero), Druida (Feral, Guardián), Bardo (Duelista) | 3 puras + 3 híbridas |
| 🦺 Cuero · 🔮 Intelecto | Monje (Tejedor de Niebla), Druida (Restauración, Equilibrio), Bardo (Trovador, Estratega) | 3 |
| 👘 Tela · 🔮 Intelecto | Sacerdote, Mago, Brujo, Nigromante, Evocador | 5 |

Quedan **4 clases en placa, 6 en cuero y 5 en tela**. Las secundarias deciden qué pieza prefiere cada una: los tanques buscan Versatilidad y Maestría, el daño físico Crítico y Celeridad, los hechiceros Crítico y Maestría, los sanadores Celeridad y Maestría. Así dos piezas del mismo tipo no valen lo mismo para todos, y hay mercado.

**Armas y joyas.**
- **Armas:** la espada da Fuerza, la daga y el arco Agilidad, el bastón Intelecto. La daga del Nigromante se adapta a Intelecto.
- **Joyas** (anillos, collares, amuletos): sin estadística principal, solo Vitalidad, secundarias y los bonos con que las crea el Joyero o el Alquimista (D-199). Nunca llevan gemas.

**Quién fabrica cada tipo:** placa la 🔨 Herrería, cuero la 🦺 Peletería, tela la 🪡 Sastrería. El ⛓️ Mallero desaparece antes de existir (D-208 cierra E-143) y la especialización de malla de la Peletería se cambia gratis (§8).

## 5. Cuatro habilidades por especialización (D-209)

- **Cuántas.** Cada especialización tiene 4 habilidades, no más (antes 8, D-79).
- **Atacar.** Falta decidir si ⚔️ Atacar cuenta como una de las 4 (E-172). **Recomendado: sí.** Atacar y 3 habilidades, todas en la barra y sin tener que elegir, como ya decía D-46 ("las 4 habilidades de la barra"). Si no cuenta, serían Atacar y 4 más, y la barra pasaría de 6 botones o habría que elegir 3 de 4.
- **Cuáles quedan.** Se decide junto con las clases personalizadas (D-214, E-182): las clases de hoy son solo el punto de partida. Cada una conserva una respuesta al aviso, lo que hace su rol y su firma del WoW.
- **Cuándo se abren.** Con 1, 3 y 6 puntos de talento, como las 3 habilidades originales.

## 6. Lo que se mejora dentro de las clases (todas las versiones del WoW)

| Sistema del WoW | Versiones | Qué era | Propuesta |
|---|---|---|---|
| Talentos en árbol | Clásico a Cata, DF y TWW | Puntos en árboles largos | ❌ Demasiado pesado para un juego de texto |
| **Filas de talentos** | MoP a SL | Cada 15 niveles eliges 1 de 3 | ✅ **Recomendado (E-174):** cada 15 niveles (15, 30, 45, 60, 75 y 90), 1 de 3 mejoras que cambian una de tus 4 habilidades o suman un pasivo; se cambia fuera de combate. La mejora pasiva de hoy por punto se queda |
| Glifos | WotLK a MoP | Pequeños cambios o cosméticos | ⏳ Más adelante, con el ✨ Encantamiento |
| Gemas y engarces | TBC en adelante | Gemas en las piezas | ✅ Ya decidido (D-198, D-199) |
| Encantamientos | Todas | Mejoras en las piezas | ✅ Ya en el juego |
| **Bonos de conjunto** | Todas | 2 y 4 piezas del mismo conjunto dan un efecto | ✅ Recomendado (E-175): conjuntos por familia de equipo, fabricados por los artesanos y de mazmorras |
| Reforja | Cata y MoP | Cambiar una secundaria por otra | ⏳ Más adelante, como servicio del Encantamiento |
| Arma artefacto, legendarios | Legion, SL | Un arma que crece o efectos únicos | ❌ Choca con "lo mejor lo fabrican los jugadores" (D-113) |
| Azerita, esencias, pactos, almas vinculadas, conductos | BfA, SL | Capas de poder por expansión | ❌ Demasiadas capas |
| Runas de grabado | Clásico de temporada | Runas que dan habilidades nuevas | ❌ Rompe las 4 habilidades |
| **Adornos de artesano** | DF | Efectos especiales en piezas fabricadas (máximo 2) | ✅ Recomendado (E-175): le da trabajo a los oficios |
| Talentos de héroe | TWW | Un tercer árbol | ❌ |

## 7. Cómo se ve en Telegram (ejemplo)

```
🛡️ Peto de roble del Herrero (placa) · nivel 20
💪/🔮 Principal +38 (Fuerza o Intelecto, según quién lo lleve)
❤️ Vitalidad +52 · 🛡️ Armadura +4 %
🎯 Crítico +21 · 🌀 Maestría +17
💎 Engarce vacío
```

La ficha del héroe suma una sección "📊 Estadísticas" con el porcentaje de cada una. La pantalla de combate no cambia: los botones son los mismos.

## 8. Qué pasa con los jugadores de hoy (D-64: nada se pierde)

- **Piezas de malla:** cada una se vuelve la misma pieza (mismo nivel, ranura y calidad) del tipo nuevo de la clase de quien la tiene: cuero para el Cazador, placa para el Chamán y tela para el Evocador; las de cualquier otra clase, cuero. Los IDs viejos se marcan `retired: true` (E-176).
- **Especialización de malla de la Peletería:** quien la eligió puede cambiarla gratis una vez.
- **Estadísticas de las piezas de hoy:** cada pieza recibe las nuevas sin perder poder. La vida pasa a Vitalidad, el ataque a la principal, la armadura se queda, y se suman secundarias según su calidad.
- **Habilidades:** las que salen se marcan `retired: true`. La barra se arma sola con las que quedan, los puntos de talento siguen sumando la mejora pasiva y nadie baja de nivel.
- **Cambio de clase de armadura:** el Cazador, el Chamán y el Evocador no pierden nada; solo cambia qué tipo rinde al 100 %.

## 9. Impacto en el código (para cuando el dueño apruebe)

**Riesgo alto:** toca el combate de todos.

| Qué | Archivos | Qué cambia |
|---|---|---|
| Estadísticas del héroe | `engine/hero/hero.py` (`hero_stats`), `engine/combat/engine.py` | Principal, Vitalidad, secundarias, terciarias y resistencias |
| Clases | `content/classes.yaml` (46 especializaciones) | Principal por especialización, Maestría, 4 habilidades, armadura de Cazador, Chamán y Evocador |
| Equipo | `content/items.yaml` (miles de piezas), `balance.yaml gear` | Estadísticas nuevas por pieza, sin malla |
| Botín y fabricación | `engine/service/game.py`, `content/professions.yaml` | Qué secundarias salen, recetas de malla retiradas |
| Textos | `content/locales/` | Nombres y explicación de cada estadística |
| Balance | `tools/sim.py`, `tools/balance_report.py`, `tests/test_balance_d110.py` | Medir rol por rol del 1 al 100 antes de subir (D-110) |

**Por fases** (con uno o dos ayudantes, D-59):
1. Tres armaduras y migración de la malla.
2. Cuatro habilidades.
3. Estadísticas de la capa simple.
4. Capa profunda, filas de talentos, conjuntos y adornos.

Cada fase con su parche, sus pruebas y su medición.

## 10. Preguntas para el dueño

En el [Sistema de preguntas](../00-vision/sistema-de-preguntas.md), tanda 1, bloques A4 y A5 (**E-170 a E-176** y **E-182 a E-186**), y en [Preguntas abiertas](../00-vision/preguntas-abiertas.md) (P-169 a P-175 y P-181 a P-185).

## 11. De dónde sale

- **World of Warcraft, todas las versiones:** la lista de estadísticas y por qué se quitaron unas (golpe y pericia en WoD, defensa y penetración en Cata, espíritu en Legion); la Maestría por especialización (Cata); la principal que se adapta a la especialización (WoD); las filas de talentos (MoP); los adornos de artesano (DF); los bonos de conjunto (desde Clásico).
- **Albion Online y Guild Wars 2:** pocas habilidades por arma o configuración, fáciles de leer.
- **Diablo:** afijos que hacen que dos piezas del mismo nivel no valgan lo mismo.
