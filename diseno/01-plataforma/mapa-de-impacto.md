# Mapa de impacto: qué se mueve cuando cambias algo

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Arquitectura modular](arquitectura-modular.md), [Convenciones de código](convenciones-de-codigo.md), [Red de sistemas](../00-vision/red-de-sistemas.md) · **Se conecta con:** todos los módulos, [Web y multiplataforma](web-y-multiplataforma.md) · **Estado:** propuesta; el mapa en sí lo pide D-42 (confirmada)

**Qué pediste.** Que cuando le pidas a la IA que crea el juego cambiar una sola cosa, la IA entienda todo lo que pasa alrededor y pueda decirte: "ok, pero esto también va a romper esto, esto y esto, o puede afectar esto y esto". Es la decisión D-42 (ver [Decisiones](../00-vision/decisiones.md)).

Este documento es **el mapa que se consulta antes de cambiar algo**: una regla, un número, un módulo, un texto o una pantalla. Las notas `[ES]` del código apuntan aquí (ver [Convenciones de código](convenciones-de-codigo.md)), y este mapa apunta a los documentos de diseño. El código ya está autorizado (D-59, que reemplaza a D-04): los ejemplos de código de este mapa son ilustrativos, y el mapa se actualiza en el mismo cambio que el código (§1.5).

**De dónde sale.**
- **Lecciones de TowerWars** (ver [Lecciones de TowerWars](../99-referencias/lecciones-de-towerwars.md)): "la ropa no contaba" (la guerra calculaba el poder por su lado y el equipo no sumaba), "si un número de balance se movió y no está en el registro, se movió a ciegas" y "la documentación vieja miente".
- **Análisis de impacto** de la ingeniería de software: antes de tocar una pieza se lista quién la usa, qué datos comparte y qué pruebas hay que repetir.
- La [Red de sistemas](../00-vision/red-de-sistemas.md) de este diseño: si todo depende de todo (D-20), hace falta un mapa de esas dependencias.

---

## 1. Cómo leerlo y cuándo se actualiza

### 1.1 Los cuatro pasos antes de cambiar algo

1. **Busca el módulo dueño** de lo que vas a cambiar en las fichas (§2). Cada dato tiene un solo dueño (regla 2 de la [arquitectura](arquitectura-modular.md)).
2. **Lee su "Si cambias esto, revisa"** y sigue las flechas hacia los otros módulos. Las referencias `C-xx` llevan a las cascadas típicas (§3).
3. **Mira si el cambio mueve un número sensible** (§4) o una regla que está escrita en varios documentos (§4.7).
4. **Mira si toca a los clientes** (§5): Telegram, web y app.

Con eso se arma el **mensaje de impacto** (plantilla en [Convenciones de código](convenciones-de-codigo.md) §6.3) **antes** de editar. Las Convenciones también fijan los cinco caminos por los que se propaga un cambio (importaciones, eventos, datos compartidos, números de balance y contrato con los clientes) y los niveles de riesgo. Este mapa da el contenido de esos cinco caminos para cada módulo.

### 1.2 Ejemplo de respuesta de impacto

El dueño dice: "las heridas graves duran muy poco, que duren más".

```
Cambio: las heridas graves pasan de 1-3 días a 2-4 días.
Dónde: datos de curación de heridas · M7 Salud · diseño: 05-salud/heridas.md §3
Esto también afecta a:
  1. Combate (M5): más rondas jugadas con penalización de herida.
  2. Construcción (M24): el dormitorio (x2) y la enfermería (x3) valen más.
  3. Oficios (M14): más demanda de médicos; más experiencia de Medicina.
  4. Economía (M13): más uso del sanatorio (sumidero) y consultas más caras.
  5. Instancias (M11): menos gente lista para mazmorras y bandas.
  6. PvP y apuestas (M12, M16): más luchadores "no aptos" en el Foso.
Reglas que toca: ninguna, si el tiempo fuera de línea sigue curando.
Números de balance: herida grave 1-3 días -> 2-4 días.
Pruebas: las de M7 y el cálculo de "sana en..." que ve el jugador.
Voy a actualizar: heridas.md §3, este mapa (C-02 y §4.2), registro de balance.
Riesgo: medio · ¿Sigo?
```

### 1.3 Tres palabras con significado fijo

| Palabra | Significa | Qué se hace |
|---|---|---|
| **Rompe** | El cambio contradice una regla que nunca se rompe o una decisión confirmada del dueño (D-xx), o deja datos o pantallas sin funcionar | No se hace sin el sí explícito del dueño |
| **Afecta** | Cambia resultados en otro módulo, aunque nada falle | Se avisa y se revisa ese módulo |
| **Medir** | Mueve un número de balance o de economía | Simulador (M21) o informe económico (M20) antes y después, y entrada en el registro de balance |

Las **propuestas** (P-xx) todavía no son ley: cambiar algo que una propuesta recomienda no "rompe", pero se avisa ("va contra la recomendación de P-xx").

### 1.4 Cómo leer una ficha

Cada ficha usa los mismos campos que el encabezado `[ES]` de los archivos de código (ver [Convenciones de código](convenciones-de-codigo.md) §2), para que el código y este mapa se puedan comparar campo por campo:

| Campo | Qué dice |
|---|---|
| **Para qué sirve** | La responsabilidad del módulo en una frase |
| **Documentos de diseño** | Dónde están sus reglas |
| **Depende de** | Lo que necesita de otros módulos. Si cambia algo allá, este módulo se puede romper |
| **Lo usan** | Quiénes lo necesitan. Si cambias este módulo, revisa a todos ellos |
| **Eventos que publica / escucha** | Las conexiones invisibles: quien publica no sabe quién escucha |
| **Datos de los que es dueño** | Lo que solo este módulo escribe. Los demás piden |
| **Reglas que nunca se rompen** | Reglas fijas del diseño o decisiones del dueño. Cambiarlas no es un ajuste: es una decisión nueva |
| **Si cambias esto, revisa** | Cascadas concretas, con el módulo afectado entre paréntesis |

**Sobre los eventos:**
- Sin marca: están en la tabla de [Arquitectura](arquitectura-modular.md) §4. Se escriben con el nombre del diseño y, entre paréntesis, el nombre en código del diccionario de [Convenciones](convenciones-de-codigo.md) §7.2: `GolpeRecibido` (`HitReceived`).
- **Propuestos:** no existen todavía. Muestran una dependencia real del diseño y se confirman en Arquitectura antes de programarlos. Su nombre en inglés se elige al agregarlos al diccionario.

**Sobre el paquete de código:** el título de cada ficha lleva el paquete propuesto en [Convenciones](convenciones-de-codigo.md) §7.1, por ejemplo `engine/health`.

### 1.5 Cuándo se actualiza

Este mapa se actualiza **en el mismo cambio** que lo vuelve viejo, nunca después:

1. Se agrega, se quita o cambia un módulo, un evento o un dato con dueño en la [arquitectura](arquitectura-modular.md).
2. Un documento de diseño agrega una dependencia nueva (un "Depende de" o "Se conecta con" nuevo en su línea de módulo).
3. Se mueve un número sensible (§4), junto con su entrada en el registro de balance.
4. Se confirma o se descarta una decisión (D-xx) o una pregunta (P-xx) que cambia una regla.
5. Con el código (D-59): en el mismo cambio que toca el código. La herramienta de grafo de dependencias de las [Convenciones](convenciones-de-codigo.md) §8 comparará el grafo real con este mapa y avisará de las diferencias.

**Quién lo actualiza:** quien hace el cambio, persona o IA.

**Si este mapa y otro documento no coinciden:** manda el documento del módulo, que es más específico, y se corrige el mapa. Por encima de los dos mandan las decisiones confirmadas del dueño. Si un documento todavía no recoge una decisión confirmada, este mapa sigue la decisión y lo anota en §6.2.

**Estado al 1 de octubre de 2026.** El diseño se está revisando en paralelo para aplicar las decisiones D-44 a D-59. Donde un documento todavía dice otra cosa, aquí se sigue la decisión y la diferencia queda anotada en §6.2. Tres decisiones cambian reglas que este mapa daba por fijas:

- **D-58: ya no hay Torre ni pisos.** El mundo es un mapa sin borde y moverse entre lugares toma tiempo real. Vocabulario (propuesta de [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)): piso → zona y región; Frente → Frontera; Techo del Piso → Techo de la Frontera. Siguen el Guardián (ahora de la región), el Eco, los Pioneros y el Viento de Cola. Se retiran el Sello del Piso y, como propuesta, la piedra de paso; las menciones que quedan al Sello (sus pruebas, `SelloObtenido`) son conexiones que se caen con él. Ya están ajustadas las fichas M2, M8, M9 y M22 y las cascadas C-05, C-08 y C-15. Donde todavía quede "piso" (las Llaves del Piso de M11, el evento `PisoAbierto`), léase "región": el nombre nuevo lo fija la [arquitectura](arquitectura-modular.md).
- **D-57: no hay límite de oficios.** El freno es el costo natural del conocimiento: tiempo, materiales, preparación y los costos de cada oficio. Ya están ajustadas la ficha M14 y la cascada C-12.
- **D-59: el código ya está autorizado** (reemplaza a D-04). Este mapa y las [Convenciones](convenciones-de-codigo.md) valen desde la primera línea.

Las demás decisiones nuevas suman sistemas sin cambiar las reglas de este mapa: roles por spec y juego en solitario (D-50), secuelas definitivas y cómo reponerlas (D-51, D-53), botín amplio (D-52), escalera de conocimiento (D-54), elixires propios (D-55) y aprender con pistas (D-56). Su dueño propuesto está en §6.1.

### 1.6 Cómo se ve en el código

Un archivo de datos de balance con su nota `[ES]` debajo, que remite a este mapa (formato de [Convenciones](convenciones-de-codigo.md) §4):

```yaml
# Wound healing windows in real hours, before rest multipliers.
# Schema: content/schemas/wound_healing.schema.yaml
#
# [ES]
# Para qué sirve: cuánto tarda en sanar sola cada herida según su gravedad.
# Documento de diseño: diseno/05-salud/heridas.md §3
# Lo leen: engine/health/wounds.py (M7). Cambia el valor de los tratamientos (M14)
#          y del descanso en casa y enfermería (M24).
# Si cambias esto, revisa: diseno/01-plataforma/mapa-de-impacto.md · C-02 y §4.2.
#          Todo cambio va al registro de balance.

minor:    {min_hours: 1,  max_hours: 6}
moderate: {min_hours: 6,  max_hours: 24}
severe:   {min_hours: 24, max_hours: 72}
critical: {min_hours: 72, max_hours: 168}
```

---

## 2. Fichas por módulo

### 2.1 Reglas que valen para todos los módulos

Si un cambio en cualquier módulo choca con una de estas, **rompe**:

| Regla | De dónde sale |
|---|---|
| El motor no sabe desde qué cliente juega cada uno; ningún cliente da ventaja | D-40, D-41, regla 1 de la [arquitectura](arquitectura-modular.md) |
| Cada dato tiene un solo dueño; los demás piden, no tocan | Regla 2 |
| Los módulos se hablan por eventos | Regla 3 |
| El contenido son datos, no código | Regla 4 |
| Identificadores estables: solo se agregan, nunca se renombran ni se reutilizan | Regla 5 |
| Todo azar usa una semilla guardada | Regla 6 |
| El motor devuelve vistas, no mensajes: estado, avisos y acciones con su ID, con los textos ya traducidos; cada cliente las dibuja | Regla 7 |
| Todo en texto y por turnos | D-05 |
| Amplio pero ligero: cada sistema tiene una capa simple por defecto y una profunda opcional | D-44 |
| Combate de 6 botones como máximo y una sola elección por ronda | D-46 |
| Sin pisos: el mapa no tiene borde y moverse entre lugares toma tiempo real | D-58 |
| Sin límites duros de oficios: el freno es el costo natural del conocimiento | D-57 |
| Clases igualadas: la diferencia la hacen los oficios y el conocimiento | D-49 |
| Sumideros siempre en porcentaje | D-27 |
| El dinero real compra solo cosméticos y aceleradores; nadie paga para apostar | D-43 |
| Todo sistema consume de otros y produce para otros | D-20, D-38, [Red de sistemas](../00-vision/red-de-sistemas.md) |
| Código en inglés con notas `[ES]`; diseño y código se actualizan juntos | D-42 |

### 2.2 Mapa rápido: qué tan peligroso es tocar cada módulo

| # | Módulo | Radio de impacto | Lo más delicado de tocar |
|---|---|---|---|
| M1 | Núcleo | Muy alto: lo usan todos | Semilla del azar, reinicios diarios y semanales, forma de los eventos, IDs, cuentas |
| M2 | Héroe | Alto | Nivel 10 (protecciones de novato), Techo de la Frontera (antes, del Piso), rasgos de linaje |
| M3 | Clases y talentos | Alto | Presupuesto de poder, IDs de habilidades, utilidades clave, la barra de 6 |
| M4 | Equipo e inventario | Muy alto | Poder de Objeto (una sola fuente de verdad), durabilidad, zona que protege cada ranura, mochilas |
| M5 | Combate | Muy alto | Mitigación, datos de `GolpeRecibido`, temporizador, tope de PvP |
| M6 | Enemigos y jefes | Medio | Avisos (de su texto dependen las Tácticas y el Bestiario), botín, contagio de monstruos |
| M7 | Salud | Alto | Duraciones, contagio, qué cura la magia, protección de novato |
| M8 | Mundo | Alto | Color de zona, tiempo de viaje (D-58), ecología, clima |
| M9 | Frente, Sellos y Fundación | Alto | Ritmo de avance de la Frontera (antes, de pisos), medidores de la ciudad, requisitos de etapa |
| M10 | Misiones | Medio | Oro que pagan (inflación), rendimiento de expediciones, investigación |
| M11 | Instancias | Medio | Carriles de recompensa, reloj de rondas |
| M12 | PvP, crimen y justicia | Alto | Reglas de caída por zona, protección del Juramento de Hierro, karma |
| M13 | Economía | Muy alto | Impuestos, bandas de precio, monedas no transferibles |
| M14 | Oficios | Alto | Costo del conocimiento (D-57), vetas, rangos y exámenes |
| M15 | Social | Medio | Tamaño de grupo, vales por reenvío |
| M16 | Minijuegos y apuestas | Bajo en técnica, muy alto en reglas del dueño | D-43, tirada pública auditable, topes diarios |
| M17 | Colecciones y logros | Bajo, salvo que dé poder | Regla de las 3 vistas, nunca poder |
| M18 | Temporadas y rankings | Medio | Duración de la temporada (la usan M7, M9, M10, M25) |
| M19 | Mensajería | Alto para los clientes | Vistas, avisos, límites de Telegram |
| M20 | Administración y telemetría | Bajo en el juego, alto en el proceso | Registro de balance, informe económico |
| M21 | Simulador de balance | Bajo en el juego, alto en el proceso | Escenarios y objetivos |
| M22 | Pagos | Bajo en técnica, muy alto en reglas del dueño | D-43, aceleradores |
| M23 | Anti-trampas | Medio | Umbrales, revisión humana |
| M24 | Construcción | Medio | Jornadas por obra, protecciones, mantenimiento |
| M25 | Propiedad | Medio | Cupos, tasa autodeclarada, intereses, impuesto de la casa |

**Las cinco autopistas del impacto.** Casi toda cascada viaja por uno de estos caminos:

```mermaid
flowchart LR
  M3[M3 Clases] --> M5[M5 Combate]
  M4[M4 Equipo] --> M5
  M5 --> M6[M6 Enemigos y jefes]
  M5 --> M21[M21 Simulador]
  M5 -. eventos .-> M7[M7 Salud]
  M7 -. demanda .-> M14[M14 Oficios]
  M14 --> M4
  M14 --> M24[M24 Construcción]
  M14 --- M13[M13 Economía]
  M13 --- M25[M25 Propiedad]
  M24 --> M9[M9 Frente y Fundación]
  M9 --> M8[M8 Mundo]
  M9 --> M2[M2 Héroe]
  M13 --> M20[M20 Telemetría]
  M19[M19 Mensajería] --> CL[Telegram, web y app]
```

1. **Poder:** M3 y M4 → M5 → M6, M11, M12 y M21. Todo número de combate termina en el simulador.
2. **Cuerpo:** M5 → M7 → M14 → M13. Cada golpe es, al final, trabajo para un médico y oro que se quema en el sanatorio.
3. **Oro:** M13 con M14, M16, M24 y M25. Toda fuente de oro necesita su sumidero.
4. **Frontera y ciudad:** M9 → M8, M2, M14, M24 y M25. Pacificar una región (antes, abrir un piso) o subir de etapa una ciudad enciende servicios, lugares y rangos.
5. **Pantalla:** todos → M19 → los tres clientes. Lo que se ve es un contrato (§5).

### 2.3 Las 25 fichas

---

#### M1 · Núcleo · `engine/core`

| | |
|---|---|
| **Para qué sirve** | La base que todos usan: la cuenta del jugador, el reloj del juego, el azar con semilla, el bus de eventos y los idiomas |
| **Documentos de diseño** | [Arquitectura modular](arquitectura-modular.md), [Web y multiplataforma](web-y-multiplataforma.md) (una cuenta para los tres clientes), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §2 (duración del día) |
| **Depende de** | Nada. Es el único módulo sin dependencias |
| **Lo usan** | Todos |
| **Eventos que publica** | Propuestos: `NuevoDiaDeJuego`, `NuevaSemana` (reinicios), `CuentaVinculada` (una cuenta de Telegram que se une a la web o a la app) |
| **Eventos que escucha** | Ninguno: transporta los de los demás |
| **Datos de los que es dueño** | Cuentas con sus identidades vinculadas (Telegram, correo y otras) y el idioma de la cuenta; reloj del juego (horas en UTC); semillas de azar y sus huellas publicadas (tirada pública auditable); el bus y el registro de eventos; los archivos de idiomas (ES y EN); la lista de IDs usados y retirados |
| **Reglas que nunca se rompen** | El motor no sabe que existen Telegram, la web ni la app. Todo azar usa una semilla guardada. Un ID nunca cambia ni se reutiliza. Los temporizadores se calculan de forma perezosa: si el servidor se reinicia, nada se pierde. Ningún texto visible se escribe en el código del motor: vive en los archivos de idiomas, y el motor entrega las vistas ya traducidas (regla 7) |

**Si cambias esto, revisa:**
- **El generador de azar o cómo se guarda la semilla** → la radiografía de combate deja de repetir peleas viejas (M20); las manchas de sangre dejan de mostrar las últimas 3 rondas reales (M8, M7); el simulador pierde la comparación con mediciones anteriores (M21); las tiradas con semilla publicada dejan de poder verificarse (M16).
- **La duración del día de juego** (6 horas reales) → ver C-19.
- **La hora o el día de los reinicios** → todo lo diario y semanal: Enfoque (M14), topes del Foso y de recompensas (M12, M16, M23), Tesoro Semanal y bloqueos de mazmorras y bandas (M11), conocimiento semanal de oficios (M14), cuotas y barras semanales de la ciudad (M9), tasas y mantenimiento semanales (M25, M24), estaciones (M8).
- **La forma de un evento o del bus** → todos los que lo escuchan (columna "Eventos que escucha" de cada ficha). Un evento se amplía agregando campos con valor por defecto; nunca se le quita ni se le cambia el significado a uno.
- **Cómo se vincula una cuenta** → la entrada en los tres clientes, la detección de multicuentas y cuentas vinculadas (M23), las Gemas de la cuenta (M22), las colecciones y la reputación de cuenta (M17, M2).
- **Agregar un idioma o cambiar una clave de texto** → todos los textos de contenido (zonas, avisos de jefes, casos, misiones), las plantillas de notas en el suelo (M6), los mensajes de M19 y los tres clientes. Una clave borrada deja un hueco en pantalla.

---

#### M2 · Héroe · `engine/hero`

| | |
|---|---|
| **Para qué sirve** | Quién es cada personaje y cuánto creció: linaje, trasfondo, apariencia, nivel, experiencia y perfil |
| **Documentos de diseño** | [Creación de personaje](../03-personaje/creacion-de-personaje.md), [Progresión](../03-personaje/progresion.md) |
| **Depende de** | M1; M9 (el Techo de la Frontera depende de hasta dónde llegó la Frontera; antes, del piso del último Sello) |
| **Lo usan** | M3 (clase al nivel 10, puntos de talento por nivel), M4 (la capacidad de carga sale del linaje y el aguante), M7 (rasgo de cuerpo del linaje, nivel 10 de la protección de novato, Resolución), M10 (misiones de trasfondo), M12 y M16 (novatos fuera del PvP y del Circuito), M13 (rasgos de linaje con PNJ), M14 (rasgo de oficio, empujón del trasfondo), M15 (gremio desde el nivel 5, mentoría hasta el 20), M22 (aceleradores de experiencia), M23 (nivel mínimo para transferir) |
| **Eventos que publica** | Propuestos: `HeroeCreado`, `NivelSubido` |
| **Eventos que escucha** | `JefeDerrotado` (`BossDefeated`), `ObjetoFabricado` (`ItemCrafted`), `HeridaTratada` (`WoundTreated`) para dar experiencia. Propuestos: `CombateTerminado`, `MisionCompletada`, `InstanciaCompletada`, `SelloObtenido` |
| **Datos de los que es dueño** | Ficha del héroe (linaje, trasfondo, apariencia, nombre único), nivel, experiencia, experiencia descansada, Renombre, Resolución. Propuesta (§6.1): reputaciones y maestrías de armas y armaduras |
| **Reglas que nunca se rompen** | Ninguna racial toca daño, curación ni control en combate, y todos los linajes tienen el mismo presupuesto. No hay puntos de estadística sueltos: los puntos por nivel van a los talentos. Nada depende de la fecha en que llegaste. El Renombre nunca da daño. Cualquier linaje puede ser cualquier clase |

**Si cambias esto, revisa:**
- **Un rasgo de linaje** → la tabla de linajes de [Peligros del entorno](../05-salud/peligros-del-entorno.md) §9 y del [Bestiario](../06-contenido/bestiario.md) §5.1 (quién resiste qué contagio), las reglas de cuerpo de Salud (M7) y el oficio que mejora (M14). Si se acerca al combate, **rompe** la regla 10 de [Balance](../03-personaje/balance.md) y D-49, y hay que medir (M21). El rasgo del Goblin con PNJ nunca puede tocar el mercado entre jugadores (M13).
- **La curva de experiencia** → el ritmo de nivel frente a la Frontera (M9), cuándo llegan los árboles de héroe (nivel 50) y Ápice (90) (M3), el valor de los aceleradores (M22), del Viento de Cola (+25 %) y de la experiencia descansada.
- **El Techo de la Frontera** (antes, Techo del Piso) → C-08.
- **El nivel de la clase (10) o de la protección de novato (10)** → el tutorial del Claro (M9), heridas, enfermedades y peligros de novato (M7), PvP, robos y Circuito (M12, M16), transferencias (M23), el kit sin clase (M3). Esa regla está escrita en siete documentos (§4.7).
- **La experiencia descansada** → el valor de dormir en posada o en casa (M24) y el de los jugadores que entran poco. Nunca se suma con un acelerador del mismo tipo (M22).
- **El Renombre** → bonos de carga (M4), banco (M13), viaje (M8) y Enfoque (M14). Si da daño, **rompe** su regla.

---

#### M3 · Clases y talentos · `engine/classes`

| | |
|---|---|
| **Para qué sirve** | Qué sabe hacer cada clase y spec: recursos, habilidades, árboles de talentos, configuraciones y aportes de grupo |
| **Documentos de diseño** | [Clases y especializaciones](../03-personaje/clases-y-especializaciones.md), [Talentos](../03-personaje/talentos.md), [Balance](../03-personaje/balance.md), [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §10 (un Límite por spec) |
| **Depende de** | M1; M2 (nivel y puntos de talento) |
| **Lo usan** | M5 (habilidades y recursos que van a la barra), M11 (rol en el buscador), M12 (ajuste PvP por spec, plantillas de la arena clasificada), M21 (el simulador corre cada spec), M11 (una Prueba de Maestría por spec), M7 (Corrupción del Sacerdote Sombra y el Devorador; Remiendo del Nigromante; el Bardo baja el estrés), M14 (consumibles que copian las utilidades clave) |
| **Eventos que publica** | Propuesto: `ConfiguracionCambiada` (spec, talentos o barra) |
| **Eventos que escucha** | Propuesto: `NivelSubido` |
| **Datos de los que es dueño** | Las 15 clases y 46 specs, recursos de clase, repertorios, árboles de talentos, configuraciones guardadas (hasta 5 por spec), presupuesto de poder por spec, aportes de grupo, Límites, IDs de habilidades |
| **Reglas que nunca se rompen** | Clases igualadas: ninguna es más fuerte que otra (D-49). La spec es la unidad de balance: 100 ± 3 puntos en 6 ejes, ninguno por encima de 35 ni por debajo de 5. Kit mínimo garantizado y autonomía en solitario. Aportes de grupo de valor parecido (~3 %) que no se suman. Clamor, resurrección en combate y disipar en 4 clases o más, más un consumible fabricado. Ninguna secundaria vale más de 1,3 veces otra. En combate, 6 botones como máximo: Atacar, 3 habilidades, Huir y Mochila (D-46). Cambiar talentos y spec es gratis en un asentamiento |

**Si cambias esto, revisa:**
- **Una habilidad** (daño, costo, enfriamiento) → el presupuesto de su spec y los objetivos del simulador (M21); el ajuste PvP y el tope del 40 % (M12, M5); la Prueba de Maestría de esa spec; las Tácticas guardadas que la usan (M5) y los Ecos que pelean con ellas (M6, M12); su texto en ES y EN.
- **Quitar o renombrar una habilidad** → **rompe** configuraciones guardadas, Tácticas, registros de combate y radiografías (M20) y botones ya enviados en Telegram. Nunca se borra: se marca retirada y la nueva lleva otro ID (C-18).
- **Un recurso de clase** (por ejemplo, la Energía que sube 25 por ronda) → todas las specs de esa clase, sus rotaciones y el simulador.
- **Clamor, resurrección en combate o disipar** → los consumibles equivalentes (Tambores de Guerra, Sales de Reanimación, Desfibrilador: M14), su precio (M13) y la regla de "4 clases + consumible".
- **Un aporte de grupo o un apoyo** (Aumentación, Estratega) → la regla de no sumar y el tope de un apoyo por grupo en contenido clasificado (M11, M18).
- **Una clase nueva** (expansión) → todos los escenarios del simulador, una Prueba de Maestría nueva, roles del buscador (M11), dominio de armadura (M4), arena (M12), textos y botones en los tres clientes.
- **La barra de combate** → cualquier botón por encima de los 6 de D-46 **rompe** la decisión y el diseño de pantalla de los tres clientes (M19, §5). Quitar el botón de Defender obliga a que cada clase tenga una habilidad defensiva para responder a los avisos.
- **Algo que haga a una clase más fuerte que otra** → **rompe** D-49 aunque el simulador diga que está "dentro del margen".

---

#### M4 · Equipo e inventario · `engine/equipment`

| | |
|---|---|
| **Para qué sirve** | Todo objeto: qué es, dónde se lleva, cuánto pesa, cuánto aguanta, qué técnica da y cuánto poder resume. También las mochilas y el inventario |
| **Documentos de diseño** | [Equipamiento](../03-personaje/equipamiento.md), [Fabricación](../07-economia/fabricacion.md) (calidad y firma). Inventario y mochilas (D-47, documento en redacción) |
| **Depende de** | M1; M2 (capacidad de carga); M14 (crea los objetos fabricados); M6 (artefactos y Recuerdos) |
| **Lo usan** | M5 (estadísticas, iniciativa por peso y Celeridad, resistencias, objetos del botón Mochila), M7 (protección por zona, capa de clima, protección contra el entorno), M11 (Poder de Objeto mínimo del buscador), M12 (botín al caer, plantillas de arena, poder de guerra), M13 (el mercado ordena por Poder de Objeto), M8 (caravanas y monturas: la carga pesa en el viaje), M21, M24 (equipo de los guardias), M17 (apariencias), M23 (transferencias sospechosas) |
| **Eventos que publica** | `ObjetoDestruido` (`ItemDestroyed`). Propuestos: `ObjetoEquipado`, `ObjetoReparado` |
| **Eventos que escucha** | `GolpeRecibido` (`HitReceived`) para el desgaste; `HeroeCaido` (`HeroFallen`) para el −10 % de durabilidad en zona amarilla y el botín en roja y negra (junto con M12); `ObjetoFabricado` (`ItemCrafted`) |
| **Datos de los que es dueño** | Objetos y sus siete propiedades (tramo, calidad, rareza, encantamiento, mejoras, afijos, engarces), durabilidad actual y máxima, peso, atadura, firma; ranuras equipadas; mochilas, cinturón de combate, alforjas y botiquín (D-47); carga; la fórmula del Poder de Objeto; las técnicas de equipo |
| **Reglas que nunca se rompen** | Una sola fuente de verdad para el poder: la guerra, la arena y el buscador usan el mismo número ("la ropa no contaba"). Las reglas de equipo (nivel mínimo, atadura) se validan en el motor, en un solo lugar: ni el mercado ni el almacén se las saltan. Reparar baja la durabilidad máxima y en 0 el objeto se rompe para siempre. Las mejoras nunca llegan a la base del tramo siguiente. Cada tramo sube los números ~25 %. No hay poder prestado |

**Si cambias esto, revisa:**
- **La fórmula del Poder de Objeto** → requisitos del buscador (M11), orden del mercado (M13), poder de guerra (M12), Mercado Negro, simulador (M21).
- **El desgaste o la pérdida de máxima al reparar** → cuántas semanas dura una pieza, la demanda de herreros (M14), el oro quemado en reparaciones (M13) y el valor del herrero frente al PNJ. Es el final de la cadena C-01.
- **Qué zona protege cada ranura** → probabilidad y gravedad de heridas por zona (M7), la barra de Contagio que frena la armadura de la zona ([Bestiario](../06-contenido/bestiario.md) §5.1), `/cuerpo` y la pantalla de equipo en los clientes.
- **Una técnica de equipo** → con D-46, una técnica puede ocupar una de las 3 casillas de habilidad, y las marcadas 🛡 o 💨 son respuestas que cuestan Aguante ([Equipamiento](../03-personaje/equipamiento.md) §7). Cambian la demanda de cada tipo de arma y armadura (M13, M14), las Tácticas y el simulador.
- **Las mochilas o el cinturón** (D-47) → lo que entra en el botón Mochila del combate (M5), la carga, los tipos de mochila por oficio (M14) y la pantalla de inventario de los tres clientes.
- **La tabla de carga** → iniciativa y Aguante (M5), las placas que hunden en agua profunda (M7), el Taurino (M2), el Renombre de carga.
- **La atadura** → qué se comercia (M13), mulas y comercio con dinero real (M23), botín en PvP (M12).
- **El salto por tramo (~25 %)** → todo el balance vertical (M21, M6), el Viento de Cola y el valor del equipo viejo (venderlo, desmontarlo, vestir a un alt).

---

#### M5 · Combate · `engine/combat`

| | |
|---|---|
| **Para qué sirve** | Resuelve cada pelea por rondas: quién actúa primero, qué daño hace, qué barras y estados se mueven y cuándo alguien queda derribado |
| **Documentos de diseño** | [04 · Combate](../04-combate/README.md), [Ronda y acciones](../04-combate/ronda-y-acciones.md) (en revisión por D-46), [Daño y estados](../04-combate/dano-y-estados.md), [Avisos y tácticas](../04-combate/avisos-y-tacticas.md), [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) |
| **Depende de** | M1 (semilla); M3 (habilidades de clase); M4 (estadísticas, peso, técnicas, cinturón); M6 (qué hace cada enemigo). Lee, sin escribir, el cuerpo de M7 (penalizaciones de heridas, condiciones y entorno) |
| **Lo usan** | M6; M10 (resolución rápida de encargos y expediciones, cacerías); M11; M12 (arenas, campos, invasiones, Foso); M9 (asalto al Guardián, defensa de la ciudad); M24 (defensa de construcciones); M21 (el simulador corre este mismo motor); M20 (radiografía de combate) |
| **Eventos que publica** | `GolpeRecibido` (`HitReceived`: zona, tipo de daño, crítico, vida antes y después), `HeroeDerribado` / `HeroeCaido` (`HeroDowned` / `HeroFallen`), `ParteRota` (`PartBroken`). Propuesto: `CombateTerminado` (resultado y contribución de cada uno) |
| **Eventos que escucha** | El entorno al principio de cada ronda (M7 y M8). Propuesto: `ConfiguracionCambiada` (M3) |
| **Datos de los que es dueño** | El estado de cada pelea (cola de iniciativa, Vida, Aguante, Firmeza, Postura, Escudo de ruptura, Límite, estados por acumulación, amenaza, filas y formación), las fórmulas de daño y mitigación, las reglas de PvP, los temporizadores de ronda, el registro de rondas (de ahí salen las manchas) y las Tácticas de cada héroe |
| **Reglas que nunca se rompen** | Rondas simultáneas, nunca reflejos. 6 botones como máximo y una sola elección por ronda (D-46). Todo golpe usa la semilla. Firmeza: nadie queda aturdido más de dos veces seguidas. La armadura cuenta siempre (nada de daño mínimo que la ignore). El daño por ronda no pasa por la armadura; la acumulación sí. Derribado 3 rondas antes de caer, y caer siempre deja una herida. En PvP, ningún golpe quita más del 40 % de la vida máxima. Las Tácticas no valen en el Guardián ni en la arena clasificada. Las mecánicas avanzadas no suman botones y tienen tope. Combate no escribe heridas: publica eventos |

**Si cambias esto, revisa:**
- **La fórmula de mitigación** → C-01.
- **El temporizador de ronda** → C-10.
- **El tope de golpe o la amortiguación de PvP** → C-16.
- **El Aguante, las respuestas o la Firmeza** → el valor de leer avisos (M6), las armaduras pesadas que bajan el máximo (M4), el calor y la sed que lo bajan (M7), el control en PvP (M12) y las specs de control (M21). Con D-46, el Aguante paga las respuestas al aviso y 🌀 Esquivar ([Ronda y acciones](../04-combate/ronda-y-acciones.md) §3 y §5).
- **Las 3 rondas de derribado** → resurrecciones en combate (M3), Sales de Reanimación (M14), heridas garantizadas (M7), reloj de Mítica+ (M11), derribos por el entorno (M7).
- **Los datos de `GolpeRecibido`** → Salud (heridas y barra de Contagio), Equipo (durabilidad) y Mente (estrés) al mismo tiempo. Cambiar el significado de un campo (por ejemplo, el daño antes o después de la armadura) cambia cuántas heridas aparecen **sin dar ningún error** ([Convenciones](convenciones-de-codigo.md) §5.2).
- **Una mecánica avanzada** (ruptura, golpe extra, técnicas combinadas, superficies, terreno, emboscada, moral, Límite, reacciones avanzadas, apostar turnos) → su eje en el presupuesto de poder y su objetivo en el simulador ([Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §15), los oficios que viven de ella (aceites, frascos, bombas, botas: §14 de ese documento), las Tácticas por defecto que la usan en la capa simple (D-44).
- **El rendimiento de la resolución rápida** → el botín y el desgaste de quien no juega a mano (M10), el incentivo para usar bots (M23), la oferta de materiales comunes (M13).

---

#### M6 · Enemigos y jefes · `engine/enemies`

| | |
|---|---|
| **Para qué sirve** | Cómo pelea cada enemigo: repertorio, avisos (también los que mienten), fases, postura, escudo de ruptura, partes, a quién elige como objetivo, qué contagia y qué deja |
| **Documentos de diseño** | [Jefes](../06-contenido/jefes.md), [Bestiario](../06-contenido/bestiario.md), [Avisos y tácticas](../04-combate/avisos-y-tacticas.md), [Daño y estados](../04-combate/dano-y-estados.md) §3 (partes), [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §3 y §9 (ruptura, moral) |
| **Depende de** | M5; M8 (dónde vive cada criatura y su población); M17 (conocimiento del Bestiario para las pistas); M21 (prueba de que el jefe es justo) |
| **Lo usan** | M5; M9 (el Guardián de cada región; Pioneros; Eco del Guardián; incursiones a la ciudad); M10 (presas de cacería, jefes de campo); M11 (jefes de mazmorra y banda); M4 y M14 (artefactos, Recuerdos, planos, materiales de partes); M13 (precios de materiales de monstruo); M7 (contagios de monstruo); M17 (Bestiario); M18 (jefe semanal por gremio); M15 y M16 (jefe errante con Cuerno de Invocación) |
| **Eventos que publica** | `JefeDerrotado` (`BossDefeated`). Propuestos: `MovimientoVisto` (para que M17 cuente las 3 vistas), `MonstruoConNombre` (un alfa que asciende y sale en la Gaceta) |
| **Eventos que escucha** | `ParteRota` (`PartBroken`): quita el movimiento de esa parte |
| **Datos de los que es dueño** | Ficha de cada enemigo (vida, postura, escudo, debilidades, resistencias, repertorio de 8 a 12 movimientos, textos de aviso, fases al 66 % y al 33 %, partes, contagios, modificadores), las 19 familias, los monstruos únicos, las tablas de botín, los signos de invocación, los espíritus, las notas en el suelo |
| **Reglas que nunca se rompen** | Todo golpe grande se avisa una ronda antes (dos si es devastador). Los avisos que mienten siempre dejan una pista. El jefe no escala con tu nivel: la mecánica mata igual. Un grupo que juega bien gana con equipo del tramo sin mejoras; uno que juega mal pierde aunque tenga dos tramos más. Las notas en el suelo solo usan plantillas. Vida de jefe de 5 o 6 dígitos. El Eco del Guardián tiene la misma mecánica. Un monstruo con nombre nunca pasa los números de su tramo |

**Si cambias esto, revisa:**
- **Un movimiento o su aviso** → las Tácticas que reaccionan a avisos (M5), la pista del Bestiario (M17: la pista vieja ahora miente), las fichas del Informante que se venden (M14, M13), las manchas de sangre de ese jefe (M8), la prueba de justicia (M21), los retos contextuales de anti-trampas (M23) y el texto en ES y EN.
- **La vida o el escalado** → la duración de las peleas, el reloj de Mítica+ (M11), la contribución mínima para el Sello (M9), el escalado con invocados y el jefe semanal compartido.
- **Las partes, las debilidades o lo que sueltan** → materiales exclusivos y recetas temáticas (M14, M13), la calidad de pieza en cacerías (M10), el valor del Cazador de Puntería (M3) y de los aceites que cambian el tipo de daño (M14).
- **Lo que contagia un monstruo** → C-07.
- **El botín de jefe** (artefactos, Recuerdos, planos) → recetas únicas (M14), precios (M13), protección contra mala racha (§6.1).
- **A quién elige como objetivo** → la presión sobre sanadores y el balance de sanadores y tanques (M21).
- **La regla de las 3 vistas** → vive en M17, pero cambia la dificultad real de todos los jefes.

---

#### M7 · Salud · `engine/health`

| | |
|---|---|
| **Para qué sirve** | Todo lo que le pasa al cuerpo y a la mente: heridas, condiciones, peligros del entorno, contagio y enfermedades, estrés, secuelas, muerte y rasgos adquiridos |
| **Documentos de diseño** | [05 · Salud](../05-salud/README.md), [Heridas](../05-salud/heridas.md), [Condiciones](../05-salud/condiciones.md), [Peligros del entorno](../05-salud/peligros-del-entorno.md), [Enfermedades](../05-salud/enfermedades.md), [Mente](../05-salud/mente.md), [Secuelas y muerte](../05-salud/secuelas-y-muerte.md), [Curación](../05-salud/curacion-y-tratamientos.md), [Rasgos adquiridos](../05-salud/rasgos-adquiridos.md), [Animales y cultivos](../05-salud/animales-y-cultivos.md), [Bestiario](../06-contenido/bestiario.md) §5 y §6 (contagio) |
| **Depende de** | M1; M5 (eventos); M4 (protección por zona y de clima); M8 (clima, estación, terreno, rigor del nodo, color de zona); M6 (qué contagia cada monstruo); M2 (linaje, nivel, Resolución); M14 (calidad de los remedios y nivel del médico); M24 (descanso en casa y enfermería) |
| **Lo usan** | M5 (penalizaciones); M14 (demanda de Medicina, Alquimia, Herboristería, Sastrería, Ingeniería y Cocina); M13 (el sanatorio como sumidero y techo de precio); M9 (salud pública de la ciudad, brotes y epidemias); M10 (cacería de plaga, investigación de la cura); M12 (Juramento de Hierro en PvP); M12 y M16 (apto o no apto en el Foso); M17 (cicatrices como trofeo); M19 (`/cuerpo` y avisos de etapa); M23 (retos contextuales) |
| **Eventos que publica** | `HeridaCreada` / `HeridaTratada` (`WoundCreated` / `WoundTreated`), `EnfermedadContagiada` (`DiseaseContracted`). Propuestos: `EtapaDeEntornoCambiada`, `CicatrizGanada`, `AflicionSufrida`, `PersonajeCaidoParaSiempre` (Juramento de Hierro) |
| **Eventos que escucha** | `GolpeRecibido` (`HitReceived`), `HeroeDerribado` / `HeroeCaido` (`HeroDowned` / `HeroFallen`). Propuestos: `ClimaCambiado` y `EstacionCambiada` (M8), `ObjetoEquipado` (M4), `AccidenteDeObra` (M24) |
| **Datos de los que es dueño** | Heridas; condiciones (dolor, sangrado, fatiga, Sustento, temperatura, toxicidad, Hidratación, Contaminación); barras de Contagio; etapas de peligro; enfermedades e inmunidades; estrés, cordura y corrupción; cicatrices, miembros perdidos y prótesis puestas; rasgos adquiridos; el estado de Juramento de Hierro. Propuesta (§6.1): la salud de animales y cultivos |
| **Reglas que nunca se rompen** | Salud es el único que escribe heridas. Siempre hay salida. Nunca por un solo mal dado: una secuela permanente pide varias fallas. Máximo 2 heridas graves o críticas. Protección de novato hasta el nivel 10. El tiempo fuera de línea cura y no castiga. La magia no cura heridas graves (salvo Restauración, una vez al día). Los sanadores de clase no curan enfermedades: las trata quien estudió Medicina (D-11). Una enfermedad seria a la vez, salvo en epidemias. El contagio se acumula en una barra, no es azar ciego. Nadie muere para siempre fuera del Juramento de Hierro. Los peligros avisan antes, la retirada desde la etapa grave llega siempre y no suben más de dos a la vez. Los rasgos mueven como mucho un 3 % el combate |

**Si cambias esto, revisa:**
- **La duración de las heridas** → C-02.
- **El contagio** → C-07.
- **Cuándo aparece una herida** (crítico, 50 %, 25 %, derribo) → el número de heridas por pelea, la demanda de médicos (M14), los no aptos del Foso (M12, M16), la cadena hacia secuelas. Combate manda el dato en `GolpeRecibido` (M5).
- **Lo que cura la magia** → si la magia cura heridas graves o enfermedades, **rompe** D-11 y la economía de servicios (M14, M13).
- **Una barra de entorno** (Hidratación, Contaminación, etapas) → el equipo de protección que fabrican más de diez oficios (M14), el valor de los materiales de zonas hostiles (M13), la pantalla `/cuerpo` y la cabecera de expedición en los tres clientes (§5).
- **El tope de 2 heridas graves** → el agotamiento, el ritmo de instancias (M11), la cadena de secuelas.
- **Las reglas del Juramento de Hierro** → protección en PvP (M12), Duelo de Hierro (M12, M16), Salón de los Caídos (M19), ranking (M18), creación de personaje (M2).
- **Un rasgo adquirido** → si pasa del 3 % en combate o del 10 % en su oficio, **rompe** su límite y hay que medir (M21).
- **El estrés** → el valor de bardos, taberna, templo y banquetes (M3, M14, M16), las aflicciones del Foso y el ánimo de la ciudad (M9).

---

#### M8 · Mundo · `engine/world`

| | |
|---|---|
| **Para qué sirve** | El escenario: el mapa sin borde (zonas, regiones y lugares; antes, pisos), nodos, zonas de color, terrenos, clima, estaciones, día y noche, ecología, viaje y manchas |
| **Documentos de diseño** | [02 · Mundo](../02-mundo/README.md), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (D-58, reemplaza a [Torre y pisos](../02-mundo/torre-y-pisos.md)), [Geografía y recursos](../02-mundo/geografia-y-recursos.md), [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md), [Peligros del entorno](../05-salud/peligros-del-entorno.md) §4 (rigor por terreno y tramo), [Bestiario](../06-contenido/bestiario.md) §10 (ecología) |
| **Depende de** | M1 (reloj); M9 (una región nueva pasa por descubrimiento, esfuerzo de guerra, Guardián y asentamiento antes de poblarse) |
| **Lo usan** | M7 (clima, rigor, zona); M9 (sitios de nodo para fundar; ecología que sube la amenaza de la ciudad); M10 (nodos de expedición y rastreo); M12 (zonas de color, territorios); M13 (un mercado por asentamiento, transporte por peso); M14 (cada terreno produce lo suyo; nodos para las vetas); M24 (parcelas y reglas por zona); M6 (dónde aparece cada criatura); M17 (atlas, descubridores de lugares) |
| **Eventos que publica** | Propuestos: `ClimaCambiado`, `EstacionCambiada`, `PoblacionCambiada` (Escasa, Normal, Abundante, Plaga), `NodoDescubierto`, `ManchaCreada` |
| **Eventos que escucha** | `HeroeCaido` (`HeroFallen`) para dejar la mancha; `PisoAbierto` (`FloorOpened`; con D-58, el avance de la Frontera) para que la región sea jugable. Propuestos: `PresaCazada` (baja la población), `ObraTerminada` (puentes, caminos y postas nuevas) |
| **Datos de los que es dueño** | Zonas y regiones del mapa, nodos y conexiones; el color de zona de cada nodo; terrenos; rigor de peligros por nodo; clima, estación y hora del día; poblaciones de especies; rutas y costo de viaje; manchas de sangre; rumores. Propuesta (§6.1): yacimientos únicos y Vigor |
| **Reglas que nunca se rompen** | En zona azul no se pelea ni hay peligro mortal. Moverse entre lugares toma tiempo real (D-58). Ninguna zona es autosuficiente (D-33). El rigor nunca pasa de 3. Las criaturas nativas no sufren su entorno. El mapa es contenido: sus zonas y biomas se describen en datos, no en código (regla 4) |

**Si cambias esto, revisa:**
- **El color de zona de un nodo** → qué se pierde al caer ahí (C-11), PvP e invasiones (M12), qué se puede construir (M24), recompensas de encargos (M10).
- **El tiempo de viaje** (antes, el costo de la piedra de paso por peso) → C-15.
- **La ecología** (cuánto crece o baja cada población) → precios de materiales de monstruo (M13), amenaza e incursiones a la ciudad (M9) y a las construcciones (M24), el tablón de caza (M10), las migraciones y los brotes en la fauna (M7).
- **El clima o las estaciones** → enfermedades de temporada (M7), rigor de peligros (+1 por clima, M7), cosechas, inviernos y despensa de la ciudad (M9, M14), jornadas de obra (M24), rastros de caza (M10).
- **Los terrenos de una zona o región** → qué produce y qué le falta, y por lo tanto las rutas de comercio (M13), la sal y la comida que tiene que comprar una ciudad (M9) y dónde conviene fundar.
- **Las manchas** (cuánto duran, qué muestran) → recuperar la Esencia (M13), aprender de muertes ajenas (M6), la semilla (M1).

---

#### M9 · Frente, Sellos y Fundación · `engine/front`

| | |
|---|---|
| **Para qué sirve** | La conquista y la vida política del mapa: avanzar la Frontera región por región (antes, abrir pisos y ganar Sellos), fundar ciudades y sostenerlas (comida, salud, ánimo, seguridad, orden y amenaza), gobierno, cismas, comunidades y crisis |
| **Documentos de diseño** | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (D-58: las fases de [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.1 pasan a las regiones), [Fundación y cisma](../02-mundo/fundacion-y-cisma.md), [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md), [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md), [Crisis](../02-mundo/crisis-problemas-y-soluciones.md), [Facciones](../02-mundo/facciones.md), [El Colapso y las comunidades](../02-mundo/el-colapso-y-las-comunidades.md) (D-45) |
| **Depende de** | M8; M6 (Guardián, bestias de las incursiones); M10, M11, M12, M14 y M2 (las 6 pruebas del Sello, que se retira con D-58); M14 y M24 (las necesidades se cubren con oficios y las etapas son obras); M13 (tesoro e impuestos); M7 (brotes y epidemias); M5 y M24 (defensa de la ciudad por rondas) |
| **Lo usan** | M2 (Techo de la Frontera); M8 (regiones nuevas); M12 (la guerra de castillos nace con el primer cisma; las leyes deciden qué es delito); M13 (mercados nuevos; impuestos locales); M14 (los entrenadores dependen del ala de Oficios construida y abastecida; especialidad de cada capital); M16 (leyes del juego, ala de la Fortuna); M24 (obras de servidor); M25 (plazas y parcelas nuevas, licencias del Castillo, impuesto de la casa); M18 (Pioneros por facción); M19 (aviso escalonado, Gaceta, `/ciudad`) |
| **Eventos que publica** | `PisoAbierto` (`FloorOpened`; con D-58, avance de la Frontera, nombre pendiente). Propuestos: `FaseDePisoCambiada` (de región, con D-58), `SelloObtenido` (se retira con D-58), `EtapaDeCiudadCambiada`, `MedidorDeCiudadCambiado`, `IncursionLanzada`, `CrisisIniciada`, `LeyAprobada`, `CismaDeclarado`, `CastilloFundado` |
| **Eventos que escucha** | `JefeDerrotado` (`BossDefeated`) para Pioneros y Sellos; `EnfermedadContagiada` (`DiseaseContracted`) para brotes. Propuestos: `PoblacionCambiada` (amenaza e invasiones), `ObraTerminada`, `DefensaResuelta`, `TemporadaTerminada` (fin de mandatos), `NuevoDiaDeJuego` (la cuenta diaria de la ciudad) |
| **Datos de los que es dueño** | La Frontera y la fase de cada región (antes, el Frente y cada piso), el mapa del servidor, las metas del Esfuerzo de Guerra, los Pioneros; el estado de cada asentamiento (etapa, experiencia de nodo, vasallos, población de aldeanos, despensa y raciones, medidores, amenaza, racha de etapa, cuotas y registro de aportes, pedidos); gobierno (cargos, leyes, mandatos); castillos, comunidades y relaciones; crisis activas |
| **Reglas que nunca se rompen** | Una región no se puebla hasta que cae su Guardián (D-58 lleva a las regiones las cuatro fases del piso). Los jefes de mundo siguen, repartidos por el mapa (D-08, D-58). Los Pioneros ganan prestigio, nunca poder. Gobernador electo con mandatos que vencen por temporada (D-29), máximo dos seguidos. Construir no alcanza: una etapa se sube sosteniendo sus mínimos y superando incursiones. Nada personal se pierde aunque la ciudad caiga; bajar de etapa apaga edificios, no los destruye. Cisma con mínimo de firmas y 7 días de plazo; tope de castillos. Antes del primer cisma no hay guerra de castillos. Ninguna crisis arruina a nadie para siempre |

**Si cambias esto, revisa:**
- **El ritmo de avance de la Frontera** (antes, de apertura de pisos) → C-05.
- **El consumo de comida o los umbrales de la despensa** → C-06.
- **El Techo de la Frontera o el Viento de Cola** → C-08.
- **La amenaza** (qué la sube, fuerza de la incursión) → la demanda de murallas, guardias y armas (M24, M14), los contratos de caza de control (M10), las leyes del Ecologista (M8), la comida de los guardias (C-06) y el valor de la torre de vigía.
- **Los requisitos de etapa** (población, despensa sostenida, racha, Noche de prueba) → cuánto tarda el Claro en llegar a Castillo (P-55), cuándo se encienden entrenadores, subastas, crédito, minijuegos y sanatorio (M14, M25, M13, M16, M7).
- **Las pruebas del Sello** (el Sello se retira con D-58; si su papel pasa a otra pieza, esto vale para ella) → la demanda de mapas (cartógrafos, M14), del Laberinto (M11), de la campaña (M10), de los encargos artesanales (M14) y de la Senda de sangre (M12). Quitar la prueba de PvP **rompe** el principio de que el PvP es opcional para progresar ([PvP](../06-contenido/pvp.md)).
- **El mínimo para un cisma o el tope de castillos** → cuántas facciones hay (M12, M15), el tamaño de cada ciudad para sostener sus medidores, las plazas y licencias por castillo (M25).
- **Los poderes del gobernador** → impuestos locales e impuesto de la casa (M13, M25, D-48), cuarentenas (M7), licencias (M25, M16), raciones y jornadas extra (C-06), vedas del Ecologista (M14, M8).
- **Las comunidades PNJ del Colapso** (D-45) → dónde se paga el impuesto de la casa (M25), qué reglas valen en cada reino (M12, M16), cuánto cuesta fundar en lugar de unirse.

---

#### M10 · Misiones · `engine/quests`

| | |
|---|---|
| **Para qué sirve** | Lo que hay para hacer fuera de las instancias: campañas, encargos con temporizador, tablones, expediciones, cacerías e investigaciones |
| **Documentos de diseño** | [Misiones y exploración](../06-contenido/misiones-y-exploracion.md), [Cacerías](../06-contenido/cacerias.md), [Investigaciones](../06-contenido/investigaciones.md) |
| **Depende de** | M5 (combates y resolución rápida); M8 (nodos, ecología, clima, noche); M6 (presas); M2 (trasfondo); M7 (el cuerpo se gasta en cada paso); M14 (desuello, herramientas de caza); M9 (casos que cambian el asentamiento, pedidos de la ciudad) |
| **Lo usan** | M9 (pruebas del Sello: campaña y cartografía; contratos de caza de control que bajan la amenaza); M2 (experiencia); M13 (el oro de misiones es una fuente de oro); M14 y M24 (recetas y planos que se recuperan investigando tras el Colapso, D-45); M7 (curas y vacunas investigadas); M12 (casos de crímenes entre jugadores); M17 (Bestiario, trofeos, descubrimientos); M16 (bestias vivas para el Foso); M8 (cazar baja la población) |
| **Eventos que publica** | Propuestos: `MisionCompletada`, `EncargoTerminado`, `PresaCazada`, `CasoResuelto`, `CuraDescubierta`, `InvestigacionCompletada` |
| **Eventos que escucha** | `HeroeCaido` (`HeroFallen`): se pierde lo de la expedición según la zona. `EnfermedadContagiada` (`DiseaseContracted`): cacería de plaga. Propuestos: `CrisisIniciada` (pedidos), `PoblacionCambiada` (el tablón paga más por lo que sobra) |
| **Datos de los que es dueño** | Misiones, casos y contratos de caza (datos); progreso de cada héroe; colas de encargos; tableros de pistas; el generador de casos rápidos; rangos de cazador y de investigador |
| **Reglas que nunca se rompen** | Cada caso tiene una solución lógica que se deduce con las pistas. Los casos son datos. En los casos de servidor los detalles cambian por jugador. Equivocarse en un caso rápido no castiga. El tablón paga más por lo que sobra y deja de pagar por lo que escasea |

**Si cambias esto, revisa:**
- **El oro que pagan misiones y encargos** → la inflación (M13; crisis de inflación en M9) y el informe económico (M20).
- **Lo que rinde una expedición** → la oferta de materiales de zona (M13, M14) y el valor de arriesgar en zonas rojas (M12).
- **La cola de encargos** (tamaño, duración) → el juego de toque, las casillas extra que vende M22 como comodidad y el incentivo para usar bots (M23).
- **Las cacerías** → poblaciones (M8), amenaza de la ciudad (M9), calidad de pieza para recetas excelentes (M14), bestias para el Foso (M16), trofeos (M17, M24).
- **La velocidad de la investigación** → cuánto tarda el servidor en recuperar recetas y planos tras el Colapso (M14, M24, D-45), la duración de las epidemias (M7, M9) y la carrera de médico (M14).

---

#### M11 · Instancias · `engine/instances`

| | |
|---|---|
| **Para qué sirve** | El contenido en instancia: mazmorras, Mítica+ con reloj de rondas, Profundidades con compañero, bandas y el buscador de grupos |
| **Documentos de diseño** | [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md), [Misiones y exploración](../06-contenido/misiones-y-exploracion.md) §4-8 |
| **Depende de** | M5, M6, M15 (grupos), M3 (roles), M4 (Poder de Objeto mínimo), M1 (bloqueos semanales) |
| **Lo usan** | M9 (el Laberinto es prueba del Sello), M18 (temporadas y puntuación de Mítica+), M4 (botín y Tesoro Semanal), M13 (Esencia, artefactos), M2 (las mazmorras lideran en experiencia), M17 (logros), M16 (apuestas a Mítica+) |
| **Eventos que publica** | Propuestos: `InstanciaCompletada` (nivel, rondas usadas), `LlaveCambiada`, `BotinRepartido` |
| **Eventos que escucha** | `JefeDerrotado` (`BossDefeated`); `HeroeCaido` (`HeroFallen`): cada caída suma rondas al reloj |
| **Datos de los que es dueño** | Mazmorras y bandas (datos), bloqueos de cada jugador, Llaves del Piso, afijos de la semana, la cola del buscador, el compañero de Profundidades, el resultado de cada corrida. Propuesta (§6.1): Laberinto, Laberinto Cambiante, Pruebas de Maestría, Pesadillas y Tesoro Semanal |
| **Reglas que nunca se rompen** | Caer en una instancia no hace perder nada material. Al cambiar el tamaño de una banda cambian la vida y la postura del jefe, nunca su mecánica. Botín personal por defecto, con 2 horas para regalarlo. En grupos al azar, la tirada se ve. Cada contenido da algo que los demás no dan (carriles) |

**Si cambias esto, revisa:**
- **El reloj de rondas o los afijos** → cuánto sube cada llave, la puntuación de temporada (M18), el Tesoro Semanal (M4), las apuestas a Mítica+ (M16).
- **Las recompensas de un carril** (mazmorras, bandas, Profundidades) → si un contenido pasa a dar lo mismo que otro, se pierde la regla de carriles; mueve Esencia (C-03) y materiales (M13).
- **Los bloqueos** → cuánto se juega por semana y la oferta de artefactos (M13, M14).
- **El tamaño del grupo (5) o de la banda (10 a 25)** → la composición (M3), el escalado de jefes y de su escudo de ruptura (M6), el grupo de M15.
- **El temporizador** → C-10.

---

#### M12 · PvP, crimen y justicia · `engine/pvp`

| | |
|---|---|
| **Para qué sirve** | El conflicto entre jugadores y sus consecuencias: zonas, karma, invasiones, arenas, campos, guerra de castillos, territorios, delitos, Infamia, tribunal, prisión y peleas clandestinas |
| **Documentos de diseño** | [PvP](../06-contenido/pvp.md), [Crimen y justicia](../06-contenido/crimen-y-justicia.md), [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) |
| **Depende de** | M5; M8 (zonas); M9 (castillos, facciones, leyes); M4 (botín; poder de guerra con la misma fuente de verdad); M7 (heridas, Juramento de Hierro); M10 (detectives); M15 (gremios y alianzas); M24 (fortalezas, prisión); M13 (recompensas en custodia, multas, seguros); M23 (cuentas vinculadas) |
| **Lo usan** | M13 (materiales de riesgo y botín), M18 (temporadas de arena, trofeos de guerra), M16 (apuestas a la arena y a la guerra; el Foso), M14 (materiales de zonas negras), M25 (vetas exclusivas de territorio), M17 (títulos), M8 (el karma rojo no entra a asentamientos azules) |
| **Eventos que publica** | Propuestos: `KarmaCambiado`, `DelitoCometido`, `RecompensaPublicada`, `CondenaDictada`, `TerritorioConquistado`, `BatallaDeCastillosResuelta`, `RedadaRealizada` |
| **Eventos que escucha** | `HeroeCaido` (`HeroFallen`) para el karma. Propuestos: `CasoResuelto` (orden de captura), `LeyAprobada`, `CastilloFundado`, `ApuestaResuelta` (amaños), `ContratoIncumplido` (recompensa por deudores) |
| **Datos de los que es dueño** | Karma e Infamia; recompensas; condenas y prisión; clasificación de arenas (Glicko-2); campos en curso; puestos avanzados; territorios y ventanas de asedio; delitos y rastros; juicios; fichas de luchador y calor de los locales del Circuito |
| **Reglas que nunca se rompen** | El PvP es opcional para progresar. Tope de golpe del 40 %. Nunca invasiones en zona azul, en amarilla sin bandera ni contra un nivel mucho menor. El Juramento de Hierro no se ataca fuera de zona negra y arenas. Poder de guerra con la misma fuente de verdad. Quien ataca no defiende; solo cuentan los activos de 3 días. El defensor elige la ventana de asedio. Nunca se roba lo equipado fuera de botín completo, ni la bóveda, ni a novatos; un mismo ladrón, una vez por día a la misma víctima. En el Circuito: consentimiento de los dos, rendirse siempre se puede y nunca se pierde lo no apostado |

**Si cambias esto, revisa:**
- **Lo que se pierde al caer por zona** → C-11.
- **El tope de golpe o la amortiguación de PvP** → C-16.
- **Los umbrales de karma** (naranja 1 hora; rojo con 3 muertes en 24 horas) → bandidos y cazarrecompensas, acceso a asentamientos (M8), guardias que no venden (M13), refugios de forajidos.
- **El equipo normalizado de la arena clasificada** → si se quita, gana quien farmeó más; va contra la recomendación de P-30 y hay que medir la arena (M21).
- **Las reglas de la guerra de castillos** → trofeos (M18); puestos que dan descuento de impuestos, veta y peaje (M13, M14, M8); la regla de activos (M23).
- **Los delitos o las penas** → casos para detectives (M10), multas como sumidero (M13), tribunal (juez mayor en M9), rasgo *Mala fama* (M7), orden de la ciudad (M9).
- **Las reglas del Foso** → apuestas del Circuito (M16), heridas con tope (M7), sumideros de la casa (M13).

---

#### M13 · Economía · `engine/economy`

| | |
|---|---|
| **Para qué sirve** | El dinero y el comercio: monedas, mercados con libro de órdenes, impuestos, Mercado Negro, contratos, correo y transferencias |
| **Documentos de diseño** | [Economía](../07-economia/economia.md), [Monetización](../07-economia/monetizacion.md) (reglas del oro, D-43) |
| **Depende de** | M1; M4 (los objetos que se venden); M8 (un mercado por asentamiento, transporte); M9 (impuestos locales, leyes); M23 (revisión de comercio sospechoso); M25 (los puestos bajan el impuesto) |
| **Lo usan** | Casi todos: M14, M16, M24, M25, M12, M7 (sanatorio), M9 (tesoro, mercader de emergencia), M10 (pagos de misiones), M15 (banco de gremio), M20 (informe económico) |
| **Eventos que publica** | `OrdenEjecutada` (`OrderFilled`). Propuestos: `OroTransferido`, `OroQuemado` (cada sumidero), `ContratoIncumplido` |
| **Eventos que escucha** | `PisoAbierto` (`FloorOpened`): mercado nuevo. `ParteRota` (`PartBroken`): material exclusivo. `ObjetoFabricado` (`ItemCrafted`). Propuesto: `SancionAplicada` (M23 congela el comercio) |
| **Datos de los que es dueño** | Saldos de oro, Esencia, Honor y moneda de temporada; libros de órdenes y custodias; historial de precios y bandas de precio; impuestos y comisiones; el Mercado Negro; contratos, seguros y correo |
| **Reglas que nunca se rompen** | Sumideros siempre en porcentaje (D-27). Precio mínimo y máximo obligatorio (D-26). Esencia, Honor, reputación y moneda de temporada no se transfieren (D-28). El oro nunca se vende por dinero real (D-43). El oro que entra tiene que salir, y se mide cada mes. Todo trato importante pasa por custodia del bot. Economía es el único que mueve oro |

**Si cambias esto, revisa:**
- **Los impuestos del mercado** → C-04.
- **La velocidad de la Esencia** → C-03.
- **El porcentaje quemado en transferencias** → lavado de oro y mulas (M23), préstamos y regalos entre amigos, bancos de gremio (M15).
- **El Mercado Negro** (qué compra y a cuánto) → cuánto equipo sueltan los monstruos (M6, M10), la demanda de artesanos (M14), el retiro de equipo viejo.
- **Las bandas de precio** → comercio con dinero real (M23), especulación, precios de materiales raros. Quitarlas **rompe** D-26.
- **El vencimiento de órdenes** (7 días) → tasas repetidas (sumidero) y mercados llenos de órdenes viejas.
- **Una moneda nueva** → va contra el principio de "pocas monedas" de [Economía](../07-economia/economia.md) §2; si es no transferible, entra en D-28; si se compra con dinero real, **rompe** D-43.

---

#### M14 · Oficios · `engine/professions`

| | |
|---|---|
| **Para qué sirve** | Cómo se produce todo: recolectar, refinar, fabricar (con minijuego o rápido), recetas, planos, calidad de las vetas, rangos con exámenes y especializaciones, incluidos Medicina y Construcción |
| **Documentos de diseño** | [Profesiones](../07-economia/profesiones.md), [Fabricación](../07-economia/fabricacion.md), [Profundidad de un oficio](../07-economia/profundidad-de-un-oficio.md), [Curación](../05-salud/curacion-y-tratamientos.md) §0 y §4 (Medicina), [Sistema de construcción](../09-construccion/sistema-de-construccion.md) §2 (rangos de Construcción), [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) §3 (entrenadores), [Investigación y maestría](../07-economia/investigacion-y-maestria.md) (D-54) |
| **Depende de** | M1; M2; M4 (crea los objetos); M8 (terrenos y nodos); M9 (entrenadores según el ala de Oficios; especialidad de la capital); M13 (mercado y pedidos); M24 (estaciones en casa y gremio); M10 (recetas y planos investigados) |
| **Lo usan** | M4, M7, M24, M9 (comida, conservas, herramientas comunes; contribución artesanal del Sello), M13, M16 (dados, mazos y sus versiones trucadas), M12 (Dedos de Sangre, Grilletes, armas de asedio), M6 (Cuernos de Invocación), M5 (aceites, frascos y bombas de las mecánicas avanzadas), M3 (consumibles de utilidades clave), M17 (firma, obras maestras, recetario) |
| **Eventos que publica** | `ObjetoFabricado` (`ItemCrafted`). Propuestos: `RecetaDescubierta`, `RangoDeOficioSubido`, `VetaAparecida` / `VetaAgotada` |
| **Eventos que escucha** | `HeridaTratada` (`WoundTreated`): experiencia de Medicina. Propuestos: `EtapaDeCiudadCambiada` (entrenadores disponibles), `NuevaSemana` (conocimiento semanal), `InvestigacionCompletada` (recetas recuperadas) |
| **Datos de los que es dueño** | Nivel y rango de cada oficio por personaje, conocimiento y especializaciones, maestrías por objeto, recetas aprendidas y descubiertas, planos y copias, vetas (lugar, atributos, duración), trabajadores, registro de obras maestras. Propuesta (§6.1): el Enfoque diario |
| **Reglas que nunca se rompen** | Profesiones profundas (D-10). Construir y curar se estudian: sin rango no hay trabajo de alto nivel, no ayuda cualquiera (D-11). Sin límite duro de oficios: el freno es el costo natural del conocimiento (D-57; [Profesiones](../07-economia/profesiones.md) §3 todavía dice 2 mayores). Los oficios no se comparten entre personajes. Cada rango pide examen. El conocimiento semanal tiene tope. La fabricación rápida llega como mucho a Notable. La destreza de los dedos nunca decide la calidad real. Todo lo fabricado lleva firma |

**Si cambias esto, revisa:**
- **El costo de aprender un oficio** (antes, el límite de oficios mayores) → C-12.
- **La aparición de vetas** → C-13.
- **La curva de rango** (Gran Maestro en ~1 año) → la duración del juego del artesano, cuándo hay obras maestras, quién puede curar (M7) y construir (M24) cada cosa.
- **El minijuego de fabricación** → la calidad media de todo el equipo (M4), la tasa de obras maestras y su pantalla en los tres clientes.
- **Una receta** (materiales o resultado) → la demanda de cada material (M13), los oficios proveedores y la red de "quién necesita a quién".
- **Las enfermedades laborales** → la demanda de máscaras y guantes (Sastrería, Peletería) y M7.
- **Los entrenadores o exámenes** → dependen de que la ciudad haya construido y abastezca su ala (M9, M24); si se pueden saltar, **rompe** D-11.
- **Algo que haga a un oficio obligatorio para ganar en combate** → choca con D-49 solo si crea una brecha imposible de alcanzar: la ventaja de oficio tiene techo por tramo ([Balance](../03-personaje/balance.md) §5).

---

#### M15 · Social · `engine/social`

| | |
|---|---|
| **Para qué sirve** | La gente junta: gremios, alianzas, grupos, amigos, hermandades, mentoría y salas retransmitidas |
| **Documentos de diseño** | [08 · Social](../08-social/README.md), [Gremios y vida social](../08-social/gremios-y-social.md) |
| **Depende de** | M1; M19 (chats y salas); M13 (banco de gremio, costo de crear); M2 (nivel 5 para crear un gremio) |
| **Lo usan** | M11 (grupos), M12 (gremios y alianzas en territorios y guerras), M24 (salón y obras de organización), M16 (minijuegos de gremio), M7 (jugar con tu gremio baja el estrés), M10 (casos de gremio), M18 (ranking por gremio), M25 (parcelas de gremio) |
| **Eventos que publica** | Propuestos: `GremioCreado`, `MiembroUnido` / `MiembroExpulsado`, `GrupoFormado`, `ValeEmitido` |
| **Eventos que escucha** | Propuestos: `NivelSubido` y `SelloObtenido` (metas de mentoría) |
| **Datos de los que es dueño** | Gremios, rangos y permisos, banco de gremio y su registro, vales, nivel de gremio, alianzas, grupos, amistades y hermandades, mentorías, el indicador de buen compañero |
| **Reglas que nunca se rompen** | El nivel de gremio da comodidad, nunca poder de combate. Los vales solo valen dentro del gremio y caducan rápido. No hay votos negativos entre compañeros. Grupo de hasta 5 |

**Si cambias esto, revisa:**
- **El tamaño del grupo** → mazmorras (M11) y composición (M3).
- **Los vales** → son objetos del motor de un solo uso que cambian de dueño con una orden; reenviar el mensaje es solo un atajo de Telegram (§5.3). Cambiarlos toca el banco de gremio, el inventario (M4) y el lavado de oro (M23).
- **Los límites del banco de gremio** → lavado de oro (M23) y economía de gremios (M13).
- **El nivel de gremio** → si da poder, **rompe** su regla; si da más miembros, cambia la escala de guerras y territorios (M12).
- **La mentoría** → retención de novatos y monedas de mentoría (cosméticos, M17).

---

#### M16 · Minijuegos y apuestas · `engine/minigames`

| | |
|---|---|
| **Para qué sirve** | Los juegos dentro del juego, cada uno como complemento que se enchufa, y las apuestas legales e ilegales con oro del juego |
| **Documentos de diseño** | [Minijuegos](../08-social/minijuegos-y-formatos-telegram.md), [Apuestas](../08-social/apuestas.md), [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §5 y §8 |
| **Depende de** | M13 (oro y comisiones); M1 (azar con semilla publicable); M19 (dados nativos y modo inline de Telegram); M9 (leyes, licencias, ala de la Fortuna); M25 (licencias); M24 (casinos y garitos construidos); M12 (Infamia y redadas); M10 y M14 (bestias capturadas, monturas criadas); M23 (arreglos) |
| **Lo usan** | M13 (sumideros), M7 (ganar baja el estrés y perder lo sube), M9 (ánimo de la ciudad: taberna, festivales), M17 (cartas, títulos), M15 (juegos de gremio) |
| **Eventos que publica** | Propuestos: `ApuestaResuelta`, `TiradaPublica` |
| **Eventos que escucha** | Los resultados por los que se apuesta: `JefeDerrotado` (`BossDefeated`) para el mercado de predicciones sobre Pioneros. Propuestos: `BatallaDeCastillosResuelta`, `InstanciaCompletada` |
| **Datos de los que es dueño** | Cada minijuego (complemento), mesas, pozos y libros de corredores, fichas de la Fortuna, fama de tahúr, Votos de Templanza, topes diarios de pérdida, lotería |
| **Reglas que nunca se rompen** | Nunca con dinero real: ni Stars ni Gemas se apuestan, y lo ganado nunca se vuelve dinero (D-43). Los minijuegos son opcionales y nunca dan poder de combate. Topes diarios. El azar legal es auditable (dado nativo o semilla publicada). Nadie apuesta en un evento donde participa, ni sus cuentas vinculadas. Un pozo mutuo no crea oro. Se puede apagar por región. Un minijuego se agrega o se quita sin tocar el resto |

**Si cambias esto, revisa:**
- **La comisión de la casa** → oro quemado (M13, M20) y negocio de los casinos de jugadores (M24, M25).
- **Los topes o el Voto de Templanza** → quitarlos **rompe** la regla de topes diarios y complica las tiendas de aplicaciones (P-62, P-63).
- **La tirada pública auditable** → el dado nativo de Telegram no decide ninguna tirada que cuente: la decide el motor con una semilla cuya huella se publica antes y que se revela después ([Web y multiplataforma](web-y-multiplataforma.md) §6.1). Cambiar ese mecanismo toca M1 (semillas), M5 (emboscada e iniciativa inicial), M15 (botín de grupo), M3 (Dados del Destino del Pícaro Forajido), M12 (regla de la noche del Foso), la API pública y los tres clientes (§5.3).
- **Agregar un minijuego** → recompensas con tope, un lugar en el mundo y nada de poder; si es de destreza, nunca decide calidad real (M14).
- **Las reglas de lo ilegal** (garitos, redadas) → Infamia y guardia (M12), contraseñas (M10), orden de la ciudad (M9).

---

#### M17 · Colecciones y logros · `engine/collections`

| | |
|---|---|
| **Para qué sirve** | Lo que se junta y se recuerda: Bestiario y conocimiento, colecciones, títulos, logros, cicatrices como trofeo y el registro de descubridores |
| **Documentos de diseño** | [Progresión](../03-personaje/progresion.md) §6, [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md), [Avisos y tácticas](../04-combate/avisos-y-tacticas.md) §2, [Bestiario](../06-contenido/bestiario.md) §1.5 |
| **Depende de** | Los eventos de casi todos los módulos |
| **Lo usan** | M6 (pistas en los avisos tras 3 vistas; debilidades reveladas para la ruptura; el Bestiario completo de un tramo da pistas extra); M2 y M19 (perfil, títulos); M14 (Herbario completo: más rendimiento de cosecha); M24 (museo, sala de trofeos) |
| **Eventos que publica** | Propuestos: `LogroObtenido`, `TituloObtenido`, `DescubrimientoRegistrado` |
| **Eventos que escucha** | `JefeDerrotado` (`BossDefeated`), `ObjetoFabricado` (`ItemCrafted`). Propuestos: `MovimientoVisto`, `RecetaDescubierta`, `NodoDescubierto`, `PresaCazada`, `CicatrizGanada` |
| **Datos de los que es dueño** | Colecciones (por cuenta, salvo recetario y cicatrices, que son por personaje), logros, títulos, el registro de descubridores, el conocimiento del Bestiario |
| **Reglas que nunca se rompen** | Nunca poder directo en combate: el conocimiento ayuda a decidir, no decide por ti (D-49). Se comparte por cuenta, salvo lo indicado. El primer descubridor queda registrado para siempre |

**Si cambias esto, revisa:**
- **Un bono de colección** → si se acerca al combate, **rompe** la regla y hay que medir (M21).
- **La regla de las 3 vistas** → la dificultad real de los jefes (M6), las debilidades que se revelan para la ruptura (M5) y el valor de las fichas del Informante (M14).
- **Qué es de cuenta y qué de personaje** → el valor de tener varios personajes y la experiencia heredada (M2).

---

#### M18 · Temporadas y rankings · `engine/seasons`

| | |
|---|---|
| **Para qué sirve** | El calendario competitivo: temporadas de Mítica+ y arena, ligas opcionales, tablas y recompensas por rango |
| **Documentos de diseño** | [Progresión](../03-personaje/progresion.md) §7, [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) §2, [PvP](../06-contenido/pvp.md) §5 y §7 |
| **Depende de** | M11, M12, M9 (Pioneros por facción), M1 (calendario), M13 (moneda de temporada) |
| **Lo usan** | M17 (títulos), M22 (pase de temporada). El calendario de temporadas también lo usan M9 (mandatos), M25 (licencias), M7 y M9 (una epidemia por temporada) y M10 (bestia legendaria por tramo y temporada) |
| **Eventos que publica** | Propuestos: `TemporadaIniciada`, `TemporadaTerminada` |
| **Eventos que escucha** | `JefeDerrotado` (`BossDefeated`) para los Pioneros. Propuestos: `InstanciaCompletada`, `BatallaDeCastillosResuelta`, `PersonajeCaidoParaSiempre`; resultados de arena |
| **Datos de los que es dueño** | El calendario de temporadas, puntuaciones, clasificaciones, tablas, recompensas por rango, ligas |
| **Reglas que nunca se rompen** | El poder temporal solo existe en las ligas opcionales. Las recompensas de rango son cosméticas o títulos. Los aceleradores no cuentan en lo competitivo |

**Si cambias esto, revisa:**
- **La duración de una temporada** → C-14.
- **Las recompensas por rango** → si dan poder, **rompen** la regla de "nada de poder prestado" (M3, M21).
- **Una liga con regla especial** → es el único lugar donde se puede romper una regla de diseño, y solo dentro de esa liga.

---

#### M19 · Mensajería · `engine/messaging`

| | |
|---|---|
| **Para qué sirve** | Lleva lo que pasa en el motor a cada jugador: vistas vivas, avisos con prioridad, bandeja de avisos y noticias, igual para los tres clientes. La forma de cada cliente (mensaje vivo, cola de ediciones, límites de envío de Telegram) vive en su adaptador |
| **Documentos de diseño** | [Web y multiplataforma](web-y-multiplataforma.md) §3, §6.3, §6.6 y §8, [Telegram](telegram.md) |
| **Depende de** | M1 (cuenta, idiomas) y los eventos de todos los módulos |
| **Lo usan** | Los adaptadores de cada cliente (Telegram, web, app) y todos los módulos que necesitan avisar |
| **Eventos que publica** | Propuesto: `AvisoFallido` (para reintentar o avisar por otro cliente) |
| **Eventos que escucha** | `HeridaCreada` / `HeridaTratada` (`WoundCreated` / `WoundTreated`), `PisoAbierto` (`FloorOpened`: aviso escalonado), `HeroeDerribado` / `HeroeCaido` (`HeroDowned` / `HeroFallen`), `JefeDerrotado` (`BossDefeated`), `EnfermedadContagiada` (`DiseaseContracted`: Gaceta), y cualquier evento que pida atención del jugador |
| **Datos de los que es dueño** | Preferencias de aviso de cada jugador, la bandeja de avisos (invitaciones, retos, avisos pendientes), las plantillas de aviso, el feed de noticias (Gaceta, Mercado, Salón de los Caídos, Novedades). En el adaptador de Telegram: la cola de ediciones, los límites de envío y la referencia al mensaje vivo |
| **Reglas que nunca se rompen** | Lo que no se muestra no se envía: ningún dato oculto viaja al cliente. Cada dato con su precisión pública. Informes en dos capas: resumen corto y detalle completo. Lo que abre una competencia tiene hora fija igual para todos: el aviso puede llegar escalonado, la apertura nunca. Ningún plazo es tan corto que no recibir un aviso a tiempo sea una desventaja de cliente. En Telegram: un mensaje vivo por actividad, nada pasa de 4.096 caracteres, una edición cada 3 a 5 segundos por chat, el costo nunca va en el botón |

**Si cambias esto, revisa:**
- **El formato de una vista o de un aviso** → los tres clientes (§5).
- **Los límites de envío o de edición** → solo el adaptador de Telegram: la carga del servidor y el riesgo de que Telegram frene los envíos en combates en grupo y bandas (M5, M11).
- **El aviso escalonado** → la apertura de regiones (antes, de pisos) (M9), la Guarida, las vetas excepcionales y los eventos de servidor; la hora de apertura tiene que seguir siendo la misma para todos.
- **La precisión pública de un dato** (vida del jefe en %, Aguante en fichas) → lo que puede deducir un jugador en cada cliente; una precisión más fina en un cliente **rompe** D-40.
- **Un canal** (Gaceta, Mercado) → lo que publican M9, M12, M14, M7 y M20.

---

#### M20 · Administración y telemetría · `engine/telemetry`

| | |
|---|---|
| **Para qué sirve** | Las herramientas para mirar el motor por dentro: radiografías, registro de balance, informe económico y cola de feedback |
| **Documentos de diseño** | [Arquitectura modular](arquitectura-modular.md) §5, [Economía](../07-economia/economia.md) §9, [Balance](../03-personaje/balance.md) §3 |
| **Depende de** | M1 (semillas para repetir peleas), M5, M13 y los eventos de todos |
| **Lo usan** | El equipo y el dueño; M21 (registro de balance); M23 (precios anómalos); el canal del Mercado (informe mensual público) |
| **Eventos que publica** | Propuesto: `InformeEconomicoPublicado` |
| **Eventos que escucha** | `OrdenEjecutada` (`OrderFilled`), `ObjetoDestruido` (`ItemDestroyed`). Propuesto: `OroQuemado`. En general, todos |
| **Datos de los que es dueño** | El registro de balance (cada número con antes → después y la medición), los informes, la cola de feedback, los registros de auditoría |
| **Reglas que nunca se rompen** | Mira, no cambia reglas. Todo número de balance que se mueve queda registrado. Se guarda lo mínimo (privacidad). Credenciales: nombres sí, valores jamás |

**Si cambias esto, revisa:**
- **Qué se registra** → si un número se mueve sin registro, "se movió a ciegas": **rompe** la regla de trabajo de [Balance](../03-personaje/balance.md) §3.
- **El informe económico** → es la base para ajustar impuestos, Mercado Negro y recompensas (M13, M10).

---

#### M21 · Simulador de balance · `simulator/`

| | |
|---|---|
| **Para qué sirve** | Corre cada spec, cada mecánica y cada jefe contra escenarios fijos para comprobar que el balance cumple sus objetivos antes de publicar un cambio |
| **Documentos de diseño** | [Balance](../03-personaje/balance.md) §3, [Jefes](../06-contenido/jefes.md) §5, [Talentos](../03-personaje/talentos.md) §3, [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §15, [Bestiario](../06-contenido/bestiario.md) §12 |
| **Depende de** | M5 (el mismo motor, no una copia), M3, M4 (tramos de equipo), M6, M1 (semillas) |
| **Lo usan** | El equipo, el consejo de clase y M20 (registro de balance) |
| **Eventos que publica** | Ninguno: produce mediciones, no eventos de juego |
| **Eventos que escucha** | Ninguno en vivo |
| **Datos de los que es dueño** | Escenarios fijos, objetivos numéricos, resultados históricos |
| **Reglas que nunca se rompen** | Corre antes de publicar cualquier cambio de balance. Usa el mismo motor que el juego. Objetivos: daño sostenido ±3 %, ráfaga ±5 %, mitigación y curación ±4 %, victorias en arena 47-53 %; juego básico ±10 % y óptimo ±3 % de la mediana; configuraciones de talentos a ±3 % |

**Si cambias esto, revisa:**
- **Un escenario** → las mediciones viejas dejan de compararse con las nuevas: se anota en el registro de balance.
- **Un objetivo** → es un cambio de diseño, no de número: pasa por el dueño y por [Balance](../03-personaje/balance.md). Aflojarlo tanto que una clase quede por encima de otra **rompe** D-49.

---

#### M22 · Pagos · `engine/payments`

| | |
|---|---|
| **Para qué sirve** | Cobra dinero real y entrega Gemas, cosméticos y aceleradores, aislado del resto del juego |
| **Documentos de diseño** | [Monetización](../07-economia/monetizacion.md), [Web y multiplataforma](web-y-multiplataforma.md) |
| **Depende de** | M1 (la cuenta); los medios de pago de cada cliente: Telegram Stars, pasarela web, pago de las tiendas de Apple y Google |
| **Lo usan** | M2 y M14 (aceleradores de experiencia y de oficio), la recolección de M14 (acelerador de recursos), M17 (cosméticos), M24 (segunda casa), M13 (más banco), M10 (casillas de encargos), M3 (más configuraciones) |
| **Eventos que publica** | Propuestos: `CompraConfirmada`, `AceleradorActivado`, `ReembolsoAplicado` |
| **Eventos que escucha** | Propuesto: `TemporadaIniciada` (pase de temporada) |
| **Datos de los que es dueño** | Saldo de Gemas, compras y recibos, aceleradores activos, catálogo y precios |
| **Reglas que nunca se rompen** | D-43: el dinero real compra solo cosméticos y aceleradores. Nunca oro, equipo, materiales directos, Esencia, saltos de progreso (antes, Sellos y pisos), ventaja en PvP ni revivir en el Juramento de Hierro. Las Gemas nunca se apuestan ni se cambian por oro. Aceleradores: uno por tipo, de +25 % a +50 %; no saltan el Techo de la Frontera, no cuentan en lo competitivo y no tocan equipo, artefactos ni Recuerdos. Mismo catálogo en los tres clientes. Nada se vende en alfa y beta |

**Si cambias esto, revisa:**
- **El porcentaje de un acelerador** → C-17.
- **Un producto nuevo** → pasarlo por la lista de "nunca se vende"; si da poder, **rompe** D-43.
- **Un medio de pago** → solo el adaptador de ese cliente; el catálogo y las Gemas son de la cuenta. En las tiendas hay comisión y reglas propias (P-62).

---

#### M23 · Anti-trampas · `engine/anticheat`

| | |
|---|---|
| **Para qué sirve** | Detecta multicuentas, bots y comercio sospechoso, y propone sanciones que revisa una persona |
| **Documentos de diseño** | [Seguridad y anti-trampas](seguridad-y-anti-trampas.md) |
| **Depende de** | M1 (cuentas y vínculos), M13 (órdenes y transferencias), M12 (guerras), M16 (apuestas raras), M7 y M6 (preguntas de los retos contextuales), M20 |
| **Lo usan** | M13 (congela el comercio), M12 (cuentas vinculadas no se enfrentan en la misma batalla), M16 (nadie apuesta en lo propio), M9 (solo votan residentes activos), M15 |
| **Eventos que publica** | Propuestos: `CuentaMarcada`, `ComercioCongelado`, `SancionAplicada` |
| **Eventos que escucha** | `OrdenEjecutada` (`OrderFilled`). Propuestos: `OroTransferido`, `ApuestaResuelta`; patrones de acción de todos |
| **Datos de los que es dueño** | Vínculos entre cuentas, marcas, sanciones, historial de revisiones |
| **Reglas que nunca se rompen** | Nada automático sin revisión humana, salvo el congelamiento preventivo. Sanciones escalonadas. Lo mínimo de datos. Las cuentas nuevas no transfieren durante sus primeros días. Las invitaciones pagan cuando el invitado sube de nivel |

**Si cambias esto, revisa:**
- **Un umbral de detección** → falsos positivos que congelan a jugadores honestos (M13) o trampas que pasan.
- **Los límites de cuentas nuevas** → el arranque de los novatos y la mentoría (M15).
- **Los retos contextuales** → dependen de lo que muestran `/cuerpo` y los avisos (M7, M6) en los tres clientes.

---

#### M24 · Construcción · `engine/construction`

| | |
|---|---|
| **Para qué sirve** | Levantar y defender lo construido: obras por jornadas, casas, edificios de organizaciones, obras de servidor, graneros y defensas |
| **Documentos de diseño** | [09 · Construcción](../09-construccion/README.md), [Sistema de construcción](../09-construccion/sistema-de-construccion.md), [Casa propia](../09-construccion/casa-propia.md), [Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md), [Defensa y protecciones](../09-construccion/defensa-y-protecciones.md), [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §4.3, §6.5 y §8 |
| **Depende de** | M14 (rango de Construcción y materiales), M13 (presupuesto en custodia, mantenimiento), M25 (parcelas), M5 (la defensa usa el combate y las Tácticas), M8 (zona, clima de la jornada, poblaciones), M9 (obras de servidor; la despensa y las herramientas comunes deciden el avance), M15 (permisos de gremio) |
| **Lo usan** | M9 (cada etapa de ciudad es una obra; graneros y murallas sostienen los medidores), M7 (dormitorio x2, enfermería x3), M14 (talleres y estaciones), M16 (casinos y garitos), M12 (fortalezas, prisión), M2 (descanso), M17 (museo, sala de trofeos), M8 (puentes, caminos y postas) |
| **Eventos que publica** | Propuestos: `ObraTerminada`, `AccidenteDeObra` (Salud crea la herida), `ConstruccionAtacada`, `DefensaResuelta` |
| **Eventos que escucha** | `PisoAbierto` (`FloorOpened`): obra del asentamiento nuevo. Propuestos: `IncursionLanzada` (M9), `PoblacionCambiada` (incursiones a casas y granjas), `EtapaDeCiudadCambiada` |
| **Datos de los que es dueño** | Obras y etapas, planos, calidad y durabilidad de lo construido, habitaciones y estaciones de casa, defensas y reglas de los guardias, protecciones (escudo, horas protegidas, bóveda). Propuesta (§6.1): seguidores de la casa |
| **Reglas que nunca se rompen** | Cada etapa pide un rango mínimo: no ayuda cualquiera (D-11). El presupuesto queda en custodia desde que se publica la obra. Lo que está en zona azul nunca se ataca. La bóveda nunca se roba. Escudo después de un ataque y horas protegidas. Si no se paga el mantenimiento, la obra se cierra pero no se pierde lo de adentro. La casa nunca da poder de combate. Una brecha roba una parte, nunca todo |

**Si cambias esto, revisa:**
- **Las jornadas que pide una obra** → cuánto tarda el Claro en llegar a Castillo (M9, P-55), la comida que comen los obreros (C-06), la paga de los constructores (M13), cuándo se abren servicios (M14, M16, M7).
- **El mantenimiento** → sumidero de oro (M13), casas cerradas, ruinas reclamables.
- **Los multiplicadores de descanso o de enfermería** → C-02.
- **La capacidad de los graneros** → cuánta despensa puede guardar la ciudad y cuánto se pudre (C-06).
- **Las protecciones** → si se quitan, va contra P-52 y contra el principio de no perderlo todo mientras duermes.
- **Las defensas o los guardias** → la seguridad de la ciudad (M9), las incursiones (M8), la demanda de ingenieros, carpinteros y herreros (M14), las heridas de los guardias (M7).

---

#### M25 · Propiedad · `engine/property`

| | |
|---|---|
| **Para qué sirve** | Los lugares escasos y el crédito: puestos, locales, parcelas, licencias y concesiones, con subastas, tasas, impuestos e intereses |
| **Documentos de diseño** | [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md), [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) §2 (Banco y Lonja), [Casa propia](../09-construccion/casa-propia.md) §7 |
| **Depende de** | M13 (oro, custodia); M9 (etapas de ciudad, plazas nuevas por región, licencias y tasa de la casa que fija cada gobierno); M8 (lugares y rutas); M12 (territorios para vetas exclusivas; recompensas por deudores); M1 (cobro semanal) |
| **Lo usan** | M24 (parcelas para construir), M16 (licencias de casino y corredor), M13 (los puestos bajan el impuesto y dan visibilidad), M7 (consulta médica en la plaza), M8 (peajes de las concesiones de ruta), M9 (lo recaudado va al tesoro de la ciudad) |
| **Eventos que publica** | Propuestos: `SubastaCerrada`, `PropiedadTransferida`, `TasaImpagada`, `GarantiaEmbargada`, `LicenciaOtorgada` |
| **Eventos que escucha** | Propuestos: `EtapaDeCiudadCambiada` (plazas nuevas), `TemporadaIniciada` (licencias), `NuevaSemana` (cobro), `ContratoIncumplido`, `LeyAprobada` (tasa de la casa) |
| **Datos de los que es dueño** | Quién tiene cada lugar, valores declarados, subastas, licencias, concesiones, préstamos, hipotecas, garantías, registro de crédito |
| **Reglas que nunca se rompen** | Mercado capitalista con lugares escasos, pujas, tasas e intereses (D-12). Topes: 2 puestos por capital por jugador y 1 parcela de gremio por capital por gremio. El oro de las subastas se quema. Si no pagas: una semana de gracia y vuelve a subasta, y nunca se pierden los objetos. La casa paga impuesto al reino donde está (castillo o comunidad), con la tasa que fija su gobierno dentro de un rango (D-48), y no se le aplica la tasa autodeclarada. Los intereses tienen techo y las garantías las guarda el bot |

**Si cambias esto, revisa:**
- **El cupo de puestos** → C-09.
- **El porcentaje de la tasa autodeclarada** → cuánto se declara, cuánto rota la propiedad, oro quemado (M13, M20).
- **El rango del impuesto de la casa** (D-48) → el tesoro de cada reino (M9), dónde conviene vivir y la competencia entre castillos y comunidades, el costo de tener casa frente a la posada (M24, M7 descanso).
- **El techo de intereses** → bancos de jugadores, préstamos para apuestas (M16), deudores con recompensa (M12).
- **Los topes de propiedad** → concentración de riqueza (M20) y contrapesos para quien llega tarde.

---

## 3. Cascadas típicas

Cada cascada dice **dónde está** el número o la regla, **quién es el dueño**, la **cadena** de efectos en orden, lo que pasa **también** y qué hay que **medir**. Las flechas siguen el orden en que se nota el efecto.

### C-01 · La fórmula de mitigación de armadura

**Dónde está:** `def / (def + K)`, con K = 60 que crece por tramo ([Balance](../03-personaje/balance.md) §4, [Daño y estados](../04-combate/dano-y-estados.md) §1). **Dueño:** M5.

**Cadena:** cambia el daño que entra en todo combate (M5) → cambian los críticos que pasan y cuántas veces se cruzan el 50 % y el 25 % de vida → cambian la probabilidad y la gravedad de las heridas (M7) → cambia la demanda de médicos, vendas y férulas (M14) y el uso del sanatorio (M13) → cambian el balance de tanques (mitigación ±4 %), el de tela contra placas y el PvP (victorias 47-53 %) → hay que repetir el simulador y la prueba de jefes justos (M21, M6) → cambia el valor de cada tipo de armadura en el mercado (M13) → cambia la demanda de herreros, peleteros y sastres, y de reparaciones (M14, M4).

**También:** como la acumulación de estados y de Contagio pasa por la armadura, cambian los tiempos de veneno, sangrado, quemadura y enfermedades de monstruo (M5, M7); cambian los guardias de la ciudad y de las construcciones (M9, M24); cambia la duración de duelos y del poder de guerra (M12).
**Medir:** simulador completo; heridas por zona y por pelea; precio de armaduras por tipo en el informe económico.

### C-02 · La duración de las heridas

**Dónde está:** leve 1-6 h, moderada 6-24 h, grave 1-3 días, crítica 3-7 días ([Heridas](../05-salud/heridas.md) §3). **Dueño:** M7.

**Cadena:** cambia cuánto tiempo juega cada héroe con penalización (M5: iniciativa, armas a dos manos, precisión) → cambia el valor del descanso en posada o casa (x2) y de la enfermería (x3) (M24) → cambia la demanda de médicos que aceleran la curación y el precio de las consultas, con el sanatorio como techo (M14, M13) → cambia cuántos llegan al tope de 2 heridas graves y la cadena hacia secuelas (M7) → cambia quién está apto para el Foso (M12, M16) y cuántos esperan para entrar a mazmorras y bandas (M11) → cambia la experiencia de Medicina por tratamientos (M14) → cambian los enfermos en cama de la ciudad, que comen 1,25 raciones (M9).

**También:** tiene que seguir valiendo que "el tiempo fuera de línea cura". El texto "sana en 2 d 6 h" lo calcula el motor, no se escribe a mano (§5).
**Medir:** heridas activas por jugador, tiempo medio hasta el alta, precio de las consultas.

### C-03 · La velocidad de la Esencia

**Dónde está:** se gana matando y completando contenido ([Economía](../07-economia/economia.md) §2); se gasta en mejoras, maestrías y Tesoro Semanal ([Equipamiento](../03-personaje/equipamiento.md) §3 y §9); la no depositada queda en la mancha al caer ([Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1). **Dueño:** M13.

**Cadena:** cambia el ritmo de mejoras de equipo (M4) → cambia el Poder de Objeto medio de cada tramo → cambian los objetivos de los jefes (el grupo que juega bien tiene que ganar sin mejoras) y del simulador (M6, M21) → cambia cuánto se arriesga al cargar Esencia sin depositar y cuánto vale volver a la mancha (M8) → cambia el valor del Tesoro Semanal y del carril de mazmorras, que lidera en Esencia (M11) → cambia la demanda de materiales para mejoras (M14, M13).

**También:** como no se transfiere (D-28), no hay mercado directo de Esencia. También pagan Esencia el Laberinto Cambiante, el enigma del día y la *Venganza* contra un monstruo que te derribó ([Bestiario](../06-contenido/bestiario.md) §10.4).
**Medir:** Esencia por hora y por carril, mejoras por semana, Poder de Objeto medio por tramo.

### C-04 · Los impuestos del mercado

**Dónde está:** 1,5 % por publicar + 4 % sobre la venta ([Economía](../07-economia/economia.md) §5). **Dueño:** M13.

**Cadena:** cambia el oro que se quema (M20) → cambia la inflación y el riesgo de la crisis de inflación (M9) → cambia el margen del comerciante, que tiene que cubrir impuesto y transporte entre ciudades (M8) → cambia cuánto vale un puesto, que paga menos impuesto, y por eso el valor declarado y las pujas (M25) → cambia cuánta gente vende por fuera (evasión, delito en M12) y lo atractivo de los mercados de alianza (M24) → se suma a los impuestos locales que fija el gobernador (M9).

**También:** siempre en porcentaje (D-27). El descuento Premium en impuestos que menciona [Economía](../07-economia/economia.md) §5 choca con D-43 (ver §6.2).
**Medir:** oro quemado por impuestos, volumen de comercio, diferencia de precios entre ciudades.

### C-05 · El ritmo de avance de la Frontera (antes: apertura de pisos)

**Dónde está:** con D-58, cada región nueva pasa por las cuatro fases que tenía un piso: descubrimiento, esfuerzo de guerra, asalto al Guardián y asentamiento ([Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)). Hasta que ese documento fije sus números, sirven de referencia los de [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.1: descubrimiento 2-5 días, esfuerzo de guerra 3-7 días, un paso cada 1-2 semanas. **Dueño:** M9.

**Cadena:** cambia la Frontera y con ella el nivel máximo práctico (Techo de la Frontera, M2) → cambia cuándo llegan los talentos de héroe (nivel 50) y Ápice (90) (M3) → cambia la duración de la primera era (2 a 4 años) y el calendario de contenido → cambia la oferta de plazas y parcelas nuevas, que es el contrapeso para quien llega tarde (M25) → cambia cuántas zonas quedan con Viento de Cola y cuánto bajan los materiales viejos (M13) → cambia la demanda masiva del Esfuerzo de Guerra (M14) y de obras de servidor (M24) → cambia cuándo hay entrenadores de rango Maestro (antes, en el Castillo del piso 80 o más; con D-58, por definir) (M14).

**También:** mercados nuevos (M13), avisos escalonados (M19), carreras de Pioneros (M18) y el mercado de predicciones (M16). Como viajar toma tiempo (D-58), cuanto más lejos queda la Frontera, más tardan en llegar la gente y la carga (C-15).
**Medir:** días por fase, distancia media entre los jugadores y la Frontera, precios por tramo.

### C-06 · Las necesidades de comida de la ciudad

**Dónde está:** 1 ración por residente activo y por aldeano al día real, 1,5 por guardia, 1,25 por enfermo en cama, +0,5 por jornada de obra, +0,2 y leña en invierno; la despensa se mide en días (14, 7, 3, 1, 0) ([Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §3-4 y §8; [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §2). **Dueño:** M9.

**Cadena:** cambia la demanda de agricultores, ganaderos, cazadores, pescadores y cocineros, y lo que pagan los pedidos de la ciudad (M14, M13) → cambian la capacidad de graneros que hace falta y cuánto se pudre (M24), y la demanda de conservas y de sal, que mueve el comercio con la costa y el desierto (M14, M13, M8) → cambia la velocidad de las obras, que se frenan en *Escasez* y se paran en *Hambruna* (M24) → cambia si se cumple la despensa sostenida que pide cada etapa, y con ella la racha (M9) → si falta: baja el ánimo y la salud pública, se van aldeanos, la posada no cura (M7) y sube la amenaza por comida podrida (carroñeros) → con 3 días de hambruna la ciudad baja de etapa y se apagan servicios: entrenadores, subastas, crédito, minijuegos de taberna (M14, M25, M13, M16) → crisis en cadena: hambruna → revuelta → moción de censura → cisma (M9) → guerra de castillos (M12).

**También:** si la comida sale de la caza, bajan las poblaciones (M8) y los depredadores bajan a las granjas ([Bestiario](../06-contenido/bestiario.md) §10.2). El invierno corta las cosechas y sube el consumo (C-19). Tras un cisma, las mismas necesidades se reparten entre menos manos. El mercader PNJ de emergencia (sumidero, con tope semanal) es la salida cara.
**Medir:** días de despensa por ciudad, comida podrida por día, precio de la comida, aldeanos que se van, residentes activos.

### C-07 · El contagio de un monstruo

**Dónde está:** cada golpe que contagia suma a una barra de Contagio de esa enfermedad; al llenarse, empieza la incubación ([Bestiario](../06-contenido/bestiario.md) §5-6, [Enfermedades](../05-salud/enfermedades.md) §2-3). **Dueño:** M7 (la barra y la enfermedad), M6 (qué monstruo contagia qué y cuánto suma).

**Cadena:** cambia cuántos jugadores enferman (M7) → como la incubación ya contagia, cambian el contagio entre jugadores y el mapa de epidemias (`EnfermedadContagiada` → M8, Gaceta) → cambia la demanda de médicos, alquimistas, herboristas y sastres (máscaras, ropa cerrada), y el precio de los remedios (M14, M13) → cambia la salud pública de la ciudad y la frecuencia de brotes y cuarentenas, que bajan el comercio y el ánimo (M9, M13) → cambia el valor de cazar portadores y de controlar poblaciones enfermas (M10, M8) → cambia el valor del Licántropo (olfato), del Renacido (no enferma de males naturales), del Enano y del Goblin (M2).

**También:** la armadura de la zona frena la barra (C-01); las vacunas investigadas la frenan del todo (M10); el ganado y las monturas también enferman (M7); las peleas contra bestias del Foso (M12, M16). Límites que no se tocan: nada serio antes del nivel 10 y una enfermedad seria a la vez.
**Medir:** enfermos activos, duración de los brotes, salud pública media de las ciudades, precio de remedios.

### C-08 · El Techo de la Frontera (antes: techo de nivel por piso)

**Dónde está:** con D-58, la experiencia baja cuando tu nivel supera por mucho al de la Frontera ([Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md), propuesta, todavía sin números). Antes bajaba al 10 % con 5 niveles sobre el piso de tu último Sello, como todavía dicen [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.4 y [Progresión](../03-personaje/progresion.md) §2. **Dueño:** M2 (la curva), M9 (la Frontera).

**Cadena:** cambia la distancia entre veteranos y nuevos (M2) → cambia cuándo la experiencia se vuelve Renombre (carga M4, banco M13, viaje M8, Enfoque M14) → cambia lo que rinde un acelerador de experiencia, que "acelera, no salta" (M22) → cambia la relación entre nivel y Lejanía que usan jefes y escalado (M6, M21) → cambia cuánta gente farmea zonas cercanas al Claro y la oferta de materiales viejos (M13).

**También:** si se quita, los aceleradores pagados empezarían a comprar niveles por encima de la Frontera: eso **rompe** D-43. (P-16, el nivel ligado al piso, quedó sin efecto por D-58.)
**Medir:** niveles frente a la Frontera, Renombre ganado por semana.

### C-09 · El cupo de puestos de mercado

**Dónde está:** de 10 a 40 por lugar; tope de 2 por capital por jugador ([Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) §1 y §6). **Dueño:** M25.

**Cadena:** cambia la escasez y con ella el precio de subasta y el valor declarado (M25) → cambia el oro quemado en subastas y tasas (M20) → cambia cuántos vendedores pagan menos impuesto y tienen visibilidad, y por lo tanto el volumen y los precios (M13) → cambian la carrera de comerciante y la de artesano famoso → cambian la concentración de riqueza (M20) y la fuerza de los contrapesos (parcelas de novato, plazas nuevas con cada región) → cambia la lista de puestos que muestran los tres clientes (§5).

**Medir:** precio medio de un puesto, cuántos cambian de manos, concentración de propiedad.

### C-10 · El temporizador de ronda

**Dónde está:** 45 s en mazmorra, 60-90 s en banda, ninguno en solitario ([Ronda y acciones](../04-combate/ronda-y-acciones.md) §1); 45 s en el Foso ([Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §3.1). **Dueño:** M5.

**Cadena:** cambia cuánto dura en tiempo real una pelea, una mazmorra y una banda (M11) → cambia cuántas rondas resuelven las Tácticas porque nadie eligió (M5) y cuánto vale escribirlas bien → cambia la dificultad real de leer avisos (M6) y de las mecánicas avanzadas que piden pensar la ronda → cambia la carga del servidor y el ritmo de ediciones por chat (M19) → cambia la arena en vivo y el Foso (M12) → cambian la defensa de la ciudad y de las construcciones cuando un jugador toma el mando (M9, M24).

**También:** el reloj de Mítica+ cuenta rondas, no minutos: no cambia. La duración tiene que ser la misma en los tres clientes (D-40).
**Medir:** rondas resueltas por Tácticas, grupos que se deshacen, duración media de una mazmorra.

### C-11 · Las reglas de caída por zona

**Dónde está:** amarilla: Esencia en la mancha, herida moderada, −10 % de durabilidad; roja: además, la mochila; negra: botín completo con posible destrucción ([Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1; repetida en otros tres documentos, §4.7). **Dueño:** M12 (zonas PvP), con M7 (herida) y M8 (mancha).

**Cadena:** cambia el riesgo de cada color y dónde farmea la gente (M8) → cambian la oferta y el precio de los materiales de zonas rojas y negras: riesgo = recompensa (M13) → cambia cuánto equipo se destruye y la demanda de artesanos (`ObjetoDestruido` → M4, M14, M20) → cambian el valor de los seguros y de depositar Esencia (M13) → cambia la actividad de bandidos, karma y cazarrecompensas (M12) → cambia lo que se arriesga en expediciones y ante el entorno (M10, M7).

**También:** la misma tabla está en cuatro documentos: se cambian juntos. El Juramento de Hierro tiene sus propias reglas (M7). Con las mochilas de D-47, "la mochila" de la zona roja debe definirse otra vez (qué parte del inventario cae).
**Medir:** jugadores por color de zona, objetos destruidos, precios de materiales de riesgo.

### C-12 · El costo de aprender oficios (antes: límite de oficios mayores)

**Dónde está:** D-57 (confirmada): no hay límite duro. El freno es el costo natural del conocimiento: el tiempo de investigar, materiales de zonas y estaciones distintas, la experiencia, la preparación (herramientas, estaciones) y los costos de cada oficio (entrenadores, exámenes, expedientes). Reemplaza el límite de 2 oficios mayores (P-37), que [Profesiones](../07-economia/profesiones.md) §3 todavía dice. La escalera por etapas está en [Investigación y maestría](../07-economia/investigacion-y-maestria.md) (D-54). **Dueño:** M14.

**Cadena:** cambia cuánto se necesitan los jugadores entre sí ([Red de sistemas](../00-vision/red-de-sistemas.md)) → cambian el volumen del mercado y los pedidos de fabricación (M13) → cambia el valor de tener varios personajes → como Medicina y Construcción también se estudian (D-11), cambian cuántos médicos y constructores hay y cuánto cobran (M7, M24) → cambia la carga de entrenadores y exámenes (M9) → cambian cuántos roles cubren sus cuotas en la ciudad (M9) → cambia cuánto dura la carrera del artesano.

**También:** D-49 hace de los oficios y el conocimiento la fuente principal de diferencia entre jugadores. Abaratar el conocimiento borra esa diferencia; encarecerlo hasta que nadie pueda llevar dos oficios crea un límite duro por la puerta de atrás, y eso **rompe** D-57.
**Medir:** oficios por personaje, tiempo hasta cada rango, precios de servicios, volumen de pedidos.

### C-13 · La aparición de vetas

**Dónde está:** aparecen, se agotan y reaparecen en otro nodo, rotan cada semana y tienen calidad propia ([Fabricación](../07-economia/fabricacion.md) §3, [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §6, [Geografía y recursos](../02-mundo/geografia-y-recursos.md) §2). **Dueño:** M14 (vetas), con M8 (nodos).

**Cadena:** cambian la oferta y la calidad de cada material (M14) → cambian la calidad media de lo fabricado y la tasa de obras maestras (M4) → cambia el valor de prospectar, del Enano, del cartógrafo y del informante (M2, M14) → cambian la especulación y los precios por ciudad (M13) → cambia el tráfico en nodos de zona roja con vetas buenas (M12) → puede disparar la crisis de escasez (M9).

**También:** los yacimientos únicos nunca se mueven: no confundirlos con vetas. El Gusano de Vetas agota las vetas si nadie lo caza ([Bestiario](../06-contenido/bestiario.md) §10.2). Las vetas excepcionales salen en la Gaceta (M17, M19).
**Medir:** oferta por material, calidad media, precio.

### C-14 · La duración de una temporada

**Dónde está:** 3-4 meses; la arena, 3 ([Progresión](../03-personaje/progresion.md) §7, [PvP](../06-contenido/pvp.md) §5). **Dueño:** M18.

**Cadena:** cambian los mandatos del gobernador, que vencen por temporada (M9, D-29) → cambia cada cuánto se subastan las licencias (M25) → cambia cada cuánto llega la epidemia de temporada (M7, M9) y la bestia legendaria de cada tramo (M10) → cambian las temporadas de Mítica+ y arena y sus recompensas (M11, M12) → cambian el pase de temporada (M22) y la moneda de temporada (M13).

**Medir:** participación por temporada, abandono al final de cada una.

### C-15 · El tiempo de viaje (antes: costo de la piedra de paso por peso)

**Dónde está:** D-58 (confirmada): moverse entre lugares toma tiempo real. Lo acortan los caminos, las monturas, los barcos y las postas que construyen y mantienen los jugadores; la piedra de paso se retira (propuesta de [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)). [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md) §1 y [Economía](../07-economia/economia.md) §4 todavía describen la piedra de paso. **Dueño:** M8.

**Cadena:** cambia cuánto difieren los precios entre ciudades (M13) → cambia el negocio de comerciantes, transportistas y caravanas (M13) → cambian cuántas caravanas cruzan zonas rojas y con ellas los asaltos, escoltas y seguros (M12, M13) → cambia el valor de las concesiones de ruta, de los puertos de caravanas y de las obras que acortan el viaje: caminos, puentes y postas (M25, M24) → cambia la especialidad de cada capital, que vive de mover artesanos y materiales (M14) → cambia lo que cuesta traer comida y sal a una ciudad que no las produce (M9).

**También:** si el viaje se vuelve instantáneo, se **rompe** D-58 y se pierden los mercados locales (recomendación de P-32): todos los precios se igualan y el oficio de comerciante desaparece. También cambian de valor las monturas, el Vigor (P-45) y el correo.
**Medir:** diferencia de precios entre ciudades, tiempo medio de viaje, carga movida por caravana y por correo.

### C-16 · El tope de golpe y la amortiguación en PvP

**Dónde está:** ningún golpe quita más del 40 % de la vida máxima; desde la ronda 8, −5 % de curación por ronda ([Ronda y acciones](../04-combate/ronda-y-acciones.md) §11; repetida en otros cuatro documentos, §4.7). **Dueño:** M5.

**Cadena:** cambia qué specs de ráfaga dominan la arena (M3, M21) → cambian la duración de las peleas y el valor de los sanadores (M21) → cambian el Foso (M12, M16), los Límites y las técnicas combinadas en PvP ([Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §15) y lo que el entorno quita por ronda en PvP (M7) → cambian las victorias por spec (objetivo 47-53 %) y el riesgo para D-49.

**Medir:** simulador PvP uno contra uno, duración media de arena.

### C-17 · El porcentaje de los aceleradores

**Dónde está:** de +25 % a +50 %, uno por tipo ([Monetización](../07-economia/monetizacion.md) §3). **Dueño:** M22.

**Cadena:** el acelerador de recursos mete más materiales al mundo (M14) → bajan sus precios (M13) → los sumideros en porcentaje y el informe mensual tienen que compensarlo (M20) → los materiales se venden por oro, y el oro se apuesta: es una conexión indirecta con el azar que conviene revisar con un abogado (M16, [Monetización](../07-economia/monetizacion.md) §6) → el de experiencia choca con el Techo de la Frontera (C-08) → más poder de compra puede atraer comercio con dinero real (M23).

**También:** no funcionan en lo competitivo (M18, M12). Que suban el botín de equipo está en discusión (P-65): si lo hicieran, tocarían el equipo, cosa que hoy prohíbe [Monetización](../07-economia/monetizacion.md) §3.
**Medir:** materiales que entran por aceleradores, precios de esos materiales, gasto en Gemas.

### C-18 · Renombrar o borrar un identificador

**Dónde está:** regla 5 de la [arquitectura](arquitectura-modular.md); [Convenciones](convenciones-de-codigo.md) §4. **Dueño:** el módulo del ID.

**Cadena:** un ID de habilidad, objeto, receta, jefe, misión, evento o acción que cambia → **rompe** configuraciones y Tácticas guardadas (M3, M5), inventarios y bancos (M4, M13, M15), recetarios y planos (M14), Bestiario y colecciones (M17), registros, radiografías y repeticiones (M20), traducciones (M1), botones ya enviados en Telegram, atajos de la app y enlaces de la web (§5).

**Regla:** nunca se renombra ni se reutiliza. Se crea un ID nuevo y el viejo se marca `retired: true`, con su texto, para que los registros viejos se sigan leyendo.

### C-19 · La duración del día de juego

**Dónde está:** 6 horas reales; un año de juego dura 4 semanas reales y cada semana real es una estación ([Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §2 y §4, [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §1 y §4.5; recomendación de P-11). **Dueño:** M1 (reloj), con M8 (día, noche y estaciones).

**Cadena:** cambia cada cuánto la ciudad hace su cuenta diaria (come, se ensucia, se enferma, sube la amenaza) (M9) → cambia cuándo llega el primer invierno y cuánto tiempo hay para llenar los graneros (C-06) → cambian monstruos, hierbas y jefes nocturnos, y las incursiones que llegan de noche (M8, M6, M14, M9) → cambia la luna llena, cada 7 días de juego (licantropía en M7, amenaza de la ciudad, eventos) → cambian la caza nocturna y el valor del Elfo Sombrío (M10, M2) → cambia cuánto tarda un monstruo en volverse Adulto, Veterano o Alfa ([Bestiario](../06-contenido/bestiario.md) §10.4).

**Medir:** proporción de jugadores que ven día y noche, días de despensa al llegar el invierno.

---

## 4. Números sensibles

Los parámetros que más cosas mueven. **Valor hoy** es el del diseño al 1 de octubre de 2026. Todo cambio pasa por el registro de balance (M20) y por la cascada que se indica.

### 4.1 Combate y balance

| Número | Valor hoy | Definido en | Dueño | Qué mueve |
|---|---|---|---|---|
| Mitigación de armadura | `def / (def + K)`, K = 60 que crece por tramo | [Balance](../03-personaje/balance.md) §4 | M5 | Daño, heridas, valor de las armaduras (C-01) |
| Salto por tramo | ~25 % | [Balance](../03-personaje/balance.md) §4 | M4 | Todo el balance vertical, valor del equipo viejo |
| Presupuesto de poder | 100 ± 3 en 6 ejes; cada eje entre 5 y 35 | [Balance](../03-personaje/balance.md) §2 | M3 | Toda spec, el simulador, D-49 |
| Objetivos del simulador | ±3 % sostenido; ±5 % ráfaga; ±4 % tanques y sanadores; 47-53 % de victorias | [Balance](../03-personaje/balance.md) §3 | M21 | Qué cambio de balance se publica |
| Aporte de grupo | ~3 %, no se suma | [Balance](../03-personaje/balance.md) §2 | M3 | Composición de grupos, apoyos |
| Clamor | +30 % de iniciativa y enfriamientos al doble de velocidad durante 3 rondas, una vez por pelea | [Balance](../03-personaje/balance.md) §2 | M3 | Ráfagas, Tambores de Guerra (M14) |
| Secundarias | Ninguna vale más de 1,3 veces otra | [Balance](../03-personaje/balance.md) §2 | M3, M4 | Afijos, valor de los objetos |
| Botones de combate | 6: Atacar, 3 habilidades, Huir y Mochila; una elección por ronda | D-46 ([Decisiones](../00-vision/decisiones.md)) | M5, M3 | Pantalla de los tres clientes, kit de cada clase |
| Aguante | 0 a 5; −1 por respuesta (−2 un desvío); +1 al final de cada ronda sin respuesta; la carga pesada baja el máximo en 1 | [Ronda y acciones](../04-combate/ronda-y-acciones.md) §5 | M5 | Reacciones, armaduras pesadas, calor y sed |
| Firmeza | Llena = inmune al control 3 rondas | [Ronda y acciones](../04-combate/ronda-y-acciones.md) §5 | M5 | Control en PvP y en jefes |
| Derribado | 3 rondas antes de caer | [Ronda y acciones](../04-combate/ronda-y-acciones.md) §10 | M5 | Resurrecciones, heridas, reloj de Mítica+ |
| Tope de golpe y amortiguación en PvP | 40 % de la vida máxima; −5 % de curación por ronda desde la 8 | [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11 | M5 | Arena, Foso, entorno en PvP (C-16) |
| Temporizador de ronda | 45 s en mazmorra y Foso; 60-90 s en banda; ninguno en solitario | [Ronda y acciones](../04-combate/ronda-y-acciones.md) §1 | M5 | C-10 |
| Avisos | 1 ronda antes (2 si es devastador); pista tras 3 vistas | [Avisos y tácticas](../04-combate/avisos-y-tacticas.md) §1-2 | M6, M17 | Dificultad real de los jefes |
| Fases de jefe | Al 66 % y al 33 % de vida | [Jefes](../06-contenido/jefes.md) §2 | M6 | Duración y dificultad |
| Escudo de ruptura | Común 2-3; élite 4-6; Guardián 6-10 por fase; roto = pierde acciones y +30 % de daño | [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §3 | M6, M5 | Valor de las debilidades, aceites, Bestiario |
| Límite | Se llena hacia la ronda 8-12; vale unas 3 acciones; una vez por pelea | [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §10 y §15 | M5, M3 | Ráfaga, jefes, PvP |
| Maestría de armas | Nunca más del 5 % del poder | [Progresión](../03-personaje/progresion.md) §3 | M2 | Distancia entre veterano y nuevo |
| Mítica+ | Por ejemplo, 120 rondas; con el 80 % sube 2 niveles, con el 60 % sube 3 | [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) §2 | M11 | Llaves, temporada |

### 4.2 Salud y entorno

| Número | Valor hoy | Definido en | Dueño | Qué mueve |
|---|---|---|---|---|
| Disparadores de herida | Crítico, cruzar el 50 % y el 25 % de vida, derribo | [Heridas](../05-salud/heridas.md) §4 | M7 | Heridas por pelea |
| Duración de heridas | Leve 1-6 h; moderada 6-24 h; grave 1-3 días; crítica 3-7 días | [Heridas](../05-salud/heridas.md) §3 | M7 | C-02 |
| Tope de heridas graves | 2 a la vez | [Heridas](../05-salud/heridas.md) §7 | M7 | Agotamiento, secuelas |
| Descanso | x2 en posada o casa; x3 con enfermería | [Heridas](../05-salud/heridas.md) §5 | M7, M24 | Valor de casas y posadas |
| Protección de novato | Hasta el nivel 10 | [05 · Salud](../05-salud/README.md) y otros seis documentos (§4.7) | M7, M2 | Novatos en todo el juego |
| Toxicidad | Desde el 75 % se pierde vida; al 100 % no se bebe más | [Condiciones](../05-salud/condiciones.md) §4 | M7 | Fuerza de las pociones |
| Barra de Contagio | Se llena con golpes que contagian; la frenan armadura, máscara, vacuna, inmunidad y linaje | [Bestiario](../06-contenido/bestiario.md) §5.1 | M7, M6 | C-07 |
| Subida de etapa de peligro | Cada 4, 2 o 1 pasos según cuánta protección falte; rigor máximo 3 | [Peligros del entorno](../05-salud/peligros-del-entorno.md) §2 | M7, M8 | Equipo de protección, expediciones |
| Etapa crítica de peligro | −5 % de vida por paso (−3 % por ronda) | [Peligros del entorno](../05-salud/peligros-del-entorno.md) §3 | M7 | Letalidad del entorno |
| Hidratación | Desierto de día −5 por paso; un trago +25 | [Peligros del entorno](../05-salud/peligros-del-entorno.md) §5.3 | M7 | Cantimploras, agua |
| Contaminación | +5, +10 o +20 por paso según el nodo; −10 fuera | [Peligros del entorno](../05-salud/peligros-del-entorno.md) §5.4 | M7 | Filtros, máscaras |
| Rasgos adquiridos | 5 positivos y 5 negativos; ≤3 % en combate, ≤10 % en su oficio | [Rasgos adquiridos](../05-salud/rasgos-adquiridos.md) §1 y §4 | M7 | Identidad sin poder |
| Debilidad de Resurrección | 15 minutos tras caer en la Guarida | [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1 | M7 | Ritmo de los asaltos |

### 4.3 Frontera, ciudades y tiempo

| Número | Valor hoy | Definido en | Dueño | Qué mueve |
|---|---|---|---|---|
| Techo de la Frontera (antes, del Piso) | Por definir con D-58. Antes: +5 sobre el piso del último Sello y experiencia al 10 % | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md), [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.4 | M2, M9 | C-08 |
| Viento de Cola | Sigue con D-58 para las zonas que quedaron muy atrás de la Frontera; números por definir. Antes: Eco −10 % de vida cada 5 pisos (tope 30 %) y +25 % de experiencia | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md), [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.3 | M9 | Puesta al día de quien llega tarde |
| Ritmo de la Frontera (antes, de pisos) | Referencia hasta que D-58 fije los suyos: descubrimiento 2-5 días; esfuerzo de guerra 3-7 días; un paso cada 1-2 semanas | [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.1 | M9 | C-05 |
| Sello | Se retira con D-58. Antes: Guardián + 3 de 6 pruebas | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md), [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.2 | M9 | Caminos de progreso |
| Consumo de la ciudad | 1 ración por habitante al día real; guardia 1,5; enfermo 1,25; obrero +0,5 por jornada; invierno +0,2 y leña | [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §4.2 | M9 | C-06 |
| Umbrales de despensa | 14+ días Abundancia; 7-13 Holgada; 3-6 Justa; 1-2 Escasez; 0 Hambruna | [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §3.2 | M9 | Obras, aldeanos, etapa (C-06) |
| Amenaza base por etapa | Campamento 10, Aldea 15, Villa 20, Ciudad 25, Castillo 30 por día; x1,5 en invierno | [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §6.1 | M9 | Incursiones, defensas, guardias |
| Requisitos de etapa | Población, despensa sostenida (2 a 10 días), salud, ánimo, orden, seguridad, incursiones superadas y racha (1 a 5 días) | [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §7 | M9 | Duración del Claro al Castillo (P-55) |
| Cisma | 15 % de los residentes activos o 30 jugadores (lo mayor), con un Maestro de obras; 7 días de plazo; tope de 7 castillos | [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §5-6 | M9 | Facciones, guerra |
| Mandatos | Una temporada; máximo dos seguidos | [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §4 | M9 | Política |
| Día de juego | 6 horas reales | [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §2 | M1, M8 | C-19 |
| Estación | Una semana real (un año = 4 semanas) | [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §4 | M8 | Cosechas, inviernos, enfermedades |
| Luna llena | Cada 7 días de juego | [Eventos](../06-contenido/eventos.md) | M8 | Licantropía, amenaza, bestias raras |
| Temporada | 3-4 meses (arena: 3) | [Progresión](../03-personaje/progresion.md) §7 | M18 | C-14 |

### 4.4 Economía y propiedad

| Número | Valor hoy | Definido en | Dueño | Qué mueve |
|---|---|---|---|---|
| Impuestos del mercado | 1,5 % por publicar + 4 % sobre la venta | [Economía](../07-economia/economia.md) §5 | M13 | C-04 |
| Vencimiento de órdenes | 7 días | [Economía](../07-economia/economia.md) §3 | M13 | Tasas repetidas |
| Bandas de precio | Mínimo y máximo por objeto según su historial | [Economía](../07-economia/economia.md) §3 (D-26) | M13 | Comercio con dinero real |
| Quema en transferencias | Por definir (referencia: 5 %, como el bot Iris) | [Seguridad](seguridad-y-anti-trampas.md) §4 | M13 | Lavado de oro, mulas |
| Desgaste al caer en zona amarilla | −10 % de durabilidad | [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1 | M4 | Reparaciones, herreros |
| Tasa autodeclarada | Por ejemplo, 2 % semanal; una semana de gracia | [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) §3 | M25 | Rotación de lugares, sumidero |
| Impuesto de la casa | Lo fija el gobierno del reino dentro de un rango (rango por definir) | D-48 | M25, M9 | Tesoro de cada reino, dónde vivir |
| Cupo de puestos | 10-40 por lugar; tope de 2 por capital por jugador; 1 parcela de gremio por capital | [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) §1 y §6 | M25 | C-09 |
| Subasta inicial | 48 horas; el oro se quema | [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) §2 | M25 | Sumidero |
| Aceleradores | De +25 % a +50 %; uno por tipo | [Monetización](../07-economia/monetizacion.md) §3 | M22 | C-17 |
| Comisiones del Circuito | Casa PNJ 10 %; tributo al submundo 5 %; pagaré 3 % | [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §8.1 | M16, M12 | Sumideros del azar |

### 4.5 Oficios

| Número | Valor hoy | Definido en | Dueño | Qué mueve |
|---|---|---|---|---|
| Límite de oficios | Ninguno duro (D-57): el freno es el costo del conocimiento. [Profesiones](../07-economia/profesiones.md) §3 todavía dice 2 mayores y una recolección a 100 | D-57, [Profesiones](../07-economia/profesiones.md) §3 | M14 | C-12 |
| Curva de rango | Gran Maestro en ~1 año de juego constante | [Profesiones](../07-economia/profesiones.md) §4 | M14 | Carrera del artesano |
| Fabricación rápida | Techo de calidad: Notable | [Fabricación](../07-economia/fabricacion.md) §1 | M14 | Valor del minijuego |
| Copias de plano | 10 usos | [Fabricación](../07-economia/fabricacion.md) §5 | M14 | Mercado de conocimiento |
| Especialidad de capital | +15 % de retorno de material | [Fabricación](../07-economia/fabricacion.md) §6 | M14 | Movimiento entre capitales |

### 4.6 PvP, social y plataforma

| Número | Valor hoy | Definido en | Dueño | Qué mueve |
|---|---|---|---|---|
| Karma | Naranja durante 1 hora; rojo con 3 muertes de verdes en 24 horas | [PvP](../06-contenido/pvp.md) §2 | M12 | Bandidos, cazarrecompensas |
| Guerra de castillos | Cuentan los activos de los últimos 3 días | [PvP](../06-contenido/pvp.md) §7 | M12 | Multicuentas |
| Foso | 15 rondas; topes diarios de 5, 3 y 1; desde el nivel 10 | [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §3.1 y §9 | M12, M16 | Abuso, salud |
| Gremio | 10 a 100 miembros; inactivos a los 14 días; crear desde el nivel 5 | [Gremios y vida social](../08-social/gremios-y-social.md) §1 | M15 | Escala de los gremios |
| Mentoría | Hasta el nivel 20 | [Gremios y vida social](../08-social/gremios-y-social.md) §5 | M15 | Novatos |
| Límites de Telegram | 4.096 caracteres; `callback_data` de 64 bytes; ~1 mensaje por segundo por chat, ~20 por minuto por grupo, ~30 por segundo en total; una edición cada 3-5 s | [Telegram](telegram.md) §2 y §5 | M19 | Todo lo que se muestra en Telegram |

### 4.7 Reglas escritas en más de un documento

Cuando cambian, se cambian **en todos** sus lugares en el mismo cambio. Si no, el diseño se contradice y una IA que lea el documento viejo se equivoca.

| Regla | Dónde está escrita |
|---|---|
| Qué se pierde al caer por zona | [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1, [PvP](../06-contenido/pvp.md) §1, [Torre y pisos](../02-mundo/torre-y-pisos.md) §3, [Peligros del entorno](../05-salud/peligros-del-entorno.md) §3.1 |
| Mitigación de armadura | [Balance](../03-personaje/balance.md) §4, [Daño y estados](../04-combate/dano-y-estados.md) §1 |
| Techo del Piso (con D-58, de la Frontera) | [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.4, [Progresión](../03-personaje/progresion.md) §2, [Monetización](../07-economia/monetizacion.md) §3 |
| Protección de novato (nivel 10) | [05 · Salud](../05-salud/README.md), [Heridas](../05-salud/heridas.md) §7, [Enfermedades](../05-salud/enfermedades.md) §6, [Peligros del entorno](../05-salud/peligros-del-entorno.md) §11, [Crimen y justicia](../06-contenido/crimen-y-justicia.md) §8, [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §9, [Defensa](../09-construccion/defensa-y-protecciones.md) §5, [Bestiario](../06-contenido/bestiario.md) §12 |
| Tope de golpe en PvP (40 %) | [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11, [PvP](../06-contenido/pvp.md) §5, [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §3.1, [Peligros del entorno](../05-salud/peligros-del-entorno.md) §6, [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §15 |
| Botones de combate (D-46: 6) | [Telegram](telegram.md) §3, [Balance](../03-personaje/balance.md) §1, [Clases](../03-personaje/clases-y-especializaciones.md) §4, [Equipamiento](../03-personaje/equipamiento.md) §7, [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §1, [Ronda y acciones](../04-combate/ronda-y-acciones.md) §2. Los minijuegos de [Fabricación](../07-economia/fabricacion.md) §2 y de [Sistema de construcción](../09-construccion/sistema-de-construccion.md) §4 copian el límite del combate |
| Descanso x2 y x3 | [Heridas](../05-salud/heridas.md) §5, [Casa propia](../09-construccion/casa-propia.md) §2, [Curación](../05-salud/curacion-y-tratamientos.md) §5 |
| Entrenadores y exámenes | [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) §3, [Profesiones](../07-economia/profesiones.md) §11, [Curación](../05-salud/curacion-y-tratamientos.md) §0, [Sistema de construcción](../09-construccion/sistema-de-construccion.md) §2 |
| Sumideros en porcentaje | [Economía](../07-economia/economia.md) §1, [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §8.1, [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) §3 |
| Tiradas a la vista (dado nativo → tirada pública auditable) | [Web y multiplataforma](web-y-multiplataforma.md) §6.1 (la regla que vale), [Telegram](telegram.md) §1 y §3, [Apuestas](../08-social/apuestas.md) §2, [Gremios y vida social](../08-social/gremios-y-social.md) §4, [Equipamiento](../03-personaje/equipamiento.md) §9, [Clases](../03-personaje/clases-y-especializaciones.md) §2 (Pícaro Forajido) |
| Necesidades y medidores de la ciudad | [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §2-3, [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §3 y §7, [Crisis](../02-mundo/crisis-problemas-y-soluciones.md) §1, [Red de sistemas](../00-vision/red-de-sistemas.md) §3 |
| Gobernador y mandatos | [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §4, [Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md) §4 |
| Sello y sus pruebas (se retira con D-58) | [Torre y pisos](../02-mundo/torre-y-pisos.md) §4.2, [Misiones y exploración](../06-contenido/misiones-y-exploracion.md) §5, [Profesiones](../07-economia/profesiones.md) §9 |
| Linajes y lo que resisten | [Creación de personaje](../03-personaje/creacion-de-personaje.md) §1, [Peligros del entorno](../05-salud/peligros-del-entorno.md) §9, [Bestiario](../06-contenido/bestiario.md) §5.1 |

---

## 5. Acople con los clientes: Telegram, web y app móvil

Un solo motor, un solo mundo y tres clientes de primer nivel (D-40, D-41). La Mini App de Telegram es el mismo cliente web abierto dentro de Telegram, no un cliente aparte. El detalle de cómo se arma cada cliente está en [Web y multiplataforma](web-y-multiplataforma.md) §3 y en la regla 7 de la [arquitectura](arquitectura-modular.md) ("el motor devuelve vistas, no mensajes"); si esos documentos usan otros nombres para las piezas de abajo, mandan los suyos. Entre el motor y los clientes están los servicios de juego (en el código, `engine/service/`): no tienen reglas propias, pero cambiar sus órdenes o sus vistas es cambiar el contrato de §5.2. Aquí solo va **qué cambio del motor obliga a tocar los clientes**.

### 5.1 Las tres piezas que comparten el motor y los clientes

| Pieza | Qué es | Quién la define | Regla |
|---|---|---|---|
| **Vista** | Lo que el motor responde a cada orden: el estado, los avisos y las acciones disponibles, solo con lo que ese jugador puede ver y sin formato de ningún cliente (combate, cuerpo, mercado, obra, ciudad) | El módulo dueño; la entrega M19 | Se amplía agregando campos; nunca se quita ni se renombra uno sin una versión nueva de la vista |
| **ID de acción** | El identificador de cada cosa que el jugador puede hacer (atacar, beber, pujar, firmar) | El módulo dueño | Estable y corto: cabe en los 64 bytes de `callback_data` de Telegram. Solo se agrega (C-18) |
| **Textos** | Lo que lee el jugador, en español e inglés | Los archivos de idiomas de M1 y los de contenido de cada módulo | Nunca se escriben en el código del motor. El motor los entrega ya traducidos al idioma del jugador dentro de la vista. Los clientes no inventan textos de reglas |

**La regla de oro: los clientes no calculan reglas.** Solo muestran lo que manda el motor. Es la lección de TowerWars: el nivel mínimo de una pieza estaba declarado, pero ni el mercado ni el almacén lo comprobaban. Si un cliente calcula algo (un precio, un tiempo de curación, si una acción está permitida), cada cambio de balance obliga a tocar tres clientes y tarde o temprano uno queda distinto, lo que **rompe** D-40.

### 5.2 Qué cambio del motor obliga a tocar los clientes

| Cambio en el motor | ¿Toca los clientes? | Qué hay que tocar |
|---|---|---|
| Un número de balance o de economía | No | Nada, si los clientes solo muestran. Solo las notas de versión y las guías que citen el número |
| Una regla nueva que se ve (barra, estado, etapa de peligro, medidor de ciudad) | Sí | Los tres clientes deben mostrarla. Si uno no la muestra, quien juega ahí no recibe el aviso y se **rompe** "nunca sin aviso" ([Peligros del entorno](../05-salud/peligros-del-entorno.md) §11) |
| Una acción nueva | Sí, poco | ID de acción y clave de texto en ES y EN. En combate, respetar los 6 botones (D-46); en Telegram, 2 o 3 botones por fila |
| Renombrar o quitar una acción | Sí: **rompe** | Botones ya enviados en Telegram, atajos de la app, Tácticas guardadas. Se retira, no se borra (C-18) |
| Un campo nuevo en una vista | Compatible | Los clientes viejos lo ignoran; los nuevos lo muestran |
| Quitar o renombrar un campo de una vista | Sí: **rompe** | Sobre todo la app instalada que no se actualizó. Hace falta una versión nueva de la vista |
| Un texto nuevo o cambiado | Sí, poco | El texto en ES y EN en los archivos de idiomas. En Telegram, que el mensaje no pase de 4.096 caracteres en el idioma más largo; en pantallas chicas, que el botón no se trunque |
| Un temporizador | Sí, poco | El motor manda la hora de fin y cada cliente muestra la cuenta atrás. La misma duración en todos |
| Una tirada al azar visible | Sí | Siempre la tirada pública auditable del motor: huella de la semilla antes, semilla revelada después, resultado a la vez en todos los clientes. El dado nativo de Telegram solo dibuja el número (M1, M16) |
| Un dato que debe quedar oculto (tipo real de un aviso, enfermedad sin diagnosticar, acción del rival, solución de un caso, nombre detrás de un apodo) | Sí: cuidado | Nunca se manda al cliente, ni escondido en la página. Si se envía, la web lo deja leer y **rompe** la paridad (D-40) y la regla de los avisos que mienten (M6) |
| La precisión de un dato (vida del jefe, postura, acumulaciones, Aguante) | Sí | La fija el motor y es igual para todos. Ningún cliente recibe un número más fino |
| Algo que abre una competencia (región, Guarida, veta excepcional, bestia legendaria, caso semanal) | Sí | Hora de apertura fija, anunciada antes. El aviso puede llegar escalonado; la apertura, nunca. El motor rechaza acciones antes de la hora |
| Un desempate (iniciativa, "gana quien eligió primero", combos) | Sí: cuidado | Nunca por orden de llegada ni por milisegundos: por tramos gruesos del plazo y luego una tirada del motor. Si dependiera de la velocidad, el cliente más rápido tendría ventaja |
| Un aviso urgente (te toca, te atacan, la despensa está en Justa) | Sí | Telegram: el bot solo escribe a quien le dio `/start`; app: notificación; web: aviso en pantalla. Las preferencias viven en M19 |
| Un pago | Sí | Solo el adaptador de pago de ese cliente (M22). El catálogo y las Gemas son de la cuenta |
| El orden o la cantidad de botones de combate | Sí | Las tres pantallas de combate y las Tácticas que se muestran. D-46 fija el máximo |

### 5.3 Mecánicas que nacieron en Telegram

Cada una tiene una **regla neutral** que vale en los tres clientes; la forma de Telegram es solo una representación. La tabla completa, con cómo se ve en cada cliente, está en [Web y multiplataforma](web-y-multiplataforma.md) §6, y **manda ese documento**. Aquí va lo que le importa al mapa: qué módulos se tocan si cambia la regla neutral.

| Mecánica de Telegram | Regla neutral | Módulos que la usan |
|---|---|---|
| Dados animados nativos | Tirada pública auditable | M5 (emboscada e iniciativa inicial), M15 (botín Necesidad o Codicia), M16 (taberna, Fortuna, lotería), M3 (Dados del Destino del Pícaro Forajido), M12 (regla de la noche del Foso), M1 (semillas) |
| Spoiler que tapa un resultado | Boleto sellado al comprarlo | M16 (rasca y gana) |
| Encuestas nativas y en modo quiz | Votación y pregunta del motor, con censo, plazo y recuento auditable | M9 (gobernador, leyes, moción de censura, cisma, raciones), M12 (juicios, missio del Foso), M15 (votos de gremio), M16 (trivia) |
| Reenvío como firma | Documento verificable con ID; firmar es una orden | M9 (carta de fundación, tratados), M13 (contratos), M12 (partes de guerra, informes), M17 (pruebas de hazañas) |
| Reenvío para mover objetos | Vale: objeto del motor de un uso, que cambia de dueño con una orden | M15 (vales del almacén del gremio), M4 |
| Mensaje vivo, citas plegables, `.txt` | Vista viva e informe en dos capas | M19 y todos los que muestran estado (M5, M14, M24, M9) |
| Modo inline y privado del bot | Visibilidad de cada dato: pública, de grupo o privada | M16 (mano de cartas, La Máscara), M12 (lugar y hora del Foso), M4 (inventario) |
| Grupos, temas y salas retransmitidas | Salas y espacios de comunidad del motor; el grupo de Telegram es un puente | M15 (gremio), M11 (buscador, bandas), M12 (Foso), M9 (ciudad, castillo), M6 (jefe errante con Cuerno) |
| Canales | Feed de noticias del motor | M19 (Gaceta, Mercado, Salón de los Caídos, Novedades) |
| El bot no escribe sin `/start` | Bandeja de avisos del motor | M19, M15 (invitaciones), M12 (retos), M7 (consultas médicas) |
| "Conectado" (no existe en Telegram) | Estados explícitos: "disponible para ayudar", "presente" | M6 (signos de invocación), M24 (tomar el mando en la defensa), M12 (redadas, inactividad en el Foso) |
| Juegos HTML5 y `setGameScore` | Minijuego como complemento; la puntuación la valida el servidor | M16 (salón recreativo) |
| Telegram Stars | Pagos enchufables: el motor solo recibe "compra confirmada" | M22 |
| ID de Telegram como identidad | Cuenta del juego con identidades vinculadas | M1, M23, M22 |

### 5.4 Cómo se ve en el código

Una acción disponible dentro de una vista, con su nota `[ES]` (formato de clase de [Convenciones](convenciones-de-codigo.md) §3):

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ActionOption:
    """One action the player can take right now, the same for every client.

    Attributes:
        action_id: Stable short id, e.g. "cmb.attack". Must fit Telegram's
            64-byte callback_data together with the session token.
        label: Text already translated to the player's language by the
            language catalog (M1). Never written in engine code.
        enabled: False when the action exists but cannot be used now.

    [ES]
    Qué es: una acción disponible dentro de una vista (regla 7 de la arquitectura).
        Es la misma para Telegram, la web y la app (D-40, D-41).
    Quién la usa: la crea el módulo dueño (por ejemplo M5 Combate, con los 6 botones
        de D-46); la entrega M19; cada cliente la dibuja como botón, enlace o toque.
    Si cambia, afecta: agregar un campo con valor por defecto es seguro. Quitar o
        renombrar uno rompe la app instalada y el adaptador de Telegram. Cambiar un
        action_id rompe botones ya enviados y Tácticas guardadas.
        Ver diseno/01-plataforma/mapa-de-impacto.md §5 y C-18.
    """

    action_id: str
    # Stable forever: add new ids, never rename or reuse old ones.
    # [ES] ID fijo (regla 5). Telegram lo manda en callback_data; la app y la web lo
    #      guardan en atajos. Cambiarlo rompe los tres clientes sin dar error (C-18).
    label: str
    enabled: bool = True
    # Disabled options are still shown, so players see why they cannot act.
    # [ES] Lo decide el motor (sin Aguante, pierna rota, sin objetos en el cinturón).
    #      El cliente solo lo muestra apagado: nunca calcula la regla (§5.1).
```

---

## 6. Huecos y contradicciones (propuesta)

Lo que el mapa encontró al cruzar los documentos. No se corrige aquí: cada punto se resuelve en su documento o en la [arquitectura](arquitectura-modular.md), y después se actualiza este mapa.

### 6.1 Responsabilidades sin dueño claro

| Responsabilidad | Dónde se describe | Quién la toca | Dueño propuesto |
|---|---|---|---|
| Reputaciones (asentamiento, facción, órdenes) | [Progresión](../03-personaje/progresion.md) §5 | M9 (prueba del Sello), M10 (Orden de Cazadores, Agencia), M14 (recetas) | M2 |
| Maestrías de armas y armaduras | [Progresión](../03-personaje/progresion.md) §3 | M4, M5 | M2 |
| Enfoque diario | [Economía](../07-economia/economia.md) §8 | M13, M14 | M14 |
| Vetas | [Fabricación](../07-economia/fabricacion.md) §3, [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §6 | M14 (según la arquitectura), M8 (nodos) | M14, con los nodos de M8 |
| Yacimientos únicos | [Geografía y recursos](../02-mundo/geografia-y-recursos.md) §3 | M8 (lugar), M14 (extracción), M9 (cuotas del Ecologista), M12 y M24 (reclamar con un puesto fortificado) | M8 |
| Vivienda | La arquitectura la pone en M15 y las casas en M24 | M15, M24, M25 | M24 la obra y las habitaciones; M15 las visitas y los permisos sociales |
| Laberinto, Laberinto Cambiante, Pruebas de Maestría, Pesadillas | [Misiones y exploración](../06-contenido/misiones-y-exploracion.md) §5-8 | M9, M10, M11 | M11 |
| Tesoro Semanal y protección contra mala racha | [Equipamiento](../03-personaje/equipamiento.md) §9 | M4, M6, M11, M12 | M11 cuenta las actividades; M4 entrega |
| Tácticas y Ecos | [Avisos y tácticas](../04-combate/avisos-y-tacticas.md) §3 | M5, M6 (invocar un Eco), M12 (arena asíncrona), M24 (guardias) | M5 |
| Mancha de sangre | [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1 | M8 (según la arquitectura), M5 (últimas 3 rondas), M13 (Esencia) | M8 |
| Juramento de Hierro | [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.2 | M2 (se elige al crear), M7, M12, M18 | M7 |
| Peligros del entorno | [Peligros del entorno](../05-salud/peligros-del-entorno.md) | M7 (barras y etapas), M8 (rigor y clima) | Repartido: M8 el rigor del nodo, M7 lo que le pasa al cuerpo |
| Ecología y poblaciones | [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §5, [Bestiario](../06-contenido/bestiario.md) §10 | M8, M6, M10, M9, M24 | M8 |
| Gaceta y canales | [Gremios y vida social](../08-social/gremios-y-social.md) §7 | Muchos | M19 publica; cada noticia la da el módulo que publica el evento |
| Vigor (P-45) | [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §1 | M8, M10 | M8 |
| Seguidores y trabajadores PNJ | [Casa propia](../09-construccion/casa-propia.md) §5, [Fabricación](../07-economia/fabricacion.md) §7 | M24, M14, M10 | M24 los seguidores; M14 los trabajadores |
| Aldeanos PNJ de la ciudad | [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) §2 | M9, M14, M24 | M9 |
| Salud de animales y cultivos, cría | [Animales y cultivos](../05-salud/animales-y-cultivos.md) | M7, M14 (Agricultura, Ganadería) | M7 la salud; M14 la producción |
| Robo como oficio menor | [Crimen y justicia](../06-contenido/crimen-y-justicia.md) §2 | M12, M14 | M12 el delito; M14 la curva del oficio |
| Gemas (moneda premium) | [Economía](../07-economia/economia.md) §2, [Monetización](../07-economia/monetizacion.md) | M13 la lista entre las monedas; M22 está aislado | M22: nunca se convierten en oro |
| Mochilas e inventario (D-47) | Documento en redacción | M4, M14, M5 | M4 |
| Comunidades PNJ del Colapso (D-45) | [El Colapso y las comunidades](../02-mundo/el-colapso-y-las-comunidades.md) | M9, M12, M25 | M9 |
| Museo | [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md) §3 | M24 (edificio), M17 (colección) | Repartido |
| Botín (D-52) | [Botín](../03-personaje/botin.md) | M6 (tablas), M4 (objetos), M11 (reparto en grupo), M13 (Mercado Negro) | M6 decide qué cae; M4 crea el objeto |
| Investigación, maestría y escalera de conocimiento (D-53, D-54) | [Investigación y maestría](../07-economia/investigacion-y-maestria.md), [Investigación médica](../05-salud/investigacion-medica.md) | M14, M10 (investigaciones), M7 (medicina), M9 (árbol de la ciudad) | M14; la medicina, con M7 |
| Elixires propios (D-55) | Documento en redacción | M14 (Alquimia), M7 (toxicidad y efectos) | M14 los crea; M7 aplica efectos y topes |
| Pistas y Bitácora (D-56) | [Aprendizaje y pistas](../00-vision/aprendizaje-y-pistas.md) | Todos los módulos con actividades; M19 (la pista va en la vista) | Cada módulo da sus pistas como datos; M19 las entrega; la Bitácora, M17 |
| Mapa sin borde y viaje (D-58) | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) | M8, M9 (Frontera), M13 (transporte), M24 (caminos y postas) | M8 |

### 6.2 Contradicciones entre documentos

1. **Botones de combate.** D-46 fija 6 botones y una sola elección por ronda. Ya lo aplican [Telegram](telegram.md) §3, [Balance](../03-personaje/balance.md) §1, [Clases](../03-personaje/clases-y-especializaciones.md) §4, [Equipamiento](../03-personaje/equipamiento.md) §7 (las técnicas ocupan una casilla de habilidad), [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md) §1 y [Ronda y acciones](../04-combate/ronda-y-acciones.md) §2. Falta [Fabricación](../07-economia/fabricacion.md) §2, que dice "máximo 8 botones, como en el combate", y el minijuego de [Sistema de construcción](../09-construccion/sistema-de-construccion.md) §4, que muestra 8.
2. **Descuento Premium en impuestos.** [Economía](../07-economia/economia.md) §5 lo menciona, y D-43 solo permite cosméticos y aceleradores con dinero real.
3. **Ficha de oro en las apuestas.** [Apuestas](../08-social/apuestas.md) §4 dice "si existe la ficha"; D-43 la descarta.
4. **Pagos solo con Stars.** La [arquitectura](arquitectura-modular.md) ya describe M22 con Telegram Stars, la pasarela web y las tiendas, como D-41 y [Monetización](../07-economia/monetizacion.md) §4. Queda [Economía](../07-economia/economia.md) §2, que todavía dice que las Gemas se compran con Telegram Stars.
5. **Impuesto de la casa.** [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) §3 dice "tasa fija según la ubicación"; D-48 dice que la fija el gobierno del reino dentro de un rango.
6. **Dificultades de las mazmorras.** [Torre y pisos](../02-mundo/torre-y-pisos.md) §2 dice que mazmorras y laberintos tienen Normal, Profundidades, Corrompido, Abismal y Pesadilla; [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) §1 usa Normal, Heroica, Mítica y Mítica+. Se resuelve al retirar Torre y pisos (D-58); hasta entonces vale Mazmorras y bandas.
7. **Vivienda en dos módulos.** La [arquitectura](arquitectura-modular.md) pone "vivienda" en M15 y "casas" en M24 (propuesta en §6.1).
8. **Documentos con funciones de Telegram.** La [arquitectura](arquitectura-modular.md) §2 ya deja la cola de ediciones y los límites de envío en el adaptador de Telegram, como [Web y multiplataforma](web-y-multiplataforma.md). La tabla §14 de ese documento lista los que todavía describen mecánicas con funciones de Telegram (dado nativo, reenvío como firma, encuestas); mientras no se ajusten, vale la regla neutral.
9. **Carpetas del código en español o en inglés.** La [arquitectura](arquitectura-modular.md) §6 ya cuenta los 25 módulos, pero nombra las carpetas en español (`motor/`, `contenido/`, `adaptadores/`, `pruebas/`); las [Convenciones](convenciones-de-codigo.md) §7.1 las ponen en inglés (`engine/`, `content/`, `adapters/`, `tests/`), como pide D-42. Con D-59 el código empieza ya: hay que alinearlas antes del primer archivo.
10. **Contagio por probabilidad o por barra.** [Enfermedades](../05-salud/enfermedades.md) §2 y [Heridas](../05-salud/heridas.md) §2 hablan de "riesgo" de contagio por mordida; el [Bestiario](../06-contenido/bestiario.md) §5.1 lo cambia por una barra que se acumula, "sin azar ciego".
11. **Pisos (D-58).** D-58 quita la Torre y los pisos, pero la [arquitectura](arquitectura-modular.md) (M8, M9, M11, el evento `PisoAbierto` y la regla 4) y muchos documentos ([Torre y pisos](../02-mundo/torre-y-pisos.md), [Progresión](../03-personaje/progresion.md) §1-2, [Monetización](../07-economia/monetizacion.md) §3, [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md) §1, [Economía](../07-economia/economia.md) §4, [Jefes](../06-contenido/jefes.md) §4) todavía hablan de pisos, Frente, Sello y piedra de paso. Este mapa sigue D-58 (§1.5). Falta decidir qué evento reemplaza a `PisoAbierto` y si M9 cambia de nombre, sin cambiar de número.
12. **Límite de oficios (D-57).** [Profesiones](../07-economia/profesiones.md) §3 y §13 todavía dicen 2 oficios mayores y una sola recolección a 100, y [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §2 cuenta con "cambiar de oficio mayor". D-57 quita todo límite duro.
13. **¿El nivel 10 todavía es de novato?** Casi todos los documentos dicen "hasta el nivel 10"; el [Bestiario](../06-contenido/bestiario.md) §12 dice "nivel 10 o menos" (el 10 incluido), y [Peleas clandestinas](../06-contenido/peleas-clandestinas.md) §9 deja entrar al Circuito desde el nivel 10. Hay que fijarlo y escribirlo igual en todos los documentos de §4.7. El ejemplo de las [Convenciones](convenciones-de-codigo.md) §5.3 toma el 10 como incluido.
14. **"M10" no siempre es un módulo.** [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §2 e [Investigación médica](../05-salud/investigacion-medica.md) llaman M10, M20… a los grados de Maestría. En este mapa y en el código, M1 a M25 son solo módulos. Propuesta: escribir "Maestría 10" en esos documentos.

---

Ver D-42 en [Decisiones](../00-vision/decisiones.md), las [Convenciones de código](convenciones-de-codigo.md) y la [Arquitectura modular](arquitectura-modular.md).
