# Clases y especializaciones

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Balance](balance.md) · **Alimenta a:** [Combate](../04-combate/README.md), [Talentos](talentos.md), [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) · **Estado:** propuesta (la barra de 6 está decidida en D-46, el reparto de roles responde a D-50 y la capa jugable de §7 a D-79)

**De dónde sale.**
- Las 13 clases y 40 especializaciones de *World of Warcraft* a septiembre de 2026 (expansión *Midnight*, con la tercera spec del Cazador de Demonios, **Devorador**, ya en vivo). Se suman dos clases propias que WoW nunca tuvo y que un juego por turnos pide: **Nigromante** y **Bardo**.
- De *Albion Online*, la idea de que **el equipo aporta habilidades**.
- **Los roles se reparten distinto que en WoW (D-50).** Allí el Mago, el Brujo o el Cazador solo pueden hacer daño. Aquí **cada clase tiene 3 specs de roles distintos** (el Druida, las 4). Que una clase vieja estrene rol ya se probó en *Season of Discovery* (WoW Clásico, 2023-2024): con runas, el Pícaro y el Brujo pasaron a tanquear y el Mago a curar. El Señor de la Guerra sale del Capitán de *El Señor de los Anillos Online*, que lidera con estandartes y gritos.

Total: **15 clases y 46 especializaciones**. La clase se elige al nivel 10; antes, el héroe es un aventurero sin clase con un kit básico.

> **Regla del dueño (D-50):** la clase define el sistema de combate que usas y cómo te unes a la batalla, solo o en grupo. Cada clase tiene varios roles en sus specs. Un tanque puede jugar solo, aunque le cueste; un sanador también, aunque le cueste el doble. Pero tiene que ser posible (ver §5).

---

## 1. Recursos: cada clase conserva su sabor

Cada clase mantiene su recurso de WoW, adaptado a rondas. Además, **todas** comparten dos barras (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)): **Aguante** (lo gastan las habilidades que responden a los avisos, como esquivar o bloquear) y **Firmeza** (resistencia al control).

| Recurso | Clases | Cómo funciona en turnos |
|---|---|---|
| **Ira** | Guerrero, Druida (oso) | Se gana al pegar y al recibir golpes, y decae fuera de combate. Máximo 100 |
| **Energía + Combos** | Pícaro, Druida (felino) | La energía sube 25 por ronda. Los golpes generan combos (hasta 5) y los remates los gastan |
| **Maná** | Magos, sanadores, Chamán, Druida (lechuza) | Reserva grande con regeneración pequeña por ronda. ⚔️ Atacar recupera un poco y las pociones del cinturón, más |
| **Runas + Poder rúnico** | Caballero de la Muerte | 6 runas, se regeneran 2 por ronda. Las habilidades gastan runas y generan poder rúnico |
| **Foco** | Cazador | Sube 20 por ronda. *Apuntar* (habilidad de Puntería) acumula foco extra |
| **Poder Sagrado** | Paladín | De 0 a 5, con generadores y consumidores |
| **Fragmentos de alma** | Brujo, Cazador de Demonios (Devorador) | De 0 a 5. Se generan con ciertas habilidades o cuando mueren enemigos |
| **Chi** | Monje | De 0 a 5, más energía (Viajero del Viento, Cervecero) o maná (Tejedor de Niebla) |
| **Furia** | Cazador de Demonios | Se gana con los golpes y no decae en combate |
| **Esencia** | Evocador | De 0 a 5, recupera 1 cada 2 rondas. Los hechizos **Potenciados** se cargan 1, 2 o 3 rondas: más carga da más poder y más riesgo de que te interrumpan |
| **Vorágine** | Chamán (Elemental, Tótems) | Se acumula; al llenarse, el siguiente hechizo o tótem sale gratis e instantáneo |
| **Poder Astral + Eclipse** | Druida (Equilibrio) | Cada 3 hechizos alterna entre Eclipse Solar y Lunar: el Solar potencia a los aliados y el Lunar refuerza sus controles |
| **Locura** | Sacerdote (Sombra) | Se acumula; al llenarse entra en Forma del Vacío, que también sube su **Corrupción** (ver [Mente](../05-salud/mente.md)) |
| **Cargas Arcanas** | Mago (Arcano) | De 0 a 4. Cada carga sube la potencia y el costo de maná del siguiente hechizo. El mago decide si las gasta él o se las pasa a un aliado |
| **Almas cosechadas** | Nigromante | Se ganan cuando muere cualquier criatura cerca y alimentan esbirros y curas oscuras |
| **Compás** | Bardo | Empezar una canción gasta la elección de esa ronda; después suena sola, sin gastar elecciones, hasta que el Bardo la cambie o lo silencien. Cada ronda que suena sin cortarse suma un compás, y encadenar compases sube el **Crescendo** |

## 2. Las 15 clases

**Los cuatro roles:**

| Rol | Qué hace en la pelea | Ejemplo |
|---|---|---|
| ⚔ **Ataque** | Hace el daño principal; rompe partes y postura | Mago Fuego |
| 🛡 **Defensa** | Recibe los golpes, provoca y protege a su fila: con escudo, con evasión, con barreras o con una criatura que tanquea por él | Monje Maestro Cervecero |
| ✚ **Curación** | Cura, quita estados y levanta a los derribados | Druida Restauración |
| ✦ **Soporte** | Potencia a los aliados o debilita y controla a los enemigos, y además pega | Bardo Estratega |

Cómo leer cada clase:
- **Fila** es donde suele pelear la spec (ver las filas en [Ronda y acciones](../04-combate/ronda-y-acciones.md)).
- **Firma en turnos** es la mecánica que hace que esa spec **se juegue distinto en turnos**, no solo que tenga otros números.
- **Respuestas al aviso** son las habilidades de la clase para contestar a lo que prepara el enemigo (D-46). Las puede elegir cualquier spec de la clase, y algunas specs suman una propia.
- **Aporte de grupo** es de la clase: lo da cualquier spec. Sigue las reglas de [Balance](balance.md): valor parecido entre clases, y dos iguales no se suman. No hay que confundirlo con el rol de Soporte, que es un trabajo de toda la pelea.

### Guerrero · Placas · Ira
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Furia | ⚔ Ataque | Vanguardia | Doble empuñadura. **Golpe Colosal** abre una ventana de 2 rondas en la que el objetivo recibe más daño; al critar entra en **Enfurecido** y su ⚔️ Atacar golpea dos veces. Todo el juego es preparar y aprovechar esa ventana. Ejecuta por debajo del 20 % de vida. Absorbe a la spec Armas de WoW |
| Protección | 🛡 Defensa | Vanguardia | **Bloqueo con escudo** como respuesta al aviso: anula el golpe físico que se ve venir y le baja la postura al enemigo. Es el tanque que lee el aviso |
| Señor de la Guerra | ✦ Soporte | Vanguardia | **Estandartes y gritos.** Planta un estandarte en su fila que dura 3 rondas: *de Guerra* (más daño) o *de Muralla* (menos daño recibido). Sus **gritos** cambian el estandarte sin plantar otro o lo extienden a la otra fila. Es el capitán: decide qué necesita el grupo esta ronda |

**Respuestas al aviso:** bloquear con *Bloqueo con escudo* (si lleva escudo) · desviar con *Parada* · interrumpir con *Zurrar* · cambiar de fila con *Intervenir* (salta junto a un aliado y recibe el golpe por él).
**Aporte de grupo:** **Grito de Batalla** (+poder de ataque del grupo).

### Paladín · Placas · Poder Sagrado + maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Reprensión | ⚔ Ataque | Vanguardia | Construye y gasta Poder Sagrado. **Juicio** marca al enemigo para que reciba más daño sagrado |
| Protección | 🛡 Defensa | Vanguardia | **Escudo del Vengador**, que rebota entre enemigos y silencia; **auras** que protegen a toda su fila. El tanque contra la magia |
| Sagrado | ✚ Curación | Vanguardia | **Faro de Luz**: parte de lo que cura se copia en un aliado marcado. Cura desde la vanguardia |

**Respuestas al aviso:** bloquear con *Escudo Divino* (inmune una ronda, enfriamiento largo) · proteger a otro con *Bendición de Protección* (el aliado ignora el golpe físico avisado) · interrumpir con *Reprimenda*.
**Aporte de grupo:** **Bendición** (mitigación del grupo). Resurrección en combate.

### Cazador · Malla · Foco
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Puntería | ⚔ Ataque | Retaguardia | **Apuntar** es su habilidad: una ronda de puntería y el disparo siguiente impacta seguro en la parte del cuerpo elegida, sin penalización. La mejor spec para romper partes de jefes |
| Bestias | ✦ Soporte | Retaguardia (la mascota, en vanguardia) | **La bestia marca la presa** (*Presa Marcada*): el enemigo recibe más daño de todos durante 5 rondas. *Orden de Matar* la lanza al ataque y *Aspecto de la Tortuga* frena el golpe avisado (D-72) |
| Supervivencia | ✦ Soporte | Vanguardia o retaguardia | **Trampas y control del campo.** Pone trampas en las filas enemigas que se activan en rondas siguientes (*Red* inmoviliza, *Alquitrán* quita iniciativa, *Escarcha* congela) y usa bombas. *Señuelo* desvía el siguiente golpe de un enemigo hacia un muñeco. Gana quitándole opciones al enemigo |

**Respuestas al aviso:** esquivar con *Destrabarse* (salta a la retaguardia) · desviar con *Aspecto de la Tortuga* · interrumpir con *Disparo de Supresión*.
**Aporte de grupo:** **Marca del Cazador** (revela debilidades y sube el crítico del grupo contra ese objetivo). Clamor.

### Pícaro · Cuero · Energía + Combos
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Asesinato | ⚔ Ataque | Vanguardia | Venenos por **acumulación**: llena las barras de veneno y sangrado hasta que revientan |
| Sutileza | ✦ Soporte | Vanguardia | **Golpea desde las sombras y ciega.** *Polvo Cegador* hace que el enemigo pegue más flojo 5 rondas; *Danza de las Sombras* esquiva el golpe avisado y *Contraataque* castiga (D-72) |
| Forajido | ✦ Soporte | Vanguardia | **Dados del Destino para el grupo**: tira un 🎲 nativo de Telegram en el chat y el resultado decide qué bonificación recibe todo el grupo durante 3 rondas (crítico, iniciativa, Aguante o botín extra). *Distracción* le baja la precisión a un enemigo 2 rondas y *Robar* le quita un efecto beneficioso. Azar visible y divertido |

**Respuestas al aviso:** esquivar con *Evasión* · bloquear magia con *Capa de Sombras* · interrumpir con *Patada*.
**Aporte de grupo:** **Veneno Debilitante** (el objetivo pega menos). **Secretos del Oficio** (pasa amenaza al tanque).

### Sacerdote · Tela · Maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Sombra | ⚔ Ataque | Retaguardia | Daño en el tiempo y Locura. La Forma del Vacío sube su Corrupción: riesgo a cambio de recompensa |
| Sagrado | ✚ Curación | Retaguardia | Curas masivas. Es el único sanador que puede **estabilizar heridas leves en combate**, con enfriamiento largo (ver [Heridas](../05-salud/heridas.md)) |
| Disciplina | ✦ Soporte | Retaguardia | **Previene el daño.** Escudos de luz que absorben el golpe avisado, *Sanar* de apoyo y *Penitencia*, que hace que el enemigo pegue más flojo (D-76) |

**Respuestas al aviso:** bloquear con *Palabra de Poder: Escudo* (sobre sí o sobre un aliado) · esquivar con *Desvanecerse* (*Dispersión* en Sombra) · interrumpir con *Silencio*.
**Aporte de grupo:** **Palabra de Poder: Entereza** (+vida máxima del grupo).

### Caballero de la Muerte · Placas · Runas + Poder rúnico
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Escarcha | ⚔ Ataque | Vanguardia | Acumula **Congelación** en el objetivo; al llenarse, el enemigo pierde su siguiente turno |
| Sangre | 🛡 Defensa | Vanguardia | **Golpe de Muerte** cura una parte del daño recibido en las **últimas 2 rondas**: es el tanque que quiere recibir el golpe para devolverlo |
| Profano | ✦ Soporte | Vanguardia | **Plagas que debilitan.** *Peste* baja el daño y la curación del objetivo, y *Brote* la extiende de una vez a toda su fila. Su **Ejército de los muertos** ocupa filas unas rondas y, cada esbirro que cae, suelta una nube de plaga. Hace que el enemigo rinda menos en vez de matarlo antes |

**Respuestas al aviso:** bloquear magia con *Caparazón Antimagia* · resistir un golpe físico con *Entereza Ligada al Hielo* · interrumpir con *Helada Mental* · mover al enemigo con *Agarre Mortal* (lo trae a la vanguardia).
**Aporte de grupo:** **Zona Antimagia** (menos daño mágico al grupo durante 2 rondas). Resurrección en combate.

### Chamán · Malla · Maná + Vorágine
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Elemental | ⚔ Ataque | Retaguardia | **Sobrecarga**: a veces el hechizo se repite solo. La Vorágine llena vuelve instantánea y gratis su próxima *Descarga de Lava* |
| Restauración | ✚ Curación | Retaguardia | **Sanación en Cadena**, que rebota por la fila; *Tótem de Marea*, que cura solo durante unas rondas |
| Tótems | ✦ Soporte | Vanguardia o retaguardia | Planta **tótems** que ocupan un lugar en la fila y actúan solos varias rondas: *Viento Furioso* (+iniciativa del grupo), *Piel de Piedra* (menos daño recibido), *Captura* (atrae el siguiente hechizo enemigo), *Temblor* (quita el miedo y el sueño). Como máximo 2 a la vez, y los enemigos pueden romperlos: hay que elegir dónde plantarlos y cuándo reponerlos. Antes era Mejora |

**Respuestas al aviso:** resistir con *Cambio Astral* · cambiar de fila con *Paso Espiritual* · interrumpir con *Sacudida de Viento*.
**Aporte de grupo:** Clamor (**Clamor Ancestral**). *Purgar* (le quita un efecto beneficioso al enemigo).

### Mago · Tela · Maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Fuego | ⚔ Ataque | Retaguardia | **Calentamiento**: dos críticos seguidos dan una Piroexplosión instantánea. Combustión como ráfaga |
| Escarcha | ✦ Soporte | Vanguardia | **Control con hielo.** *Escarcha Paralizante* hace que el enemigo pegue más flojo 5 rondas; *Barrera de Hielo* absorbe el golpe avisado y *Lanza de Hielo* remata (D-72) |
| Arcano | ✦ Soporte | Retaguardia | **Cargas Arcanas para el grupo.** Las acumula y decide si las quema o se las **pasa a un aliado**: cada carga potencia la siguiente habilidad de ese aliado. *Fuente de Maná* devuelve recurso al grupo. Fuera de combate abre **portales** a asentamientos ya visitados, con las mismas reglas de peso que la Piedra de paso (ver [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md)): un servicio que puede cobrar |

**Respuestas al aviso:** bloquear con *Bloque de Hielo* (inmune una ronda, enfriamiento largo) · cambiar de fila con *Traslación* · interrumpir con *Contrahechizo*.
**Aporte de grupo:** **Intelecto Arcano** (+maná y poder de hechizo del grupo). Clamor (**Distorsión Temporal**). **Mesa de Conjuración**: comida y agua que cuentan para el Sustento (ver [Condiciones](../05-salud/condiciones.md)).

### Brujo · Tela · Maná + Fragmentos de alma
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Destrucción | ⚔ Ataque | Retaguardia | Guarda fragmentos para la **Descarga del Caos**, de crítico garantizado |
| Demonología | 🛡 Defensa | Retaguardia (el demonio, en vanguardia) | **Un demonio guardián tanquea.** El *Guardia Vil* ocupa la vanguardia, provoca y recibe los golpes. Con *Vínculo Demoníaco*, el daño que recibe el demonio se reparte con el brujo, y los fragmentos de alma lo curan o lo potencian. *Sacrificio* lo hace estallar para darle al brujo un escudo grande cuando todo va mal, a cambio de 2 rondas sin tanque hasta invocarlo otra vez |
| Aflicción | ✦ Soporte | Retaguardia | **Maldiciones que debilitan.** Una maldición por enemigo y varias activas a la vez: *Debilidad* (pega menos), *Lenguas* (pierde iniciativa), *Agonía* (se cura menos). El valor está en lo que el enemigo deja de hacer. *Drenar Alma* lo sostiene y remata |

**Respuestas al aviso:** resistir con *Resolución Inagotable* · cambiar de fila con *Círculo Demoníaco* (vuelve al punto que marcó) · interrumpir con *Bloqueo de Hechizo* (lo hace su demonio).
**Aporte de grupo:** **Piedra de Salud** (una curación de un uso para cada miembro). **Piedra de Alma** (resurrección). **Ritual de Invocación** (trae a un compañero al asentamiento).

### Monje · Cuero · Chi + Energía/Maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Viajero del Viento | ⚔ Ataque | Vanguardia | **Golpes en combo**: bonificación si nunca repite la misma habilidad dos rondas seguidas (⚔️ Atacar cuenta como una más) |
| Maestro Cervecero | 🛡 Defensa | Vanguardia | **Tambaleo**: el daño recibido **se reparte en las 3 rondas siguientes** y se puede purgar. Un tanque pensado de verdad para turnos |
| Tejedor de Niebla | ✚ Curación | Retaguardia | Curas **canalizadas**: cada ronda seguida que mantiene la misma, cura más; si lo interrumpen o cambia de acción, se corta. También cura al pegar |

**Respuestas al aviso:** esquivar con *Rodar* (también cambia de fila) · desviar con *Toque de Karma* · interrumpir con *Golpe de Mano de Lanza*.
**Aporte de grupo:** **Palma Mística** (el objetivo recibe más daño físico). **Parálisis**.

### Druida · Cuero · según la forma
El único con los 4 roles, como en WoW.

| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Feral | ⚔ Ataque | Vanguardia | Sangrados y combos. **Acecho** para abrir desde sigilo |
| Guardián | 🛡 Defensa | Vanguardia | Forma de oso con Ira. **Regeneración Frenética** convierte ira en vida |
| Restauración | ✚ Curación | Retaguardia | **Curas en el tiempo** que actúan cada ronda: el sanador que planifica por adelantado |
| Equilibrio | ✦ Soporte | Retaguardia | **Eclipse que potencia al grupo.** Alterna solar y lunar cada 3 hechizos: el Eclipse Solar sube el daño de los aliados de su fila y el Lunar alarga sus controles. *Raíces Enredadoras* impide cambiar de fila y *Ciclón* saca a un enemigo de la pelea una ronda. Hay que planificar el ciclo con la fase del jefe |

**Respuestas al aviso:** resistir con *Piel de Corteza* · cambiar de fila con *Carrerilla Salvaje* · interrumpir con *Golpe de Cráneo* (*Rayo Solar* a distancia).
**Aporte de grupo:** **Marca de lo Salvaje** (+estadísticas). **Renacer** (resurrección en combate).

### Cazador de Demonios · Cuero · Furia
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Estrago | ⚔ Ataque | Vanguardia | **Salto Vil**: cambia de fila y golpea en la misma elección; si lo usa en la ronda del golpe avisado, además lo esquiva. Metamorfosis como ráfaga |
| Venganza | 🛡 Defensa | Vanguardia | **Sigilos** que se activan con una ronda de retraso en la fila elegida: el tanque que predice |
| Devorador | ✦ Soporte | Retaguardia | **Reparte el poder de las almas.** Consume las almas de los enemigos caídos (fragmentos de alma) y las **entrega** a sus aliados: a quien la recibe, cada alma le da recurso, más daño o un escudo pequeño. Usa Intelecto, y el Vacío sube su Corrupción |

**Respuestas al aviso:** esquivar con *Desenfoque* · cambiar de fila con *Retirada Vil* (salta a la retaguardia) · interrumpir con *Alteración*.
**Aporte de grupo:** **Marca del Caos** (el objetivo recibe más daño mágico). **Visión Espectral** (revela lo invisible y lo que está en sigilo).

### Evocador · Malla · Esencia
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Devastación | ⚔ Ataque | Retaguardia | Hechizos **Potenciados** de 1 a 3 rondas de carga |
| Preservación | ✚ Curación | Retaguardia | **Eco** duplica la próxima cura, y **Rebobinar** devuelve al grupo parte del daño recibido en las últimas 2 rondas. Magia del tiempo hecha para turnos |
| Aumentación | ✦ Soporte | Retaguardia | **Potencia a un aliado** directamente: *Poder de Ébano* le presta una parte de sus estadísticas y *Presciencia* le asegura el crítico de su siguiente golpe. Sigue la regla de familias: no se suma con otra potenciación sobre el mismo aliado (ver [Balance](balance.md)) |

**Respuestas al aviso:** resistir con *Escamas Obsidianas* · cambiar de fila con *Planear* · interrumpir con *Sofocar*.
**Aporte de grupo:** Clamor (**Furia del Vuelo**).

### Nigromante · Tela · Almas cosechadas *(clase propia)*
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Plaga | ⚔ Ataque | Retaguardia | Enfermedades de combate que **saltan** de un enemigo a otro por fila |
| Legión | 🛡 Defensa | Retaguardia (los esqueletos, en vanguardia) | **Muro de esqueletos.** Levanta esqueletos en la vanguardia que provocan y **se sacrifican**: cada uno bloquea un golpe entero o explota. Las almas cosechadas reponen el muro. Un tanque que se construye con lo que muere |
| Drenaje | ✚ Curación | Retaguardia | **Sanador oscuro**: cura a los aliados con la vida que le quita a los enemigos, o pagando con la propia |

**Respuestas al aviso:** bloquear con *Hueso Protector* (un esqueleto recibe el golpe por él o por un aliado) · esquivar con *Forma Espectral* (los golpes físicos lo atraviesan una ronda) · interrumpir con *Grito del Sepulcro*.
**Aporte de grupo:** **Cosecha** (cuando muere un enemigo, el grupo recupera un poco de recurso). Resurrección en combate. Fuera de combate: **Remiendo**, el único que cura heridas a los Renacidos sin médico.

### Bardo · Cuero · Compás *(clase propia)*
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Duelista | ⚔ Ataque | Vanguardia | **Danza de espadas**: combos que salen al elegir las habilidades en la secuencia correcta, como un ritmo |
| Trovador | ✚ Curación | Retaguardia | **Baladas**: la canción cura a todo el grupo cada ronda mientras suena; el Trovador usa sus elecciones en curas puntuales sin cortarla |
| Estratega | ✦ Soporte | Retaguardia | El único que **mueve la cola de iniciativa** a voluntad: *Allegro* adelanta a un aliado y *Contratiempo* retrasa a un enemigo. Diseñado para turnos |

**Respuestas al aviso:** esquivar con *Paso de Baile* (también cambia de fila) · bloquear con *Nota Sostenida* (un escudo de sonido absorbe un golpe) · interrumpir con *Disonancia*.
**Aporte de grupo:** **Himno de Valor**. Clamor. Fuera de combate **baja el estrés** del grupo y de los clientes de la taberna (ver [Mente](../05-salud/mente.md)). Origen: el Animador de *Star Wars Galaxies*, que curaba el cansancio de batalla tocando en la cantina.

## 3. Mapa y recuento de roles

| Clase | ⚔ Ataque | 🛡 Defensa | ✚ Curación | ✦ Soporte |
|---|---|---|---|---|
| Guerrero | Furia | Protección | — | Señor de la Guerra |
| Paladín | Reprensión | Protección | Sagrado | — |
| Cazador | Puntería | Bestias | — | Supervivencia |
| Pícaro | Asesinato | Sutileza | — | Forajido |
| Sacerdote | Sombra | — | Sagrado | Disciplina |
| Caballero de la Muerte | Escarcha | Sangre | — | Profano |
| Chamán | Elemental | — | Restauración | Tótems |
| Mago | Fuego | Escarcha | — | Arcano |
| Brujo | Destrucción | Demonología | — | Aflicción |
| Monje | Viajero del Viento | Maestro Cervecero | Tejedor de Niebla | — |
| Druida | Feral | Guardián | Restauración | Equilibrio |
| Cazador de Demonios | Estrago | Venganza | — | Devorador |
| Evocador | Devastación | — | Preservación | Aumentación |
| Nigromante | Plaga | Legión | Drenaje | — |
| Bardo | Duelista | — | Trovador | Estratega |
| **Total: 46** | **15** | **11** | **8** | **12** |

- **Toda clase tiene una spec de Ataque:** cualquiera puede elegir el camino más cómodo para jugar solo y cambiar de spec gratis en un asentamiento para ir en grupo (ver [Talentos](talentos.md)).
- 11 clases pueden tanquear, 8 pueden curar y 12 pueden hacer de Soporte.
- **Qué cambió respecto a WoW:** pasan a Defensa Cazador Bestias, Pícaro Sutileza, Mago Escarcha y Brujo Demonología; pasan a Soporte Cazador Supervivencia, Pícaro Forajido, Sacerdote Disciplina, Caballero Profano, Mago Arcano, Brujo Aflicción, Druida Equilibrio y Cazador de Demonios Devorador. Son nuevas el Señor de la Guerra (Furia se queda con el Golpe Colosal de Armas) y Tótems (antes Mejora).

## 4. La barra de 6: clase + equipo (D-46)

**De dónde sale.** En *Albion Online* no hay clases: el arma que empuñas da tus habilidades principales y cada pieza de armadura da una más. En WoW la clase decide todo y la botonera crece sin fin. Aquí la clase decide y el equipo suma, pero **nunca hay más de 6 botones** (D-46).

| Botón | Qué es |
|---|---|
| ⚔️ **Atacar** | El golpe básico de tu arma (o el hechizo básico de tu spec). Siempre está, genera recurso y cuenta como la primera de tus 4 "habilidades". Cuando cargas tu Límite, se transforma en él (ver [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md)) |
| ✨ **Habilidad 1, 2 y 3** | Las 3 que elegiste del repertorio de tu spec. Una de ellas puede ser la **técnica de tu arma o de tu armadura**: la espada larga da *Tajo Circular*, la lanza *Estocada Profunda*, el escudo torre *Muro* (propuesta P-68; lista en [Equipamiento](equipamiento.md)) |
| 🏃 **Huir** | Se resuelve al final de la ronda. Donde no se puede huir (Guardianes, arena) se vuelve **🌀 Esquivar** (propuesta P-67) |
| 🎒 **Mochila** | En combate abre solo el **cinturón** (abajo) |

**Reglas de la barra:**
- **Una sola elección por ronda.** No hay acción rápida ni reacción aparte: si respondes al aviso, esa es tu ronda. Elegir entre pegar o protegerte es la decisión que importa.
- **Siempre hay con qué responder al aviso.** Cada clase tiene en su repertorio habilidades defensivas o de reposicionamiento (las "Respuestas al aviso" de cada clase, §2). La configuración inicial de cada spec trae una en la barra; quitarla es decisión del jugador. Y donde no se puede huir, Huir pasa a Esquivar.
- **El resto del repertorio se cambia fuera de combate**, con las configuraciones guardadas de [Talentos](talentos.md) ("mazmorra", "solitario", "PvP"…).
- **Como máximo una técnica de equipo en la barra** (P-68), de arma o de armadura, en lugar de una habilidad de clase. Las técnicas defensivas de armadura (*Capa de Humo*, *Barrera Rúnica*, *Resistir*) cuentan como respuestas al aviso (ver [Equipamiento](equipamiento.md) §7). Así el equipo sigue importando por lo que hace, sin sumar botones.

**El cinturón.**
- Pocas casillas que llenas **antes** de pelear; cuántas, según el cinturón que lleves (de 3 a 6; ver [Inventario y mochilas](inventario-y-mochilas.md), D-47).
- Qué va: pociones de vida, **pociones de resistencia** (contra fuego, frío o veneno: sirven para responder al aviso), remedios para estados (antídoto para el veneno, venda para el sangrado, ungüento para la quemadura, tónico caliente para la congelación), bombas y comida rápida.
- Usar un objeto **gasta la elección de la ronda**.
- La **Toxicidad** limita cuántas pociones aguantas (ver [Condiciones](../05-salud/condiciones.md)).
- Lo que no está en el cinturón no se usa en combate: la mochila grande se abre fuera de la pelea.

**Partes del cuerpo sin botón propio.** Apuntar deja de ser un botón aparte. La forma más ligera:
1. **Por defecto, ⚔️ Atacar va al torso.** Un toque, sin menús.
2. **Algunas habilidades llevan la parte incluida:** *Golpe de Escudo* va a la cabeza (puede aturdir), *Tajo a las Corvas* a las piernas, *Desarmar* a los brazos. Es la forma normal de romper partes.
3. **Apuntar con Atacar (opcional, capa profunda):** si lo activas en tus opciones, al tocar Atacar contra un monstruo con partes rompibles aparece una fila de partes ([Cabeza] [Brazos] [Piernas] [Cola]…). La parte elegida **se recuerda** en las rondas siguientes, así que después vuelve a ser un solo toque. Las penalizaciones de precisión de [Daño y estados](../04-combate/dano-y-estados.md) se aplican igual.
4. El Cazador de Puntería tiene *Apuntar* como habilidad: sin penalización y con impacto seguro.

Por qué así: el jugador nuevo nunca ve el menú de partes, el que quiere cazar materiales lo tiene a un ajuste de distancia y no se suma ningún botón (D-44, D-46).

**Cómo se ve en Telegram** (contra un Guardián, donde Huir aparece como Esquivar):

```
🟥 Tú — 🛡 Guerrero Protección · Vanguardia
⚠️ El Coloso hunde los puños en el suelo… la tierra
tiembla bajo la VANGUARDIA.

[⚔️ Atacar]           [🛡 Bloqueo con escudo]
[🔨 Quebrantahuesos]  [🗣 Grito desafiante]
[🌀 Esquivar]         [🎒 Mochila]
```

*Quebrantahuesos* es la técnica de la maza ocupando una casilla. Tres filas de dos botones caben igual en Telegram, en la web y en el móvil.

**Por qué conviene.**
- La clase conserva su identidad (WoW): la firma de la spec vive en sus 3 habilidades.
- Dentro de la misma spec hay variedad según el arma y la armadura (Albion).
- **El equipo importa por lo que hace, no solo por sus números.** Eso le da demanda a cada tipo de arma y armadura que fabrican los artesanos, y hace que perder equipo en una zona negra duela y se pueda reemplazar.
- Con una sola elección por ronda, leer el aviso vuelve a ser la habilidad principal.

## 5. Solo y en grupo

La clase decide **cómo peleas** y **cómo te unes a la batalla**. Toda spec puede jugar sola el contenido en solitario (misiones, encargos, Profundidades normales); lo que cambia es cuánto le cuesta según su rol (D-50). Los números exactos y cómo se miden están en [Balance](balance.md) (regla 4).

### Solo

| Rol | Cómo gana solo | Cuánto tarda (contra Ataque) | Qué le da el modo en solitario |
|---|---|---|---|
| ⚔ Ataque | Mata rápido y se cubre con su respuesta al aviso y el cinturón | 1× (la referencia) | No lo necesita |
| ✦ Soporte | Sus debilitamientos y controles le quitan peligro al enemigo | Algo más: ~1,25× | Sus potenciaciones de grupo también cuentan para él y para su compañero |
| 🛡 Defensa | Casi no cae, pero mata despacio | Más: ~1,5× | **Represalia:** parte del daño que bloquea, esquiva o absorbe vuelve como daño. La mascota, el demonio o los esqueletos también pegan |
| ✚ Curación | Se cura a sí mismo y aguanta, pero hace poco daño | El doble: ~2× | **Autosostén:** parte de la curación que sobra pasa a daño contra el enemigo, y curarse a sí mismo cuesta menos |

- **El modo en solitario se enciende solo** cuando no hay otro jugador en la pelea (con compañero PNJ o sin él) y se apaga en cuanto entra uno. No existe en grupo ni en PvP.
- **Siempre posible:** el simulador comprueba que toda spec gana el contenido en solitario de su anillo con juego básico (ver [Balance](balance.md)).
- **Ayudas para el rol lento:** el compañero PNJ de las [Profundidades](../06-contenido/misiones-y-exploracion.md) cubre el rol que te falta (un sanador lleva un compañero de Ataque); la configuración guardada "solitario" pone en la barra lo que mejor rinde solo; y cambiar de spec es gratis en cualquier asentamiento.
- **Por qué Defensa y Curación tardan más:** es el precio del rol que el grupo más necesita. A cambio, en grupo son los más buscados y los que más recompensa extra reciben (abajo).

### En grupo

| Contenido | Composición |
|---|---|
| Mazmorra (5) | **1 🛡 + 1 ✚ + 3 de ⚔ o ✦** |
| Banda (10 a 25) | Flexible. Guía: 2 🛡, 1 ✚ cada 5 jugadores y el resto ⚔ o ✦. Las mecánicas piden roles, nunca clases |
| Profundidades (1 a 5) | Libre; el compañero PNJ completa lo que falte |
| Arena y campos de batalla | Libre (la curación se amortigua en PvP; ver [Balance](balance.md)) |
| Mundo abierto (jefes errantes, defensas de asentamiento) | Libre: te sumas a la pelea en curso desde la ronda siguiente |

**Cómo te unes:**
- **Buscador de grupos por rol** (ver [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md)): te anotas con uno o varios roles de tu clase (un Druida puede anotarse a los 4) y, al entrar, se activa la spec del rol que te tocó.
- **Llamada a las armas** (de WoW): cuando falta un rol, casi siempre 🛡 o ✚, el buscador da una bolsa extra a quien entre con ese rol: moneda y materiales del juego, nunca nada de dinero real (D-43).
- **Tu rol se ve junto a tu nombre** en el mensaje del combate (🛡 Bram, ✚ Lyra) y decide tu fila de partida: Defensa en vanguardia, Curación en retaguardia. Las excepciones están en la columna "Fila" de cada spec.
- **Un ✦ Soporte ocupa el lugar de un ⚔ Ataque** y el grupo rinde igual: pega menos, pero hace rendir más a los demás. Dos efectos de Soporte de la misma familia no se suman sobre el mismo aliado (ver [Balance](balance.md), regla 5).
- Además, cada clase suma su **aporte de grupo** (§2).

## 6. Orden de lanzamiento: la historia de WoW como calendario

Lanzar 15 clases a la vez es imposible de equilibrar y de producir. Se propone repetir el orden en que WoW las fue sumando:

| Momento | Clases | Equivalente en WoW |
|---|---|---|
| **Lanzamiento** | Guerrero, Paladín, Cazador, Pícaro, Sacerdote, Chamán, Mago, Brujo, Druida | Las 9 de 2004 |
| **Expansión 1** | Caballero de la Muerte | *Wrath of the Lich King* (2008) |
| **Expansión 2** | Monje | *Mists of Pandaria* (2012) |
| **Expansión 3** | Cazador de Demonios | *Legion* (2016) |
| **Expansión 4** | Evocador | *Dragonflight* (2022) |
| **Expansión 5** | Nigromante | Propia |
| **Expansión 6** | Bardo | Propia |

Desde el lanzamiento ya están los 4 roles: 28 specs, de ellas 9 de Ataque, 7 de Defensa, 4 de Curación y 8 de Soporte.

Cada clase nueva llega con su evento, su zona de inicio especial y una cadena de historia. Ver [Hoja de ruta](../00-vision/hoja-de-ruta.md).


## 7. Lo que ya está en el juego: 8 habilidades por especialización (D-79)

Las secciones de arriba son el diseño completo. En la versión jugable, cada una de las 45 especializaciones tiene **8 habilidades**: las 3 de siempre y 5 nuevas inspiradas en las habilidades emblemáticas de esa especialización en World of Warcraft (las del Nigromante y el Bardo, clases propias, siguen la misma idea). Cada especialización conserva su rol (D-72) y cada clase sigue cubriendo al menos dos roles.

**Desbloqueo** (puntos de talento en esa especialización; ver [Talentos](talentos.md) §5):

| Habilidad | 1.ª | 2.ª | 3.ª | 4.ª | 5.ª | 6.ª | 7.ª | 8.ª |
|---|---|---|---|---|---|---|---|---|
| Puntos | 1 | 3 | 6 | 10 | 16 | 24 | 34 | 46 |
| Nivel, con todo en una sola | 2 | 4 | 7 | 11 | 17 | 25 | 35 | 47 |

**La barra sigue siendo de 6 botones (D-46):** ⚔️ Atacar, 3 habilidades, 🎒 Mochila y 🏃 Huir (o 🌀 Esquivar). Las 3 habilidades se eligen en 🌟 Talentos → 🎛️ Barra de combate:
- **Casilla 1:** una respuesta al aviso (🛡 bloquear, 💨 esquivar o 🫧 escudo), elegida entre las que abriste.
- **Casillas 2 y 3:** cualquier otra habilidad que abriste, de cualquier especialización de tu clase.
- **Si no eliges,** la barra se arma sola: tu respuesta más nueva, tu golpe más nuevo y tu otra habilidad más nueva.

**Números bajos al inicio.** Las primeras habilidades tienen valores modestos (las mejoras de daño de las 3 primeras bajaron de 60 % a 50 %) y las nuevas se mueven en el mismo rango: golpes de ×1 a ×2,8 el ataque, mejoras de daño de 30 a 35 %, debilitamientos de 25 a 50 % (los más altos duran solo 2 o 3 rondas), curas de 20 a 45 % de la vida. Las tardías son un poco más fuertes, pero con más costo o más rondas de espera. Hay dos piezas nuevas en el combate: habilidades que **dan recurso** (como *Sed de Sangre*, +15 de Ira) y golpes que **suman combos** (como *Mutilar*, +2), para que Pícaro, Druida Feral y Bardo Duelista armen sus remates como en WoW.

**Las 45 especializaciones:**

| Especialización | Rol | 1 a 3 (1, 3 y 6 puntos) | 4 a 8 (10, 16, 24, 34 y 46 puntos) |
|---|---|---|---|
| 💢 Guerrero · Furia | ⚔ Ataque | Golpe Colosal, Ejecutar, Parada | Sed de Sangre, Reflejo de Hechizos, Temeridad, Regeneración Enfurecida, Desenfreno |
| 🏰 Guerrero · Protección | 🛡 Defensa | Golpe heroico, Bloqueo con escudo, Segundo aliento | Golpe con Escudo, Grito Desmoralizador, Venganza, Muro de Escudo, Última Resistencia |
| 🚩 Guerrero · Señor de la Guerra | ✦ Soporte | Estandarte de Guerra, Estandarte de Muralla, Intervenir | Grito de Batalla, Lanzamiento Heroico, Golpe Mortal, Grito de Reunión, Grito Intimidador |
| ⚖️ Paladín · Reprensión | ⚔ Ataque | Juicio, Veredicto del Templario, Escudo Divino | Hoja de Justicia, Palabra de Gloria, Cólera Vengativa, Estela de Cenizas, Sentencia de Ejecución |
| 🔰 Paladín · Protección | 🛡 Defensa | Escudo del Vengador, Bendición de Protección, Aura de Devoción | Consagración, Escudo de los Justos, Defensor Ardiente, Guardián de los Reyes Ancestrales, Imposición de Manos |
| 🌅 Paladín · Sagrado | ✚ Curación | Destello de Luz, Faro de Luz, Escudo Divino | Juicio de Luz, Luz Sagrada, Bendición de Sacrificio, Luz del Alba, Prisma Sagrado |
| 🎯 Cazador · Puntería | ⚔ Ataque | Apuntar, Disparo Certero, Destrabarse | Disparo Arcano, Disparo de Contención, Supervivencia del Más Apto, Fuego Rápido, Disparo Mortal |
| 🐺 Cazador · Bestias | ✦ Soporte | Orden de Matar, Aspecto de la Tortuga, Presa Marcada | Disparo de Púas, Intimidación, Cólera de las Bestias, Euforia, Llamada de lo Salvaje |
| 🪤 Cazador · Supervivencia | ✦ Soporte | Trampa de Alquitrán, Marca del Cazador, Señuelo | Bomba de Fuego Salvaje, Bozal, Golpe de Raptor, Trampa Congelante, Asalto Coordinado |
| 🐍 Pícaro · Asesinato | ⚔ Ataque | Eviscerar, Evasión, Patada | Mutilar, Garrote, Vial Carmesí, Marca de la Muerte, Envenenar |
| 🌑 Pícaro · Sutileza | ✦ Soporte | Danza de las Sombras, Contraataque, Polvo Cegador | Golpe en los Riñones, Amago, Ceguera, Símbolos de Muerte, Técnica Secreta |
| 🏴‍☠️ Pícaro · Forajido | ✦ Soporte | Dados del Destino, Distracción, Capa de Sombras | Disparo de Pistola, Gubia, Riposte, Golpe Fantasmal, Ola de Asesinatos |
| 👁️ Sacerdote · Sombra | ⚔ Ataque | Toque Vampírico, Tortura Mental, Dispersión | Palabra de las Sombras: Dolor, Silencio, Peste Devoradora, Alarido Psíquico, Palabra de las Sombras: Muerte |
| 😇 Sacerdote · Sagrado | ✚ Curación | Plegaria de Sanación, Renovar, Palabra de Poder: Escudo | Sanación Relámpago, Palabra Sagrada: Castigo, Rezo de Alivio, Espíritu Guardián, Palabra Sagrada: Serenidad |
| 📿 Sacerdote · Disciplina | ✦ Soporte | Sanar, Escudo de luz, Penitencia | Purgar al Malvado, Supresión de Dolor, Infusión de Poder, Palabra de Poder: Resplandor, Cisma |
| 🧊 Caballero de la Muerte · Escarcha | ⚔ Ataque | Golpe de Escarcha, Helada Mental, Entereza Ligada al Hielo | Explosión Aullante, Pilar de Escarcha, Arrasar, Invierno Despiadado, Furia del Vermis de Escarcha |
| 🫀 Caballero de la Muerte · Sangre | 🛡 Defensa | Golpe de Muerte, Escudo de Huesos, Hervor de Sangre | Desgarro de Médula, Sangre Vampírica, Arma de Runas Danzante, Muerte y Descomposición, Bebesangre |
| ☣️ Caballero de la Muerte · Profano | ✦ Soporte | Peste, Ejército de los muertos, Caparazón Antimagia | Espiral de la Muerte, Atracción Letal, Transformación Oscura, Brote, Apocalipsis |
| 🌩️ Chamán · Elemental | ⚔ Ataque | Descarga de Lava, Choque de Llamas, Paso Espiritual | Descarga de Relámpagos, Corte de Viento, Guardián de Tormentas, Choque de Tierra, Elemental de Fuego |
| 🌊 Chamán · Restauración | ✚ Curación | Sanación en Cadena, Tótem de Marea, Cambio Astral | Mareas Vivas, Choque de Escarcha, Escudo de Tierra, Ola de Sanación, Ascensión |
| 🗿 Chamán · Tótems | ✦ Soporte | Tótem Viento Furioso, Tótem Piel de Piedra, Tótem de Captura | Golpe de Tormenta, Tótem de Condensador, Tótem de Corriente Sanadora, Latigazo de Lava, Espíritu Feral |
| ☄️ Mago · Fuego | ⚔ Ataque | Piroexplosión, Combustión, Bloque de Hielo | Explosión de Fuego, Contrahechizo, Bomba Viviente, Barrera Ardiente, Meteorito |
| 🌨️ Mago · Escarcha | ✦ Soporte | Barrera de Hielo, Lanza de Hielo, Escarcha Paralizante | Nova de Escarcha, Venas Heladas, Ventisca, Orbe Congelado, Púa Glacial |
| 💠 Mago · Arcano | ✦ Soporte | Poder Arcano, Ralentizar, Barrera Prismática | Misiles Arcanos, Supernova, Imagen Reflejada, Toque del Magi, Tromba Arcana |
| 🌋 Brujo · Destrucción | ⚔ Ataque | Descarga del Caos, Inmolar, Resolución Inagotable | Incinerar, Espiral Mortal, Conflagrar, Pacto Oscuro, Invocar Infernal |
| 👹 Brujo · Demonología | 🛡 Defensa | Hachazo Vil, Vínculo Demoníaco, Sacrificio | Descarga Demoníaca, Furia de las Sombras, Armadura Demoníaca, Drenar Vida, Tirano Demoníaco |
| 🕸️ Brujo · Aflicción | ✦ Soporte | Maldición de Debilidad, Drenar Alma, Círculo Demoníaco | Corrupción, Miedo, Atormentar, Putrefacción de Alma, Éxtasis Maléfico |
| 🌪️ Monje · Viajero del Viento | ⚔ Ataque | Patada del Sol Naciente, Palma Mística, Rodar | Palma del Tigre, Golpe de Mano de Lanza, Puños de Furia, Tormenta, Tierra y Fuego, Toque de la Muerte |
| 🍺 Monje · Maestro Cervecero | 🛡 Defensa | Golpe de Barril, Toque de Karma, Brebaje Purificador | Soplo de Fuego, Barrido de Pierna, Brebaje Celestial, Barril Explosivo, Invocar a Niuzao |
| 🌫️ Monje · Tejedor de Niebla | ✚ Curación | Niebla Envolvente, Vivificar, Capullo de Vida | Parálisis, Niebla Renovadora, Té de Enfoque Atronador, Regalo de Sheilun, Revivir |
| 🐆 Druida · Feral | ⚔ Ataque | Mordedura Feroz, Desgarrar, Piel de Corteza | Triturar, Testarazo, Furia del Tigre, Instintos de Supervivencia, Ira Primigenia |
| 🐻 Druida · Guardián | 🛡 Defensa | Destrozar, Pelaje de Hierro, Regeneración Frenética | Vapulear, Rugido Incapacitador, Magullar, Furia del Durmiente, Encarnación de Ursoc |
| 🌸 Druida · Restauración | ✚ Curación | Rejuvenecimiento, Alivio Presto, Corteza de Hierro | Fuego Lunar, Recrecimiento, Flor de Vida, Crecimiento Salvaje, Tranquilidad |
| 🦇 Cazador de demonios · Estrago | ⚔ Ataque | Golpe del Caos, Metamorfosis, Salto Vil | Mordisco Demoníaco, Disrupción, Desdibujar, Rayo Ocular, La Cacería |
| 👺 Cazador de demonios · Venganza | 🛡 Defensa | Sigilo de Llamas, Púas Demoníacas, Sigilo de Miseria | Cizallar, Sigilo de Silencio, Hendidura de Alma, Marca Ígnea, Devastación Vil |
| 🕳️ Cazador de demonios · Devorador | ✦ Soporte | Entregar Alma, Marca del Caos, Escudo de Almas | Consumir, Rayo del Vacío, Cambio de Fase, Cosecha de Almas, Estrella Colapsante |
| 🐲 Evocador · Devastación | ⚔ Ataque | Aliento de Fuego, Desintegrar, Planear | Llama Viva, Sofocar, Furia Dragontina, Estrella Destrozadora, Oleada de Eternidad |
| ⏳ Evocador · Preservación | ✚ Curación | Eco, Rebobinar, Escamas Obsidianas | Flor Esmeralda, Dilatación Temporal, Aliento Onírico, Anomalía Temporal, Flor Espiritual |
| 🔆 Evocador · Aumentación | ✦ Soporte | Poder de Ébano, Presciencia, Salto Temporal | Erupción, Distorsión Temporal, Escamas Abrasadoras, Sublevación, Aliento de Eones |
| 🪦 Nigromante · Plaga | ⚔ Ataque | Plaga Reptante, Estallido Pútrido, Forma Espectral | Toque de Putrefacción, Enjambre de Moscas, Contagio, Ola de Pestilencia, Epidemia |
| 🧟 Nigromante · Legión | 🛡 Defensa | Hueso Protector, Levantar Esqueletos, Grito del Sepulcro | Golpe de Hueso, Muro de Cadáveres, Coloso de Huesos, Festín de Cadáveres, Legión Inmortal |
| 🧛 Nigromante · Drenaje | ✚ Curación | Sifón Vital, Pacto de Sangre, Velo de Almas | Mano de la Tumba, Marchitar, Transfusión, Cosecha Vital, Segador de Almas |
| 🤺 Bardo · Duelista | ⚔ Ataque | Floritura Final, Estocada Rítmica, Paso de Baile | Estocada Doble, Contrapunto, Finta, Crescendo, Gran Final |
| 🎶 Bardo · Trovador | ✚ Curación | Balada Curativa, Nota Curativa, Nota Sostenida | Canción de Cuna, Himno de Esperanza, Acorde Disonante, Coro Celestial, Réquiem de Vida |
| 🥁 Bardo · Estratega | ✦ Soporte | Allegro, Contratiempo, Calderón | Staccato, Síncopa, Compás de Espera, Fortissimo, Sinfonía de Guerra |

Datos: `content/classes.yaml` (habilidades y números), `content/locales/es_clases.yaml` (nombres), `content/balance.yaml` (`talents`). Balance medido con `tools/sim.py`.

Ver P-12, P-14, P-67 y P-68 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md). La barra de 6 está decidida (D-46) y el reparto de roles responde a D-50.
