# Defensa y protecciones de lo construido

> **Módulo** [09 · Construcción](README.md) · **Depende de:** [Sistema de construcción](sistema-de-construccion.md), [Combate](../04-combate/README.md), [Avisos y tácticas](../04-combate/avisos-y-tacticas.md) · **Se conecta con:** [PvP](../06-contenido/pvp.md), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (ecología), [Profesiones](../07-economia/profesiones.md) · **Estado:** propuesta

**Interpretación.** Pediste "sistemas de protecciones controladas de enemigos". Aquí se entiende como **defender lo que construiste** (casa, granja, salón, fortaleza, asentamiento) de ataques de monstruos y de jugadores, con defensas y guardias que **tú configuras y controlas**, y con protecciones para que nadie pierda todo mientras duerme. Si la idea era otra, se ajusta.

**De dónde sale.**
- *Valheim* y *Conan Exiles*: los monstruos atacan las bases de los jugadores en oleadas (en Conan, "la Purga").
- *Rust* y *Clash of Clans*: defensas de base, y **escudos** de protección después de un ataque o mientras estás desconectado.
- *They Are Billions* y los juegos de defensa de torres: oleadas que se ven venir.
- *Albion Online* y *Lineage 2*: ventanas de asedio a horas fijas elegidas por el defensor.
- *Final Fantasy XII*: las reglas automáticas (*gambits*) para que tus guardias actúen solos.

---

## 1. Quién ataca y dónde

| Amenaza | Dónde | Cuándo |
|---|---|---|
| **Alimañas** (plagas, ladrones de cosecha) | Granjas y casas en zonas amarillas | Frecuente, poco daño |
| **Incursión de monstruos** | Construcciones en zonas amarillas, rojas y negras | Cuando la población de una especie crece sin control (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)), en eclipses o en luna llena |
| **Invasión del piso** | Asentamientos enteros | Evento de servidor (ver [Eventos](../06-contenido/eventos.md)) |
| **Saqueadores** (jugadores) | Construcciones en zonas rojas | En cualquier momento, salvo protección activa |
| **Asedio** (gremios) | Fortalezas en zonas negras | En la ventana de asedio que eligió el defensor |
| **Redada de la guardia** | Garitos y casinos ilegales | Evento (ver [Apuestas](../08-social/apuestas.md)) |

Las construcciones en **zonas azules nunca son atacadas.** Quien quiera paz absoluta la tiene; quien construye en zonas peligrosas gana más (más producción, más recursos, territorios) y acepta defender.

## 2. Las defensas

Todas se **construyen o se fabrican** (con su plano, sus materiales y sus jornadas), tienen durabilidad y se reparan:

| Defensa | Qué hace | Quién la hace |
|---|---|---|
| **Cerco y empalizada** | Frena a las alimañas | Construcción (Peón) |
| **Muralla** | Resiste el daño; hay que romperla para entrar | Construcción (Albañil o más), Cantería |
| **Puerta reforzada** | Un punto fuerte que se puede cerrar | Construcción + Herrería |
| **Torre de vigía** | Aviso anticipado: te llega un mensaje antes del ataque | Construcción |
| **Torre de arqueros o balista** | Ataca sola en cada ronda de la defensa | Carpintería + Ingeniería |
| **Trampas** (fosos, cepos, pinchos, runas explosivas) | Daño y control a los atacantes que pasan | Ingeniería, Herrería, Encantamiento |
| **Protección rúnica** | Escudo mágico que absorbe daño hasta romperse | Encantamiento |
| **Alarma mágica** | Te avisa por Telegram, aunque estés desconectado | Inscripción |
| **Guardias** | PNJ contratados o seguidores (ver [Casa propia](casa-propia.md)) que pelean por ti | Se contratan y se equipan con equipo real |
| **Perros y bestias de guardia** | Detectan el sigilo y atacan | Crianza y doma (captura viva en [Cacerías](../06-contenido/cacerias.md)) |

## 3. Defensas que tú controlas

**Las defensas y los guardias pelean con reglas que tú escribes**, las mismas [Tácticas](../04-combate/avisos-y-tacticas.md) del combate:

```
Guardia 1 (Capitán Orrin, lanza):
1. Si un enemigo está en la puerta      → Estocada Profunda
2. Si hay un aliado derribado           → Levantar
3. Si mi vida < 25 %                    → Retroceder al salón
4. Siempre                              → Proteger la puerta

Torre de arqueros:
1. Si hay enemigos con escudo           → Flecha perforante
2. Si hay un enemigo lanzando hechizo   → Disparo de interrupción
3. Siempre                              → Al más cercano
```

- **Si estás conectado** cuando llega el ataque, te avisa el bot y puedes **tomar el mando**: juegas la defensa por rondas, dando órdenes a guardias y torres, además de pelear con tu héroe.
- **Si no estás**, la defensa se resuelve sola con tus reglas, y te llega el parte.
- **Tus amigos y tu gremio** reciben el aviso y pueden entrar a defender (como los signos de invocación, ver [Jefes](../06-contenido/jefes.md)).

## 4. Cómo se resuelve un ataque

1. **Aviso.** Si tienes torre de vigía, llega un mensaje con tiempo ("*una manada de lobos de hielo baja hacia tu granja: llegan en 20 minutos*").
2. **Oleadas.** El ataque llega en 2 a 5 oleadas, cada una resuelta con el combate por rondas en un **tablero de nodos** (puerta, muralla, patio, salón, almacén).
3. **Defensas en acción.** Las torres disparan, las trampas saltan, los guardias siguen sus reglas.
4. **Resultado:**
   - **Defendido:** botín de los atacantes (materiales de monstruo, trofeos) y experiencia para los guardias.
   - **Brecha:** los atacantes llegan al almacén y roban una parte (nunca todo), o dañan edificios que hay que reparar.
5. **Parte:** un resumen reenviable, con los detalles plegados.

## 5. Protecciones (para no perderlo todo mientras duermes)

| Protección | Cómo funciona | De dónde sale |
|---|---|---|
| **Zona azul** | Lo que está en zona azul nunca se ataca | Albion |
| **Escudo de protección** | Después de un ataque de jugadores, la construcción queda protegida un tiempo (por ejemplo, 24 horas) | *Clash of Clans* |
| **Horas protegidas** | El dueño elige un tramo diario en el que no pueden atacarlo jugadores (su horario de dormir) | *Rust* (servidores con protección offline) |
| **Ventana de asedio** | Las fortalezas solo se asedian en la ventana semanal que elige el defensor | Albion, *Lineage 2* |
| **Bóveda** | Una parte del almacén nunca se puede robar | *Clash of Clans* |
| **Seguro** | Se paga una prima y se cobra parte de lo perdido (ver [Economía](../07-economia/economia.md)) | EVE |
| **Novato protegido** | Las construcciones de jugadores de nivel bajo no se atacan | Varios |

## 6. Cómo se conecta con todo

- **Farmeo:** la ecología decide cuándo llegan las incursiones; cazar a tiempo las evita.
- **Fabricación:** cada defensa y cada guardia equipado sale de los artesanos.
- **Construcción:** reparar después de un ataque es trabajo pagado para los constructores.
- **Salud:** los guardias y los defensores se hieren; los médicos los curan.
- **Progresión:** las defensas tienen rangos y mejoras, y los guardias suben de nivel.
- **PvP:** saqueos y asedios en zonas rojas y negras.
