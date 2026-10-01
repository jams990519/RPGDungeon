# Supervivencia del asentamiento: construir no alcanza

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Fundación y cisma](fundacion-y-cisma.md) (el Claro, los campamentos y sus etapas), [Sistema de construcción](../09-construccion/sistema-de-construccion.md), [Defensa y protecciones](../09-construccion/defensa-y-protecciones.md) · **Se conecta con:** [Ciudades y el Castillo](ciudades-y-castillo.md), [Crisis](crisis-problemas-y-soluciones.md), [Geografía y recursos](geografia-y-recursos.md), [Mundo vivo](mundo-vivo-y-viaje.md) (estaciones, noche, ecología), [Enfermedades](../05-salud/enfermedades.md), [Condiciones](../05-salud/condiciones.md), [Mente](../05-salud/mente.md), [Curación](../05-salud/curacion-y-tratamientos.md), [Peligros del entorno](../05-salud/peligros-del-entorno.md), [Animales y cultivos](../05-salud/animales-y-cultivos.md), [Cacerías](../06-contenido/cacerias.md), [Bestiario](../06-contenido/bestiario.md), [Crimen y justicia](../06-contenido/crimen-y-justicia.md), [Eventos](../06-contenido/eventos.md), [Profesiones](../07-economia/profesiones.md), [Red de sistemas](../00-vision/red-de-sistemas.md) · **Estado:** §0 está en el juego: la obra y los campamentos desde la 0.9.2 y **la despensa (§0.4)** como primera parte de esta propuesta (D-93, provisional); todo lo demás es propuesta (capa profunda)

**Qué pidió el dueño.** Que crear el castillo sea difícil de verdad: que haya que **mantener una cantidad de comida**, **mantener sana a la población**, **progresar en conjunto** y **defenderse de enemigos y bestias**. Que no sea "vamos a construir y ya".

**Cómo leer este documento.** Hasta campamento, subir de etapa es **pagar materiales** (§0). El dueño aceptó por voz que, desde aldea, subir pida algo más (D-93, provisional), y se programa por partes (§16): **la primera, la despensa, ya está en el juego (§0.4)**. Lo demás (población, salud, ánimo, amenaza, incursiones, rachas) es la **capa profunda** que se sumaría encima, primero en el Claro y después, más liviana, en los campamentos de jugadores; todavía no está programado.

**Palabras.** Aquí "ciudad" o "asentamiento" quiere decir el Claro o un campamento de jugadores. Las etapas son las del juego: **fogata, campamento, aldea, pueblo, ciudad y castillo**. Los documentos viejos decían "Claro" para la primera etapa y "Villa" para la cuarta.

---

## 0. Lo que ya existe (en el juego)

### 0.1 La obra común del Claro

- Todo el servidor aporta materiales a una sola obra. Cuando se completa la lista de la etapa, el Claro sube para todos: fogata → campamento → aldea → pueblo → ciudad → castillo (`settlement.stages`).
- Cada material da 2 de experiencia y 1 de mérito. La obra muestra a los 5 que más aportaron.
- Cada etapa abarata la posada y suma 1 zona al territorio del Claro (D-81).
- El Claro nunca baja de etapa.
- El detalle y los números están en [Fundación y cisma](fundacion-y-cisma.md) §1.

### 0.2 Los campamentos de jugadores

- Se fundan lejos del Claro con 20 de madera y 10 de piedra, en una zona explorada al 100 % (D-71, D-87).
- Tienen nombre único y miembros que acepta el fundador: 2 al nivel 1 y 2 más por nivel (D-84).
- Crecen cuando un miembro paga 15 de madera, 10 de piedra y 5 de fibra por el nivel actual y elige qué zona vecina toman; desde el nivel 6 también paga 🪎 cofres: 1 de 6 a 7, 2 de 7 a 8 y 3 de 8 a 9 (D-92, provisional). Cambian de nombre en los niveles 3, 5, 7 y 9: aldea, pueblo, ciudad y castillo (D-81, D-87).
- En su territorio nadie es atacado y sus miembros recolectan un 50 % más.
- Hoy no tienen servicios, ni almacén, ni obra común propia. El detalle está en [Fundación y cisma](fundacion-y-cisma.md) §2.

### 0.3 Lo que falta para "construir no alcanza"

Hoy no hay población, salud pública, amenaza ni incursiones. La comida llegó con la despensa (§0.4), en su capa simple. Todo lo de abajo es la propuesta para que, además de pagar, haya que **sostener**.

### 0.4 La despensa (en el juego, D-93 provisional)

La primera parte de este documento: la **capa simple** de §3.1, §3.2, §4.2 y §7. Sin aldeanos, sin medidores de salud ni ánimo, sin rachas y sin incursiones.

**La comida.**
- 🍖 **Carne** (vale 2 raciones): la sueltan las **bestias** al perder (lobos, jabalíes, ratas, osos, arañas, escorpiones, tortugas, víboras, mantis y caimanes), con un 40 a 60 % de probabilidad, 1 o 2 piezas. Los humanoides, los no muertos, los hongos y los limos no sueltan carne. Es un material: el mercader la compra barata (1 🥉).
- 🥖 **Provisiones** (vale 1 ración): las vende el mercader del Claro a **15 🥉**, a propósito caras: es la salida de emergencia y un sumidero de monedas (§15.8). El mercader no las vuelve a comprar. Todavía no tienen tope por semana.
- Una **ración** es lo que come un residente en un día real. Ningún recurso nuevo aparece en las zonas: la comida sale de las peleas y del mercader.

**Quién come.**
- Cada **residente activo** come **1 ración por día real**. Activo es quien tocó un botón en las **últimas 24 horas**: quien no juega no come y no arrastra a nadie (§15.3).
- **Residentes del Claro:** los jugadores activos que no son miembros de un campamento, más los miembros de campamentos que **aportaron al Claro** (materiales o comida) en esas mismas 24 horas. Es la regla de §7.1, con "ese día" en lugar de "esa semana".
- **Residentes de un campamento:** sus miembros activos.
- El consumo se cuenta al mirar la despensa, como los recursos que vuelven en las zonas: no hace falta un reloj que corra para todos.

**Dónde está y cómo se llena.**

| Lugar | Desde | Dónde se ve | Cómo se llena |
|---|---|---|---|
| **El Claro** | Aldea (hasta campamento, subir sigue siendo solo pagar) | Una línea en 🏕️ Campamento y el detalle en 🔥 Obra del campamento | **🌾 Aportar comida** en la obra: pasa toda la comida de la mochila a la despensa |
| **Un campamento de jugadores** | Nivel 3 (aldea) | La pantalla del campamento, para sus miembros | **🌾 Aportar comida** estando en el campamento |

- Cada ración aportada da **2 de experiencia y 1 de mérito**, como la obra común. En el Claro, el mérito suma al ranking de la obra.
- La despensa nunca toma comida de la mochila de nadie: solo entra lo que cada uno aporta.

**Estados** (días que alcanza la comida con los residentes activos de hoy):

| Días | Estado | Qué pasa hoy |
|---|---|---|
| 14 o más | 🟢 Abundancia | Nada especial todavía |
| 7 a 13 | 🟢 Holgada | Normal |
| 3 a 6 | 🟡 Justa | Normal (el aviso es el estado mismo) |
| 1 a 2 | 🟠 Escasez | Normal |
| 0 (menos de 1 día) | 🔴 Hambruna | En el Claro, **la posada no cura** (avisa por qué y no cobra) y **la obra no sube**. En un campamento, **no puede crecer** hasta llenarla |

**Subir de etapa en el Claro.** Desde aldea, además de la obra pagada, la despensa tiene que alcanzar unos días: **4 para pasar a pueblo, 5 para pasar a ciudad y 7 para pasar a castillo** (`pantry.min_days_to_rise`). Son los números de "Despensa sostenida" de §7.1 corridos una etapa, porque la despensa recién se abre en aldea. Si la obra está completa y faltan días, **la etapa espera**: la obra muestra cuántos faltan y el Claro **sube solo** en el próximo aporte de comida o de materiales que lo deje en el mínimo. Todavía no hay racha (§7.1, punto 2) ni Noche de prueba (punto 3).

**Lo que nunca pasa** (§11, §15): el Claro nunca baja de etapa y un campamento nunca pierde niveles, zonas ni miembros por hambre. Al llegar la despensa, el Claro (si ya era aldea o más) y cada campamento de nivel 3 o más empezaron con **7 días de comida para todos los que podrían comer de ella** (todos los héroes sin campamento, o todos los miembros), para que nadie empiece castigado. Lo mismo vale cuando un asentamiento llega por primera vez a aldea.

**Los números** están en `content/balance.yaml` (`pantry`), la comida en `content/items.yaml` (`food`) y la carne en el botín de `content/enemies.yaml`. Son orientativos y se ajustan en la beta. Pruebas: `tests/test_pantry.py`.

## De dónde sale

- *Frostpunk*: la **esperanza** y el **descontento** como medidores de la ciudad; las **raciones**; el **libro de leyes**, donde cada ley resuelve un problema y crea otro.
- *Banished*: la **despensa** que hay que llenar en otoño para pasar el invierno, la **hambruna**, las enfermedades por falta de higiene y una población que **crece o muere** según cómo la cuides.
- *RimWorld*: las **incursiones crecen con la riqueza** de la colonia.
- *They Are Billions*: el **ruido** de los edificios atrae a las hordas.
- *Valheim*: el **progreso** atrae ataques a la base.
- *Dwarf Fortress*: los **asedios** llegan atraídos por la riqueza.
- *Northgard*: los **inviernos** bajan la producción y suben el consumo.
- *Don't Starve Together*: las **estaciones** cambian todo.
- *Anno*: las **necesidades suben con el nivel de la población**.
- *Ashes of Creation*: los nodos que crecen con la actividad de los jugadores.

**La regla (propuesta).** Terminar una obra no sube la etapa. La sube una ciudad que **come, está sana, está a salvo y trabaja junta** durante días seguidos. Construir es la mitad del trabajo; **sostener** es la otra mitad.

**Dónde se aplicaría.**

| Lugar | Capa | Desde qué etapa | Por qué |
|---|---|---|---|
| **El Claro** | Completa: todo este documento | Al subir a aldea. Hasta campamento sigue siendo solo pagar, para que el tutorial no se trabe | Es la obra de todo el servidor: tiene la gente para sostenerla |
| **Campamentos de jugadores** | Ligera (§7.2): despensa chica, incursiones a la medida de sus miembros, una Noche de prueba antes de castillo | Desde aldea (nivel 3) | Tienen pocos miembros (de 6 a 18). No pueden cargar con los mínimos del Claro |

## 1. El bucle de la ciudad

```
PRODUCIR ──> GUARDAR ──> CONSUMIR ──> CRECER ──> ATRAER AMENAZA ──> DEFENDER
(campos,     (graneros,  (residentes, (más gente, (riqueza, ruido,    (murallas,
 caza,        conservas)  aldeanos,    más obras)  noche, ecología)    guardias,
 pesca)                   obreros)                                     rondas)
   ^                                                                      |
   └──── la salud, el ánimo y el orden deciden cuánto rinde todo ─────────┘
```

Cada **día de juego** (6 horas reales; ver [Mundo vivo](mundo-vivo-y-viaje.md)) la ciudad hace su **cuenta**: come, gasta, se ensucia, se enferma o se cura, y la amenaza sube. El resultado se ve en `/ciudad` y se resume una vez por día real.

Las ocho necesidades de [Fundación y cisma](fundacion-y-cisma.md) §3 siguen igual. Cinco se vuelven **medidores con umbrales** (§3): comida, salud, ánimo, defensa y orden. Las otras tres (materiales, herramientas y tesoro) alimentan las obras y el mantenimiento (§8). Los materiales ya existen: son los 6 recursos que hoy se recolectan (D-87).

**Amplio pero ligero** (D-44). **Capa simple:** el jugador ve los cinco medidores en `/ciudad` y toca **📋 Aportar**, igual que hoy toca 🤲 Aportar en la obra común. **Capa profunda:** aldeanos, raciones, leyes y defensa por tramos, para el gobierno y para quien quiera meterse.

## 2. La población

### 2.1 Quién vive en la ciudad

| Habitante | Quién es | Cuenta para la etapa | Come (raciones por día real) | Qué aporta |
|---|---|---|---|---|
| 🧑 **Residente jugador** | Es miembro del campamento (en el Claro, ver quién cuenta en §7.1) o tiene casa o paga posada, y entró al juego en los últimos 7 días | Sí | 1, solo los días en que juega | Todo: oficios, obras, defensa, votos |
| 🧑‍🌾 **Aldeano PNJ** | Llega solo si hay vivienda y comida (§2.2) | Sí | 1 | Trabajo básico (§2.3) |
| 💂 **Guardia PNJ** | Contratado con oro y equipado con equipo real (ver [Defensa](../09-construccion/defensa-y-protecciones.md)) | Sí | 1,5 | Defensa y orden |
| 🤕 **Enfermo** (PNJ) | Un aldeano o guardia en cama | Sí | 1,25 (caldos) | Nada mientras está enfermo |
| 🎒 **Refugiado** | Llega por una crisis (ver [Crisis](crisis-problemas-y-soluciones.md)) y se acepta o no (§10) | Solo si consigue vivienda | 1 | Se vuelve aldeano si se queda |
| 🧳 **Visitante** | Jugador que pasa por la ciudad sin vivir en ella | No | 0 | Comercio |

- **Un residente que deja de jugar no perjudica a nadie.** El día que no entra, no come de la despensa. Pasados 7 días sin entrar, deja de contar como población. Cuando vuelve, vuelve a contar. Su casa y sus cosas siguen intactas.
- **El comedor común.** Mientras la despensa no esté en hambruna, el residente **al día** con su cuota (§9.2) que entra a la ciudad recupera su Sustento hasta *Normal* sin gastar su comida (ver [Condiciones](../05-salud/condiciones.md)). Los demás también comen ahí, pagando un plato barato; los novatos hasta el nivel 10 comen gratis siempre. Los platos de cocinero siguen dando sus bonos aparte. La ciudad **nunca toma comida del inventario personal** de nadie.
- **El ganado** come forraje, no raciones, y tiene su propia salud (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md)).

### 2.2 Cómo llegan y cómo se van los aldeanos

| Llegan si… (cada día real) | Se van si… |
|---|---|
| Hay **vivienda libre** (cabañas comunes, barracones, cuartos de la posada) | La despensa está en **hambruna**: se va 1 de cada 10 por día |
| La despensa tiene **7 días o más** | La salud pública baja de **30**: se va 1 de cada 20 por día |
| La salud pública y el ánimo están en **50 o más** | El ánimo baja de **30**: se va 1 de cada 20 por día |
| La seguridad no está en *Vulnerable* | Hubo una **brecha** en una incursión: se va 1 de cada 10 de golpe |
| Llega cada día **1 por cada 5 camas libres** (mínimo 1), el doble durante un festival o si la Gaceta habla bien de la ciudad. Así lo que frena a la población es la vivienda, la comida y la salud, no la espera | Hay **hacinamiento** de más del 20 %: se van los que sobran |

- Los aldeanos pueden **morir** en una brecha o en un brote grave. Es una pérdida de la ciudad, no de ningún jugador: queda en el cementerio y en la historia del lugar, y baja el ánimo.
- Los PNJ del Claro (hoy, el viejo mercader y quien cuida la posada; como propuesta, también una sanadora y una cazadora) son los primeros aldeanos y **nunca se van**.

### 2.3 Qué hacen los aldeanos

Los aldeanos hacen el trabajo básico, **despacio y sin calidad**. Nunca reemplazan a un jugador con oficio.

| Trabajo | Qué hace | Rinde |
|---|---|---|
| **Campesino** | Cuida los campos comunes y el huerto | 1,5 raciones por día (fuera del invierno) |
| **Aguador** | Saca agua, la hierve, cuida el pozo | Suma a la cobertura de agua limpia |
| **Barrendero** | Limpia calles, letrinas y el estercolero | Sube la higiene |
| **Leñador** | Junta leña para el fogón y el invierno | 3 de leña por día |
| **Peón de obra** | Acarrea y cimenta en las obras | Un cuarto de jornada de Peón por día (nunca etapas de Albañil o más) |
| **Vigía** | Mira desde la empalizada | Aviso de incursión (más corto que una torre de vigía) |
| **Ayudante de enfermería** | Cuida a los enfermos | Suma un poco al control de un brote |

- **Tope:** los aldeanos nunca producen más del **35 %** de la comida que la ciudad necesita, ni más del **20 %** de las jornadas de una obra. El resto lo ponen los jugadores.
- **Quién los reparte:** antes del Pueblo, la asamblea de residentes (votación con una encuesta de Telegram); desde el Pueblo, el Maestro de Obras mayor y el gobernador (ver [Fundación y cisma](fundacion-y-cisma.md)).
- Un aldeano enfermo, hambriento o descontento trabaja la mitad. Uno en huelga no trabaja (§3).

### 2.4 La población decide las necesidades

Como en *Anno*, cada etapa pide más que la anterior. Si falta algo de la lista, el ánimo y la salud bajan cada día hasta que se cubra.

| Etapa | Qué pide la población, además de lo anterior |
|---|---|
| **Campamento** | Comida, agua del pozo, techo, fogón |
| **Aldea** | Comida de **2 grupos** (ver la variedad en [Condiciones](../05-salud/condiciones.md)), letrinas, enfermería, granero |
| **Pueblo** | Comida de **3 grupos**, taberna, templo, muralla, cementerio |
| **Ciudad** | Comida de **4 grupos**, baños y alcantarillado, sanatorio, guardia, mercado abastecido |
| **Castillo** | Comida de **5 grupos**, un festival por estación, academia, agua de cisterna o acueducto |

**Vivienda:** cada cabaña común aloja a 5 aldeanos y cada barracón a 20; la posada aloja residentes. Si hay más habitantes que camas, hay **hacinamiento**: baja la salud y el ánimo por cada 10 % de exceso.

## 3. Los medidores de la ciudad

### 3.1 Qué los mueve

| Medidor | Qué mide | Lo sube | Lo baja |
|---|---|---|---|
| 🌾 **Despensa** | Cuántos días alcanza la comida guardada al consumo actual | Cosechas, caza, pesca, ganado, cocina (estira la comida), conservas, compras a otros castillos | El consumo diario, la comida que se pudre, los robos al granero, las brechas |
| ⚕️ **Salud pública** (0-100) | Lo sana que está la ciudad | Agua limpia, letrinas, baños, cementerio, enfermería con médicos de turno, comida variada, poco hacinamiento | Agua sucia, basura, hacinamiento, cadáveres sin enterrar, comida podrida, ratas, hambre, frío sin leña, brotes |
| 🎶 **Ánimo** (0-100) | La esperanza de la gente | Comida variada, banquetes, bardos y taberna, templo, festivales, defensas ganadas, obras inauguradas, reconocimiento público | Hambre, raciones reducidas, muertes, brechas, jornadas extra, cuarentenas, impuestos de emergencia, hacinamiento, invierno |
| 🛡 **Seguridad** (%) | La defensa de la ciudad comparada con la fuerza de la próxima incursión | Murallas, puertas, torres, trampas, guardias equipados, perros de guardia, braseros y faroles de noche, defensores anotados en turnos | Murallas dañadas, guardias heridos, armas gastadas, noche sin luz, una amenaza que crece más rápido que las defensas |
| ⚖️ **Orden** (0-100) | Cuánto se respetan las reglas | Patrullas de la guardia, juez y tribunal, leyes claras, taberna con licencia, ánimo alto | Hambre, ánimo bajo, hacinamiento, refugiados sin casa, garitos, forajidos cerca (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) |

La **Seguridad** se calcula así: **defensa de la ciudad ÷ fuerza esperada de la próxima incursión**. La defensa suma murallas, torres, trampas, guardias y el promedio de defensores que se presentaron en las últimas tres incursiones.

### 3.2 Qué pasa en cada umbral

**🌾 Despensa**

| Días de comida | Estado | Qué pasa |
|---|---|---|
| 14 o más | 🟢 **Abundancia** | +ánimo cada día; llegan más aldeanos; las obras avanzan un 5 % más (obreros bien comidos) |
| 7 a 13 | 🟢 **Holgada** | Normal |
| 3 a 6 | 🟡 **Justa** | No llegan aldeanos; aviso en el grupo; los pedidos de comida pagan el doble |
| 1 a 2 | 🟠 **Escasez** | −ánimo y −salud cada día; las obras avanzan a la mitad; se puede votar el racionamiento |
| 0 | 🔴 **Hambruna** | Cierra el comedor común; la posada no cura; se van aldeanos; las obras se paran; se declara la crisis de Hambruna (§4.7) |

**⚕️ Salud pública**

| Valor | Estado | Qué pasa |
|---|---|---|
| 80-100 | 🟢 **Sana** | Riesgo de brote mínimo; los residentes ganan un poco de inmunidad extra contra las enfermedades |
| 60-79 | 🟢 **Normal** | Riesgo de brote bajo |
| 40-59 | 🟡 **Frágil** | Riesgo de brote doble; los aldeanos enfermos trabajan la mitad |
| 20-39 | 🟠 **Enferma** | Brote casi seguro; la enfermería se satura; no llegan aldeanos; los residentes pueden contagiarse |
| 0-19 | 🔴 **Epidemia local** | Se van y mueren aldeanos; las obras se paran; la cuarentena se vota sola en el grupo |

**🎶 Ánimo**

| Valor | Estado | Qué pasa |
|---|---|---|
| 80-100 | 🟢 **Esperanzada** | Los aldeanos trabajan un 10 % más; llegan más; baja el estrés de los residentes en la ciudad (ver [Mente](../05-salud/mente.md)) |
| 60-79 | 🟢 **Tranquila** | Normal |
| 40-59 | 🟡 **Inquieta** | Quejas en el grupo; las leyes duras bajan el ánimo el doble |
| 20-39 | 🟠 **Descontenta** | Huelgas: la mitad de los aldeanos no trabaja; −orden cada día |
| 0-19 | 🔴 **Revuelta** | Crisis de Revuelta (ver [Crisis](crisis-problemas-y-soluciones.md)); servicios cerrados; si ya hay gobierno, se abre sola una moción de censura contra el gobernador |

**🛡 Seguridad**

| Valor | Estado | Qué pasa |
|---|---|---|
| 150 % o más | 🟢 **Protegida** | Muchos ataques se rinden antes de llegar: cuentan como defendidos, pero sin botín. La Noche de prueba y los asedios nunca se rinden; +ánimo |
| 100-149 % | 🟢 **Firme** | Normal |
| 70-99 % | 🟡 **Expuesta** | Aviso; la próxima incursión puede abrir brecha |
| Menos de 70 % | 🔴 **Vulnerable** | Brecha probable; no llegan aldeanos; −ánimo cada día |

**⚖️ Orden**

| Valor | Estado | Qué pasa |
|---|---|---|
| 80-100 | 🟢 **Ordenada** | Sin robos; las licencias rinden más |
| 50-79 | 🟢 **Normal** | Normal |
| 30-49 | 🟡 **Revoltosa** | Robos al granero (se pierde el 1 % de la despensa por día); aparecen garitos |
| 10-29 | 🟠 **Desorden** | Contrabando, sabotajes (posible incendio; ver [Crisis](crisis-problemas-y-soluciones.md)), saqueadores PNJ dentro de los muros |
| 0-9 | 🔴 **Anarquía** | La guardia pierde el control; servicios cerrados hasta que se recupere |

**Los medidores se encadenan.** El hambre baja la salud y el ánimo; el ánimo bajo baja el orden; el desorden roba comida. Una ciudad que descuida una cosa termina con tres problemas, como en *Frostpunk*.

## 4. La comida

La unidad es la **ración**: lo que come un habitante en un día real.

### 4.1 Producción

| Fuente | Quién | Rinde (orientativo) | Estación |
|---|---|---|---|
| **Campos comunes** | Agricultores ([Profesiones](../07-economia/profesiones.md)) | 20 a 40 raciones de grano por jornada de campo, según el rango y la tierra | Nada en invierno (salvo invernadero); el triple en la cosecha de otoño |
| **Huertos** | Agricultores, campesinos PNJ | Poco, pero constante | Primavera a otoño |
| **Ganado** | Ganaderos | Leche y huevos cada día; carne al sacrificar | Todo el año, con forraje guardado en invierno |
| **Caza** | Cazadores ([Cacerías](../06-contenido/cacerias.md)) | 10 a 25 raciones de carne por presa | Menos en invierno; depende de la ecología: si se sobrecaza, no hay |
| **Pesca** | Pescadores | 8 a 20 raciones por salida | Menos en invierno (pesca en hielo) |
| **Recolección** | Herboristas | Bayas, hongos, raíces | Primavera y verano |
| **Comercio** | Comerciantes | Lo que se compre a otros nodos o castillos | Todo el año; caravanas expuestas en zonas rojas |
| **Cocina** | Cocineros | **Estira la comida:** 1 ración cruda se vuelve 1,5 en el fogón común; un guiso con 3 grupos de alimentos se vuelve 2 y sube la salud | Todo el año |

La geografía decide qué es fácil y qué hay que comprar: una ciudad en la llanura tiene grano; una en la montaña tiene que comprarlo (ver [Geografía y recursos](geografia-y-recursos.md)).

### 4.2 Consumo

| Quién | Raciones por día real |
|---|---|
| Residente jugador | 1, solo los días en que juega |
| Aldeano PNJ | 1 |
| Guardia PNJ | 1,5 |
| Enfermo en cama | 1,25 |
| Obrero en una jornada de obra | +0,5 por jornada (§8) |
| Cualquier habitante en invierno | +0,2 (el frío da hambre), y además 1 de leña |

### 4.3 Graneros

La comida se guarda en edificios. Lo que no cabe **se pudre en el suelo** al día siguiente. *Desde* es la etapa en la que ya se puede construir.

| Edificio | Desde | Capacidad | Extra |
|---|---|---|---|
| **Almacén del fogón** | Fogata | 200 raciones | Las ratas se llevan un poco cada día |
| **Granero de madera** | Campamento | 1.500 raciones | Con gatos o trampas, sin ratas |
| **Ahumadero y salazón** | Aldea | — | Convierte carne y pescado en conservas (§4.4) |
| **Bodega fría** | Pueblo | 1.000 raciones frescas | La comida fresca dura el doble |
| **Granero de piedra** | Pueblo | 5.000 raciones | Sin ratas; resiste incendios; las brechas se llevan la mitad de lo normal |
| **Silos del Castillo** | Ciudad | 12.000 raciones | Parte de su contenido nunca se puede robar |

Se pueden levantar **varios de cada uno**, cada uno con su obra. Así una ciudad de 500 jugadores en el Claro puede guardar los días de despensa que pide cada etapa (§7.1) con varios almacenes del fogón.

### 4.4 Comida que se echa a perder

| Alimento | Dura fresco | Cómo se conserva | Dura conservado | Quién conserva |
|---|---|---|---|---|
| Carne | 2 días | **Salada** (sal de la costa o del desierto) o **ahumada** (ahumadero y leña) | 20 días salada, 15 ahumada | Cocina |
| Pescado | 1 día | Salado, ahumado o seco | 15 a 20 días | Cocina, Pesca |
| Leche | 1 día | Queso | 30 días | Ganadería, Cocina |
| Frutas y verduras | 4 días | Conservas en vinagre o miel, secado | 40 días en frasco, 20 secas | Cocina (frascos de vidrio de la Joyería) |
| Grano | 60 días | Granero de piedra | 120 días | — |
| Harina | 30 días | — | — | Molino |
| Pan y guisos | 3 días | — | — | Cocina |

- `/ciudad` muestra cuánto se pudrió hoy. Una ciudad que caza mucho y no sala la carne **pierde comida y atrae carroñeros** (§6.1).
- **La sal mueve el comercio:** una ciudad del bosque o de la montaña tiene que comprarla a la costa o al desierto.

### 4.5 Estaciones e inviernos

Cada semana real avanza una estación (ver [Mundo vivo](mundo-vivo-y-viaje.md)). Un año entero dura cuatro semanas reales, así que en la primera temporada llega **por lo menos un invierno**.

| Estación | Producción | Consumo | Qué conviene hacer |
|---|---|---|---|
| 🌱 **Primavera** | Siembra: los campos rinden poco la primera mitad; vuelven las migraciones (más caza) | Normal | Sembrar, reparar lo que rompió el invierno |
| ☀️ **Verano** | Los campos crecen, buena pesca, mucha recolección | Más agua; sube la fiebre del pantano | Ampliar campos, juntar leña |
| 🍂 **Otoño** | **Cosecha grande** (campos ×3), festival de difuntos | Normal | **Llenar los graneros y conservar**: es la semana más importante del año |
| ❄️ **Invierno** | Campos en cero, caza a la mitad, pesca −30 % | +20 % de comida y leña para todos; sube la gripe | Vivir de lo guardado; defenderse de las bestias hambrientas (§6.1) |

**El primer invierno.** El servidor abre a fines del verano, así que el primer invierno llega en la tercera semana, después de un solo otoño para prepararse, cuando la aldea apenas se sostiene. Es la primera gran prueba del servidor, como en *Banished*: quien no guardó en otoño pasa hambre.

### 4.6 Raciones

| Ración | Cuánto se come | Efecto |
|---|---|---|
| **Banquete** | 1,5 | +ánimo, +salud, −estrés de los residentes; gasta mucho |
| **Completa** | 1 | Normal |
| **Reducida** | 0,75 | La despensa dura un tercio más; −ánimo leve cada día |
| **Mínima** | 0,5 | La despensa dura el doble; −ánimo fuerte, −salud, las obras avanzan un 25 % menos |

Cambiar la ración es una decisión de gobierno (§10).

### 4.7 Hambruna

| Momento | Qué pasa |
|---|---|
| **Día 0** | La despensa llega a cero. Cierra el comedor común, la posada deja de curar y el bot avisa en el grupo |
| **Día 1** | Se van aldeanos (1 de cada 10 por día). Las obras se paran. La racha de etapa vuelve a cero (§7). Se publican pedidos de comida con paga triple |
| **Día 2** | −10 de salud y −15 de ánimo por día. Sube el riesgo de brote y de revuelta |
| **Día 3** | Si sigue, se **apagan los servicios** de la etapa (§11). La etapa no se pierde |

La comida personal de los jugadores nunca se toca. La hambruna es de la ciudad.

## 5. Salud pública

### 5.1 Lo que mantiene sana a la ciudad

| Obra o servicio | Desde | Qué cubre | Si falta |
|---|---|---|---|
| **Pozo** | Fogata | Agua limpia para 25 habitantes | Se bebe agua sucia: disentería (ver [Enfermedades](../05-salud/enfermedades.md)) |
| **Cisterna** | Pueblo | Guarda 5 días de agua para la sequía | En la sequía no hay agua (ver [Crisis](crisis-problemas-y-soluciones.md)) |
| **Acueducto** | Ciudad | Agua limpia para toda la ciudad (Ingeniería y Construcción) | Hay que seguir sumando pozos |
| **Letrinas** | Campamento | Higiene para 15 habitantes cada una | −salud, sube el riesgo de brote |
| **Estercolero** | Campamento | Saca la basura de las calles; da **abono** para los campos | Basura, ratas y carroñeros |
| **Alcantarillado** | Pueblo | Higiene para un barrio de 100 | Las letrinas no alcanzan para una ciudad grande |
| **Baños y lavadero** | Pueblo | +salud y +ánimo | La ciudad se ensucia |
| **Cementerio** | Aldea (antes, una fosa fuera del campamento) | Los muertos se entierran lejos del agua | Cadáveres sin enterrar: brote (Podredumbre Gris) y carroñeros que suben la amenaza (§6.1) |
| **Enfermería** | Campamento | Camas para aldeanos enfermos; turnos médicos (§5.3) | Los enfermos contagian en sus casas |
| **Sanatorio** | Pueblo | Diagnóstico exacto, cuarentena, cirugía (ver [Ciudades y el Castillo](ciudades-y-castillo.md)) | Los brotes graves duran mucho más |
| **Lazareto** | Aldea | Aislar enfermos fuera de los muros durante un brote | La cuarentena baja más el ánimo y el comercio |

Además: la **comida variada** sube la salud; el **hacinamiento**, la **comida podrida**, el **frío sin leña** y la **lluvia en el pantano** la bajan (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md)).

### 5.2 Brotes: una carrera entre contagio y control

Cada día de juego hay un **riesgo de brote** que depende de la salud pública, la estación y el terreno. Un brote usa la misma idea que las enfermedades de los jugadores: **una carrera entre dos barras** (ver [Enfermedades](../05-salud/enfermedades.md)).

- **Contagio:** sube solo cada día de juego, más rápido con poca higiene y mucho hacinamiento.
- **Control:** sube con lo que hacen los jugadores.

| Quién ayuda | Cómo sube el control |
|---|---|
| **Médicos y enfermeros** | Diagnostican el brote (sin diagnóstico, los remedios rinden la mitad) y hacen turnos de enfermería |
| **Alquimistas y herboristas** | Fabrican los remedios del brote |
| **Cocineros** | Caldos que suben la inmunidad |
| **Aguadores y constructores** | Hierven el agua, arreglan letrinas, levantan el lazareto |
| **Gobierno** | Declara la cuarentena (§10) |
| **Cazadores** | Eliminan a los animales portadores (ver [Cacerías](../06-contenido/cacerias.md)) |

Si el control llega a 100 primero, el brote termina y la ciudad queda inmune a esa enfermedad un tiempo. Si gana el contagio, los aldeanos se enferman, se van o mueren, y los residentes pueden contagiarse. Siempre con las reglas normales de cada enfermedad: protección de novato hasta el nivel 10 y **nunca la muerte de un personaje** fuera del Juramento de Hierro.

Qué brote toca según el lugar: disentería con agua sucia, Gripe de Escarcha en invierno, Fiebre del Pantano en terreno de pantano, Podredumbre Gris con cadáveres sin enterrar, fiebre del establo si se enferma el ganado (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md)).

### 5.3 El papel de los médicos

- **Turno de enfermería:** un jugador con Medicina trabaja un turno en la enfermería (una acción rápida o un minijuego corto). Cura a varios aldeanos, sube la salud pública y el control del brote, y cobra del tesoro con la garantía del bot. Es la mejor forma de que un **Enfermero** novato suba de rango (ver [Curación](../05-salud/curacion-y-tratamientos.md)).
- **Médico de la ciudad:** desde el Pueblo, el gobernador puede pagar un sueldo semanal a uno o más médicos.
- **Después de cada incursión** hay heridos: los médicos los estabilizan en la misma defensa (§6.5) o los atienden después.

## 6. Amenaza: lo que crece atrae

### 6.1 El medidor de amenaza

La **Amenaza** es una barra de 0 a 100 %. Sube cada día con la **atracción** de la ciudad. Al llegar a 100 %, una incursión sale hacia la ciudad.

| Atrae (puntos por día real, orientativo) | Cuánto |
|---|---|
| **Base de la etapa** | Campamento 10 · Aldea 15 · Pueblo 20 · Ciudad 25 · Castillo 30 |
| **Riqueza** (despensa, almacén común, tesoro, edificios), como en *RimWorld* | +5 por cada escalón: pobre, modesta, próspera, rica, opulenta |
| **Tamaño** | +1 por cada 25 habitantes |
| **Ruido**, como en *They Are Billions* | +2 por cada forja o fundición encendida, +1 por cada 10 jornadas de obra del día, +3 por cada mina activa cerca, +5 por un festival |
| **Desequilibrio ecológico** (ver [Mundo vivo](mundo-vivo-y-viaje.md) y la ecología del [Bestiario](../06-contenido/bestiario.md)) | +5 a +15 por cada especie *Abundante* o en *Plaga* cerca; +5 si se sobrecazó una presa y sus depredadores bajan a buscar el ganado (si faltan ciervos, el Lobo Gris baja a las granjas) |
| **Basura, comida podrida y cadáveres** | +3 si se pudren más de 50 raciones por día o quedan cuerpos sin enterrar: carroñeros (Cuervo de Carroña, ratas, necrófagos) |
| **Invierno** | Todo lo anterior ×1,5: las bestias tienen hambre |
| **Luna llena y eclipse** (ver [Eventos](../06-contenido/eventos.md)) | +20 y +40 de una vez |

| La bajan | Cuánto |
|---|---|
| **Patrullas** de guardias o jugadores alrededor de la ciudad | −5 por patrulla completada |
| **Contratos de caza de control** (una manada que acecha, un oso que baja al corral) | −10 por contrato cumplido; si muere el alfa de la manada que iba a atacar, esa incursión llega más débil |
| **Ley de silencio nocturno** (§10) | Las forjas no suman ruido de noche |
| **Leyes del Ecologista** que mantienen equilibradas las especies (ver [Fundación y cisma](fundacion-y-cisma.md)) | Quitan la atracción ecológica |

- Después de una incursión defendida, la amenaza vuelve al **10 %**. Después de una brecha, al **30 %**: los que ganaron vuelven pronto.
- **La noche:** cuando la barra llega a 100 %, el ataque llega en la próxima noche de juego 7 veces de cada 10 (§6.3).
- **Fuerza de la incursión:** la base de la etapa, más un 10 % por escalón de riqueza, más un 10 % por cada 50 habitantes, más el bono del terreno, más un 20 % si es de noche. La fuerza esperada se ve en `/ciudad` antes de que llegue.

**Por qué conviene.** Crecer tiene un precio. Una ciudad rica, ruidosa y grande atrae más y peores enemigos, así que cada obra nueva pide también más defensa, más comida para los guardias y más cazadores que controlen las bestias de alrededor. Así la defensa **nunca se resuelve una vez y para siempre**.

### 6.2 Qué ataca, por etapa

Los enemigos son de la **zona**: su Lejanía, su anillo y su terreno (ver [Mapa infinito y viaje](mapa-infinito-y-viaje.md)). Su nivel nunca pasa del nivel de la zona más 2; lo que crece es **cuántos son, cuántas oleadas traen y qué tan listos son**.

| Etapa | Qué llega | Oleadas | Novedad |
|---|---|---|---|
| **Fogata** | Alimañas que roban del fogón. La **primera noche** es parte del tutorial: unos lobos rondan y la cazadora PNJ enseña a defender | 1 | Protección de fundación: no hay brechas reales |
| **Campamento** | Jabalíes, alimañas, una manada chica de lobos | 1-2 | Primer ataque de verdad: empalizada y fogatas |
| **Aldea** | Manadas grandes con su alfa, bestias grandes de la zona, **saqueadores PNJ** que salen de los campamentos de bandidos (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) | 2-3 | **Ataques nocturnos**; los saqueadores van directo al granero |
| **Pueblo** | Bandas de saqueadores con jefe, bestias alfa, enjambres, incendiarios | 3 | Atacan por dos lados a la vez; algunos prenden fuego (cadena de cubos, ver [Crisis](crisis-problemas-y-soluciones.md)) |
| **Ciudad** | Hordas mixtas, una **bestia mayor** con postura y partes rompibles, bandidos con escalas y ariete | 4 | Tres frentes a la vez; los enemigos buscan el punto más débil de la muralla |
| **Castillo** | **Asedio de un monstruo grande** (§6.4) con su séquito, además de las incursiones normales | 5 + jefe | Se anuncia con días de anticipación y se juega a hora fija |

### 6.3 Qué ataca, por terreno

Cada región tiene de 2 a 4 terrenos (ver [Geografía y recursos](geografia-y-recursos.md)), y la ciudad recibe a los enemigos de los que tiene cerca.

| Terreno | Incursiones típicas (nombres del [Bestiario](../06-contenido/bestiario.md)) | Monstruo de asedio (etapa Castillo) |
|---|---|---|
| 🌲 **Bosque** | Lobo Gris en manada con su alfa, Araña Tejedora, Cuervo de Carroña que roba del botín, Duendecillo Burlón | **Coloso de Corteza**: un árbol viejo y podrido que camina |
| 🌾 **Llanura** | Lobo Gris, Jabalí Colmillo de Hierro, Langosta de Plaga en los campos (verano), Bandido de Camino, Espantapájaros Animado | **Toro de Tormenta** |
| 🌊 **Costa y lagos** | Cangrejo Acorazado, Pez Colmillo en los vados, Corsario de Costa (saqueadores en barca) | **Cangrejo de Asedio** |
| ⛰️ **Montaña** | Kóbold Minero que roba, Rata de Escoria que se come la comida, Cíclope de Cantera, Grifo de Montaña que se lleva el ganado | **Rey Kóbold** con su ariete |
| 🐸 **Pantano** | Mosquitos de Ciénaga que traen brotes, Sapo Bilioso, Necrófago, Caimán de Lodo, Cultista de la Podredumbre | **Hidra del Lodo** |
| 🏜️ **Desierto** | Escorpión de Vidrio, Tigre de Duna, Buitre de Hueso, Remolino de Arena | **Escorpión Rey** |
| ❄️ **Tundra** | Ventisquero, Novia de Escarcha con ventisca, Licántropo Salvaje en luna llena | **Yeti Anciano** |
| 🕳️ **Cueva y subsuelo** | Araña Nodriza, Murciélago Vampiro, Kóbold Minero, Micelio Andante | **Gran Gusano de Roca**, que sale del suelo dentro de los muros |
| 🌋 **Tierras volcánicas** | Elemental de Magma, Sabueso Infernal, Masa de Escoria junto a las forjas | **Coloso de Magma** |
| 🌸 **Tierras flotantes** | Mantarraya del Cielo, Céfiro, Polilla Lunar | **Roc del Borde** |

- Cada especie pelea con su arquetipo del [Bestiario](../06-contenido/bestiario.md): la manada rodea y huye si cae el alfa, el ladrón va al granero, el carroñero remata a los derribados.
- Los **monstruos de asedio** son nuevos: se proponen como únicos de asedio para el Bestiario, uno por terreno, siempre con los números del anillo donde está la ciudad.
- Un alfa que creció porque nadie lo cazó (ver los monstruos que crecen en el [Bestiario](../06-contenido/bestiario.md)) puede **encabezar una incursión con su nombre**, y la Gaceta lo cuenta.

**Los ataques nocturnos** traen además lo que solo sale de noche (ver [Mundo vivo](mundo-vivo-y-viaje.md)): Fuego Fatuo, Espantapájaros Animado, Necrófago, Murciélago Vampiro, Tigre de Duna y, en luna llena, Licántropo Salvaje. De noche, sin **braseros en la muralla** y **faroles** (Ingeniería y Destilación para el aceite), los defensores pierden precisión y los vigías ven tarde.

### 6.4 El asedio del monstruo grande

En la etapa de Castillo, y como prueba final para llegar a ella, llega un **monstruo de asedio**: para subir a Castillo, **la Noche de prueba es este asedio** (§7). Funciona como un jefe (ver [Jefes](../06-contenido/jefes.md)): tiene fases, postura, partes rompibles y avisos, y su vida **escala con los defensores**, como la de los Guardianes. Así un castillo chico, nacido de un cisma, puede ganarlo.

1. **Avistamiento.** Los exploradores lo ven a **3 días** de la ciudad. La Gaceta lo anuncia.
2. **Preparación.** Tres días para trabajar:
   - los **cazadores** lo rastrean y lo hostigan: cada parte que le rompen antes del asedio la trae rota;
   - los **constructores** refuerzan la muralla y levantan balistas;
   - los **alquimistas** fabrican fuego y venenos;
   - los **médicos** juntan vendas y preparan la enfermería;
   - los **agricultores y cocineros** llenan la despensa, porque durante el asedio no se sale a los campos.
3. **Hora fija.** Los residentes votan la hora del asedio dentro de una ventana, para que pueda venir la mayor cantidad de gente (como la ventana de asedio de [Defensa](../09-construccion/defensa-y-protecciones.md)).
4. **El asedio.** Cinco oleadas de su séquito y después el monstruo, en varios frentes a la vez.
5. **Resultado.** Si se gana: trofeo en la plaza, materiales únicos repartidos por aporte y títulos. Si se pierde: daños grandes (§11) y el monstruo se retira a su guarida, desde donde volverá en una semana **con las partes que le rompieron y sin recuperar toda la vida que le quitaron**: cada intento acerca la victoria.

### 6.5 Cómo se defiende, por rondas

La defensa usa las reglas de [Defensa y protecciones](../09-construccion/defensa-y-protecciones.md): aviso de la torre de vigía, oleadas por rondas en un **tablero de nodos**, defensas que actúan solas y guardias con [Tácticas](../04-combate/avisos-y-tacticas.md). Lo que agrega la ciudad:

- **Tablero de la ciudad:** campos y afueras · empalizada o muralla (por tramos: norte, río, campos) · puerta · corral · granero · enfermería · plaza. Los enemigos buscan comida (granero, corral), gente (aldeanos) y obras en curso.
- **Todos los roles tienen algo que hacer:**

| Rol | Qué hace en la defensa |
|---|---|
| Guerreros y cazadores | Pelean en la muralla, en la puerta o salen a los campos |
| Arqueros y magos | Disparan desde la muralla y las torres |
| Constructores | Reparan la muralla en plena ronda y cierran brechas |
| Ingenieros | Manejan balistas y activan trampas |
| Médicos | Estabilizan heridos en la enfermería y los devuelven a la pelea |
| Bardos | Bajan el miedo y el estrés de los defensores |
| Cocineros, aldeanos y cualquiera | Cadena de cubos si hay fuego, braseros encendidos, llevar flechas a la muralla |

- **Turnos de guardia:** un residente puede anotarse para una noche. Si está conectado cuando llega el ataque, juega; si no, pelea su **Eco** con sus Tácticas (ver [Jefes](../06-contenido/jefes.md)). Así la ciudad está defendida en todos los husos horarios, y cada turno cuenta como aporte (§9). Si el Eco cae, el jugador no se lleva ninguna herida.
- **Rondas de 60 segundos**, como en las bandas (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)).
- **Caer en la defensa.** La defensa es una instancia, como una mazmorra, así que caer sigue la regla de mazmorra de [Secuelas y muerte](../05-salud/secuelas-y-muerte.md): no se pierde nada material y queda una herida moderada (leve para los novatos hasta el nivel 10). En un asentamiento de **zona azul nadie cae para siempre**, tampoco los personajes del Juramento de Hierro: ahí caer no los mata, como en la arena. La zona azul protege a las personas; lo que se juega en la incursión son las cosas de la ciudad. En los asentamientos de zonas amarillas, rojas o negras rigen las reglas de caída de esa zona.

**Una excepción a la zona segura.** Hoy, en el territorio del Claro y de los campamentos nadie es atacado: ni al llegar, ni al explorar, ni al recolectar (D-81). Eso sigue igual para las personas. [Defensa](../09-construccion/defensa-y-protecciones.md) dice además que lo construido en zona azul nunca se ataca. Esta propuesta lo cambia solo para **lo común de los asentamientos que levantan los jugadores**, desde aldea y también después de llegar a castillo: las incursiones de monstruos y de saqueadores PNJ **sí atacan** murallas, granero, corral, obras en curso y aldeanos. Ya hay base para esto: las especies que nadie caza "invaden las zonas azules" ([Mundo vivo](mundo-vivo-y-viaje.md), §5), la *Plaga* del [Bestiario](../06-contenido/bestiario.md) hace lo mismo, y Defensa ya incluye la *Invasión de la región* contra asentamientos enteros. Las **casas de los jugadores y lo que hay dentro nunca se atacan**, y en zona azul no hay saqueo entre jugadores. Falta anotar la excepción en Defensa y registrarla como decisión provisional.

| Resultado | Qué pasa |
|---|---|
| **Defendida** | Botín de los atacantes al fondo común, repartido por aporte; +ánimo, +seguridad; cuenta como incursión superada para la etapa |
| **Brecha parcial** | Se pierde hasta el 15 % de la despensa o parte del ganado; 1 o 2 edificios dañados; aldeanos heridos; −ánimo |
| **Derrota** | Se pierde hasta el 30 % de la despensa; edificios dañados; la obra en curso pierde hasta un 10 % de avance; se van aldeanos y pueden morir algunos |

## 7. Requisitos de etapa: sostener, no solo construir

### 7.1 En el Claro

Para que el Claro suba a aldea o más harían falta tres cosas:

1. **La obra de la etapa** pagada, como hoy (`settlement.stages`, ver [Fundación y cisma](fundacion-y-cisma.md) §1).
2. **La racha:** con la obra ya pagada, todos los mínimos de la tabla cumplidos durante cierta cantidad de **días reales seguidos**. La racha no cuenta antes de pagar la obra: primero se construye y después se demuestra que se puede sostener.
3. **La Noche de prueba:** al completar la racha, la subida hace ruido y llega una incursión especial esa noche. Si se defiende, el Claro sube. Si no, la subida se aplaza 2 días y no se pierde nada. Para subir a **castillo**, la Noche de prueba es el **asedio del monstruo grande** (§6.4).

| Subir a | Obras extra (además de los materiales de hoy) | Población mínima | Despensa sostenida | Salud | Ánimo · Orden · Seguridad | Incursiones superadas en la etapa | Aportes colectivos | Racha |
|---|---|---|---|---|---|---|---|---|
| **Campamento** | — (hoy: solo materiales) | — | — | — | — | La primera noche, como tutorial y sin brechas reales | — | — |
| **Aldea** | Granero, letrinas, empalizada, cabañas comunes | 40 (10 jugadores) | 4 días | 50 | Ánimo 40 | 1 | 4 de cada 10 residentes al día con su cuota (§9.2); 3 categorías de pedidos de la semana cubiertas (§9.1) | 2 días |
| **Pueblo** | Ahumadero y salazón, segundo pozo, cementerio, lazareto, torre de vigía | 120 (15 jugadores) | 5 días | 60 | Ánimo 50 · Orden 40 | 2, una de noche | 5 de cada 10 al día; una semana con todos los pedidos cubiertos | 3 días |
| **Ciudad** | Granero de piedra, cisterna, alcantarillado, baños, torres en cada tramo de muralla | 300 (20 jugadores) | 7 días | 65 | Ánimo 55 · Orden 50 · Seguridad *Firme* | 3, una de saqueadores | 55 de cada 100 al día; **un invierno pasado sin hambruna** | 4 días |
| **Castillo** | Silos, acueducto | 600 (30 jugadores) | 10 días | 70 | Ánimo 60 · Orden 60 · Seguridad *Firme* | 4 y el **asedio del monstruo grande** (§6.4) | 6 de cada 10 al día; las 7 categorías de pedidos cubiertas | 5 días |

- **Mientras el Claro es campamento** no hay mínimos: pagar sigue alcanzando, para que el tutorial nunca se trabe. La capa profunda empieza al subir a aldea.
- **Población mínima:** el número entre paréntesis es cuántos jugadores tienen que estar entre los residentes. El resto pueden ser aldeanos y guardias, a los que hay que alojar, alimentar y mantener sanos. Lo más que se pide, 30 jugadores, es el mínimo de firmantes de un cisma en el Claro (ver [Fundación y cisma](fundacion-y-cisma.md) §6.1).
- **Residentes del Claro:** los jugadores activos que no son miembros de un campamento, más los miembros de campamentos que aportaron al Claro esa semana. Así nadie tiene que elegir entre su campamento y la sede común.
- **Quién cuenta para la participación** ("X de cada 10 al día"): solo los residentes que jugaron **3 días o más** en la semana.
- **La racha es indulgente con los tropiezos cortos.** Si un mínimo falla, la racha se congela. Solo vuelve a cero si falla durante un día real entero.
- Los números son orientativos y se ajustan en la beta. La meta es la de P-55: de **4 a 6 semanas** desde la fogata hasta castillo.

### 7.2 En los campamentos de jugadores (capa ligera)

Un campamento tiene de 2 a 18 miembros. La capa ligera mide todo **por miembro** y nunca le quita lo ganado:

| Nivel | Qué se suma a pagar los materiales de hoy |
|---|---|
| **1-2 (campamento)** | Nada. Fundar y crecer siguen como hoy |
| **3-4 (aldea)** | **Despensa chica** en el almacén común: 1 ración por miembro activo por día. Si se vacía, el campamento no puede agrandarse hasta llenarla. Nunca pierde zonas ni niveles |
| **5-6 (pueblo)** | **Una incursión por semana**, con la fuerza escalada a los miembros activos. La juegan los miembros conectados; los demás pelean con su Eco. Si se pierde, se pierde parte de la despensa y nada más |
| **7-8 (ciudad)** | Un medidor de **salud** simple: con la despensa llena y una enfermería, se mantiene solo. Si baja, la recolección extra del territorio (+50 %) se apaga hasta que suba |
| **9 (castillo)** | **Noche de prueba** antes de pasar a castillo: una incursión grande con un jefe de la zona. Si se pierde, se reintenta a los 2 días |

- **Lo que nunca pasa:** un campamento activo nunca pierde niveles, zonas ni miembros por fallar. Lo que se apaga son servicios, hasta que se recuperen.
- **El campamento abandonado** es otra cosa: sin miembros activos durante semanas, decae (ver [Fundación y cisma](fundacion-y-cisma.md) §4.1).

## 8. Los obreros también comen

Una obra no es solo piedra y madera:

- **Comida:** cada jornada de obra gasta **media ración extra** de la despensa (el comedor de los obreros). La muralla del Pueblo pide unas 400 jornadas: son **200 raciones más** que hay que producir antes.
- **Herramientas:** cada jornada gasta durabilidad de las **herramientas comunes** del almacén (palas, martillos, sierras, picos). Las hacen y las reparan herreros y carpinteros.
- **Agua y salud:** con la salud pública en *Enferma* hay más accidentes de obra (ver [Sistema de construcción](../09-construccion/sistema-de-construccion.md)).

| Estado | Avance de las obras |
|---|---|
| Despensa en *Abundancia* | +5 % |
| Despensa *Holgada* o *Justa* | Normal |
| Despensa en *Escasez* | La mitad |
| **Hambruna** | **Paradas** |
| Herramientas comunes al 50 % o más | Normal |
| Herramientas por debajo del 50 % | La mitad, y más riesgo de accidente |
| **Sin herramientas** | **Paradas** |
| Jornadas extra (§10) | +50 %, con más comida y menos ánimo |

Así, planear una obra grande es planear también la comida y las herramientas, como en *Frostpunk*. El Maestro de Obras mayor ve la cuenta antes de empezar: "*Muralla: 400 jornadas · 200 raciones · 60 herramientas · 8 días con el ritmo actual*".

La paga de los constructores no cambia: sigue saliendo del presupuesto de la obra (ver [Sistema de construcción](../09-construccion/sistema-de-construccion.md)).

## 9. Progresar en conjunto

### 9.1 Registro de aportes

Todo lo que alguien hace por la ciudad queda registrado como **mérito**, por categoría:

| Categoría | Qué cuenta |
|---|---|
| 🌾 Comida | Raciones entregadas, conservas hechas, cosechas en campos comunes |
| 🪵 Materiales y herramientas | Materiales donados, herramientas fabricadas o reparadas |
| 🏗 Obras | Jornadas trabajadas |
| 🛡 Defensa | Incursiones defendidas, turnos de guardia, patrullas, contratos de caza de control |
| ⚕️ Salud | Turnos de enfermería, remedios entregados, brotes controlados |
| 🎶 Ánimo | Noches de bardo, banquetes, festivales organizados |
| ⚖️ Orden | Patrullas, juicios, delitos resueltos |

- `/ciudad aportes` muestra el registro **por jugador, por rol y por gremio**.
- **Tope diario por categoría:** después de cierto mérito en un día, cada aporte suma menos. Diez jugadores con mucho oro no pueden cargar solos con una ciudad.

### 9.2 Cuotas semanales

- Cada semana la ciudad calcula sola lo que va a necesitar: comida según el consumo y la estación, vendas según los brotes, jornadas según las obras, turnos de guardia según la amenaza.
- Eso se publica como **pedidos** (ver [Fundación y cisma](fundacion-y-cisma.md)) que cualquiera puede tomar, con paga del tesoro y mérito.
- **La cuota del residente:** se le pide a cada residente un aporte pequeño por semana, en la categoría que quiera. Alcanza con algo que se hace jugando normal: una jornada de obra, un turno de guardia o de enfermería, entregar la carne de una cacería o una cosecha. Quien lo cumple queda **al día**: comedor común gratis, posada más barata y el sello de "Vecino al día" en el perfil. Quien no lo cumple no pierde nada más que eso, y su voto vale lo mismo.
- **Para subir de etapa** hace falta que cierta parte de los residentes esté al día (§7). La masa tiene que moverse, no solo unos pocos.

### 9.3 Metas de la ciudad

Cada semana hay una o dos metas con nombre, con premio para toda la ciudad:

| Meta | Premio |
|---|---|
| "Llenar el granero antes del invierno" | Banquete de invierno: +ánimo durante 3 días |
| "Cazar la manada del Arroyo antes de la luna llena" | Esa noche no hay incursión de lobos |
| "Cero brotes esta semana" | +inmunidad para todos los residentes |
| "Terminar la muralla norte" | Inauguración con festival |

### 9.4 Reconocimiento público

- **Pilares de la semana:** la Gaceta y el grupo de la ciudad publican a los que más aportaron **en cada rol** (agricultor, cazador, cocinero, constructor, médico, defensor, bardo), no un único ranking. Así brilla cada forma de jugar.
- **Títulos:** "Mano del Granero", "Guardián de la Empalizada", "Sanador del Brote", "Voz del Invierno".
- **Placa en la plaza** con los nombres de quienes sostuvieron cada etapa, además de los Fundadores de cada edificio.
- **Primer aporte:** quien aporta por primera vez sale nombrado en el resumen del día. A los nuevos también se los ve.

## 10. Decisiones difíciles

Como en el libro de leyes de *Frostpunk*: cada decisión arregla un problema y crea otro. Antes del Pueblo las vota la **asamblea** de residentes (encuesta de Telegram de 12 horas); desde el Pueblo las toma el **gobierno** (ver [Fundación y cisma](fundacion-y-cisma.md)).

| Decisión | A favor | En contra | Duración |
|---|---|---|---|
| **Racionar** (reducida o mínima) | La despensa dura un tercio más, o el doble | −ánimo cada día; con la mínima, −salud y obras más lentas | Hasta que se levante |
| **Banquete de emergencia** | Gran subida de ánimo y salud | Gasta 3 días de despensa en uno | 1 día |
| **Cuarentena** | El contagio sube mucho más despacio | −ánimo, −comercio, no entran caravanas, menos jornadas de obra | Hasta que termine el brote |
| **Jornadas extra** | Las obras avanzan un 50 % más | Más comida, −ánimo, más accidentes | 3 días |
| **Aceptar refugiados** | Más manos y más población para la etapa | Más bocas, hacinamiento, riesgo de brote, −orden si no hay casas | Permanente |
| **Cerrar las puertas** | Nada de lo anterior | −ánimo; −reputación con el castillo vecino que los mandó | Permanente |
| **Priorizar la muralla** | Las obras de defensa avanzan el doble | Se frenan las demás, incluso el sanatorio | Hasta que se termine |
| **Priorizar el sanatorio** | La salud pública sube más rápido; brotes más cortos | Se frena la muralla; la seguridad queda baja | Hasta que se termine |
| **Impuesto de emergencia** | Tesoro para pagar pedidos de comida o comprar a otros castillos | −ánimo; algunos aldeanos se van a otros nodos | 1 semana |
| **Leva de defensa** | Los aldeanos forman una milicia: +seguridad | No trabajan en los campos: menos comida; pueden morir en la defensa | Hasta la próxima incursión |
| **Silencio nocturno** | Las forjas no hacen ruido de noche: menos amenaza | Menos fabricación; los herreros protestan | Permanente |
| **Batida de caza** | Baja la amenaza ecológica, entra carne | Riesgo de sobrecaza: la especie escasea la temporada siguiente | 2 días |
| **Veda de caza** | La especie se recupera | Menos carne; si dura mucho, la especie crece y ataca | 1 semana |
| **Quemar los campos con tizón** | Frena la plaga de cultivos | Se pierde la cosecha de esos campos | Una vez |
| **Comprar comida al castillo vecino** | Comida ya | Precio alto; deuda o dependencia del vecino | Una vez |
| **Toque de queda** | +orden | −ánimo, menos actividad en la taberna y el mercado de noche | Hasta que se levante |
| **Festival en plena crisis** | +ánimo fuerte | Gasta comida y suma ruido (amenaza) | 1 día |

- Cada decisión tiene **enfriamiento**: no se puede poner y sacar cada hora.
- La Gaceta cuenta las decisiones y sus resultados: "*el invierno de las raciones mínimas*" queda en la historia de la ciudad.

## 11. El fracaso: qué se pierde y qué no

**La regla nueva:** hoy el Claro nunca baja de etapa y un campamento nunca pierde zonas ni niveles. La propuesta lo respeta: **las etapas, los niveles y las zonas ganadas no se pierden**. Lo que se apaga, mientras dura el problema, son **servicios**.

| Qué pasa | Cuándo | Cómo se recupera |
|---|---|---|
| **La racha vuelve a cero** | Un mínimo falla durante un día real entero (la hambruna siempre lo provoca) | Sostener de nuevo |
| **Edificios dañados** | Brechas, incendios, sabotajes | Jornadas de reparación de los constructores (trabajo pagado) |
| **Obras que pierden avance** | Una derrota en una incursión (hasta un 10 %) | Más jornadas |
| **Aldeanos que se van o mueren** | Hambruna, brotes, brechas, ánimo bajo | Vuelven a llegar cuando la ciudad mejora |
| **Servicios apagados** | Dos medidores en rojo durante 3 días reales seguidos, o hambruna de 3 días | La etapa y sus zonas se quedan. Se apagan los servicios de la etapa (posada más barata, almacén, estaciones). Para encenderlos basta sostener la mitad de la racha y ganar una Noche de prueba |
| **Ruinas** | Solo un campamento **abandonado**: semanas sin miembros activos (ver [Fundación y cisma](fundacion-y-cisma.md) §4.1) | Otro grupo puede refundarlo. El Claro nunca queda en ruinas |

**Nunca se pierde, pase lo que pase con la ciudad:**
- la mochila, las monedas, el equipo, los niveles, los talentos y los títulos de cada jugador. Si un almacén se apaga, lo guardado ahí se sigue pudiendo retirar;
- la **casa** de cada jugador y lo que hay dentro (cuando existan las casas). Si un campamento queda en ruinas, el dueño puede **trasladarla gratis y sin pérdida** a otro asentamiento;
- el mérito aportado y el nombre de los **Fundadores** en cada edificio.

El fracaso es de la ciudad y deja historia. Nunca arruina a un personaje (D-64: el progreso de los jugadores se guarda para siempre).

## 12. Escala: 500 jugadores no lo vuelven fácil

Con más de 500 jugadores listos para la beta (ver [Decisiones](../00-vision/decisiones.md), D-39), la masa podría resolverlo todo en un día. Para que no pase:

- **Todo va por habitante:** el consumo, las cuotas, la cobertura de pozos y letrinas, la vivienda. El doble de gente es el doble de trabajo.
- **La amenaza crece con la población y la riqueza:** más gente trae incursiones más fuertes y con **más frentes a la vez**, cada uno con sus puestos. La masa se reparte en lugar de amontonarse.
- **Topes por persona:** las jornadas tienen Energía limitada y el mérito diario rinde menos después de cierto punto (§9.1).
- **Participación mínima:** hace falta que una parte de los residentes esté al día (§7), no que unos pocos pongan todo.
- **Un tiempo que no se compra con gente:** la racha empieza recién con las obras terminadas (14 días en total sumando las cuatro etapas, de aldea a castillo), la Ciudad pide haber pasado un invierno (el primero llega en la tercera semana, §4.5) y el asedio se anuncia 3 días antes. Ni con 500 jugadores perfectos se llega al Castillo antes de unas 4 semanas y media, dentro de la meta de 4 a 6.
- **Tierra y vivienda limitadas:** cada nodo tiene una cantidad fija de parcelas de cultivo y de lugar para casas. Más gente pide más tierra, y eso empuja a fundar campamentos vasallos cerca y a comerciar entre ellos (ver [Fundación y cisma](fundacion-y-cisma.md) §4.1).

| Población (jugadores + PNJ) | Consumo por día | Reserva para el invierno | Fuerza media de incursión | Frentes a la vez | Puestos de defensa |
|---|---|---|---|---|---|
| 50 | ~55 raciones | ~350 | ~150 | 1 | 15 |
| 150 | ~170 | ~1.000 | ~300 | 2 | 40 |
| 300 | ~340 | ~2.000 | ~480 | 3 | 80 |
| 650 (500 jugadores y 150 aldeanos) | ~730 | ~4.500 | ~900 | 4-5 | 160 |

## 13. Cómo se ve

### 13.1 La pantalla `/ciudad`

Igual en Telegram, en la web y en la app: el mismo motor, los mismos números.

```
🔥 El Claro · Aldea → Pueblo (Lejanía 0 · 🌲 Bosque, 🌾 Pradera)
Racha de etapa: ✅✅⬜ 2/3 días
👥 Población 134/150 · 61 jugadores · 68 aldeanos · 5 guardias

🌾 Despensa  ▓▓▓▓▓░░░░░ 5,2 días  🟡 Justa   (mín. 5)
   hoy: +149 producido · −156 comido · −9 podrido
⚕️ Salud     ▓▓▓▓▓▓▓░░░ 68  🟢 Normal       (mín. 60)
🎶 Ánimo     ▓▓▓▓▓░░░░░ 52  🟡 Inquieta     (mín. 50)
⚖️ Orden     ▓▓▓▓▓▓▓░░░ 71  🟢 Normal       (mín. 40)
🛡 Seguridad 112 % 🟢 Firme (defensa 470 · próxima 420)

👁 Amenaza   ▓▓▓▓▓▓▓░░░ 72 % · llega: probablemente esta noche
   Por qué: 3 forjas encendidas, manada sin cazar en el Arroyo
❄️ El invierno llega en 3 días · reserva de invierno: 810/1.000

📋 Pedidos de la semana
🌾 Grano o carne salada ......  410/1.200
🧂 Sal ........................   60/200
🩹 Vendas .....................   41/60
🪵 Leña para el invierno ......  380/1.000
🔨 Herramientas reparadas .....   12/40
🛡 Turnos de guardia nocturna .   18/42
🏹 Contrato: el alfa del Arroyo     0/1

Tú: ✅ al día · mérito de la semana 340 (🌾 Comida)

[📋 Aportar]   [🏗 Obras]     [👥 Aldeanos]
[⚖️ Decisiones] [🏆 Aportes]  [🛡 Defensa]
```

### 13.2 Una incursión nocturna, por rondas

**El aviso** (llega a los anotados y al grupo de la ciudad):

```
🔔 Torre de vigía · El Claro
🐺 Tres manadas de Lobo Gris (14 lobos) y su alfa bajan del Arroyo.
Llegan en 25 minutos · 🌑 de noche · fuerza 420 · defensa 470
Anotados: 23 defensores · 5 guardias y 2 torres con sus Tácticas

[🛡 Anotarme]  [🔥 Encender braseros]  [🪤 Poner trampas]
```

**Una ronda:**

```
🌑 Defensa del Claro · Oleada 1/3 · Ronda 2 · ⏱ 60 s
Empalizada norte ▓▓▓▓▓▓▓░░░ 70 %   Puerta ▓▓▓▓▓▓▓▓▓░ 90 %
Granero 🌾 a salvo · Corral 🐑 3 lobos dando vueltas
Braseros 4/6 encendidos: precisión normal en la empalizada
⚠️ El alfa olfatea el corral: la próxima ronda salta la cerca.

Tú: Ilsa (cazadora) · empalizada norte · ❤️ 82 % · 🔋 4/5
[⚔️ Disparar al alfa]   [🔥 Flecha incendiaria]
[🎯 Tiro a la pata]     [🌀 Rodar a cubierto]
[🏃 Bajar al corral]    [🎒 Mochila]
```

Son los 6 botones del combate (D-46 en [Decisiones](../00-vision/decisiones.md)): ⚔️ Atacar, tres habilidades y 🎒 Mochila. En la defensa, 🏃 Huir sirve para **cambiar de puesto** en el tablero. Los puestos de oficio también tienen como máximo 6 botones, con sus tareas: el constructor ve *Reparar tramo* y *Cerrar brecha*; el médico, *Estabilizar* y *Llevar a la enfermería*.

Mientras tanto, Bram (constructor) repara la empalizada, Mara (médica) estabiliza a un aldeano mordido en la enfermería y dos aldeanos llevan carbón a los braseros que faltan.

**El parte** (reenviable, con los detalles plegados):

```
📜 Parte · Noche 14 · El Claro
✅ Incursión superada (3/3 oleadas) · para la etapa: 2/2 ✅
Enemigos: 14 lobos y el alfa (último golpe: Ilsa)
Daños: empalizada norte −18 % · 2 ovejas perdidas · 1 aldeano herido
Botín al fondo común: 28 pieles, 1 piel de alfa · se reparte por aporte
🛡 Seguridad +5 · 🎶 Ánimo +6 · 👁 Amenaza 72 % → 10 %
Pilares de la noche: Ilsa (defensa) · Bram (obras) · Mara (salud)
```

## 14. Cómo se conecta

Su fila en la [Red de sistemas](../00-vision/red-de-sistemas.md):

| Consume | Produce | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|
| Comida, sal, leña, agua, materiales, herramientas, remedios, vendas, armas para guardias, jornadas, turnos de guardia y de enfermería | Etapas de ciudad, servicios, aldeanos que trabajan, incursiones (botín de monstruo, pacientes, trabajo de reparación), mérito y títulos, historia para la Gaceta | Grano, carne, pescado, sal, leña, hierbas, pieles | Conservas, herramientas, defensas, remedios, faroles, frascos | Rangos de Agricultura, Cocina, Medicina y Construcción; nivel de los defensores; etapa de la ciudad |

**A quién le da trabajo:**

| Oficio o rol | Qué hace aquí |
|---|---|
| **Agricultura y Ganadería** | La base de la despensa; abono del estercolero; forraje para el invierno |
| **Caza y Pesca** | Carne y pescado; contratos de control que bajan la amenaza |
| **Cocina** | Estira la comida, hace conservas, banquetes y caldos para los brotes |
| **Construcción** | Graneros, pozos, letrinas, murallas; reparar después de cada incursión |
| **Herrería y Carpintería** | Herramientas comunes, armas de los guardias, balistas, cercos |
| **Medicina, Alquimia y Herboristería** | Turnos de enfermería, control de brotes, remedios |
| **Ingeniería y Destilación** | Faroles y aceite, trampas, balistas, acueducto |
| **Joyería** | Frascos de vidrio para conservas |
| **Comercio** | Traer comida y sal de otros terrenos y castillos |
| **Bardos y taberneros** | Ánimo de la ciudad y de los defensores |
| **Guerreros, guardias y cazadores** | Defensa, patrullas, turnos de guardia |
| **Gobierno** | Decisiones difíciles, cuotas, reparto de aldeanos |

## 15. Principios anti-frustración

1. **Nada personal se pierde.** Ni las cosas, ni la casa, ni el progreso del personaje, aunque la ciudad falle.
2. **Lo ganado entre todos tampoco.** Las etapas del Claro y los niveles y zonas de un campamento no bajan: se apagan servicios (§11).
3. **No jugar no castiga.** Quien no entra deja de contar y deja de comer; no arrastra a la ciudad ni se arrastra a sí mismo.
4. **Siempre hay aviso.** La amenaza se ve subir, la torre de vigía avisa antes del ataque, el invierno se anuncia con días y la despensa avisa en *Justa*.
5. **Los tropiezos cortos no borran todo.** La racha se congela antes de volver a cero.
6. **Cada rol cuenta.** Se puede sostener una ciudad sin pelear nunca: recolectando, cocinando, curando, construyendo o cantando en la taberna.
7. **Los novatos aprenden sin miedo.** Hasta que el Claro es campamento, subir es solo pagar, y la primera noche es tutorial.
8. **Siempre hay una salida cara.** El mercader del Claro vende comida de emergencia a precio alto (sumidero de monedas), con un tope por semana.

## 16. Para decidir

- **Lo principal, para el dueño:** ¿subir de etapa debe pedir algo más que pagar materiales? Recomendación: sí, pero solo en el Claro desde aldea y con la capa ligera en los campamentos desde aldea (§7), porque así se cumple "que no sea construir y ya" sin trabar a los grupos chicos. Si dice que sí, se registra como decisión y se programa por partes: primero la despensa, después las incursiones. **Respuesta:** el dueño dijo que sí por voz (D-93, provisional) y la despensa ya está en el juego (§0.4). Siguen las incursiones.
- **Para confirmar con el dueño (despensa):** el tope por semana de las provisiones (§15.8, todavía sin tope), si los días mínimos para subir quedan corridos una etapa (§0.4) y si la despensa necesita un tope de capacidad antes de los graneros (§4.3).
- Los números exactos de consumo, producción, amenaza y requisitos (se ajustan en la beta).
- Si se acepta la excepción a la zona segura (§6.5): que las incursiones ataquen lo común del asentamiento, nunca las casas ni a las personas.
- Si los aldeanos pueden morir o solo irse (la propuesta: pueden morir en brechas y brotes graves).
- Si los campamentos nacidos de un cisma empiezan con la misma curva o con una más corta.
