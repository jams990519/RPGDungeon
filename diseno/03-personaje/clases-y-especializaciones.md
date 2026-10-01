# Clases y especializaciones

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Balance](balance.md) · **Alimenta a:** [Combate](../04-combate/README.md), [Talentos](talentos.md), [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) · **Estado:** propuesta (la barra de 6 está decidida en D-46, el reparto de roles responde a D-50 y la capa jugable de §7 a D-79)

**De dónde sale.**
- Las 13 clases y 40 especializaciones de *World of Warcraft* a septiembre de 2026 (expansión *Midnight*, con la tercera spec del Cazador de Demonios, **Devorador**, ya en vivo). Se suman dos clases propias que WoW nunca tuvo y que un juego por turnos pide: **Nigromante** y **Bardo**.
- De *Albion Online*, la idea de que **el equipo aporta habilidades**.
- **Los nombres son propios (D-135).** De WoW salen la estructura de clases y specs y la idea de cada habilidad, no sus nombres: en octubre de 2026 se cambiaron los nombres visibles de 241 habilidades y 23 ataques básicos que copiaban la traducción oficial de WoW o la traducían palabra por palabra (revisión C-150 del cuestionario de beta). Los IDs no cambiaron. La tabla está en §8.
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

**Cómo se nota el rol en una pelea sola (D-110, en el juego desde la pasada de balance de clases y roles):** el ⚔ Ataque mata en menos rondas y termina con menos vida; el ✦ Soporte queda en medio; la 🛡 Defensa tarda ~1,5 veces más pero termina con más vida que el Ataque de su clase (desde el nivel 25: tiene más armadura base que su hermano de Ataque, sus puntos le suman armadura y su barra automática guarda una curación); la ✚ Curación es la que más tarda (~2 veces) y la que más vida deja. Las cifras y cómo se miden están en [Balance](balance.md) §7.

Cómo leer cada clase:
- **Fila** es donde suele pelear la spec (ver las filas en [Ronda y acciones](../04-combate/ronda-y-acciones.md)).
- **Firma en turnos** es la mecánica que hace que esa spec **se juegue distinto en turnos**, no solo que tenga otros números.
- **Respuestas al aviso** son las habilidades de la clase para contestar a lo que prepara el enemigo (D-46). Las puede elegir cualquier spec de la clase, y algunas specs suman una propia.
- **Aporte de grupo** es de la clase: lo da cualquier spec. Sigue las reglas de [Balance](balance.md): valor parecido entre clases, y dos iguales no se suman. No hay que confundirlo con el rol de Soporte, que es un trabajo de toda la pelea.

### Guerrero · Placas · Ira
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Furia | ⚔ Ataque | Vanguardia | Doble empuñadura. **Rompecorazas** abre una ventana de 2 rondas en la que el objetivo recibe más daño; al critar entra en **Enfurecido** y su ⚔️ Atacar golpea dos veces. Todo el juego es preparar y aprovechar esa ventana. Ejecuta por debajo del 20 % de vida. Absorbe a la spec Armas de WoW |
| Protección | 🛡 Defensa | Vanguardia | **Bloqueo con escudo** como respuesta al aviso: anula el golpe físico que se ve venir y le baja la postura al enemigo. Es el tanque que lee el aviso |
| Señor de la Guerra | ✦ Soporte | Vanguardia | **Estandartes y gritos.** Planta un estandarte en su fila que dura 3 rondas: *de Guerra* (más daño) o *de Muralla* (menos daño recibido). Sus **gritos** cambian el estandarte sin plantar otro o lo extienden a la otra fila. Es el capitán: decide qué necesita el grupo esta ronda |

**Respuestas al aviso:** bloquear con *Bloqueo con escudo* (si lleva escudo) · desviar con *Parada* · interrumpir con *Zurrar* · cambiar de fila con *Interponerse* (salta junto a un aliado y recibe el golpe por él).
**Aporte de grupo:** **Arenga de Guerra** (+poder de ataque del grupo).

### Paladín · Placas · Poder Sagrado + maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Reprensión | ⚔ Ataque | Vanguardia | Construye y gasta Poder Sagrado. **Juicio** marca al enemigo para que reciba más daño sagrado |
| Protección | 🛡 Defensa | Vanguardia | **Escudo Acallador**, que rebota entre enemigos y silencia; **auras** que protegen a toda su fila. El tanque contra la magia |
| Sagrado | ✚ Curación | Vanguardia | **Candil del Alba**: parte de lo que cura se copia en un aliado marcado. Cura desde la vanguardia |

**Respuestas al aviso:** bloquear con *Amparo Celestial* (inmune una ronda, enfriamiento largo) · proteger a otro con *Gracia Protectora* (el aliado ignora el golpe físico avisado) · interrumpir con *Reprimenda*.
**Aporte de grupo:** **Bendición** (mitigación del grupo). Resurrección en combate.

### Cazador · Malla · Foco
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Puntería | ⚔ Ataque | Retaguardia | **Apuntar** es su habilidad: una ronda de puntería y el disparo siguiente impacta seguro en la parte del cuerpo elegida, sin penalización. La mejor spec para romper partes de jefes |
| Bestias | ✦ Soporte | Retaguardia (la mascota, en vanguardia) | **La bestia marca la presa** (*Presa Marcada*): el enemigo recibe más daño de todos durante 5 rondas. *Zarpazo a la Orden* la lanza al ataque y *Concha Cerrada* frena el golpe avisado (D-72) |
| Supervivencia | ✦ Soporte | Vanguardia o retaguardia | **Trampas y control del campo.** Pone trampas en las filas enemigas que se activan en rondas siguientes (*Red* inmoviliza, *Brea* quita iniciativa, *Escarcha* congela) y usa bombas. *Señuelo* desvía el siguiente golpe de un enemigo hacia un muñeco. Gana quitándole opciones al enemigo |

**Respuestas al aviso:** esquivar con *Salto Atrás* (salta a la retaguardia) · desviar con *Concha Cerrada* · interrumpir con *Disparo de Supresión*.
**Aporte de grupo:** **Ojo del Rastreador** (revela debilidades y sube el crítico del grupo contra ese objetivo). Clamor.

### Pícaro · Cuero · Energía + Combos
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Asesinato | ⚔ Ataque | Vanguardia | Venenos por **acumulación**: llena las barras de veneno y sangrado hasta que revientan |
| Sutileza | ✦ Soporte | Vanguardia | **Golpea desde las sombras y ciega.** *Polvo Cegador* hace que el enemigo pegue más flojo 5 rondas; *Vals de Penumbra* esquiva el golpe avisado y *Contraataque* castiga (D-72) |
| Forajido | ✦ Soporte | Vanguardia | **Dados del Destino para el grupo**: tira un 🎲 nativo de Telegram en el chat y el resultado decide qué bonificación recibe todo el grupo durante 3 rondas (crítico, iniciativa, Aguante o botín extra). *Distracción* le baja la precisión a un enemigo 2 rondas y *Robar* le quita un efecto beneficioso. Azar visible y divertido |

**Respuestas al aviso:** esquivar con *Evasión* · bloquear magia con *Capote Negro* · interrumpir con *Patada*.
**Aporte de grupo:** **Veneno Debilitante** (el objetivo pega menos). **Secretos del Oficio** (pasa amenaza al tanque).

### Sacerdote · Tela · Maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Sombra | ⚔ Ataque | Retaguardia | Daño en el tiempo y Locura. La Forma del Vacío sube su Corrupción: riesgo a cambio de recompensa |
| Sagrado | ✚ Curación | Retaguardia | Curas masivas. Es el único sanador que puede **estabilizar heridas leves en combate**, con enfriamiento largo (ver [Heridas](../05-salud/heridas.md)) |
| Disciplina | ✦ Soporte | Retaguardia | **Previene el daño.** Escudos de luz que absorben el golpe avisado, *Sanar* de apoyo y *Remordimiento*, que hace que el enemigo pegue más flojo (D-76) |

**Respuestas al aviso:** bloquear con *Verbo Protector* (sobre sí o sobre un aliado) · esquivar con *Desvanecerse* (*Cuerpo de Humo* en Sombra) · interrumpir con *Silencio*.
**Aporte de grupo:** **Palabra de Poder: Entereza** (+vida máxima del grupo).

### Caballero de la Muerte · Placas · Runas + Poder rúnico
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Escarcha | ⚔ Ataque | Vanguardia | Acumula **Congelación** en el objetivo; al llenarse, el enemigo pierde su siguiente turno |
| Sangre | 🛡 Defensa | Vanguardia | **Cobro de Sangre** cura una parte del daño recibido en las **últimas 2 rondas**: es el tanque que quiere recibir el golpe para devolverlo |
| Profano | ✦ Soporte | Vanguardia | **Plagas que debilitan.** *Peste* baja el daño y la curación del objetivo, y *Brote* la extiende de una vez a toda su fila. Su **Leva de Difuntos** ocupa filas unas rondas y, cada esbirro que cae, suelta una nube de plaga. Hace que el enemigo rinda menos en vez de matarlo antes |

**Respuestas al aviso:** bloquear magia con *Velo Negador* · resistir un golpe físico con *Piel de Témpano* · interrumpir con *Silencio Helado* · mover al enemigo con *Agarre Mortal* (lo trae a la vanguardia).
**Aporte de grupo:** **Zona Antimagia** (menos daño mágico al grupo durante 2 rondas). Resurrección en combate.

### Chamán · Malla · Maná + Vorágine
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Elemental | ⚔ Ataque | Retaguardia | **Sobrecarga**: a veces el hechizo se repite solo. La Vorágine llena vuelve instantáneo y gratis su próximo *Chorro de Magma* |
| Restauración | ✚ Curación | Retaguardia | **Cura Saltarina**, que rebota por la fila; *Tótem de Oleaje*, que cura solo durante unas rondas |
| Tótems | ✦ Soporte | Vanguardia o retaguardia | Planta **tótems** que ocupan un lugar en la fila y actúan solos varias rondas: *Ventarrón* (+iniciativa del grupo), *Granito* (menos daño recibido), *Captura* (atrae el siguiente hechizo enemigo), *Temblor* (quita el miedo y el sueño). Como máximo 2 a la vez, y los enemigos pueden romperlos: hay que elegir dónde plantarlos y cuándo reponerlos. Antes era Mejora |

**Respuestas al aviso:** resistir con *Forma de Ánima* · cambiar de fila con *Andar Etéreo* · interrumpir con *Sacudida de Viento*.
**Aporte de grupo:** Clamor (**Clamor Ancestral**). *Purgar* (le quita un efecto beneficioso al enemigo).

### Mago · Tela · Maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Fuego | ⚔ Ataque | Retaguardia | **Calentamiento**: dos críticos seguidos dan un Estallido Ígneo instantáneo. Ardor Desatado como ráfaga |
| Escarcha | ✦ Soporte | Vanguardia | **Control con hielo.** *Escarcha Paralizante* hace que el enemigo pegue más flojo 5 rondas; *Escudo de Cellisca* absorbe el golpe avisado y *Picahielos* remata (D-72) |
| Arcano | ✦ Soporte | Retaguardia | **Cargas Arcanas para el grupo.** Las acumula y decide si las quema o se las **pasa a un aliado**: cada carga potencia la siguiente habilidad de ese aliado. *Fuente de Maná* devuelve recurso al grupo. Fuera de combate abre **portales** a asentamientos ya visitados, con las mismas reglas de peso que la Piedra de paso (ver [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md)): un servicio que puede cobrar |

**Respuestas al aviso:** bloquear con *Encierro Helado* (inmune una ronda, enfriamiento largo) · cambiar de fila con *Traslación* · interrumpir con *Contrahechizo*.
**Aporte de grupo:** **Intelecto Arcano** (+maná y poder de hechizo del grupo). Clamor (**Tiempo Torcido**). **Mesa de Conjuración**: comida y agua que cuentan para el Sustento (ver [Condiciones](../05-salud/condiciones.md)).

### Brujo · Tela · Maná + Fragmentos de alma
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Destrucción | ⚔ Ataque | Retaguardia | Guarda fragmentos para el **Bólido Infernal**, de crítico garantizado |
| Demonología | 🛡 Defensa | Retaguardia (el demonio, en vanguardia) | **Un demonio guardián tanquea.** Ocupa la vanguardia, provoca y recibe los golpes. Con *Vínculo Demoníaco*, el daño que recibe el demonio se reparte con el brujo, y los fragmentos de alma lo curan o lo potencian. *Sacrificio* lo hace estallar para darle al brujo un escudo grande cuando todo va mal, a cambio de 2 rondas sin tanque hasta invocarlo otra vez |
| Aflicción | ✦ Soporte | Retaguardia | **Maldiciones que debilitan.** Una maldición por enemigo y varias activas a la vez: *Enclenque* (pega menos), *Lenguas* (pierde iniciativa), *Agonía* (se cura menos). El valor está en lo que el enemigo deja de hacer. *Sorbo de Alma* lo sostiene y remata |

**Respuestas al aviso:** resistir con *Terquedad Oscura* · cambiar de fila con *Círculo de Regreso* (vuelve al punto que marcó) · interrumpir con *Bloqueo de Hechizo* (lo hace su demonio).
**Aporte de grupo:** **Piedra de Salud** (una curación de un uso para cada miembro). **Piedra de Alma** (resurrección). **Ritual de Invocación** (trae a un compañero al asentamiento).

### Monje · Cuero · Chi + Energía/Maná
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Viajero del Viento | ⚔ Ataque | Vanguardia | **Golpes en combo**: bonificación si nunca repite la misma habilidad dos rondas seguidas (⚔️ Atacar cuenta como una más) |
| Maestro Cervecero | 🛡 Defensa | Vanguardia | **Tambaleo**: el daño recibido **se reparte en las 3 rondas siguientes** y se puede purgar. Un tanque pensado de verdad para turnos |
| Tejedor de Niebla | ✚ Curación | Retaguardia | Curas **canalizadas**: cada ronda seguida que mantiene la misma, cura más; si lo interrumpen o cambia de acción, se corta. También cura al pegar |

**Respuestas al aviso:** esquivar con *Rodar* (también cambia de fila) · desviar con *Karma Instantáneo* · interrumpir con *Golpe a la Garganta*.
**Aporte de grupo:** **Palma Quebrantadora** (el objetivo recibe más daño físico). **Parálisis**.

### Druida · Cuero · según la forma
El único con los 4 roles, como en WoW.

| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Feral | ⚔ Ataque | Vanguardia | Sangrados y combos. **Acecho** para abrir desde sigilo |
| Guardián | 🛡 Defensa | Vanguardia | Forma de oso con Ira. **Lamerse las Heridas** convierte ira en vida |
| Restauración | ✚ Curación | Retaguardia | **Curas en el tiempo** que actúan cada ronda: el sanador que planifica por adelantado |
| Equilibrio | ✦ Soporte | Retaguardia | **Eclipse que potencia al grupo.** Alterna solar y lunar cada 3 hechizos: el Eclipse Solar sube el daño de los aliados de su fila y el Lunar alarga sus controles. *Maraña de Raíces* impide cambiar de fila y *Ciclón* saca a un enemigo de la pelea una ronda. Hay que planificar el ciclo con la fase del jefe |

**Respuestas al aviso:** resistir con *Piel de Roble* · cambiar de fila con *Salto de Ciervo* · interrumpir con *Golpe de Cráneo* (*Rayo Solar* a distancia).
**Aporte de grupo:** **Marca de lo Salvaje** (+estadísticas). **Renacer** (resurrección en combate).

### Cazador de Demonios · Cuero · Furia
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Estrago | ⚔ Ataque | Vanguardia | **Brinco de Azufre**: cambia de fila y golpea en la misma elección; si lo usa en la ronda del golpe avisado, además lo esquiva. Metamorfosis como ráfaga |
| Venganza | 🛡 Defensa | Vanguardia | **Glifos** que se activan con una ronda de retraso en la fila elegida: el tanque que predice |
| Devorador | ✦ Soporte | Retaguardia | **Reparte el poder de las almas.** Consume las almas de los enemigos caídos (fragmentos de alma) y las **entrega** a sus aliados: a quien la recibe, cada alma le da recurso, más daño o un escudo pequeño. Usa Intelecto, y el Vacío sube su Corrupción |

**Respuestas al aviso:** esquivar con *Desenfoque* · cambiar de fila con *Retirada Vil* (salta a la retaguardia) · interrumpir con *Alteración*.
**Aporte de grupo:** **Estigma Infernal** (el objetivo recibe más daño mágico). **Visión Espectral** (revela lo invisible y lo que está en sigilo).

### Evocador · Malla · Esencia
| Spec | Rol | Fila | Firma en turnos |
|---|---|---|---|
| Devastación | ⚔ Ataque | Retaguardia | Hechizos **Potenciados** de 1 a 3 rondas de carga |
| Preservación | ✚ Curación | Retaguardia | **Eco** duplica la próxima cura, y **Rebobinar** devuelve al grupo parte del daño recibido en las últimas 2 rondas. Magia del tiempo hecha para turnos |
| Aumentación | ✦ Soporte | Retaguardia | **Potencia a un aliado** directamente: *Fuerza Prestada* le presta una parte de sus estadísticas y *Corazonada* le asegura el crítico de su siguiente golpe. Sigue la regla de familias: no se suma con otra potenciación sobre el mismo aliado (ver [Balance](balance.md)) |

**Respuestas al aviso:** resistir con *Escamas de Basalto* · cambiar de fila con *Planear* · interrumpir con *Sofocar*.
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
- **Qué cambió respecto a WoW:** pasan a Defensa Cazador Bestias, Pícaro Sutileza, Mago Escarcha y Brujo Demonología; pasan a Soporte Cazador Supervivencia, Pícaro Forajido, Sacerdote Disciplina, Caballero Profano, Mago Arcano, Brujo Aflicción, Druida Equilibrio y Cazador de Demonios Devorador. Son nuevas el Señor de la Guerra (Furia se queda con el Rompecorazas de Armas) y Tótems (antes Mejora).

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

Las secciones de arriba son el diseño completo. En la versión jugable, cada una de las 45 especializaciones tiene **8 habilidades**: las 3 de siempre y 5 nuevas inspiradas en las habilidades emblemáticas de esa especialización en World of Warcraft (las del Nigromante y el Bardo, clases propias, siguen la misma idea). La idea viene de WoW, pero **el nombre es propio** (D-135; tabla de cambios en §8). Cada especialización conserva su rol (D-72) y cada clase sigue cubriendo al menos dos roles.

**Desbloqueo** (puntos de talento en esa especialización; ver [Talentos](talentos.md) §5):

| Habilidad | 1.ª | 2.ª | 3.ª | 4.ª | 5.ª | 6.ª | 7.ª | 8.ª |
|---|---|---|---|---|---|---|---|---|
| Puntos | 1 | 3 | 6 | 10 | 16 | 24 | 34 | 46 |
| Nivel, con todo en una sola | 2 | 4 | 7 | 11 | 17 | 25 | 35 | 47 |

**La barra sigue siendo de 6 botones (D-46):** ⚔️ Atacar, 3 habilidades, 🎒 Mochila y 🏃 Huir (o 🌀 Esquivar). Las 3 habilidades se eligen en 🌟 Talentos → 🎛️ Barra de combate:
- **Casilla 1:** una respuesta al aviso (🛡 bloquear, 💨 esquivar o 🫧 escudo), elegida entre las que abriste.
- **Casillas 2 y 3:** cualquier otra habilidad que abriste, de cualquier especialización de tu clase.
- **Si no eliges,** la barra se arma sola: tu respuesta más nueva, tu golpe más nuevo y tu otra habilidad más nueva.

**Números bajos al inicio.** Las primeras habilidades tienen valores modestos (las mejoras de daño de las 3 primeras bajaron de 60 % a 50 %) y las nuevas se mueven en el mismo rango: golpes de ×1 a ×2,8 el ataque, mejoras de daño de 30 a 35 %, debilitamientos de 25 a 50 % (los más altos duran solo 2 o 3 rondas), curas de 20 a 45 % de la vida. Las tardías son un poco más fuertes, pero con más costo o más rondas de espera. Hay dos piezas nuevas en el combate: habilidades que **dan recurso** (como *Acero Sediento*, +15 de Ira) y golpes que **suman combos** (como *Mutilar*, +2), para que Pícaro, Druida Feral y Bardo Duelista armen sus remates como en WoW.

**Las 45 especializaciones:**

| Especialización | Rol | 1 a 3 (1, 3 y 6 puntos) | 4 a 8 (10, 16, 24, 34 y 46 puntos) |
|---|---|---|---|
| 💢 Guerrero · Furia | ⚔ Ataque | Rompecorazas, Tajo Final, Parada | Acero Sediento, Espejo de Acero, A Tumba Abierta, Aliento de Rabia, Vendaval de Tajos |
| 🏰 Guerrero · Protección | 🛡 Defensa | Golpe valeroso, Bloqueo con escudo, Segundo aliento | Golpe con Escudo, Bramido Desalentador, Venganza, Baluarte Cerrado, Todavía en Pie |
| 🚩 Guerrero · Señor de la Guerra | ✦ Soporte | Estandarte de Guerra, Estandarte de Muralla, Interponerse | Arenga de Guerra, Hacha Voladora, Tajo Funesto, Llamada a Filas, Alarido de Espanto |
| ⚖️ Paladín · Reprensión | ⚔ Ataque | Juicio, Condena Radiante, Amparo Celestial | Filo Justiciero, Aliento de Fe, Furor Sagrado, Rastro de Brasas, Fallo Inapelable |
| 🔰 Paladín · Protección | 🛡 Defensa | Escudo Acallador, Gracia Protectora, Aura de Constancia | Suelo Ungido, Égida Firme, Llama Tenaz, Centinela de Antaño, Milagro a Tiempo |
| 🌅 Paladín · Sagrado | ✚ Curación | Fulgor Sanador, Candil del Alba, Amparo Celestial | Luz Delatora, Claridad Sanadora, Carga Compartida, Amanecer Tibio, Vitral Radiante |
| 🎯 Cazador · Puntería | ⚔ Ataque | Apuntar, Disparo Certero, Salto Atrás | Flecha Rúnica, Flecha Mordaza, Pellejo Duro, Ráfaga de Flechas, Tiro de Remate |
| 🐺 Cazador · Bestias | ✦ Soporte | Zarpazo a la Orden, Concha Cerrada, Presa Marcada | Flecha Dentada, Intimidación, Rabia de Manada, Euforia, Aullido de la Jauría |
| 🪤 Cazador · Supervivencia | ✦ Soporte | Charco de Brea, Ojo del Rastreador, Señuelo | Bomba Incendiaria, Bozal, Lanzada Feroz, Cepo de Escarcha, Caza en Pareja |
| 🐍 Pícaro · Asesinato | ⚔ Ataque | Eviscerar, Evasión, Patada | Mutilar, Garrote, Tónico de Bolsillo, Señal Fatal, Envenenar |
| 🌑 Pícaro · Sutileza | ✦ Soporte | Vals de Penumbra, Contraataque, Polvo Cegador | Codazo Bajo, Amago, Ceguera, Marcas del Verdugo, Truco del Gremio |
| 🏴‍☠️ Pícaro · Forajido | ✦ Soporte | Dados del Destino, Distracción, Capote Negro | Disparo de Pistola, Dedo en el Ojo, Riposte, Puñal de Niebla, Juerga de Puñales |
| 👁️ Sacerdote · Sombra | ⚔ Ataque | Beso Vampírico, Suplicio Mental, Cuerpo de Humo | Susurro Doliente, Silencio, Hambre Negra, Chillido Mental, Susurro Final |
| 😇 Sacerdote · Sagrado | ✚ Curación | Súplica Curativa, Bálsamo Lento, Verbo Protector | Remedio Rápido, Voz de Reproche, Oración Viajera, Abrigo del Alma, Voz de Calma |
| 📿 Sacerdote · Disciplina | ✦ Soporte | Sanar, Escudo de luz, Remordimiento | Llama Expiatoria, Dolor Adormecido, Fervor Compartido, Verbo Radiante, Fisura del Alma |
| 🧊 Caballero de la Muerte · Escarcha | ⚔ Ataque | Filo Gélido, Silencio Helado, Piel de Témpano | Lamento del Norte, Corazón de Hielo, Arrasar, Frío de Tumba, Rugido Glacial |
| 🫀 Caballero de la Muerte · Sangre | 🛡 Defensa | Cobro de Sangre, Coraza Osaria, Fiebre Carmesí | Tajo al Tuétano, Sangre Tozuda, Hoja Espectral, Tierra Podrida, Brindis de Sangre |
| ☣️ Caballero de la Muerte · Profano | ✦ Soporte | Peste, Leva de Difuntos, Velo Negador | Dardo Funesto, Garfio Sombrío, Gul Enfurecido, Brote, Apocalipsis |
| 🌩️ Chamán · Elemental | ⚔ Ataque | Chorro de Magma, Ascua Persistente, Andar Etéreo | Centella, Ráfaga Cortante, Tormenta Guardada, Puño de Roca, Elemental de Fuego |
| 🌊 Chamán · Restauración | ✚ Curación | Cura Saltarina, Tótem de Oleaje, Forma de Ánima | Rocío Sanador, Escarcha Mordaz, Coraza de Barro, Torrente Vital, Ascensión |
| 🗿 Chamán · Tótems | ✦ Soporte | Tótem de Ventarrón, Tótem de Granito, Tótem de Captura | Mazazo de Trueno, Tótem de Chispas, Tótem de Manantial, Puño de Brasa, Jauría Espiritual |
| ☄️ Mago · Fuego | ⚔ Ataque | Estallido Ígneo, Ardor Desatado, Encierro Helado | Fogonazo, Contrahechizo, Bomba de Relojería, Cortina de Fuego, Meteorito |
| 🌨️ Mago · Escarcha | ✦ Soporte | Escudo de Cellisca, Picahielos, Escarcha Paralizante | Estallido Helado, Pulso Helado, Ventisca, Bola de Nieve, Estaca de Hielo |
| 💠 Mago · Arcano | ✦ Soporte | Desborde Arcano, Ralentizar, Cúpula Irisada | Chispas Errantes, Supernova, Reflejo Burlón, Sello del Erudito, Aguacero Arcano |
| 🌋 Brujo · Destrucción | ⚔ Ataque | Bólido Infernal, Inmolar, Terquedad Oscura | Incinerar, Lazo de Pavor, Avivar Llamas, Trato Sombrío, Coloso de Azufre |
| 👹 Brujo · Demonología | 🛡 Defensa | Hachazo Demoníaco, Vínculo Demoníaco, Sacrificio | Dardo de Azufre, Sacudida Umbría, Escamas de Diablo, Sanguijuela Sombría, Señor de Diablillos |
| 🕸️ Brujo · Aflicción | ✦ Soporte | Maldición Enclenque, Sorbo de Alma, Círculo de Regreso | Corrupción, Miedo, Atormentar, Alma Rancia, Delirio Maldito |
| 🌪️ Monje · Viajero del Viento | ⚔ Ataque | Patada Ascendente, Palma Quebrantadora, Rodar | Palmada Rápida, Golpe a la Garganta, Lluvia de Puños, Ecos del Puño, Punto Final |
| 🍺 Monje · Maestro Cervecero | 🛡 Defensa | Barrilazo, Karma Instantáneo, Trago Limpio | Eructo Ardiente, Zancadilla, Cerveza de Nubes, Tonel Reventón, Embestida del Buey |
| 🌫️ Monje · Tejedor de Niebla | ✚ Curación | Manto de Bruma, Soplo Vital, Crisálida | Parálisis, Bruma Fresca, Té Bien Cargado, Don de las Nubes, Revivir |
| 🐆 Druida · Feral | ⚔ Ataque | Dentellada Final, Desgarrar, Piel de Roble | Triturar, Testarazo, Arrebato Felino, Lomo Erizado, Zarpazo Salvaje |
| 🐻 Druida · Guardián | 🛡 Defensa | Destrozar, Pelambre Espesa, Lamerse las Heridas | Vapulear, Bramido de Oso, Magullar, Despertar del Oso, Oso Ancestral |
| 🌸 Druida · Restauración | ✚ Curación | Savia Nueva, Hoja Curativa, Abrazo del Roble | Quemadura Lunar, Retoño, Flor Paciente, Maleza Sanadora, Calma del Bosque |
| 🦇 Cazador de demonios · Estrago | ⚔ Ataque | Desgarro Infernal, Metamorfosis, Brinco de Azufre | Dentellada Oscura, Disrupción, Desdibujar, Mirada Ardiente, Presa Sin Escape |
| 👺 Cazador de demonios · Venganza | 🛡 Defensa | Glifo de Llamas, Piel Espinosa, Glifo de Angustia | Cizallar, Glifo Mudo, Partealmas, Hierro al Rojo, Aliento de Azufre |
| 🕳️ Cazador de demonios · Devorador | ✦ Soporte | Entregar Alma, Estigma Infernal, Escudo de Almas | Consumir, Haz del Abismo, Paso Entre Mundos, Banquete de Almas, Sol Hundido |
| 🐲 Evocador · Devastación | ⚔ Ataque | Aliento de Fuego, Desintegrar, Planear | Llama Hambrienta, Sofocar, Cólera de Escamas, Astro Quebrado, Marea de Siglos |
| ⏳ Evocador · Preservación | ✚ Curación | Eco, Rebobinar, Escamas de Basalto | Pétalo Sanador, Instante Eterno, Suspiro del Sueño, Grieta del Tiempo, Floración Tardía |
| 🔆 Evocador · Aumentación | ✦ Soporte | Fuerza Prestada, Corazonada, Atajo del Tiempo | Erupción, Tiempo Torcido, Escamas Hirvientes, Tierra Rebelde, Bocanada Eterna |
| 🪦 Nigromante · Plaga | ⚔ Ataque | Plaga Reptante, Estallido Pútrido, Forma Espectral | Toque de Putrefacción, Enjambre de Moscas, Contagio, Ola de Pestilencia, Epidemia |
| 🧟 Nigromante · Legión | 🛡 Defensa | Hueso Protector, Levantar Esqueletos, Grito del Sepulcro | Golpe de Hueso, Muro de Cadáveres, Coloso de Huesos, Festín de Cadáveres, Legión Inmortal |
| 🧛 Nigromante · Drenaje | ✚ Curación | Sifón Vital, Pacto de Sangre, Velo de Almas | Mano de la Tumba, Marchitar, Transfusión, Cosecha Vital, Guadaña de Almas |
| 🤺 Bardo · Duelista | ⚔ Ataque | Floritura Final, Estocada Rítmica, Paso de Baile | Estocada Doble, Contrapunto, Finta, Crescendo, Gran Final |
| 🎶 Bardo · Trovador | ✚ Curación | Balada Curativa, Nota Curativa, Nota Sostenida | Canción de Cuna, Copla del Mañana, Acorde Disonante, Coro Celestial, Réquiem de Vida |
| 🥁 Bardo · Estratega | ✦ Soporte | Allegro, Contratiempo, Calderón | Staccato, Síncopa, Compás de Espera, Fortissimo, Sinfonía de Guerra |

Datos: `content/classes.yaml` (habilidades y números), `content/locales/es_clases.yaml` (nombres), `content/balance.yaml` (`talents`). Balance medido con `tools/sim.py`.

Ver P-12, P-14, P-67 y P-68 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md). La barra de 6 está decidida (D-46) y el reparto de roles responde a D-50.

## 8. Nombres propios: qué nombres cambiaron (D-135)

**De dónde sale.** El dueño decidió que el mundo use **nombres propios y originales, no los de World of Warcraft** (D-135, entrevista E-19). La revisión del cuestionario de beta (C-150) encontró que muchas habilidades usaban la traducción oficial de WoW (*Sed de Sangre*, *Temeridad*, *Imposición de Manos*, *Toque de la Muerte*…). Se cambió **solo el nombre que ve el jugador**: los IDs (`sed_de_sangre`, `temeridad`…), los números y lo que hace cada habilidad siguen igual, así que nada guardado se rompe.

**Cómo se eligieron.**
- **Se cambia** todo nombre que copia uno de WoW, en inglés o en español, o lo traduce palabra por palabra, y las palabras raras que solo se entienden como traducción de WoW (*Temeridad*, *Vivificar*, *Presciencia*, *Penitencia*).
- **Se queda** la palabra común que cualquier juego usaría para esa acción, aunque WoW también la use: *Parada*, *Patada*, *Evasión*, *Juicio*, *Apuntar*, *Señuelo*, *Silencio*, *Miedo*, *Peste*, *Ventisca*, *Meteorito*, *Contrahechizo*, *Bola de fuego*, *Eviscerar*, *Mutilar*, *Drenar*… También se quedan *Bloqueo con escudo*, *Segundo aliento*, *Aliento de Fuego*, *Elemental de Fuego* y *Disparo de Pistola*, que son descripciones.
- **El nombre nuevo** dice lo mismo que hace la habilidad, cabe en un botón (2 o 3 palabras) y sigue el tono del mundo, oscuro pero con esperanza y algo de humor (D-161): *A Tumba Abierta*, *Milagro a Tiempo*, *Eructo Ardiente*, *Candil del Alba*. Lo demoníaco huele a **azufre** (antes era "vil", la palabra de WoW). No repite otro nombre del juego.
- **Clases, especializaciones y recursos no cambiaron.** Algunos son propios de WoW (*Caballero de la Muerte*, *Cazador de demonios*, *Evocador*, *Viajero del Viento*, *Maestro Cervecero*, *Tejedor de Niebla*, *Reprensión*, *Vorágine*, *Poder Astral*…), pero las 15 clases las confirmó el dueño (D-151): cambiarlos es pregunta para él.
- **Lo que todavía no está en el juego** (§1 a §6: *Zurrar*, *Reprimenda*, *Desvanecerse*, *Agarre Mortal*, *Traslación*, *Retirada Vil*, *Forma del Vacío*, las maldiciones *Lenguas* y *Agonía*…) conserva su nombre de diseño. Cada uno se renombra con esta misma regla cuando entre al juego.

<details>
<summary>Tabla completa: antes → ahora, por especialización (⚔️ = ataque básico)</summary>

| Especialización | Antes → ahora |
|---|---|
| 💢 Guerrero · Furia | Golpe Colosal → Rompecorazas · Ejecutar → Tajo Final · Sed de Sangre → Acero Sediento · Reflejo de Hechizos → Espejo de Acero · Temeridad → A Tumba Abierta · Regeneración Enfurecida → Aliento de Rabia · Desenfreno → Vendaval de Tajos |
| 🏰 Guerrero · Protección | Golpe heroico → Golpe valeroso · Grito Desmoralizador → Bramido Desalentador · Muro de Escudo → Baluarte Cerrado · Última Resistencia → Todavía en Pie |
| 🚩 Guerrero · Señor de la Guerra | Intervenir → Interponerse · Grito de Batalla → Arenga de Guerra · Lanzamiento Heroico → Hacha Voladora · Golpe Mortal → Tajo Funesto · Grito de Reunión → Llamada a Filas · Grito Intimidador → Alarido de Espanto |
| ⚖️ Paladín · Reprensión | ⚔️ Golpe de cruzado → Mandoble justo · Veredicto del Templario → Condena Radiante · Escudo Divino → Amparo Celestial · Hoja de Justicia → Filo Justiciero · Palabra de Gloria → Aliento de Fe · Cólera Vengativa → Furor Sagrado · Estela de Cenizas → Rastro de Brasas · Sentencia de Ejecución → Fallo Inapelable |
| 🔰 Paladín · Protección | ⚔️ Martillo del justo → Martillazo firme · Escudo del Vengador → Escudo Acallador · Bendición de Protección → Gracia Protectora · Aura de Devoción → Aura de Constancia · Consagración → Suelo Ungido · Escudo de los Justos → Égida Firme · Defensor Ardiente → Llama Tenaz · Guardián de los Reyes Ancestrales → Centinela de Antaño · Imposición de Manos → Milagro a Tiempo |
| 🌅 Paladín · Sagrado | ⚔️ Choque sagrado → Golpe de alba · Destello de Luz → Fulgor Sanador · Faro de Luz → Candil del Alba · Escudo Divino → Amparo Celestial · Juicio de Luz → Luz Delatora · Luz Sagrada → Claridad Sanadora · Bendición de Sacrificio → Carga Compartida · Luz del Alba → Amanecer Tibio · Prisma Sagrado → Vitral Radiante |
| 🎯 Cazador · Puntería | ⚔️ Disparo firme → Tiro sereno · Destrabarse → Salto Atrás · Disparo Arcano → Flecha Rúnica · Disparo de Contención → Flecha Mordaza · Supervivencia del Más Apto → Pellejo Duro · Fuego Rápido → Ráfaga de Flechas · Disparo Mortal → Tiro de Remate |
| 🐺 Cazador · Bestias | ⚔️ Disparo de cobra → Flecha rápida · Orden de Matar → Zarpazo a la Orden · Aspecto de la Tortuga → Concha Cerrada · Disparo de Púas → Flecha Dentada · Cólera de las Bestias → Rabia de Manada · Llamada de lo Salvaje → Aullido de la Jauría |
| 🪤 Cazador · Supervivencia | Trampa de Alquitrán → Charco de Brea · Marca del Cazador → Ojo del Rastreador · Bomba de Fuego Salvaje → Bomba Incendiaria · Golpe de Raptor → Lanzada Feroz · Trampa Congelante → Cepo de Escarcha · Asalto Coordinado → Caza en Pareja |
| 🐍 Pícaro · Asesinato | Vial Carmesí → Tónico de Bolsillo · Marca de la Muerte → Señal Fatal |
| 🌑 Pícaro · Sutileza | Danza de las Sombras → Vals de Penumbra · Golpe en los Riñones → Codazo Bajo · Símbolos de Muerte → Marcas del Verdugo · Técnica Secreta → Truco del Gremio |
| 🏴‍☠️ Pícaro · Forajido | ⚔️ Golpe siniestro → Navajazo · Capa de Sombras → Capote Negro · Gubia → Dedo en el Ojo · Golpe Fantasmal → Puñal de Niebla · Ola de Asesinatos → Juerga de Puñales |
| 👁️ Sacerdote · Sombra | ⚔️ Explosión mental → Punzada mental · Toque Vampírico → Beso Vampírico · Tortura Mental → Suplicio Mental · Dispersión → Cuerpo de Humo · Palabra de las Sombras: Dolor → Susurro Doliente · Peste Devoradora → Hambre Negra · Alarido Psíquico → Chillido Mental · Palabra de las Sombras: Muerte → Susurro Final |
| 😇 Sacerdote · Sagrado | ⚔️ Fuego sagrado → Lumbre bendita · Plegaria de Sanación → Súplica Curativa · Renovar → Bálsamo Lento · Palabra de Poder: Escudo → Verbo Protector · Sanación Relámpago → Remedio Rápido · Palabra Sagrada: Castigo → Voz de Reproche · Rezo de Alivio → Oración Viajera · Espíritu Guardián → Abrigo del Alma · Palabra Sagrada: Serenidad → Voz de Calma |
| 📿 Sacerdote · Disciplina | Penitencia → Remordimiento · Purgar al Malvado → Llama Expiatoria · Supresión de Dolor → Dolor Adormecido · Infusión de Poder → Fervor Compartido · Palabra de Poder: Resplandor → Verbo Radiante · Cisma → Fisura del Alma |
| 🧊 Caballero de la Muerte · Escarcha | Golpe de Escarcha → Filo Gélido · Helada Mental → Silencio Helado · Entereza Ligada al Hielo → Piel de Témpano · Explosión Aullante → Lamento del Norte · Pilar de Escarcha → Corazón de Hielo · Invierno Despiadado → Frío de Tumba · Furia del Vermis de Escarcha → Rugido Glacial |
| 🫀 Caballero de la Muerte · Sangre | ⚔️ Golpe de corazón → Tajo carmesí · Golpe de Muerte → Cobro de Sangre · Escudo de Huesos → Coraza Osaria · Hervor de Sangre → Fiebre Carmesí · Desgarro de Médula → Tajo al Tuétano · Sangre Vampírica → Sangre Tozuda · Arma de Runas Danzante → Hoja Espectral · Muerte y Descomposición → Tierra Podrida · Bebesangre → Brindis de Sangre |
| ☣️ Caballero de la Muerte · Profano | ⚔️ Golpe de plaga → Mordida pútrida · Ejército de los muertos → Leva de Difuntos · Caparazón Antimagia → Velo Negador · Espiral de la Muerte → Dardo Funesto · Atracción Letal → Garfio Sombrío · Transformación Oscura → Gul Enfurecido |
| 🌩️ Chamán · Elemental | ⚔️ Descarga de rayo → Chispazo · Descarga de Lava → Chorro de Magma · Choque de Llamas → Ascua Persistente · Paso Espiritual → Andar Etéreo · Descarga de Relámpagos → Centella · Corte de Viento → Ráfaga Cortante · Guardián de Tormentas → Tormenta Guardada · Choque de Tierra → Puño de Roca |
| 🌊 Chamán · Restauración | ⚔️ Choque de tierra → Salpicón · Sanación en Cadena → Cura Saltarina · Tótem de Marea → Tótem de Oleaje · Cambio Astral → Forma de Ánima · Mareas Vivas → Rocío Sanador · Choque de Escarcha → Escarcha Mordaz · Escudo de Tierra → Coraza de Barro · Ola de Sanación → Torrente Vital |
| 🗿 Chamán · Tótems | ⚔️ Golpe de tormenta → Golpe de chubasco · Tótem Viento Furioso → Tótem de Ventarrón · Tótem Piel de Piedra → Tótem de Granito · Golpe de Tormenta → Mazazo de Trueno · Tótem de Condensador → Tótem de Chispas · Tótem de Corriente Sanadora → Tótem de Manantial · Latigazo de Lava → Puño de Brasa · Espíritu Feral → Jauría Espiritual |
| ☄️ Mago · Fuego | Piroexplosión → Estallido Ígneo · Combustión → Ardor Desatado · Bloque de Hielo → Encierro Helado · Explosión de Fuego → Fogonazo · Bomba Viviente → Bomba de Relojería · Barrera Ardiente → Cortina de Fuego |
| 🌨️ Mago · Escarcha | ⚔️ Descarga de escarcha → Dardo de hielo · Barrera de Hielo → Escudo de Cellisca · Lanza de Hielo → Picahielos · Nova de Escarcha → Estallido Helado · Venas Heladas → Pulso Helado · Orbe Congelado → Bola de Nieve · Púa Glacial → Estaca de Hielo |
| 💠 Mago · Arcano | ⚔️ Misil arcano → Chispa arcana · Poder Arcano → Desborde Arcano · Barrera Prismática → Cúpula Irisada · Misiles Arcanos → Chispas Errantes · Imagen Reflejada → Reflejo Burlón · Toque del Magi → Sello del Erudito · Tromba Arcana → Aguacero Arcano |
| 🌋 Brujo · Destrucción | Descarga del Caos → Bólido Infernal · Resolución Inagotable → Terquedad Oscura · Espiral Mortal → Lazo de Pavor · Conflagrar → Avivar Llamas · Pacto Oscuro → Trato Sombrío · Invocar Infernal → Coloso de Azufre |
| 👹 Brujo · Demonología | ⚔️ Descarga de sombras → Dardo umbrío · Hachazo Vil → Hachazo Demoníaco · Descarga Demoníaca → Dardo de Azufre · Furia de las Sombras → Sacudida Umbría · Armadura Demoníaca → Escamas de Diablo · Drenar Vida → Sanguijuela Sombría · Tirano Demoníaco → Señor de Diablillos |
| 🕸️ Brujo · Aflicción | Maldición de Debilidad → Maldición Enclenque · Drenar Alma → Sorbo de Alma · Círculo Demoníaco → Círculo de Regreso · Putrefacción de Alma → Alma Rancia · Éxtasis Maléfico → Delirio Maldito |
| 🌪️ Monje · Viajero del Viento | ⚔️ Palma del tigre → Palmada rápida · Patada del Sol Naciente → Patada Ascendente · Palma Mística → Palma Quebrantadora · Palma del Tigre → Palmada Rápida · Golpe de Mano de Lanza → Golpe a la Garganta · Puños de Furia → Lluvia de Puños · Tormenta, Tierra y Fuego → Ecos del Puño · Toque de la Muerte → Punto Final |
| 🍺 Monje · Maestro Cervecero | ⚔️ Palma del tigre → Palmada rápida · Golpe de Barril → Barrilazo · Toque de Karma → Karma Instantáneo · Brebaje Purificador → Trago Limpio · Soplo de Fuego → Eructo Ardiente · Barrido de Pierna → Zancadilla · Brebaje Celestial → Cerveza de Nubes · Barril Explosivo → Tonel Reventón · Invocar a Niuzao → Embestida del Buey |
| 🌫️ Monje · Tejedor de Niebla | Niebla Envolvente → Manto de Bruma · Vivificar → Soplo Vital · Capullo de Vida → Crisálida · Niebla Renovadora → Bruma Fresca · Té de Enfoque Atronador → Té Bien Cargado · Regalo de Sheilun → Don de las Nubes |
| 🐆 Druida · Feral | Mordedura Feroz → Dentellada Final · Piel de Corteza → Piel de Roble · Furia del Tigre → Arrebato Felino · Instintos de Supervivencia → Lomo Erizado · Ira Primigenia → Zarpazo Salvaje |
| 🐻 Druida · Guardián | Pelaje de Hierro → Pelambre Espesa · Regeneración Frenética → Lamerse las Heridas · Rugido Incapacitador → Bramido de Oso · Furia del Durmiente → Despertar del Oso · Encarnación de Ursoc → Oso Ancestral |
| 🌸 Druida · Restauración | Rejuvenecimiento → Savia Nueva · Alivio Presto → Hoja Curativa · Corteza de Hierro → Abrazo del Roble · Fuego Lunar → Quemadura Lunar · Recrecimiento → Retoño · Flor de Vida → Flor Paciente · Crecimiento Salvaje → Maleza Sanadora · Tranquilidad → Calma del Bosque |
| 🌿 Druida · Equilibrio | ⚔️ Fuego estelar → Lumbre estelar · Raíces Enredadoras → Maraña de Raíces · Carrerilla Salvaje → Salto de Ciervo |
| 🦇 Cazador de demonios · Estrago | ⚔️ Mordisco del demonio → Garra de azufre · Golpe del Caos → Desgarro Infernal · Salto Vil → Brinco de Azufre · Mordisco Demoníaco → Dentellada Oscura · Rayo Ocular → Mirada Ardiente · La Cacería → Presa Sin Escape |
| 👺 Cazador de demonios · Venganza | Sigilo de Llamas → Glifo de Llamas · Púas Demoníacas → Piel Espinosa · Sigilo de Miseria → Glifo de Angustia · Sigilo de Silencio → Glifo Mudo · Hendidura de Alma → Partealmas · Marca Ígnea → Hierro al Rojo · Devastación Vil → Aliento de Azufre |
| 🕳️ Cazador de demonios · Devorador | ⚔️ Rayo del vacío → Destello del abismo · Marca del Caos → Estigma Infernal · Rayo del Vacío → Haz del Abismo · Cambio de Fase → Paso Entre Mundos · Cosecha de Almas → Banquete de Almas · Estrella Colapsante → Sol Hundido |
| 🐲 Evocador · Devastación | ⚔️ Llama viva → Llama hambrienta · Llama Viva → Llama Hambrienta · Furia Dragontina → Cólera de Escamas · Estrella Destrozadora → Astro Quebrado · Oleada de Eternidad → Marea de Siglos |
| ⏳ Evocador · Preservación | ⚔️ Llama viva → Llama hambrienta · Escamas Obsidianas → Escamas de Basalto · Flor Esmeralda → Pétalo Sanador · Dilatación Temporal → Instante Eterno · Aliento Onírico → Suspiro del Sueño · Anomalía Temporal → Grieta del Tiempo · Flor Espiritual → Floración Tardía |
| 🔆 Evocador · Aumentación | Poder de Ébano → Fuerza Prestada · Presciencia → Corazonada · Salto Temporal → Atajo del Tiempo · Distorsión Temporal → Tiempo Torcido · Escamas Abrasadoras → Escamas Hirvientes · Sublevación → Tierra Rebelde · Aliento de Eones → Bocanada Eterna |
| 🧛 Nigromante · Drenaje | Segador de Almas → Guadaña de Almas |
| 🎶 Bardo · Trovador | Himno de Esperanza → Copla del Mañana |

</details>

Datos: `content/locales/es.yaml` y `content/locales/es_clases.yaml` (`ability.<id>.name` y `class.<id>.attack_name`).
