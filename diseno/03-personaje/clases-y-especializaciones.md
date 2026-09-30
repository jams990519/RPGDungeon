# Clases y especializaciones

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Balance](balance.md) · **Alimenta a:** [Combate](../04-combate/README.md), [Talentos](talentos.md) · **Estado:** propuesta

**De dónde sale.** Las 13 clases y 40 especializaciones de *World of Warcraft* a septiembre de 2026 (expansión *Midnight*, con la tercera spec del Cazador de Demonios, **Devorador**, ya en vivo). Se suman dos clases propias que WoW nunca tuvo y que un juego por turnos pide: **Nigromante** y **Bardo**. De *Albion Online* se toma la idea de que **el equipo aporta habilidades**.

Total: **15 clases y 46 especializaciones**. La clase se elige al nivel 10; antes, el héroe es un aventurero sin clase con un kit básico.

---

## 1. Recursos: cada clase conserva su sabor

Cada clase mantiene su recurso de WoW, adaptado a rondas. Además, **todas** comparten dos barras (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)): **Aguante** (para reacciones como esquivar o bloquear) y **Firmeza** (resistencia al control).

| Recurso | Clases | Cómo funciona en turnos |
|---|---|---|
| **Ira** | Guerrero, Druida (oso) | Se gana al pegar y al recibir golpes, y decae fuera de combate. Máximo 100 |
| **Energía + Combos** | Pícaro, Druida (felino) | La energía sube 25 por ronda. Los golpes generan combos (hasta 5) y los remates los gastan |
| **Maná** | Magos, sanadores, Chamán, Druida (lechuza) | Reserva grande con regeneración pequeña por ronda. Meditar (una acción) recupera más |
| **Runas + Poder rúnico** | Caballero de la Muerte | 6 runas, se regeneran 2 por ronda. Las habilidades gastan runas y generan poder rúnico |
| **Foco** | Cazador | Sube 20 por ronda. Esperar una ronda apuntando acumula foco extra |
| **Poder Sagrado** | Paladín | De 0 a 5, con generadores y consumidores |
| **Fragmentos de alma** | Brujo, Cazador de Demonios (Devorador) | De 0 a 5. Se generan con ciertas habilidades o cuando mueren enemigos |
| **Chi** | Monje | De 0 a 5, más energía (Viajero del Viento, Cervecero) o maná (Tejedor de Niebla) |
| **Furia** | Cazador de Demonios | Se gana con los golpes y no decae en combate |
| **Esencia** | Evocador | De 0 a 5, recupera 1 cada 2 rondas. Los hechizos **Potenciados** se cargan 1, 2 o 3 rondas: más carga da más poder y más riesgo de que te interrumpan |
| **Vorágine** | Chamán (Elemental, Mejora) | Se acumula; al llenarse, el siguiente hechizo sale gratis e instantáneo |
| **Poder Astral + Eclipse** | Druida (Equilibrio) | Cada 3 hechizos alterna entre Eclipse Solar y Lunar, que potencian ramas distintas |
| **Locura** | Sacerdote (Sombra) | Se acumula; al llenarse entra en Forma del Vacío, que también sube su **Corrupción** (ver [Mente](../05-salud/mente.md)) |
| **Cargas Arcanas** | Mago (Arcano) | De 0 a 4. Cada carga sube el daño y el costo de maná: el mago decide cuándo quemar y cuándo conservar |
| **Almas cosechadas** | Nigromante | Se ganan cuando muere cualquier criatura cerca y alimentan esbirros y curas oscuras |
| **Compás** | Bardo | La canción sostenida ocupa la acción rápida de cada ronda; cambiar de canción rompe el compás. Encadenar compases sube el **Crescendo** |

## 2. Las 15 clases

Leyenda de roles: 🛡 Tanque · ✚ Sanador · ⚔ Daño cuerpo a cuerpo · 🏹 Daño a distancia · ✦ Apoyo.

La columna "Firma" es la mecánica que hace que esa spec **se juegue distinto en turnos**, no solo que tenga otros números. Los "aportes de grupo" siguen las reglas de [Balance](balance.md): tienen valor parecido entre sí y dos iguales no se suman.

### Guerrero · Placas · Ira
| Spec | Rol | Firma en turnos |
|---|---|---|
| Armas | ⚔ | **Golpe Colosal** abre una ventana de 2 rondas en la que el objetivo recibe más daño. Todo el juego es preparar y aprovechar esa ventana. Ejecuta por debajo del 20 % de vida |
| Furia | ⚔ | Doble empuñadura. Al critar entra en **Enfurecido** y, mientras dure, gana una acción rápida extra por ronda |
| Protección | 🛡 | **Bloqueo con escudo** como reacción: anula los golpes físicos que se ven venir. Es el tanque que lee el aviso |

Aporte de grupo: **Grito de Batalla** (+poder de ataque del grupo).

### Paladín · Placas · Poder Sagrado + maná
| Spec | Rol | Firma en turnos |
|---|---|---|
| Sagrado | ✚ | **Faro de Luz**: parte de lo que cura se copia en un aliado marcado. Cura desde la vanguardia |
| Protección | 🛡 | **Escudo del Vengador**, que rebota entre enemigos y silencia; auras que protegen a su fila |
| Reprensión | ⚔ | Construye y gasta Poder Sagrado. **Juicio** marca al enemigo para que reciba más daño sagrado |

Aporte: **Bendición** (mitigación del grupo). Resurrección en combate.

### Cazador · Malla · Foco
| Spec | Rol | Firma en turnos |
|---|---|---|
| Bestias | 🏹 | La **mascota es una segunda unidad** en el campo, con iniciativa propia: puede provocar, flanquear o proteger |
| Puntería | 🏹 | **Apuntar** (esperar una ronda) garantiza el impacto en la parte del cuerpo elegida. La mejor spec para romper partes de jefes |
| Supervivencia | ⚔ | Pone **trampas** en las filas enemigas que se activan en rondas siguientes; usa bombas |

Aporte: **Marca del Cazador** (revela debilidades y sube el crítico del grupo contra ese objetivo). Clamor.

### Pícaro · Cuero · Energía + Combos
| Spec | Rol | Firma en turnos |
|---|---|---|
| Asesinato | ⚔ | Venenos por **acumulación**: llena las barras de veneno y sangrado hasta que revientan |
| Forajido | ⚔ | **Dados del Destino**: tira un 🎲 nativo de Telegram en el chat y el resultado decide su bonificación durante 4 rondas. Azar visible y divertido |
| Sutileza | ⚔ | **Danza de las Sombras**: entra en sigilo entre rondas y encadena golpes a partes del cuerpo (a la cabeza, para aturdir) |

Aporte: **Veneno Debilitante** (el objetivo pega menos). **Secretos del Oficio** (pasa amenaza al tanque).

### Sacerdote · Tela · Maná
| Spec | Rol | Firma en turnos |
|---|---|---|
| Disciplina | ✚ | **Cura haciendo daño** (Expiación) y pone **escudos preventivos**: premia adivinar el siguiente golpe del jefe leyendo el aviso |
| Sagrado | ✚ | Curas masivas. Es el único sanador que puede **estabilizar heridas leves en combate**, con enfriamiento largo (ver [Heridas](../05-salud/heridas.md)) |
| Sombra | 🏹 | Daño en el tiempo y Locura. La Forma del Vacío sube su Corrupción: riesgo a cambio de recompensa |

Aporte: **Palabra de Poder: Entereza** (+vida máxima del grupo). **Infusión de Poder** (potencia a un aliado).

### Caballero de la Muerte · Placas · Runas + Poder rúnico
| Spec | Rol | Firma en turnos |
|---|---|---|
| Sangre | 🛡 | **Golpe de Muerte** cura una parte del daño recibido en las **últimas 2 rondas**: es el tanque que quiere recibir el golpe para devolverlo |
| Escarcha | ⚔ | Acumula **Congelación** en el objetivo; al llenarse, el enemigo pierde su siguiente turno |
| Profano | ⚔ | **Ejército de los muertos** y plagas de combate. Sus esbirros ocupan filas |

Aporte: **Zona Antimagia** (menos daño mágico al grupo durante 2 rondas). Resurrección en combate.

### Chamán · Malla · Maná + Vorágine
| Spec | Rol | Firma en turnos |
|---|---|---|
| Elemental | 🏹 | Planta **tótems** que actúan solos durante varias rondas. Con **Sobrecarga**, a veces el hechizo se repite |
| Mejora | ⚔ | Armas imbuidas; la Vorágine acumulada vuelve instantáneo su próximo hechizo |
| Restauración | ✚ | **Sanación en Cadena**, que rebota por la fila; tótems de curación |

Aporte: Clamor (**Clamor Ancestral**). Tótems de utilidad.

### Mago · Tela · Maná
| Spec | Rol | Firma en turnos |
|---|---|---|
| Arcano | 🏹 | Cargas Arcanas: ciclos de quemar y conservar maná. El que mejor planifica una pelea larga |
| Fuego | 🏹 | **Calentamiento**: dos críticos seguidos dan una Piroexplosión instantánea. Combustión como ráfaga |
| Escarcha | 🏹 | Control: **congela** filas. Con Dedos de Escarcha, el siguiente golpe cuenta como si el objetivo estuviera congelado |

Aporte: **Intelecto Arcano** (+maná y poder de hechizo del grupo). Clamor (**Distorsión Temporal**). **Mesa de Conjuración**: comida y agua que cuentan para el Sustento (ver [Condiciones](../05-salud/condiciones.md)).

### Brujo · Tela · Maná + Fragmentos de alma
| Spec | Rol | Firma en turnos |
|---|---|---|
| Aflicción | 🏹 | Mantiene varias maldiciones activas en varios objetivos y remata con **Drenar Alma** |
| Demonología | 🏹 | Invoca demonios que **actúan en la cola de iniciativa** unas rondas. Su poder está en sincronizarlos |
| Destrucción | 🏹 | Guarda fragmentos para la **Descarga del Caos**, de crítico garantizado |

Aporte: **Piedra de Salud** (una curación de un uso para cada miembro). **Piedra de Alma** (resurrección). **Ritual de Invocación** (trae a un compañero al asentamiento).

### Monje · Cuero · Chi + Energía/Maná
| Spec | Rol | Firma en turnos |
|---|---|---|
| Maestro Cervecero | 🛡 | **Tambaleo**: el daño recibido **se reparte en las 3 rondas siguientes** y se puede purgar. Un tanque pensado de verdad para turnos |
| Tejedor de Niebla | ✚ | Curas **canalizadas** que siguen si nadie lo interrumpe; también cura al pegar |
| Viajero del Viento | ⚔ | **Golpes en combo**: bonificación si nunca repite la misma habilidad dos rondas seguidas |

Aporte: **Palma Mística** (el objetivo recibe más daño físico). **Parálisis**.

### Druida · Cuero · según la forma
| Spec | Rol | Firma en turnos |
|---|---|---|
| Equilibrio | 🏹 | **Eclipse**: alterna solar y lunar cada 3 hechizos; hay que planificar el ciclo con la fase del jefe |
| Feral | ⚔ | Sangrados y combos. **Acecho** para abrir desde sigilo |
| Guardián | 🛡 | Forma de oso con Ira. **Regeneración Frenética** convierte ira en vida |
| Restauración | ✚ | **Curas en el tiempo** que actúan cada ronda: el sanador que planifica por adelantado |

Aporte: **Marca de lo Salvaje** (+estadísticas). **Renacer** (resurrección en combate).

### Cazador de Demonios · Cuero · Furia
| Spec | Rol | Firma en turnos |
|---|---|---|
| Estrago | ⚔ | **Salto Vil**: cambia de fila gratis y esquiva. Metamorfosis como ráfaga |
| Venganza | 🛡 | **Sigilos** que se activan con una ronda de retraso en la fila elegida: el tanque que predice |
| Devorador | 🏹 | Media distancia, con Intelecto. **Consume almas** de enemigos caídos para potenciarse |

Aporte: **Marca del Caos** (el objetivo recibe más daño mágico). **Visión Espectral** (revela lo invisible y lo que está en sigilo).

### Evocador · Malla · Esencia
| Spec | Rol | Firma en turnos |
|---|---|---|
| Devastación | 🏹 | Hechizos **Potenciados** de 1 a 3 rondas de carga |
| Preservación | ✚ | **Eco** duplica la próxima cura, y **Rebobinar** devuelve al grupo parte del daño recibido en las últimas 2 rondas. Magia del tiempo hecha para turnos |
| Aumentación | ✦ | Potencia a los aliados. **Sus efectos no se suman con los de otro apoyo**, y en contenido clasificado solo puede haber uno por grupo |

Aporte: Clamor (**Furia del Vuelo**).

### Nigromante · Tela · Almas cosechadas *(clase propia)*
| Spec | Rol | Firma en turnos |
|---|---|---|
| Legión | 🏹 | Levanta esqueletos que ocupan la vanguardia y se sacrifican: explotan o bloquean un golpe |
| Plaga | 🏹 | Enfermedades de combate que **saltan** de un enemigo a otro por fila |
| Drenaje | ✚ | **Sanador oscuro**: cura a los aliados con la vida que le quita a los enemigos, o pagando con la propia |

Aporte: **Cosecha** (cuando muere un enemigo, el grupo recupera un poco de recurso). Resurrección en combate. Fuera de combate: **Remiendo**, el único que cura heridas a los Renacidos sin médico.

### Bardo · Cuero · Compás *(clase propia)*
| Spec | Rol | Firma en turnos |
|---|---|---|
| Trovador | ✚ | **Baladas** sostenidas: cura a todo el grupo cada ronda mientras mantiene la canción |
| Estratega | ✦ | El único que **mueve la cola de iniciativa**: *Allegro* adelanta a un aliado y *Contratiempo* retrasa a un enemigo. Diseñado para turnos. No se suma con Aumentación |
| Duelista | ⚔ | **Danza de espadas**: combos que salen al pulsar los botones en la secuencia correcta, como un ritmo |

Aporte: **Himno de Valor**. Clamor. Fuera de combate **baja el estrés** del grupo y de los clientes de la taberna (ver [Mente](../05-salud/mente.md)). Origen: el Animador de *Star Wars Galaxies*, que curaba el cansancio de batalla tocando en la cantina.

## 3. Recuento de roles

| Rol | Cuántas | Specs |
|---|---|---|
| 🛡 Tanque | 6 | Guerrero Protección, Paladín Protección, Caballero Sangre, Monje Cervecero, Druida Guardián, Cazador de Demonios Venganza |
| ✚ Sanador | 9 | Paladín Sagrado, Sacerdote Disciplina, Sacerdote Sagrado, Chamán Restauración, Monje Tejedor, Druida Restauración, Evocador Preservación, Nigromante Drenaje, Bardo Trovador |
| ✦ Apoyo | 2 | Evocador Aumentación, Bardo Estratega |
| ⚔/🏹 Daño | 29 | Todas las demás |

## 4. La barra de 8: clase + equipo (el híbrido WoW + Albion)

**De dónde sale.** En *Albion Online* no hay clases: el arma que empuñas da tus habilidades principales y cada pieza de armadura da una más (el pecho, un defensivo; las botas, una de movimiento; el casco, una de utilidad). En WoW la clase decide todo.

**Cómo queda.** En combate, cada héroe tiene **8 botones**:

| Botones | De dónde vienen |
|---|---|
| Atacar · Defender | Siempre presentes |
| 4 habilidades de clase | Elegidas del repertorio de tu spec (tu configuración) |
| 1 técnica de **arma** | Según el tipo de arma: la espada larga da *Tajo Circular*, la lanza *Estocada Profunda*, el escudo torre *Muro* |
| 1 técnica de **armadura** | Según la pieza de pecho o las botas: *Carga* (botas de placas), *Capa de Humo* (pecho de cuero), *Barrera Rúnica* (túnica) |

Más un menú secundario sin límite: Objetos, Apuntar, Fila/Formación, Registro. La lista de técnicas está en [Equipamiento](equipamiento.md).

**Por qué conviene.**
- La clase conserva su identidad (WoW).
- Dentro de la misma spec hay variedad real según el arma y la armadura (Albion).
- **El equipo importa por lo que hace, no solo por sus números.** Eso le da demanda a cada tipo de arma y armadura que fabrican los artesanos, y hace que perder equipo en una zona negra duela y se pueda reemplazar.

## 5. Orden de lanzamiento: la historia de WoW como calendario

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

Cada clase nueva llega con su evento, su zona de inicio especial y una cadena de historia. Ver [Hoja de ruta](../00-vision/hoja-de-ruta.md).

Ver P-12, P-13 y P-14 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
