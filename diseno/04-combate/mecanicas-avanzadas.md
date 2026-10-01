# Mecánicas avanzadas de combate

> **Módulo** [04 · Combate](README.md) · **Depende de:** [Ronda y acciones](ronda-y-acciones.md), [Daño y estados](dano-y-estados.md), [Avisos y tácticas](avisos-y-tacticas.md), [Clases](../03-personaje/clases-y-especializaciones.md), [Balance](../03-personaje/balance.md) · **Se conecta con:** [Jefes](../06-contenido/jefes.md), [PvP](../06-contenido/pvp.md), [Geografía y recursos](../02-mundo/geografia-y-recursos.md), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md), [Cacerías](../06-contenido/cacerias.md), [Crimen y justicia](../06-contenido/crimen-y-justicia.md), [Heridas](../05-salud/heridas.md), [Peligros del entorno](../05-salud/peligros-del-entorno.md), [Profesiones](../07-economia/profesiones.md) · **Estado:** propuesta

**De dónde sale.** Cada mecánica dice su origen en su apartado. En resumen:
- *Octopath Traveler*: escudos y debilidades que rompen al enemigo (§3), y guardar puntos para gastarlos juntos (§12).
- *Persona* y *Shin Megami Tensei III: Nocturne*: el turno extra por pegar una debilidad (§4).
- *Chrono Trigger*: técnicas dobles y triples entre personajes (§5).
- *Divinity: Original Sin 2*: superficies y nubes que reaccionan entre sí (§6).
- *Fire Emblem*, *XCOM* y *Darkest Dungeon*: el terreno, la altura y la luz (§7).
- *Final Fantasy*, *D&D 5.ª edición* y *Darkest Dungeon*: la sorpresa y la emboscada (§8).
- *Battle Brothers*, *Persona 5*, *Undertale* y *Monster Hunter*: enemigos que huyen, se rinden o se enfurecen (§9).
- *Final Fantasy VII* y *Final Fantasy X*: la barra de Límite (§10).
- *Sekiro* y *Clair Obscur: Expedition 33*: el desvío perfecto y el contraataque (§11).
- *Bravely Default*: defender para guardar y soltarlo todo después (§12).

**Por qué este documento.** El motor base (rondas simultáneas, avisos, barras, filas) ya hace que el combate sea de lectura y no de reflejos. Estas diez mecánicas le suman **decisiones en cada ronda**: a quién romper, con quién combinar, dónde prender el aceite, cuándo guardar y cuándo soltar. Ninguna suma botones ni rompe el presupuesto de poder.

---

## 1. Reglas para todas

1. **Ningún botón nuevo y una sola elección por ronda.** La barra es de 6 botones (D-46, ver [Ronda y acciones](ronda-y-acciones.md)): no hay acción rápida, ni botón de Defender, ni menú de Más. Cada mecánica transforma un botón, usa una respuesta o un objeto de la 🎒 Mochila, o se dispara sola.
2. **Leer, no apretar rápido.** Todo se decide al elegir la ronda, con lo que dice el aviso. Nada depende de la velocidad del pulgar.
3. **Todo tiene tope**, por ronda o por pelea.
4. **Todo pasa por el simulador** y cuenta en un eje del presupuesto de 100 puntos (ver [Balance](../03-personaje/balance.md)).
5. **Todo le da trabajo a alguien:** aceites, frascos, botas, grilletes, pergaminos (§14).
6. **Nada es permanente.** Lo peor que dejan es una herida que se cura (ver [Heridas](../05-salud/heridas.md)). Fuera del Juramento de Hierro, nada arruina un personaje.
7. **Amplio pero ligero** (D-44 en [Decisiones](../00-vision/decisiones.md)). La capa simple es jugar normal: las [Tácticas](avisos-y-tacticas.md) por defecto ya rompen, reaccionan y guardan cargas a un nivel básico. La capa profunda (combinar, encadenar, leer la forma de cada golpe) es para quien la busca.

### Dónde vive cada mecánica

| Mecánica | Dónde se elige | ¿Suma botones? |
|---|---|---|
| Ruptura | Sale sola al pegar debilidades, o apuntando con **⚔️ Atacar** a una parte débil | No |
| Golpe extra | Sale solo al final de la ronda; no se elige | No |
| Técnicas combinadas | Se disparan solas si coinciden las etiquetas; el bot marca con 🔗 la habilidad que combina | No |
| Elementos y superficies | Habilidades con elemento y lanzables del cinturón (**🎒 Mochila**) | No |
| Terreno | Se aplica solo | No |
| Emboscada | Antes del combate, en el mensaje de exploración | No (fuera del combate) |
| Moral y rendición | Tres botones de voto que reemplazan la botonera mientras dura el temporizador de la ronda | No (reemplaza) |
| Límite | **Atacar** se convierte en el Límite cuando la barra está llena | No (reemplaza) |
| Reacciones avanzadas | Las respuestas de siempre, elegidas como la jugada de la ronda; lo nuevo es acertar la forma y la ronda | No |
| Guardar y soltar | Usar una **respuesta** guarda una carga; las cargas se **desatan** solas contra un enemigo roto | No |

### Orden de aprendizaje y protección de novato

| Nivel | Se abre | Por qué ahí |
|---|---|---|
| 1 | Ruptura y golpe extra | Se entienden con el primer enemigo: "pégale donde le duele" |
| 3 | Superficies | El primer frasco de aceite llega en el tutorial del Claro |
| 5 | Reacciones perfectas | Ya conoces los avisos |
| 7 | Guardia y Desatar | Ya sabes reconocer una ventana |
| 10 | Técnicas combinadas, Límite y emboscadas totales **contra ti** | Llega la clase y termina la protección de novato |
| Siempre | Terreno y moral enemiga | Son del mundo, no del jugador |

---

## 2. Etiquetas e iconos

Las mecánicas usan dos juegos de iconos que no se mezclan.

**Tipos de daño** (para debilidades y resistencias, ver [Daño y estados](dano-y-estados.md)): 🪓 Corte · 🏹 Perforación · 🔨 Contundente · 🔥 Fuego · ❄️ Escarcha · 🌿 Naturaleza · ⚡ Rayo · 🔮 Arcano · 🌑 Sombra · ✨ Sagrado · 🕳 Vacío.

**Etiquetas de técnica** (para las técnicas combinadas, §5). Cada habilidad de clase y cada técnica de equipo lleva **una sola** etiqueta, que se lee en su descripción y en el registro. ⚔️ Atacar y 🌀 Esquivar no llevan etiqueta:

| Etiqueta | Qué habilidades la llevan |
|---|---|
| 💥 Pesado | Golpes que bajan Postura: *Golpe Colosal*, *Quebrantahuesos* |
| 🛡 Guardia | Bloqueos, provocaciones, muros |
| ✚ Cura | Curas directas y escudos de sanador |
| 🎯 Marca | Marcar, revelar, apuntar a una parte |
| 🌀 Control | Aturdir, paralizar, silenciar, derribar |
| 💨 Movimiento | Saltos, cargas, cambios de fila ofensivos |
| 🐾 Bestia | Órdenes a la mascota |
| 💀 Esbirro | Invocaciones y esbirros |
| 🎵 Canción | Canciones y compases del Bardo |
| 🩸 Sangre | Sangrados y robo de vida |
| 🟢 Plaga | Venenos y enfermedades de combate |
| 🔥 ❄️ ⚡ 🌿 ✨ 🌑 🔮 | El elemento o la escuela mística de la habilidad |

---

## 3. Ruptura

**De dónde sale.** *Octopath Traveler* (2018). Cada enemigo tiene un número de escudos y unas debilidades ocultas (tipos de arma y elementos) que se descubren probando. Cada golpe a una debilidad quita un escudo. Sin escudos, el enemigo queda roto: pierde su turno y recibe más daño.

**Cómo funciona.**
- Casi todo enemigo tiene **🔰 Escudo** (fichas) y de 1 a 4 **debilidades**, entre tipos de daño y partes del cuerpo.
- Las debilidades empiezan como ❓. Se revelan al pegarlas, con el Bestiario (3 victorias), con la Marca del Cazador o con una ficha del Informante (ver [Avisos y tácticas](avisos-y-tacticas.md)).
- Cada impacto que pega una debilidad quita 1 🔰. **Apuntar** a una parte débil (opción dentro de ⚔️ Atacar, o efecto de ciertas habilidades) también cuenta: el vientre expuesto del Wyrm de las Dunas es débil a perforación.
- Las habilidades de varios impactos quitan 1 por impacto, con tope de 2 por acción. Las técnicas combinadas y el Límite quitan 2.
- Con 🔰 en 0, el enemigo queda **💫 Roto**:
  - pierde su acción de esta ronda (si todavía no actuó) y la de la ronda siguiente;
  - **lo que estaba preparando se cancela**, aunque lo haya avisado;
  - no puede reaccionar (no bloquea ni esquiva);
  - recibe **+30 % de daño**.
- Al final de la ronda siguiente se recupera con el escudo lleno y la **Firmeza llena**: no se le puede aturdir enseguida.

| Enemigo | 🔰 | Debilidades | Al recuperarse |
|---|---|---|---|
| Común | 2-3 | 1-2 | Escudo lleno |
| Élite | 4-6 | 2-3 | Escudo lleno |
| Jefe de campo y Guardián | 6-10 por fase | 3-4 | Escudo lleno +1, y **Recompuesto** 2 rondas (el escudo no baja) |
| Muro | 10-14 por fase | 3-4, que cambian en cada fase | Igual que el Guardián |
| Enjambres e invocaciones menores | Sin escudo | — | Mueren rápido: no hace falta romperlos |

- **Golpes Inevitables.** Cada jefe tiene 1 o 2 movimientos que la ruptura no cancela, por ejemplo las transiciones de fase. El aviso los marca con ‼️.
- **En bandas**, el escudo del jefe sube 1 por cada 2 jugadores por encima de 5, y ningún jugador quita más de 2 🔰 por ronda.

### Ruptura y Postura conviven

| | 🟫 Postura | 🔰 Ruptura |
|---|---|---|
| Quién la tiene | Solo enemigos grandes | Casi todos los enemigos |
| Qué la baja | Golpes pesados, bloqueos y desvíos, de cualquier tipo de daño | Solo debilidades: tipo de daño o parte débil |
| Cómo se ve | Barra | Fichas e iconos de debilidad (❓ hasta descubrirlas) |
| Al romperse | Aturdido 1 ronda; la siguiente acción de cada jugador contra él es crítico | Pierde su acción, cancela lo que preparaba y recibe +30 % de daño |
| Premia | Al grupo que pega fuerte y lee los avisos | Al grupo que conoce al enemigo y lleva variedad de daño |
| Se recupera | De a poco | De golpe y llena |

Si las dos se rompen a la vez es un **Quiebre**: el enemigo no pierde más rondas, pero los premios se suman (crítico garantizado y +30 %). Es el momento de gastar el Límite (§10) y las cargas guardadas (§12).

**Botón.** Ninguno nuevo. Se rompe con las habilidades de siempre, eligiendo bien el tipo de daño, o con **Apuntar** a la parte débil. Los **aceites de arma** (Alquimia) cambian el tipo de daño del arma durante 3 rondas, desde la **🎒 Mochila** (gasta la ronda, como todo objeto).

**Cómo se ve.**

```
🦂 Escorpión de Vidrio (élite)  ❤️ 58%
🔰🔰🔰🔰 4   Débil: 🔨 ❄️ ❓
⚠️ Levanta el aguijón y apunta a Lyra…
```

```
🔨 Bram: Quebrantahuesos → DEBILIDAD · 🔰 1→0
💫 ¡RUPTURA! El Escorpión queda roto hasta el final de la ronda 5
   ✖ Aguijón sobre Lyra: cancelado
```

**Cómo se equilibra.**
- Toda spec pega al menos **dos tipos de daño** con su kit (arma incluida). Cualquiera suma un tercero con aceites de arma o con la técnica *Chispa* de la varita. Nadie queda sin forma de romper.
- Los enemigos mezclan debilidades físicas, elementales, místicas y de parte: ninguna composición queda afuera.
- El simulador mide las **rondas hasta la primera ruptura** de cada spec en cada escenario: todas a ±10 % de la mediana.
- En jefes, de 1 a 2 rupturas por fase en juego óptimo. Si un grupo rompe más, se sube el escudo; el daño no se toca.
- Eje del presupuesto: **Control**.

---

## 4. Golpe extra por debilidad

**De dónde sale.** La saga *Persona* (desde *Persona 3*) y su origen, el sistema *Press Turn* de *Shin Megami Tensei III: Nocturne*. Pegar una debilidad o hacer un crítico tumba al enemigo y da un turno extra ("One More"). Si caen todos, llega el *All-Out Attack*. En *Persona 5*, el *Baton Pass* le pasa el turno extra a un aliado, con un bono.

**Cómo funciona.** Hay una sola elección por ronda (D-46), así que el golpe extra **no se elige**: sale solo.
- Si tu acción pega una **debilidad** o hace un **crítico**, ganas un **✦ Golpe extra**: un ataque con tu arma al 50 %, que sale **al final de la misma ronda** contra el mismo objetivo (o el enemigo más cercano, si ese cayó). Suma acumulación y quita escudo si el arma es una debilidad.
- **🤝 Relevo.** Si tu arma no pega ninguna debilidad del objetivo y la de un aliado sí, el golpe extra pasa solo a ese aliado (al que no tuvo uno esta ronda), con +25 %. Así el mago que rompe con escarcha le pasa el golpe al arquero que pega el vientre.
- Las técnicas combinadas, el Límite y el contraataque de un desvío (§11) **no** dan golpe extra. El golpe extra no genera otro.
- **Tope:** 1 golpe extra por jugador por ronda.
- **Asalto Total.** Si todos los enemigos quedan rotos a la vez (los que no tienen escudo no cuentan), cada jugador recibe un golpe rápido gratis, que cuenta como su golpe extra de esa ronda (no se suma a otro). Si son humanoides, el grupo puede **intimidarlos** en lugar de pegar: se rinden (ver §9).
- **Los enemigos también lo usan.** Los que tienen el rasgo *Oportunista* ganan golpe extra cuando critican o cuando pegan a un jugador mojado, congelado o derribado. El Bestiario lo anota.

**Botón.** Ninguno: sale solo y aparece en el resumen de la ronda.

**Cómo se ve.**

```
✦ Golpe extra de Lyra (pegó una debilidad)
   → 🤝 Relevo a Ossian: su arco pega el VIENTRE
   🏹 Golpe rápido al VIENTRE: 118 · 🔰 1→0
```

**Cómo se equilibra.**
- Nunca hay más de **1 golpe extra por jugador y ronda**, venga de donde venga. Los efectos que antes daban una acción rápida extra (Clamor, *Enfurecido* del Guerrero Furia) ya dan iniciativa o potencia (ver [Ronda y acciones](ronda-y-acciones.md)), así que no se suman con este.
- El golpe extra vale poco a propósito: es medio ataque. Lo que vale es la decisión previa: llevar variedad de daño y elegir quién pega cada debilidad.
- El simulador mide el daño de los golpes extra: **no más del 8 %** del total de ninguna spec, y a ±2 puntos entre specs.
- No existe en PvP: los jugadores no tienen debilidades, y un crítico en PvP no regala turnos.
- Eje del presupuesto: **Daño sostenido**.

---

## 5. Técnicas combinadas

**De dónde sale.** *Chrono Trigger* (1995). Las técnicas dobles y triples unen las técnicas de dos o tres personajes en un ataque nuevo. Todos los que participan tienen que tener su turno listo a la vez, y cada uno paga su parte del costo.

**Cómo funciona.**
- Si dos (o tres) jugadores eligen en la misma ronda habilidades cuyas **etiquetas** (§2) forman una técnica, **y van al mismo objetivo** (el mismo enemigo, el mismo aliado o la misma fila), la técnica se dispara sola al resolverse la última de esas acciones.
- Cada uno paga su habilidad como siempre. La técnica **suma** un efecto; no reemplaza las acciones.
- Si una de las acciones no sale (la interrumpen, la esquivan, cae quien la usa), no hay técnica.
- **Topes:**
  - una técnica combinada por cada 5 jugadores por ronda;
  - cada jugador participa en una por ronda;
  - la misma técnica tiene 3 rondas de enfriamiento; las triples, 6.
- **Coordinación sin botones.** Mientras el grupo elige, el mensaje vivo muestra la etiqueta y el objetivo de lo que ya eligió cada aliado ("Lyra ❄️→Wyrm"), sin decir la habilidad exacta. Si una de tus habilidades completaría una técnica, su botón muestra 🔗. Puedes cambiar tu elección hasta que se acabe el tiempo.
- **Libro de Técnicas.** Al principio todas las técnicas están ocultas. La primera vez que una se dispara, queda en tu Libro (colección de cuenta, ver [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md)) y el bot empieza a sugerírtela. El primero del servidor en descubrir cada técnica entra al registro de descubridores. Inscripción vende **pergaminos de técnica** que la revelan sin haberla hecho: conocimiento, no poder.
- **Nombre propio, balance por etiqueta.** Cada pareja de la tabla tiene su nombre y su texto. Cualquier otra pareja con las mismas etiquetas dispara la misma técnica, con el mismo número y otro nombre. El sabor es de *Chrono Trigger*; el balance es por etiqueta.

### Técnicas dobles

| Técnica | Etiquetas | Pareja típica | Efecto |
|---|---|---|---|
| **Témpano Quebrado** | ❄️ + 💥 | Mago Escarcha + Guerrero Armas | El golpe pesado parte la escarcha: cuenta como debilidad doble (−2 🔰) y hace el doble de daño a la Postura. En humanoides PNJ, fractura segura |
| **Baluarte** | 🛡 + ✚ | Guerrero Protección + Sacerdote Disciplina | El bloqueo cubre a toda la vanguardia esa ronda, y el escudo preventivo pasa a toda la fila a mitad de valor |
| **Crepúsculo** | ✨ + 🌑 | Paladín Reprensión + Sacerdote Sombra | Daño que ignora resistencias místicas y quita un beneficio del enemigo |
| **Pira de Huesos** | 💀 + 🔥 | Nigromante Legión + Evocador Devastación | Los esqueletos de la vanguardia estallan en fuego: Quemadura en la fila de enfrente y la deja en 🔥 Llamas |
| **Tempestad** | ⚡ + 🌿 | Chamán Elemental + Druida Equilibrio | El rayo salta por toda la fila enemiga (hasta 3 objetivos). A los mojados los aturde |
| **Tijera** | 🎯 + 🎯 (misma parte) | Cazador Puntería + Pícaro Sutileza | La parte apuntada recibe el doble de daño de rotura esa ronda |
| **Pacto de Sangre** | 🛡 + 🩸 | Caballero de la Muerte Sangre + Nigromante Drenaje | El daño que ese enemigo le hace al tanque esta ronda vuelve como curación a la retaguardia (30 %) |
| **Epidemia** | 🟢 + 🟢 | Nigromante Plaga + Pícaro Asesinato | Las enfermedades de combate saltan a toda la fila y la barra de Veneno sube el doble |
| **Pinza** | 💨 + 🛡 | Cazador de Demonios Estrago + Paladín Protección | Provocado de frente y atacado por la espalda: el enemigo pierde su reacción y la *Puñalada Trapera* vale contra él |
| **Contrapunto** | 🎵 + 🌀 | Bardo Estratega + cualquier Monje (*Parálisis*) | El enemigo pasa al final de la cola y su aviso se retrasa una ronda. No vale contra golpes Inevitables |
| **Té de Raíces** | 🛡 + 🌿 | Monje Maestro Cervecero + Druida Restauración | Las curas en el tiempo purgan el *Tambaleo*: el daño repartido del tanque baja a la mitad |
| **Manada** | 🐾 + 🛡 | Cazador Bestias + Druida Guardián | Toda la fila enemiga ataca a la vanguardia 1 ronda, y la mascota flanquea: su próximo golpe es crítico |

### Técnicas triples

| Técnica | Etiquetas | Trío típico | Efecto |
|---|---|---|---|
| **Tríada Elemental** | 🔥 + ❄️ + ⚡ | Mago Fuego + Caballero de la Muerte Escarcha + Chamán Elemental | Daño elemental a todos los enemigos; cada uno pierde 1 🔰 por cada uno de esos tres elementos que sea su debilidad. Deja la fila ⚡ electrificada |
| **Muralla Viviente** | 🛡 + ✚ + 🎵 | Paladín Protección + Chamán Restauración + Bardo Trovador | El grupo entero ignora el siguiente golpe en área de esta ronda o la siguiente. No vale contra golpes Inevitables |
| **Sentencia** | 🎯 + 🌑 + 🩸 | Cazador Supervivencia + Brujo Aflicción + Pícaro Asesinato | Todas las barras de acumulación del objetivo revientan a la vez (en jefes, a mitad de efecto) |
| **Cacería Salvaje** | 🐾 + 💨 + 🩸 | Cazador Bestias + Cazador de Demonios Estrago + Druida Feral | El objetivo queda rodeado: no puede huir ni cambiar de fila en 3 rondas, y todos los golpes cuentan como por la espalda. Ideal contra presas que huyen (§9) |

Las 15 clases aparecen al menos una vez. Las demás specs entran con las mismas etiquetas.

**Botón.** Ninguno nuevo. Se eligen las habilidades de siempre; el 🔗 en el botón avisa que combinan.

**Cómo se ve.**

```
Elegido: Lyra ❄️→Wyrm · Bram 🛡 respuesta · Mirra ✚→vanguardia
🔗 Posible: Témpano Quebrado (Lyra ❄️ + tu 💥)
```

**Cómo se equilibra.**
- Una técnica doble vale entre un 20 % y un 35 % más que las dos acciones por separado. Una triple, hasta un 50 %.
- Toda spec tiene habilidades con al menos 3 etiquetas distintas. El simulador comprueba que cada spec pueda entrar en un número parecido de técnicas (±1): no hay spec "de combos" ni spec sin combos.
- Las técnicas piden etiquetas, no specs. Ninguna pelea pide "dos Chamanes" (ver [Balance](../03-personaje/balance.md), regla 10).
- El simulador mide su aporte: **no más del 10 %** del daño o la curación del grupo, y ninguna composición rinde más de un **5 %** por encima de la media gracias a ellas.
- **En PvP** (2v2, 3v3 y campos), los efectos de control de las técnicas (aturdir, inmovilizar, rodear) duran la mitad y llenan la Firmeza, no hay fractura segura y *Sentencia* revienta a mitad de efecto, como en jefes.
- En solitario cuentan el compañero PNJ de las [Profundidades](../06-contenido/misiones-y-exploracion.md), los Espíritus y los Ecos (ver [Jefes](../06-contenido/jefes.md)). Nadie queda afuera por jugar solo.
- Eje del presupuesto: **Utilidad de grupo**.

---

## 6. Elementos y superficies

**De dónde sale.** *Divinity: Original Sin 2* (2017). El suelo y el aire guardan superficies y nubes (agua, aceite, fuego, veneno, hielo, vapor, humo) que reaccionan entre sí. El agua electrificada aturde, el aceite se prende, el veneno explota con fuego y el hielo hace resbalar. Las superficies también se pueden bendecir o maldecir.

**Cómo funciona.** En lugar de casillas, cada **fila** de cada bando guarda dos estados:
- 1 **superficie** (en el suelo), que dura 3 rondas;
- 1 **nube** (en el aire), que dura 2 rondas.

Una superficie nueva que no reacciona con la anterior la reemplaza. Para salir de una, se cambia de fila con una respuesta 🔁 o 💨 (ver [Ronda y acciones](ronda-y-acciones.md) §8), salvo que el suelo lo impida.

| Estado | De dónde sale | Qué le hace a quien está en esa fila |
|---|---|---|
| 💧 **Agua** | Lluvia, pantano, hechizos de agua, frascos | Queda **Mojado** 2 rondas: la Congelación acumula ×1,5 y la Quemadura ×0,5. Es el mismo Mojado de [Peligros del entorno](../05-salud/peligros-del-entorno.md); la capa encerada lo evita |
| 🛢 **Aceite** | Frascos de Alquimia, babosas, gólems de brea | Pegajoso: las respuestas 💨 y 🔁 cuestan +1 🔋. Muy inflamable |
| 🔥 **Llamas** | Fuego sobre aceite, suelo volcánico | Daño pequeño por ronda y acumulación de Quemadura |
| 🧊 **Hielo** | Escarcha sobre agua | Resbaladizo: esquivar cuesta +1 🔋, y quien recibe un golpe 💥 cae (la ronda siguiente no puede usar respuestas) |
| 🟩 **Charco tóxico** | Venenos, Nigromante Plaga, criaturas de pantano | Acumulación de Veneno cada ronda |
| ☁️ **Vapor** | Fuego sobre agua | Precisión a distancia −15 % hacia y desde esa fila |
| 🌫 **Niebla o humo** | Clima, bombas de humo (Ingeniería), tormentas de arena | Precisión a distancia −25 % hacia y desde esa fila; +2 al sigilo (§8) |
| ☣️ **Nube tóxica** | Bombas de veneno, criaturas pútridas | Acumulación de Veneno cada ronda |
| ⚡ **Nube eléctrica** | Rayo sobre vapor | Aturde 1 ronda a los mojados de la fila |

### Reacciones

| Sobre… | + 🔥 Fuego | + ❄️ Escarcha | + ⚡ Rayo |
|---|---|---|---|
| 💧 Agua | ☁️ Vapor | 🧊 Hielo | Agua electrificada: aturde a los mojados |
| 🛢 Aceite | 💣 Estallido y 🔥 Llamas | Se espesa: pegajoso 2 rondas más | 🔥 Llamas |
| 🟩 Charco tóxico | 💣 **Se inflama**: estallido de fuego y 🔥 Llamas | 🧊 Hielo | — |
| 🔥 Llamas | Se avivan: +1 ronda | Se apagan y queda 💧 Agua | — |
| 🧊 Hielo | Se derrite en 💧 Agua | +1 ronda | — |
| ☁️ Vapor | — | Se condensa en 💧 Agua | ⚡ Nube eléctrica |
| ☣️ Nube tóxica | 💣 **Explota**: gran estallido en la fila | — | — |
| 🌫 Niebla | Se disipa | — | — |

- **✨ Sagrado consagra** la superficie: el agua cura un poco por ronda a los aliados y quema a los no-muertos; las llamas consagradas no queman a los aliados. **🌑 Sombra la maldice**: el fuego maldito no se apaga con agua y el agua maldita sube el estrés (ver [Mente](../05-salud/mente.md)).
- **Todo aturdimiento llena la Firmeza**, como cualquier control. El agua electrificada no sirve para dejar quieto a un jefe.
- **Las vanguardias se tocan.** Un 💣 estallido en una vanguardia salpica a la otra a mitad de daño. Prender el aceite bajo el enemigo cuando tu tanque está pegado a él tiene precio.

**Botón.** Las habilidades con elemento de siempre, la técnica *Chispa* de la varita (enciende) y los **lanzables** del cinturón (**🎒 Mochila**): frascos de aceite, agua y veneno (Alquimia), bombas de humo y de escarcha (Ingeniería). Máximo **3 lanzables por pelea**.

**Cómo se ve.**

```
Filas enemigas: Vanguardia 🛢 Aceite (2) · Retaguardia 🌫 Niebla (1)
Tus filas:      Vanguardia —            · Retaguardia —
⚠️ La Babosa de Brea se infla… va a escupir aceite
   sobre tu VANGUARDIA.
```

**Cómo se equilibra.**
- Las superficies **no distinguen bandos**: los enemigos también las crean y las prenden, y los avisos lo dicen.
- Un estallido nunca le quita a un jugador más del **20 % de su vida máxima**. A un jefe le quita una cantidad fija, no un porcentaje: no sirve para derretir jefes de 6 dígitos.
- Toda spec puede crear y detonar con lanzables y con la varita. Las specs elementales lo hacen sin gastar lanzables, y eso ya está contado en su presupuesto.
- El simulador mide el **daño de entorno**: no más del 15 % del total de un grupo en juego óptimo.
- Ejes del presupuesto: **Control** (lo que estorba) y **Daño sostenido** (los estallidos).

---

## 7. Terreno de combate

**De dónde sale.** *Fire Emblem* (el bosque da evasión y cuesta movimiento), *XCOM* (la altura da puntería), *Darkest Dungeon* (la luz de la antorcha cambia el riesgo de cada sala) y *Divinity: Original Sin 2* (la lluvia moja a todos).

**Cómo funciona.** Cada combate ocurre en un nodo del mapa, con el terreno de ese nodo (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md)), el clima del piso y la hora (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)). La cabecera del combate lo dice, y **se sabe antes de entrar**: prepararse es parte del juego.

Dos capas, sin repetir reglas:
- **Peligros** (frío, calor, sed, gas, oscuridad, tormenta, lava). Sus efectos por ronda, sus etapas y su equipo están en [Peligros del entorno](../05-salud/peligros-del-entorno.md). Las criaturas nativas no los sufren; los visitantes sí.
- **Táctica** (este apartado). Lo que el terreno le hace a las filas, las superficies, la precisión y el sigilo. Vale igual para los dos bandos.

**Regla de oro:** el terreno mueve acumulaciones, precisión, iniciativa, Aguante y filas. **Casi nunca el daño bruto.**

| Terreno o clima | Dónde | Efecto táctico en la ronda | Contra (y quién lo fabrica) |
|---|---|---|---|
| ❄️ **Nieve profunda** | Tundra, tramo VI (Picos Helados), ventisca | Además de lo que dice Peligros del entorno (cambiar de fila cuesta la acción entera, huir falla el doble, esquivar cuesta +1 🔋): la Congelación acumula +25 % | Raquetas de nieve (Carpintería y Peletería) |
| 🐸 **Pantano** | Tramo IV (Pantano Putrefacto) | Las dos vanguardias empiezan en 💧 Agua. Cada 3 rondas aparece un 🟩 charco tóxico (avisado). Las picaduras suman Veneno y pueden traer la Fiebre del Pantano (ver [Enfermedades](../05-salud/enfermedades.md)) | Repelente (Herboristería y Alquimia), máscara con filtro contra la miasma |
| 🌑 **Oscuridad** | Cuevas (tramo III), noche sin luz, tramo IX (Abismo Umbrío) | La precisión baja según la etapa de oscuridad (ver Peligros del entorno). Además: los avisos llegan con menos detalle y +2 al sigilo | Antorcha (Carpintería) o farol (Herrería): quita la penalización en tu fila, pero te delata y los enemigos te eligen primero |
| ⛰️ **Altura** | Montaña, tramo VII (Ruinas Olvidadas), tierras flotantes, murallas | El bando alto tiene +10 % de precisión a distancia y sus golpes 💥 derriban. El bajo necesita una Carga o una ronda para subir | *Carga* (botas de placas), *Salto Vil* |
| 🌧 **Lluvia** | Clima | Las filas a cielo abierto quedan 💧 Mojadas (el mismo estado de Peligros del entorno: además, el frío cuenta un punto más). Quemadura ×0,5. Arcos −10 % de precisión | Capa encerada (Sastrería): nunca quedas Mojado. Cuerdas enceradas (Carpintería) para los arcos |
| 🌫 **Niebla** | Clima | 🌫 en todas las filas: precisión a distancia −25 % (reemplaza la penumbra de Peligros del entorno; no se suman), +2 al sigilo | — (es de los dos bandos) |
| ⛈ **Tormenta** | Clima, terreno abierto | El rayo avisado de Peligros del entorno busca a quien lleve más metal. Si cae en una fila 💧 Mojada, salta a todos los mojados de esa fila | Capa encerada; soltar el arma de metal |
| 🏜️ **Tormenta de arena** | Desierto, tramo V (Desierto Ardiente) | Las ráfagas dejan 🌫 en la vanguardia | Velo de desierto (Sastrería): ves en la tormenta |
| 🌋 **Suelo volcánico** | Tierras volcánicas, tramo VIII (Ciudadela en Llamas) | Grietas avisadas dejan 🔥 Llamas en una fila. Un golpe 💥 cerca del borde de lava deja una quemadura grave | Botas de obsidiana (Herrería) |
| 🌲 **Bosque espeso** | Bosque, tramo I (Bosque Susurrante) | La retaguardia tiene cobertura: −10 % de precisión a distancia contra ella. +1 al sigilo | — |
| 🕳 **Pasillo estrecho** | Cuevas, laberintos, mazmorras | Caben como máximo 2 combatientes por vanguardia. Los golpes en área alcanzan a menos | — |

**Botón.** Ninguno: se aplica solo. Los contras son el equipo de [Peligros del entorno](../05-salud/peligros-del-entorno.md) y se preparan antes de salir.

**Cómo se ve.**

```
⚔️ Ronda 1 · Saqueadores de Turba (3)
📍 Pantano · 🌧 Lluvia · 🌙 Noche
Terreno: vanguardias en 💧 Agua · todos Mojados
         esquivar +1 🔋 · fuego débil · rayo fuerte
```

**Cómo se equilibra.**
- Los efectos tácticos valen para los dos bandos. La ventaja es de quien se preparó.
- El simulador corre cada spec en una **rueda de terrenos**: en promedio, todas a ±5 % de la mediana, y ninguna pierde más del 10 % en un terreno si lleva su contra.
- Cada Guardián tiene una guarida con terreno fijo, que figura en su ficha: el Wyrm pelea en arena.
- La arena clasificada de PvP es siempre terreno neutro.
- No es un eje del presupuesto: se mide como **dispersión** entre terrenos.

---

## 8. Emboscada e iniciativa inicial

**De dónde sale.** El ataque preventivo y el ataque por la espalda de la saga *Final Fantasy*, que en los juegos con filas invierte las del grupo sorprendido. La sorpresa de *D&D 5.ª edición*: sigilo contra percepción, y el sorprendido no actúa en su primer turno. Y *Darkest Dungeon*, donde la luz de la antorcha cambia quién sorprende a quién.

**Cómo funciona.** Antes de un combate en el mundo abierto (nodos, cacerías, caravanas, zonas rojas), el bot compara dos números:
- **Sigilo** de quien se acerca: 10 más modificadores. El grupo usa el sigilo de su miembro **más ruidoso**.
- **Alerta** de quien espera: 10 más modificadores.

Cada lado suma un 🎲 nativo de Telegram, tirado a la vista de todos.

| Suma al sigilo | Suma a la alerta |
|---|---|
| Noche +2 · niebla +2 · lluvia +1 | Un **vigía** en el grupo +3 (mientras vigila, no recolecta) |
| Capa de camuflaje (Sastrería) +2 | Perro o bestia de guardia (Ganadería) +2 |
| Habilidad de sigilo (Pícaro, Druida Feral) +3 | Seguir su rastro: lo encontraste tú (ver [Cacerías](../06-contenido/cacerias.md)) +3 |
| Cebo: la presa vino a tu nodo +2 | Conocer la especie (Bestiario) +1 |
| Placas o carga pesada −3 · farol encendido −3 | Fogata o farol encendido −2 (deslumbra) |

| Diferencia | Resultado | Efecto |
|---|---|---|
| +5 o más | **Emboscada total** | Quien embosca tiene una **ronda gratis**: el otro no actúa ni usa respuestas. Las filas del sorprendido quedan **invertidas** esa ronda (la retaguardia, adelante). Si el nodo tiene altura, es de quien embosca |
| +1 a +4 | **Ventaja** | En la primera ronda, quien embosca actúa entero antes en la cola, y el otro no puede usar respuestas |
| 0 | **Encuentro** | Combate normal |
| Negativa | **Al revés** | Si gana el que esperaba, la emboscada es suya, con la misma escala |

Después de la primera ronda, la iniciativa vuelve a ser la de siempre.

**Antes de tirar, el grupo decide** cómo acercarse. Una opción clave: que el más ruidoso **espere atrás**. El tanque de placas no cuenta para el sigilo, pero entra recién en la ronda 2.

**Límites.**
- Hasta el nivel 10, contra ti nunca sale peor que **Ventaja** (protección de novato).
- En PvP solo hay emboscadas donde ya hay PvP: zonas rojas y negras, amarillas con bandera, invasiones (ver [PvP](../06-contenido/pvp.md)). Nunca en zonas azules.
- Los Guardianes no se emboscan: su guarida empieza siempre en Encuentro. Los jefes de campo y las bestias legendarias sí.
- En la **resolución rápida**, la emboscada se tira igual y se aplica sola.

**Botón.** Fuera del combate, en el mensaje de exploración.

**Cómo se ve.**

```
👣 Piso 34 · Pantano Putrefacto · 🌫 Niebla · 🌙 Noche
Ves 3 Saqueadores de Turba junto a una fogata. No te vieron.
Tu sigilo: 11 (niebla +2, noche +2, Bram en placas −3)
Su alerta:  11 (un vigía +3, fogata −2)

[🐍 Acercarse en sigilo]  [⚔️ Atacar de frente]
[🐢 Que Bram espere atrás] [↩️ Retirarse]
```

```
🐢 Bram espera atrás. Tu sigilo sube a 14.
🎲 Tú: 4 → 18 · 🎲 Ellos: 2 → 13
⚡ ¡EMBOSCADA TOTAL! (+5) Ronda gratis · sus filas, invertidas
```

**Cómo se equilibra.**
- Premia la preparación, no la clase: cualquiera puede llevar capa, vigía o perro, o seguir un rastro. El +3 de las specs de sigilo cuenta en su eje de **Autonomía**.
- El simulador mide cuántos encuentros abren con ventaja: entre **15 % y 25 %** para un grupo que se prepara y menos del 10 % para uno que no. Ninguna composición pasa del 30 %.
- La ronda gratis tiene los mismos topes que cualquier ronda (en PvP, 40 % de la vida por acción).

---

## 9. Moral enemiga

**De dónde sale.** *Battle Brothers*: la moral de cada enemigo pasa de firme a vacilante y a la huida. *Persona 5*: con todos los enemigos en el suelo, se los rodea y se negocia dinero, un objeto o que se unan. *Undertale*: perdonar en lugar de matar. *Monster Hunter*: el monstruo herido cojea y huye a su nido.

**Cómo funciona.**
- Los enemigos con mente tienen **Moral**, con cuatro estados: 💪 Firme · 😰 Vacilante (−10 % de precisión) · 🏳️ Quebrado (intenta huir o rendirse al final de la ronda) · 😡 Enfurecido.

| Baja la moral | Sube la moral o enfurece |
|---|---|
| Cae un aliado suyo | Derriban a un jugador |
| Cae su líder (baja mucho) | Su líder da un grito (se avisa) |
| Ruptura propia, Asalto Total | Una bestia que protege a sus crías: **Enfurecido** |
| Quedar en inferioridad de 2 a 1 | Fanáticos cuando cae su sacerdote: **Enfurecido** |
| Recibir una técnica combinada o un Límite | — |

- **😡 Enfurecido:** +25 % de daño, −25 % de defensa; no huye ni se rinde. El aviso lo anuncia: "*el lobo alfa aúlla sobre el cuerpo de su compañero…*".
- **Huir** tiene las mismas reglas que para los jugadores (ver [Ronda y acciones](ronda-y-acciones.md)): no puede con una pierna rota ni si lo bloquea alguien más rápido. Quien huye se lleva su botín; en una cacería, deja un rastro para seguirlo.
- **Rendirse:** un humanoide quebrado que no puede huir **pide cuartel**. Las bestias no se rinden: huyen o quedan **acorraladas**, y entonces se pueden capturar.

| Enemigo | Moral | Qué suele hacer |
|---|---|---|
| Bestias | Media | Huyen heridas; se enfurecen si protegen crías |
| Humanoides (bandidos, soldados, saqueadores) | Media-baja | Se rinden |
| Fanáticos y cultistas | Alta | Se enfurecen |
| No-muertos, constructos, invocaciones | Sin moral | Pelean hasta el final |
| Jefes de campo y bestias legendarias | Especial | Huyen a su guarida al 25 % de vida (ver [Cacerías](../06-contenido/cacerias.md)) |
| Guardianes y Muros | Sin moral | Nunca huyen: tienen fases |

### La decisión

Cuando alguien se rinde, la pelea se pausa (los enemigos no actúan) y la botonera se reemplaza por tres botones de voto durante el temporizador normal de la ronda (45 s en grupo; sin límite en solitario):

| Opción | Requisito | Qué da | Qué cuesta |
|---|---|---|---|
| ⛓ **Capturar** | Grilletes (Herrería) para humanoides; red o jaula para bestias | Humanoide: entregarlo a la Guardia (cobras su recompensa, si tiene), interrogarlo (una pista para una [investigación](../06-contenido/investigaciones.md)) o pedir rescate. Bestia: doma o venta a un criador | Gasta los grilletes o la red. El prisionero pesa en la mochila hasta el asentamiento, y se escapa si caes |
| 🕊 **Perdonar** | — | Reputación con el asentamiento o la facción del piso. A veces deja la bolsa (la mitad del botín) o un rumor (un campamento, un yacimiento) | Pierdes su Esencia y la otra mitad del botín. Puede volver: agradecido o con rencor |
| 🗡 **Rematar** | — | Botín y Esencia completos | Humanoide: **Infamia** solo para quien remata (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)), y los demás enemigos de ese grupo dejan de rendirse. No da Infamia si tenía orden de busca "vivo o muerto". Bestia: nada |

- Cada jugador vota; nadie gana por pulsar primero. Al cerrar el tiempo gana la opción más votada. Si hay empate o nadie vota, se **perdona** (la opción que no cuesta nada). Si gana Rematar, la Infamia es solo para quienes la votaron; si gana Capturar, se gastan los grilletes de uno de quienes la votaron.
- Tras un Asalto Total contra humanoides (§4), la misma ventana ofrece **Intimidar**: se rinden todos a la vez.

**Botón.** Ninguno en la botonera normal. La votación la reemplaza solo mientras dura el temporizador de esa ronda.

**Cómo se ve.**

```
🏳️ El Bandido Tuerto tira el hacha y pide cuartel.
   Tiene precio: 120 🪙 (Guardia del Piso 34)

[⛓ Capturar (grilletes: 2)]  [🕊 Perdonar]
[🗡 Rematar · ⚠️ Infamia]
⏱ 45 s · Gana la más votada · Empate o nadie: Perdonar
```

**Cómo se equilibra.**
- La moral acorta las peleas comunes, pero quien huye o es perdonado da **menos**: si huye, sin botín y con media Esencia; si se perdona, la mitad. El simulador mide **botín y Esencia por ronda**: con moral nunca sale más que sin ella.
- No toca a los jefes que importan: Guardianes y Muros no tienen moral, y su balance no cambia.
- No pertenece a ninguna spec. Toca la **Autonomía** (peleas en solitario un poco más cortas) y se mide como rondas por pelea común: objetivo, entre 10 % y 20 % menos.
- La Infamia nunca llega por accidente: solo por rematar a quien se rindió.

---

## 10. Límite

**De dónde sale.** *Final Fantasy VII*: la barra de Límite se llena al recibir daño y, cuando está llena, el comando de Atacar se convierte en el Límite. *Final Fantasy X*: el *Overdrive*, con modos que deciden qué acciones cargan la barra.

**Cómo funciona.**
- Cada jugador tiene una barra **🌟 Límite** de 0 a 100. Empieza vacía en cada pelea y se vacía al terminar.
- Siempre se carga con dos cosas:
  - **recibir daño:** +1 por cada 2 % de tu vida máxima que pierdes;
  - **proteger aliados:** +8 cada vez que bloqueas, desvías o recibes un golpe dirigido a otro, provocas a un enemigo que iba por un aliado, pones un escudo que absorbe un golpe o levantas a un derribado.
- Además, cada jugador elige un **modo** (se cambia fuera de combate):

| Modo | Qué suma |
|---|---|
| Estoico | El daño recibido cuenta doble |
| Protector | Proteger aliados cuenta doble |
| Lector | +12 por cada reacción perfecta o interrupción acertada (§11) |

- Llena, el botón **⚔️ Atacar** pasa a ser **🌟 el Límite de tu spec**. Se usa **una vez por pelea**, como acción.
- Cada una de las 46 specs tiene el suyo. Algunos ejemplos:

| Clase · spec | Límite | Efecto |
|---|---|---|
| Guerrero · Armas | **Golpe del Titán** | Golpe 💥 que abre la ventana de *Golpe Colosal* 3 rondas y le quita al enemigo la mitad de la Postura que le queda |
| Guerrero · Protección | **Última Muralla** | 2 rondas: recibe todos los golpes dirigidos a la vanguardia, con la mitad de daño |
| Paladín · Sagrado | **Amanecer** | Levanta a todos los derribados con 30 % de vida y cura al grupo |
| Cazador · Puntería | **Disparo Imposible** | Rompe al instante la parte apuntada (en un Muro, la deja a un golpe) |
| Pícaro · Asesinato | **Veneno Maestro** | Todas las barras de acumulación del objetivo suben al 90 % |
| Sacerdote · Disciplina | **Égida** | Escudo al grupo que absorbe entero el siguiente golpe avisado, con tope |
| Caballero de la Muerte · Sangre | **Festín Carmesí** | *Golpe de Muerte* que cura el daño recibido en las últimas 4 rondas, no en 2 |
| Chamán · Elemental | **Ojo de la Tormenta** | Llena la Vorágine y deja 3 rondas de rayos en la fila enemiga; a los mojados los aturde |
| Mago · Escarcha | **Invierno Eterno** | Congelación llena en toda la fila enemiga; en jefes, +50 % a la barra |
| Brujo · Destrucción | **Lluvia de Caos** | 3 *Descargas del Caos* de crítico garantizado, repartidas |
| Monje · Maestro Cervecero | **Purga Total** | Purga todo el *Tambaleo* y lo devuelve como daño al enemigo |
| Druida · Restauración | **Florecer** | Todas sus curas en el tiempo se aplican de golpe al grupo |
| Cazador de Demonios · Venganza | **Sello Infernal** | Sigilo en las dos filas enemigas que se activa esta misma ronda, sin retraso, y silencia |
| Evocador · Preservación | **Rebobinado Total** | La vida de todo el grupo vuelve a la de hace 2 rondas (solo si era más alta) |
| Nigromante · Legión | **Marea de Huesos** | Llena la vanguardia de esqueletos durante 3 rondas; cada uno bloquea un golpe |
| Bardo · Estratega | **Gran Final** | Ordena a su gusto la cola de iniciativa de la ronda siguiente (menos los golpes Inevitables) |

**Botón.** **Atacar** se transforma. No suma botones.

**Cómo se ve.**

```
🟥 Bram — Guerrero Protección · Vanguardia
🌟 Límite ▓▓▓▓▓▓▓▓▓▓ ¡LISTO!

[🌟 Última Muralla]  [🛡 Bloqueo con escudo]
```

**Cómo se equilibra.**
- Todos los Límites valen lo mismo: unas **3 acciones buenas de su spec**, ±10 %. Cada uno se mide y va al registro de balance.
- Los modos hacen que todas las specs llenen la barra al mismo ritmo: en un jefe estándar, entre la **ronda 8 y la 12**, con ±1 ronda entre specs. Un daño a distancia que casi no recibe golpes usa el modo Lector y carga leyendo avisos.
- En peleas cortas casi no se llega: el Límite es un momento de jefe, no de cada pelea.
- Respeta los números chicos: ningún Límite muestra más de 4 dígitos.
- En PvP carga a la **mitad** de ritmo y respeta el tope del 40 %.
- Eje del presupuesto: **Ráfaga** para el daño; **Supervivencia** o **Utilidad de grupo** para tanques, sanadores y apoyos.

---

## 11. Reacciones avanzadas

**De dónde sale.** *Sekiro* (2019): desviar en el momento justo le rompe la postura al enemigo; los ataques peligrosos se anuncian con un símbolo, y cada tipo tiene su respuesta (la estocada se contrarresta con el *Mikiri*, el barrido se salta). *Clair Obscur: Expedition 33* (2025): combate por turnos en el que esquivar y desviar los golpes enemigos es parte del juego, y desviar todos los golpes de un ataque devuelve un contraataque. Aquí se queda la idea y se quita el reflejo: **se acierta leyendo, no apretando a tiempo.**

**Cómo funciona.**
- Cada ataque enemigo tiene una **forma**, que se adivina en el texto del aviso. Cuando el Bestiario ya registró el movimiento (3 veces visto), el aviso la dice con su icono.
- Una reacción es **perfecta** si es la respuesta correcta para esa forma **y** se eligió en la ronda en que cae el golpe. Con los golpes retrasados (ver [Avisos](avisos-y-tacticas.md)), reaccionar una ronda antes gasta el Aguante y no cuenta.

| Forma | Pista típica en el aviso | Reacción perfecta | Otras reacciones |
|---|---|---|---|
| 🗡 **Estocada** | "*echa el brazo atrás y apunta a X*" | Desviar | Esquivar: medio daño |
| 🌊 **Barrido** | "*la cola se enrosca hacia la retaguardia*" | Esquivar, o Bloquear (el tanque cubre su fila) | Desviar: medio daño |
| 🔨 **Aplastamiento** | "*levanta las dos manos sobre la vanguardia*" | Esquivar | Bloquear: te rompe la guardia (pierdes todo el Aguante) |
| ✨ **Conjuro o aliento** | "*inhala*", "*las runas se encienden*" | Interrumpir si canaliza; Bloquear con escudo o barrera si no | Esquivar: medio daño |
| 🔗 **Combo** | "*tres golpes en tres rondas*" | La que pida cada golpe | — |

| Reacción perfecta | Premio |
|---|---|
| ⚔️ **Desvío perfecto** | **Contraataque** gratis: golpe ligero (50 %) con mucho daño a la Postura; quita 1 🔰 si tu arma es su debilidad. Recuperas 1 🔋 |
| 💨 **Esquiva perfecta** | Te recolocas: cambias de fila gratis, y tu acción de la ronda siguiente va primera en la cola |
| 🛡 **Bloqueo perfecto** | Nadie de tu fila recibe daño, y el enemigo pierde Postura |
| ✋ **Interrupción perfecta** | El enemigo queda silenciado 1 ronda y pierde 1 🔰 |
| 🔗 **Cadena perfecta** | Acertar todos los golpes de un combo da un **contraataque doble** al final y +20 de Límite |

- Desviar cuesta **2 🔋**; las otras reacciones, 1. Es la apuesta alta: si fallas la forma, recibes el golpe entero.
- Máximo **1 contraataque por jugador por ronda**.

**Botón.** Ninguno nuevo. La reacción es una de tus **respuestas** (o una habilidad con ✋), elegida como tu jugada de la ronda: va primero y esa ronda no atacas (ver [Ronda y acciones](ronda-y-acciones.md) §3). Lo nuevo es que acertar la forma y la ronda tiene premio.

**Cómo se ve.**

```
⚠️ El Caballero Hueco echa la lanza atrás y apunta a TI.
   (Bestiario: 🗡 estocada)
🟨 Tú — Pícaro Sutileza · Vanguardia   🔋 ●●●○○

[⚔️ Atacar]          [🤺 Réplica · 2🔋]
[💨 Evasión]         [✋ Patada]
[🏃 Huir]            [🎒 Mochila]
```

```
⚔️ ¡DESVÍO PERFECTO! Apartas la lanza del Caballero Hueco
   Contraataque 140 · 🟫 −220 · 🔋 +1
```

**Cómo se equilibra.**
- Toda clase tiene al menos una respuesta y toda spec una interrupción en su repertorio (ver [Ronda y acciones](ronda-y-acciones.md) §3 y [Daño y estados](dano-y-estados.md) §4). Quien no lleva la respuesta justa para una forma tiene 🌀 Esquivar o la poción de resistencia, que reducen el daño pero nunca son perfectas. Los tanques suman su bloqueo de firma.
- El simulador supone **30 % de reacciones perfectas** en juego básico (con Tácticas) y **70 %** en juego óptimo. Esa diferencia entra en el margen del techo parejo (±3 % en juego óptimo).
- El contraataque pega poco: vale por la Postura, el escudo y el Aguante que devuelve.
- En PvP, las habilidades cargadas, apuntadas o potenciadas de los jugadores también muestran su forma al rival: se vuelve un juego de leer al otro. El contraataque respeta el tope del 40 %.
- Eje del presupuesto: **Supervivencia**.

---

## 12. Guardar y soltar: Guardia y Desatar

**De dónde sale.** *Bravely Default* (2012): *Default* defiende y guarda un punto; *Brave* los gasta para actuar hasta cuatro veces en un turno, incluso endeudándose. Aquí no puede haber varias acciones por ronda (D-46), así que se usa la forma del *Boost* de *Octopath Traveler*: los puntos guardados no dan más turnos, sino que hacen más fuerte una sola acción (más golpes o más potencia), y se sueltan cuando el enemigo está roto.

**Cómo funciona.**
- **🛡 Guardia.** Cada ronda en que tu jugada es una **respuesta** (bloquear, esquivar, desviar, reposicionar, proteger) o 🌀 Esquivar, ganas **1 ⏳ Carga**. Máximo 3. No hay botón de Defender: guardar cuesta lo mismo que defenderse, una ronda sin atacar y el Aguante.
- **⏩ Desatar.** No es un botón. Cuando tu objetivo está 💫 Roto (§3) o con la 🟫 Postura rota, tu siguiente ⚔️ Atacar o habilidad de daño contra él gasta todas tus cargas. Cada carga suma **un impacto más** a los ataques con arma y a las habilidades de varios impactos, o **+25 % de potencia** a las demás.
- Si prefieres guardarlas para otro momento, se cambia en tus [Tácticas](avisos-y-tacticas.md), fuera de la pelea.
- Reglas:
  - los impactos de más no quitan más de 2 🔰 por acción (§3);
  - el Límite no se desata;
  - las cargas se pierden al terminar la pelea.

**Botón.** Ninguno. Guardas al usar tus respuestas y sueltas con tu ataque de siempre.

**Cómo se ve.**

```
🟦 Ossian — Cazador Puntería · Retaguardia
⏳ Cargas ●●○   El Wyrm está 💫 ROTO

⏩ Ossian desata 2 cargas:
   🏹 Disparo Apuntado → VIENTRE 380 (+50 %)
⏳ Cargas 0
```

**Cómo se equilibra.**
- Guardar no crea daño: lo **mueve** a la ventana buena (una ruptura, una postura rota, el *Golpe Colosal*). Cada carga cuesta una ronda sin atacar y Aguante. El simulador compara el daño en 20 rondas con y sin guardar: **+5 % como máximo**.
- La ráfaga en 3 rondas sigue dentro de ±5 % entre specs, aunque desaten.
- No existe en PvP: los jugadores no tienen escudo ni Postura.
- Eje del presupuesto: **Ráfaga**.

---

## 13. Cómo se encadenan

Las mecánicas se piensan juntas. Una pelea común bien jugada puede pasar por casi todas:

```
EMBOSCADA ──> SUPERFICIE ──> RUPTURA ──> GOLPE EXTRA ──> ASALTO TOTAL ──> RENDICIÓN
(ronda        (aceite y      (cancela    (relevo al      (todos rotos)    (capturar,
 gratis)       fuego)         el aviso)   que rompe)                       perdonar)
```

Un grupo de noche en el Pantano Putrefacto embosca a tres saqueadores. Lanza aceite a su vanguardia y lo prende con la *Chispa* de una varita. Rompe al líder con escarcha antes de que dé la orden; el golpe extra pasa solo al Cazador, que rompe al segundo, y con todos rotos los intimida. El líder tiene precio en el piso: grilletes y recompensa. Nadie apretó nada rápido.

---

## 14. Qué oficio vive de cada mecánica

| Oficio | Qué vende para estas mecánicas |
|---|---|
| **Alquimia** | Aceites de arma (cambian el tipo de daño: Ruptura), frascos de aceite, agua y veneno (superficies), repelente (pantano) |
| **Ingeniería** | Bombas de humo y de escarcha |
| **Herrería** | Grilletes (capturar), botas con clavos (hielo), faroles (oscuridad), botas de obsidiana (suelo volcánico) |
| **Sastrería** | Capa de camuflaje (sigilo), capa encerada (nunca quedas Mojado), velo de desierto (tormenta de arena) |
| **Carpintería** | Antorchas (oscuridad), cuerdas enceradas (arcos bajo la lluvia), jaulas (captura); raquetas de nieve, junto con Peletería |
| **Encantamiento** | Runas de elemento de un uso: el arma pega otro elemento durante una pelea |
| **Inscripción** | Pergaminos de técnica (Libro de Técnicas); fichas de debilidades y formas de ataque, que vende el Informante |
| **Ganadería** | Perros y bestias de guardia (alerta; ver [Defensa](../09-construccion/defensa-y-protecciones.md)) |
| **Medicina y Primeros Auxilios** | Las heridas que dejan los resbalones, los estallidos y las llamas |

El resto del equipo contra el entorno (abrigos, máscaras, filtros, repelente) está en [Peligros del entorno](../05-salud/peligros-del-entorno.md).

- Todo lo que pasa en estas mecánicas llega a Salud como evento: caer en el hielo es un derribo (contusión), un estallido deja quemaduras y una nube tóxica suma veneno (ver [Heridas](../05-salud/heridas.md)).
- Nada de esto se compra con dinero real. Los Límites y las técnicas pueden tener apariencias (texto, emoji, marco del mensaje) que se ganan jugando (ver [Monetización](../07-economia/monetizacion.md)).
- Cada mecánica llena su fila en la tabla de la [Red de sistemas](../00-vision/red-de-sistemas.md): consume consumibles y equipo fabricados, y produce heridas, prisioneros, reputación e Infamia.

---

## 15. Dónde aplica cada mecánica y cómo se mide

| Mecánica | PvE | PvP | Jefes | Eje | Qué mide el simulador | Objetivo |
|---|---|---|---|---|---|---|
| **Ruptura** | Sí | No (los jugadores no tienen escudo) | Sí: escudo por fase, Recompuesto, golpes Inevitables | Control | Rondas hasta la primera ruptura, por spec | ±10 % entre specs; 1-2 rupturas por fase de jefe |
| **Golpe extra** | Sí | No | Sí, 1 por jugador y ronda | Daño sostenido | Daño aportado por golpes extra | ≤ 8 % del total de la spec; ±2 puntos entre specs |
| **Técnicas combinadas** | Sí (con PNJ y Ecos en solitario) | Sí en 2v2, 3v3 y campos, con el tope del 40 % | Sí, 1 por cada 5 jugadores y ronda | Utilidad de grupo | Técnicas accesibles por spec y aporte al grupo | ±1 técnica entre specs; ≤ 10 % del grupo; ninguna composición +5 % |
| **Superficies** | Sí | Sí | Sí: los jefes también las crean (avisadas) | Control y Daño sostenido | Daño de entorno; valor con y sin lanzables | ≤ 15 % del total; estallido ≤ 20 % de la vida de un jugador |
| **Terreno** | Sí | Sí en mundo abierto y campos; la arena clasificada es neutra | Sí: guarida con terreno fijo | — (dispersión) | Rendimiento por spec en la rueda de terrenos | ±5 % de media; nunca −10 % con su contra |
| **Emboscada** | Sí | Sí, solo en zonas rojas, negras, amarillas con bandera e invasiones | No contra Guardianes; sí jefes de campo y bestias legendarias | Autonomía | Encuentros que abren con ventaja | 15-25 % preparado, < 10 % sin preparar, ninguna composición > 30 % |
| **Moral** | Sí | No (los jugadores no tienen moral) | No (Guardianes y Muros); los jefes de campo huyen | Autonomía | Rondas por pelea común; botín y Esencia por ronda | −10 % a −20 % de rondas; botín por ronda ≤ sin moral |
| **Límite** | Sí | Sí, a mitad de ritmo, con el tope del 40 % | Sí: es su momento | Ráfaga, Supervivencia o Utilidad | Ronda media de llenado; valor del Límite | Ronda 8-12, ±1 entre specs; valor = 3 acciones ±10 % |
| **Reacciones avanzadas** | Sí | Sí: se lee la forma de las habilidades del rival | Sí: son la base de la lectura | Supervivencia | Rendimiento con 30 % y 70 % de reacciones perfectas | Dentro del techo parejo (±3 % en óptimo) |
| **Guardar y soltar** | Sí | No (los jugadores no tienen escudo ni Postura) | Sí: para las ventanas de ruptura | Ráfaga | Daño en 20 rondas con y sin guardar | ≤ +5 %; ráfaga ±5 % entre specs |

Las Tácticas pueden usar todas las mecánicas con reglas propias ("si el jefe no está roto, guardar las cargas"; "si el aviso es una estocada contra mí → 🤺 Réplica"). El **juego básico** del simulador corre con las Tácticas por defecto; el **juego óptimo**, con el mejor plan. Todo cambio va al registro de balance (ver [Balance](../03-personaje/balance.md)).

---

## 16. Cómo se ve en Telegram: una técnica combinada y una ruptura

Guardián del Piso 45, el Wyrm de las Dunas (ver [Jefes](../06-contenido/jefes.md)). Es débil a escarcha y a perforación en el vientre, y resiste fuego y corte. En la ronda anterior, Mirra le lanzó un frasco de agua a su vanguardia. Ahora el Wyrm prepara su *Aliento de Vidrio*, un golpe retrasado.

```
⚔️ Ronda 9 · Guardián del Piso 45 — Wyrm de las Dunas
📍 Desierto Ardiente · 🌙 Noche · 💨 Viento del sur
Fase 1/3  ❤️ 72% ▓▓▓▓▓▓▓░░░   🟫 Postura ▓▓▓▓▓░░░░░
🔰🔰🔰 3   Débil: ❄️ 🏹(vientre) ❓   Resiste: 🔥 🪓
Filas del Wyrm: Vanguardia 💧 Agua (2)

⚠️ El Wyrm inhala… y retiene el aire.
   (Bestiario: ✨ aliento retrasado. Cae la PRÓXIMA ronda)

🟥 Tú — Guerrero Armas · Vanguardia
❤️ 1.140/1.480   💢 Ira 70   🔋 ●●●○○
🌟 Límite 64%   ⏳ Cargas 1

Elegido: Lyra ❄️→Wyrm · Ossian 💨 respuesta
         Bram 🛡 respuesta · Mirra ✚→vanguardia
🔗 Posible: Témpano Quebrado (Lyra ❄️ + tu 💥)

Turnos: Lyra → Tú → WYRM → Ossian → Bram → Mirra
⏱ 45 s

[⚔️ Atacar]             [💥 Golpe Colosal 🔗]
[🩸 Golpe Mortal]        [🤺 Parada]
[🌀 Esquivar]           [🎒 Mochila]
```

Es un Guardián: no se huye, así que el quinto botón es 🌀 Esquivar. Ossian y Bram usan una respuesta aunque el aliento cae la próxima ronda: pierden Aguante, pero guardan una carga para cuando el Wyrm esté roto (§12). Elegiste *Golpe Colosal* contra el Wyrm. Al resolverse, el mismo mensaje se edita con el resumen:

```
Ronda 9 — resumen
❄️ Lyra: Lanza de Escarcha → DEBILIDAD · 🔰 3→2
   💧 El Wyrm estaba Mojado: ❄️ Congelación ▓▓▓▓▓▓▓░░░
🔗 TÉMPANO QUEBRADO (Lyra ❄️ + Tú 💥)
   Tu Golpe Colosal parte la escarcha: 540 · 🔰 2→0 · 🟫 −260
💫 ¡RUPTURA! El Wyrm queda ROTO hasta el final de la ronda 10
   ✖ Aliento de Vidrio: cancelado
   Recibe +30 % de daño · no puede reaccionar
⏳ Ossian y Bram usan su respuesta: +1 carga (Ossian 2 · Bram 1)
✚ Mirra: escudo preventivo a la vanguardia (180 c/u)
✦ Golpe extra de Lyra → 🤝 Relevo a Ossian (su arco pega el VIENTRE)
   🏹 Golpe rápido al VIENTRE: 118
🌟 Límite: Tú 71% · Bram 88%
▸ Registro completo (tocar para abrir)
```

Y la cabecera de la ronda siguiente ya cuenta la oportunidad:

```
⚔️ Ronda 10 · Wyrm de las Dunas — 💫 ROTO (hasta el final de esta ronda)
+30 % de daño · no reacciona   🟫 Postura ▓▓░░░░░░░░ (¡cerca del Quiebre!)
⏳ Ossian 2 · Bram 1: se ⏩ desatan en su próximo golpe al Wyrm roto
🌟 Bram: Límite 88 %
```

La última línea del resumen es una cita plegable con cada número, como en [Ronda y acciones](ronda-y-acciones.md). El *Golpe Colosal* sigue siendo de corte, que el Wyrm resiste. La técnica combinada es lo que le permite a un Guerrero Armas romper a un enemigo que le resiste: eso es lo que hace interesante elegir con quién atacar.

---

## 17. Preguntas abiertas

Para sumar a [Preguntas abiertas](../00-vision/preguntas-abiertas.md) con su número:
- ¿El mensaje vivo muestra la etiqueta y el objetivo de lo que eligió cada aliado antes de resolver? Propuesta: sí, sin decir la habilidad exacta.
- ¿Quién decide una rendición en grupo: el primero que pulsa o una votación? Propuesta: votación al cerrar el temporizador, para que no gane el más rápido (regla 2, §1); la Infamia, solo para quienes votaron Rematar.
- ¿Los jugadores pueden rendirse en zona roja (entregar la mochila a cambio de no caer)? Propuesta: dejarlo para después del lanzamiento.
- ¿La barra de Límite se conserva entre las peleas de una misma mazmorra? Propuesta: no; el Límite es un momento de jefe.
- ¿Las cargas se desatan solas contra un enemigo roto o el jugador elige cuándo? Propuesta: solas, con la opción de guardarlas en las Tácticas, para no sumar botones (D-46).
