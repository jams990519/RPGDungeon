# Ronda y acciones

> **Módulo** [04 · Combate](README.md) · **Depende de:** [Clases](../03-personaje/clases-y-especializaciones.md), [Equipamiento](../03-personaje/equipamiento.md), [Inventario y mochilas](../03-personaje/inventario-y-mochilas.md), [Balance](../03-personaje/balance.md) · **Alimenta a:** [Salud](../05-salud/README.md) (por eventos), [Jefes](../06-contenido/jefes.md), [PvP](../06-contenido/pvp.md) · **Estado:** propuesta, con D-46 (6 botones) y D-50 (roles) aplicadas

**De dónde sale.**
- *World of Warcraft*: los roles (tanque, sanador, daño y apoyo), la amenaza, las interrupciones y los avisos de "agruparse" y "separarse".
- *Pokémon*: el menú de combate más probado que existe. Cuatro movimientos, la mochila y huir; una elección por turno, y los movimientos defensivos (como *Protección*) se resuelven antes que todo.
- *Elden Ring* y *Dark Souls*: el aguante que se gasta al esquivar y bloquear, y la postura que se rompe y abre un golpe crítico.
- *Final Fantasy X*: la cola de turnos siempre visible, y que se puede manipular.
- *Darkest Dungeon*: las filas deciden qué puedes hacer.
- **TowerWars**: rondas simultáneas de 90 s que ya funcionan en Telegram.

**Por qué este diseño.** En Telegram no hay reflejos: hay lectura y decisión. El combate premia **leer bien el aviso y planificar**, que es lo que vuelve difícil a un jefe de Elden Ring cuando se le quita la velocidad. Además tiene que ser **ligero** (D-44): seis botones que caben en la pantalla de un teléfono y **una sola elección por ronda** (D-46). La profundidad está en lo que llevas a la pelea (tus 3 habilidades y tu cinturón) y en cuándo usas cada cosa, no en cuántos botones aprietas.

---

## 1. La ronda

Todo combate se divide en **rondas**. En cada una:

1. **El bot muestra el estado** en un mensaje vivo: vidas, recursos, la cola de iniciativa y **el aviso** de lo que prepara el enemigo.
2. **Todos eligen a la vez**, con temporizador: 45 s en mazmorra, 60-90 s en banda, ninguno en solitario. Cada jugador toca **un solo botón**.
3. **Se resuelve** en el orden de §6 y el mensaje se edita con el resumen.

Elegir a la vez evita esperar uno por uno a otros cuatro jugadores, que en Telegram mata cualquier grupo.

**Una sola elección.** No hay acción rápida ni reacción preparada aparte: lo que eliges es lo que haces. Si te defiendes, esa ronda no atacas; si bebes una poción, tampoco. Esa renuncia es la decisión. Los efectos que antes daban una acción rápida extra (el Clamor, el *Enfurecido* del Guerrero Furia) pasan a dar iniciativa o potencia.

**Elegir objetivo no cuenta.** Si hay un solo objetivo posible, el botón actúa directo. Si hay varios, aparece un segundo teclado con los objetivos, y el que eligió el tanque del grupo sale primero, marcado con 🎯.

## 2. La barra de 6 botones

```
[⚔️ Atacar]       [✨ Habilidad 1]
[✨ Habilidad 2]  [✨ Habilidad 3]
[🏃 Huir]         [🎒 Mochila]
```

| Botón | Qué hace |
|---|---|
| ⚔️ **Atacar** | El golpe básico de tu spec con tu arma. No cuesta recurso: lo **genera** (ira, combos, foco, chi; maná en los lanzadores). Es la primera de tus cuatro "habilidades". En los specs de Curación, sobre un aliado es su **cura básica**. Contra enemigos con partes, deja apuntar (ver [Daño y estados](dano-y-estados.md)). Con la barra de Límite llena se convierte en el Límite (ver [Mecánicas avanzadas](mecanicas-avanzadas.md)) |
| ✨ **Habilidad 1, 2 y 3** | Las tres que elegiste de tu spec antes de pelear. Una de las casillas puede llevar la **técnica de tu arma o de tu armadura** (P-68; ver [Equipamiento](../03-personaje/equipamiento.md)) |
| 🏃 **Huir** | Intentas salir de la pelea (§10). Donde no se puede huir (Guardianes, arena), el botón es **🌀 Esquivar** (P-67) |
| 🎒 **Mochila** | Abre tu **cinturón**: los pocos objetos que preparaste para pelear (§4). Usar uno gasta la ronda |

El botón siempre dice "Atacar"; el resumen dice qué hiciste ("Golpe siniestro", "Disparo firme"). Así la barra se lee igual en las 46 specs.

**Cómo se eligen las 3 habilidades.** Fuera de combate, en tus configuraciones de talentos (hasta 5 guardadas por spec: "banda", "mazmorra", "solitario"…; ver [Talentos](../03-personaje/talentos.md)). Lo demás que aprendiste no se usa en esa pelea. Elegir según el enemigo es parte de prepararse: contra la Bruja llevas una interrupción; contra el Coloso, un bloqueo.

**Al menos una respuesta.** Toda clase tiene entre sus habilidades elegibles al menos una **respuesta**: una defensiva o de reposicionamiento (§3). No es obligatorio llevarla, pero la configuración por defecto trae una, y si la quitas el juego avisa: *"⚠️ Sin respuesta: solo podrás contestar los avisos con la Mochila"*.

### Lo que antes era acción rápida o reacción

| Antes | Ahora |
|---|---|
| Botón **Defender** | No existe. Te defiendes con una respuesta (§3), con 🌀 Esquivar donde no se huye, o con una poción de resistencia |
| **Reacción preparada** (esquivar, bloquear, desviar) | Una respuesta elegida como tu jugada de la ronda. Se resuelve antes que los golpes |
| **Interrumpir** | Efecto ✋ de ciertas habilidades y bombas (ver [Daño y estados](dano-y-estados.md)) |
| **Beber una poción** | 🎒 Mochila. Gasta la ronda |
| **Cambiar de fila** | La fila inicial la da tu rol; se cambia con habilidades de reposicionamiento (§8) |
| **Agruparse / dispersarse** | Ya no se elige. Todos cuentan como agrupados; las respuestas 💨 te sacan del alcance (§8) |
| **Apuntar a una parte** | Opción dentro de ⚔️ Atacar, o efecto de ciertas habilidades |
| **Marcar un objetivo** | Automático: el objetivo del tanque sale marcado 🎯 para todos |
| **Mantener una canción, un aura o un tótem** | Se pone con una habilidad y sigue solo unas rondas |
| **Meditar** | ⚔️ Atacar genera el recurso; las pociones de maná van en el cinturón |
| **Levantar a un aliado** | Desde 🎒 Mochila (§10) |
| **Técnicas de equipo fijas** | Ocupan una de las 3 casillas, si quieres (P-68) |

## 3. Respuestas: defenderse sin botón de Defender

Una **respuesta** es una habilidad con etiqueta defensiva. Tiene tres reglas:

1. **Va primero.** Se resuelve al principio de la ronda, antes que cualquier golpe, sin importar la iniciativa. Por eso sirve para contestar un aviso.
2. **Cuesta Aguante:** 1 🔋, o 2 🔋 si es un desvío (la apuesta alta). Sin Aguante no hay respuesta.
3. **Dura la ronda** y cubre todos los golpes de esa ronda. Las defensivas mayores protegen más y tienen enfriamiento largo.

| Tipo | Qué hace | Contra qué sirve |
|---|---|---|
| 🛡 **Bloquear** | Frena el golpe. El bloqueo de un tanque en vanguardia cubre a **toda su fila** | Golpes a una fila, aplastamientos, alientos (con escudo o barrera) |
| 💨 **Esquivar** | El golpe no te toca y quedas fuera del alcance esa ronda. Eso es "dispersarse" | Barridos, saltos en cadena, explosiones en área, golpes marcados |
| 🤺 **Desviar** | Apartas el golpe; si aciertas su forma, contraatacas (ver las reacciones perfectas en [Mecánicas avanzadas](mecanicas-avanzadas.md)) | Estocadas y golpes marcados |
| 🔁 **Reposicionar** | Cambias de fila, o tu criatura se pone delante | Golpes a una fila; acercarte o alejarte |
| 🫧 **Proteger** | Escudo o bendición sobre ti o sobre un aliado | Golpes marcados a otro, daño en área total |

**El costo real es la ronda:** quien se defiende no ataca. Y el Aguante impide defenderse siempre: solo se recupera en las rondas en que no usas una respuesta (§5). Por eso un golpe retrasado o una finta castigan a quien se defiende antes de tiempo (ver [Avisos y tácticas](avisos-y-tacticas.md)).

### Una respuesta por clase, como mínimo

Ejemplos de respuestas que comparten todas las specs de cada clase. Los specs de Defensa suman además la suya de firma. Las técnicas de equipo defensivas (*Muro*, *Capa de Humo*, *Barrera Rúnica*; ver [Equipamiento](../03-personaje/equipamiento.md) §7) también son respuestas.

| Clase | Respuestas de ejemplo |
|---|---|
| Guerrero | 🤺 *Parada* · 🔁 *Intervenir* (salta delante de un aliado y recibe su golpe). Protección suma 🛡 *Bloqueo con escudo*, que cubre la fila |
| Paladín | 🛡 *Escudo Divino* · 🫧 *Bendición de Protección* (un aliado no recibe daño físico esa ronda) |
| Cazador | 💨 *Destrabarse* (salta a la retaguardia y esquiva) · 🤺 *Aspecto de la Tortuga* |
| Pícaro | 💨 *Evasión* · 🛡 *Capa de Sombras* (frena la magia) |
| Sacerdote | 🫧 *Palabra de Poder: Escudo* · 💨 *Desvanecerse* |
| Caballero de la Muerte | 🛡 *Caparazón Antimagia* (frena conjuros y alientos) · 🛡 *Entereza Ligada al Hielo* (mayor) |
| Chamán | 🛡 *Cambio Astral* · 🔁 *Paso Espiritual* |
| Mago | 💨 *Traslación* (cambia de fila y esquiva) · 🛡 *Bloque de Hielo* (mayor) |
| Brujo | 🛡 *Resolución Inagotable* · 🔁 *Círculo Demoníaco* (vuelve al punto que marcó) |
| Monje | 💨 *Rodar* · 🤺 *Toque de Karma* (devuelve parte del golpe) |
| Druida | 🛡 *Piel de Corteza* · 💨 *Carrerilla Salvaje* |
| Cazador de Demonios | 💨 *Desenfoque* · 🔁 *Retirada Vil* (salta a la retaguardia). Estrago suma *Salto Vil* (cambia de fila, golpea y esquiva) |
| Evocador | 🛡 *Escamas Obsidianas* · 💨 *Planear* |
| Nigromante | 🛡 *Hueso Protector* (un esqueleto recibe el golpe) · 💨 *Forma Espectral* |
| Bardo | 💨 *Paso de Baile* (esquiva y cambia de fila) · 🫧 *Nota Sostenida* (escudo sonoro al grupo) |

Los nombres y números finales viven en [Clases](../03-personaje/clases-y-especializaciones.md). El [Balance](../03-personaje/balance.md) exige a cada spec un defensivo mayor, uno menor (o autocuración) y una forma de reposicionarse o escapar: con eso, toda clase llega a cualquier aviso con algo que contestar.

## 4. El cinturón: la Mochila en combate

En combate, 🎒 **Mochila** no abre toda la mochila: abre solo el **cinturón**, unas pocas casillas que preparas antes de pelear. Lo demás no se toca hasta que termina la pelea. Cuántas casillas tienes y cuántos objetos caben en cada una depende del cinturón que lleves (ver [Inventario y mochilas](../03-personaje/inventario-y-mochilas.md)).

- **Usar un objeto gasta tu elección de la ronda** y se resuelve primero, igual que una respuesta.
- **La Toxicidad limita las pociones:** cada poción suma, y al 100 % no puedes beber más (ver [Condiciones](../05-salud/condiciones.md)). La comida y las vendas no suman.
- **Se rellena solo** desde la mochila al terminar cada pelea, si tienes con qué.

| Objeto | Para qué sirve en combate | Quién lo hace |
|---|---|---|
| 🧪 **Poción de vida** | Cura de golpe | Alquimia |
| 🔥 **Poción de resistencia** (fuego, escarcha, sombra, veneno…, y *Piel de Piedra* contra lo físico) | Menos daño de ese tipo durante 3 rondas. Es la respuesta a un aviso que tiene **cualquier clase**, y cubre un combo entero | Alquimia |
| 💧 **Poción de recurso** (maná y similares) | Devuelve parte del recurso | Alquimia |
| 💊 **Remedio** (antídoto, ungüento para quemaduras, tónico caliente, coagulante) | Vacía la barra de un estado y corta su daño por ronda (ver [Daño y estados](dano-y-estados.md)) | Alquimia, Primeros Auxilios |
| 🩹 **Venda** | Corta el sangrado; levanta a un aliado derribado con más vida | Sastrería, Primeros Auxilios |
| 💣 **Bomba** | Daño en área de un tipo, o una superficie (aceite, brea, humo). La bomba de destello interrumpe | Ingeniería, Alquimia |
| 🍖 **Comida rápida** | Cura un poco durante 3 rondas, sin Toxicidad | Cocina |

Preparar el cinturón es parte del conocimiento del jugador que pide D-49: el que sabe qué viene lleva la poción justa (ver [Balance](../03-personaje/balance.md)). Las casillas del cinturón se fabrican y se ganan; no se venden por dinero real (D-43).

## 5. Las barras

En pantalla se ven siempre tres: Vida, recurso y Aguante. Las demás aparecen solo cuando importan.

| Barra | Qué es | Cómo se mueve | Cuándo se ve |
|---|---|---|---|
| ❤️ **Vida** | Lo de siempre | Daño y curación | Siempre |
| 🔷 **Recurso de clase** | Ira, maná, runas… (ver [Clases](../03-personaje/clases-y-especializaciones.md)) | Atacar lo genera; las habilidades lo gastan | Siempre |
| 🔋 **Aguante** (0-5) | La barra de Souls, en fichas: lo que pagan las respuestas y 🌀 Esquivar | −1 por respuesta (−2 un desvío). +1 al final de cada ronda en que no usaste ninguna. La carga pesada baja el máximo en 1 | Siempre |
| ⚓ **Firmeza** | Resistencia al control | Cada aturdimiento, silencio o derribo que recibes la llena. Llena = **inmune al control durante 3 rondas**. Se vacía sola | Solo cuando estás inmune (⚓) |
| 🟫 **Postura** (solo enemigos grandes) | La postura de Elden Ring y Sekiro | Los golpes pesados, los bloqueos y los desvíos la bajan. Rota = el enemigo queda **aturdido 1 ronda** y la siguiente acción de cada jugador contra él es un **golpe crítico** | En el enemigo |

**Firmeza** responde al problema del control encadenado de WoW: nadie puede quedar aturdido más de dos veces seguidas, y funciona igual en PvE y en PvP. En los jefes, es lo que impide encadenarles aturdimientos sin fin.

## 6. Iniciativa y orden de la ronda

Cada ronda se resuelve en tres pasos:

1. **Respuestas y objetos** (las respuestas de §3, 🌀 Esquivar y 🎒 Mochila): antes que nada.
2. **Todo lo demás, por iniciativa**, enemigos incluidos: Atacar, las habilidades y los golpes avisados.
3. **Huir**: al final.

- Cada combatiente tiene **Iniciativa**, que sale de la Celeridad del equipo, del peso de la armadura y de las heridas en las piernas.
- La **cola de las próximas 8 acciones** está siempre a la vista, como en *Final Fantasy X*.
- El Bardo Estratega mueve la cola, ciertos golpes la retrasan y el Clamor la acelera.
- Si hay empate, gana quien eligió primero: así se premia no hacer esperar al grupo.

## 7. El rol: cómo te unes a la batalla (D-50)

La **clase** define tu sistema de combate: su recurso, su firma y sus respuestas. La **spec** define tu **rol**: qué haces en un grupo y cómo te las arreglas solo. Cada clase tiene specs de tres roles distintos (el Druida, de los cuatro), así que nadie queda atado a uno (ver [Clases](../03-personaje/clases-y-especializaciones.md)).

| Rol | En grupo | Fila al empezar | Modo en solitario | Tiempo en solitario |
|---|---|---|---|---|
| ⚔ **Ataque** | Daño: mata rápido, rompe partes y postura | Vanguardia si pega cuerpo a cuerpo; retaguardia si pega a distancia | No lo necesita: es su forma natural de jugar | Referencia (1×) |
| ✦ **Soporte** | Potencia a los aliados, debilita y controla a los enemigos | Según su arma | Sus potenciadores de grupo caen sobre él mismo; sus debilitadores siguen igual | Algo más lento (alrededor de 1,25×) |
| 🛡 **Defensa** | Atrae a los enemigos y bloquea por su fila | Vanguardia (o su criatura) | **Represalia:** parte de lo que bloquea o mitiga vuelve como daño al atacante | Más lento (alrededor de 1,5×) |
| ✚ **Curación** | Mantiene vivo al grupo y quita estados | Retaguardia | Parte de su curación pasa a daño, y se cura a sí mismo | El doble (2×), pero siempre posible |

- **En grupo:** una mazmorra de 5 pide 1 Defensa, 1 Curación y 3 de Ataque o Soporte. Las bandas son flexibles: los jefes se diseñan para composiciones libres (ver [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md)).
- **En solitario:** todos los roles pueden hacer todo el contenido en solitario. El **modo en solitario** se activa solo cuando peleas sin aliados y se apaga cuando entra alguien. Un tanque solo tarda más, y un sanador solo tarda el doble, pero los dos ganan.
- **Clases igualadas (D-49):** ningún rol rinde más que otro. El balance compara cada spec con las de su rol, y los tiempos de esta tabla son el objetivo del eje de Autonomía (ver [Balance](../03-personaje/balance.md)).
- **Defensa con criatura:** en los specs que defienden con una criatura (la mascota del Cazador de Bestias, el demonio guardián del Brujo de Demonología, los esqueletos del Nigromante de Legión), la criatura ocupa la vanguardia y su dueño se queda atrás.

## 8. Filas: te las da el rol

Dos filas por bando:

| Fila | Quién suele estar | Regla |
|---|---|---|
| **Vanguardia** | Defensa, cuerpo a cuerpo, criaturas | Puede pegar cuerpo a cuerpo y recibe los golpes de frente |
| **Retaguardia** | Distancia, Curación | No pega cuerpo a cuerpo (salvo lanzas y habilidades de alcance). Mientras haya alguien en vanguardia, los enemigos cuerpo a cuerpo no llegan a ella |

- **No eliges fila.** Al empezar, el juego te pone en la que corresponde a tu rol y tu arma (§7).
- **Cambias de fila solo con un efecto:** una respuesta 🔁 o 💨 que lo diga (*Destrabarse*, *Traslación*, *Salto Vil*), una técnica como *Carga*, la esquiva perfecta, o un empujón enemigo. La *Flecha Clavadora* impide cambiar.
- **Vanguardia vacía:** si nadie de tu bando queda en vanguardia (todos derribados, o juegas solo sin criatura), la retaguardia pasa a recibir los golpes cuerpo a cuerpo. Por eso un sanador solo pelea de frente, y por eso su modo en solitario lo ayuda.

**Agruparse y dispersarse, sin formación.** Ya no hay una formación que elegir: todos cuentan como **agrupados**.
- Ante un **salto en cadena** o una **explosión en área**, una respuesta 💨 (o 🌀 Esquivar) te saca del alcance esa ronda: eso es dispersarse.
- Ante un **golpe compartido** (el meteoro que se reparte), lo correcto es quedarse: el daño se divide entre quienes no se apartaron, y un bloqueo 🛡 de fila o un escudo 🫧 lo baja más.

Los jefes avisan qué viene. "*La bruja marca a tres objetivos con fuego que salta…*": los marcados esquivan. "*El gigante levanta un meteoro sobre el grupo…*": todos se quedan y el tanque bloquea.

## 9. Amenaza

- Cada enemigo tiene una tabla de amenaza que el tanque ve: `Coloso → 🎯 Bram (tanque) · 2.º Lyra (+15 %)`.
- El ⚔️ Atacar de los specs de Defensa genera mucha amenaza, así que el tanque sostiene al enemigo sin gastar casillas.
- **Provocar** es una habilidad de los specs de Defensa: obliga al objetivo durante 2 rondas, para recuperar a un enemigo que se escapó. Se reparte entre los tanques del grupo.
- Algunos jefes **no siempre** siguen la amenaza: ciertos movimientos buscan al sanador, al más débil o a quien más daño hizo. El aviso lo dice. En TowerWars, que el jefe busque primero al sanador y después al más débil funcionó bien como presión; aquí es un rasgo de algunos jefes, no de todos.

## 10. Derribado, levantar y huir

- **Derribado.** Al llegar a 0 de vida no mueres: quedas **derribado** 3 rondas, sangrando, y te arrastras solo a la retaguardia. Tu barra se apaga salvo 🎒 Mochila, para un objeto de emergencia.
- **Levantar.** Cuando un aliado está derribado, la 🎒 Mochila muestra primero *"🤝 Levantar a Lyra"*. Gasta la ronda, no necesita objeto y lo deja con poca vida; con una 🩹 venda, con más. Si ya pasó el plazo, hace falta una resurrección en combate.
- **Caído.** Si pasan las 3 rondas o recibes un golpe de remate, caes. Qué significa depende de la zona y del modo (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)). Caer siempre deja una herida.
- **🏃 Huir.** Se resuelve al final de la ronda. Falla si tienes una pierna herida de gravedad o si te bloquea un enemigo más rápido; la carga ligera ayuda (ver [Equipamiento](../03-personaje/equipamiento.md)). En grupo, huyes tú solo y los demás siguen.
- **🌀 Esquivar** (P-67). Donde no se puede huir (Guardianes de región, arena, ciertos eventos), el botón Huir se vuelve una esquiva básica que tiene cualquier clase. Es una respuesta: va primero, cuesta 1 🔋 y reduce a la mitad el daño de los golpes que te alcancen esa ronda. No corta canalizaciones ni sirve contra los golpes que el aviso marca como imposibles de esquivar. Las respuestas de clase son mejores cuando aciertan la forma del golpe.
- A un Guardián no se le huye: si el grupo se rinde, abandona la instancia con un comando, fuera de la barra.

## 11. PvE y PvP no son el mismo combate

| Regla | PvE | PvP |
|---|---|---|
| Firmeza | Sí | Sí, con ventana más larga |
| Amortiguación de curación | No | Sí: desde la ronda 8, −5 % de curación por ronda |
| Tope de golpe | No | Ninguna acción puede quitar más del **40 % de la vida máxima** de un jugador |
| Modificadores por spec | No | Cada spec tiene un ajuste PvP propio (WoW hace lo mismo) |
| Botón Huir | 🏃 Huir (🌀 Esquivar en Guardianes) | 🌀 Esquivar en la arena; en el mundo abierto se puede huir |
| Cinturón | El tuyo | En la arena clasificada, el mismo para todos |
| Equipo | El tuyo | Normalizado en la arena clasificada (ver [PvP](../06-contenido/pvp.md)) |

## 12. Cómo se ve en Telegram

Un Guardián: no se puede huir, así que el quinto botón es 🌀 Esquivar.

```
⚔️ Ronda 7 · Guardián de la región — Coloso de Cristal
Fase 2/3  ❤️ 61% ▓▓▓▓▓▓░░░░   🟫 Postura ▓▓▓▓▓▓▓▓░░

⚠️ El Coloso hunde los puños en el suelo… la tierra
tiembla bajo la VANGUARDIA.

🟥 Tú — Guerrero Protección 🛡 · Vanguardia
❤️ 842/1.200   💢 Ira 55   🔋 Aguante ●●●○○
🩹 Brazo izq.: corte moderado
🎒 Cinturón: 🧪 Vida ×2 · 🪨 Piel de Piedra ×1 · 🩹 Venda ×1 · 💣 Destello ×1

Turnos: Tú → Lyra → COLOSO → Bram → Ossian
⏱ 45 s

[⚔️ Atacar]            [🛡 Bloqueo con escudo]
[🗣 Grito desafiante]  [💥 Golpe de escudo ✋]
[🌀 Esquivar]          [🎒 Mochila]
```

Después de resolverse, el mismo mensaje pasa a:

```
Ronda 7 — resumen
🛡 Bloqueaste el Terremoto por toda la vanguardia
   (🔋 −1 · 🟫 −180 de postura al Coloso)
✨ Lyra cura a Bram 210
💥 Ossian rompe el BRAZO DERECHO del Coloso: pierde "Puño de Cuarzo"
🩸 Bram: contusión en la pierna izquierda (leve)
▸ Registro completo (tocar para abrir)
```

La última línea es una cita plegable con cada número.

En solitario, sin temporizador y con el modo en solitario activo. Aquí sí se puede huir:

```
🌲 Bosque de Ceniza · Lobo Gris ❤️ 74%

⚠️ El lobo se agacha y mira tu garganta…

🟨 Tú — Sacerdote Sagrado ✚ · solo (modo en solitario)
❤️ 410/620   🔷 Maná 340/500   🔋 ●●●●○
🎒 Cinturón: 🧪 Vida ×1 · 💊 Coagulante ×1 · 🍖 Pan de viaje ×2

[⚔️ Atacar]         [✨ Fuego Sagrado]
[✨ Renovar]        [🫧 Palabra de Poder: Escudo]
[🏃 Huir]           [🎒 Mochila]
```
