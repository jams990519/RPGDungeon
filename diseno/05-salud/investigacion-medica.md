# Investigación médica: del primer caso a la regeneración

> **Módulo** [05 · Salud](README.md) · **Depende de:** [Enfermedades](enfermedades.md), [Secuelas y muerte](secuelas-y-muerte.md), [Curación](curacion-y-tratamientos.md), [Geografía y recursos](../02-mundo/geografia-y-recursos.md) (terrenos, yacimientos únicos), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (estaciones, clima, día y noche) · **Se conecta con:** [Investigación y maestría](../07-economia/investigacion-y-maestria.md) (Puntos de Investigación, proyectos, árbol de la ciudad, patentes), [Investigaciones](../06-contenido/investigaciones.md), [Profesiones](../07-economia/profesiones.md), [Fabricación](../07-economia/fabricacion.md), [Bestiario](../06-contenido/bestiario.md) (muestras), [Animales y cultivos](animales-y-cultivos.md), [Peligros del entorno](peligros-del-entorno.md), [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) (patentes), [Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md) · **Estado:** propuesta

**Qué pediste.**
- "Así como perder una pierna, tiene que haber una amplia gama de investigaciones para incluso reponerla, pero luego de tener un alto nivel en la medicina."
- "No es algo que puedas obtener de la noche a la mañana. Tienes que empezar a estudiar la enfermedad primero, las diferentes enfermedades; luego que las conozcas, cuáles son sus problemas, y a partir de ahí empezar a ver qué tipo de materiales o recursos, que se encuentran en algún área específica con alguna estación específica, te permitan llegar a regenerar."

Este documento arma eso. **Nadie cura lo que no conoce.** Toda cura nueva sale de una escalera de siete etapas, que empieza mirando enfermos y termina en un protocolo escrito. La cima de esa escalera es la **Regeneración**: reponer una pierna perdida (D-53, ver [Decisiones](../00-vision/decisiones.md)).

**De dónde sale.**
- *Pathologic 2*: el médico examina a cada enfermo, prepara tinturas con las hierbas de la estepa y decide a quién dar los pocos remedios que tiene. Curar es saber y es escasez.
- *Plague Inc.*: la cura avanza en una barra que sube más rápido cuantos más países investigan. En el modo *The Cure* primero se investiga el brote, después se entiende la enfermedad, y solo entonces avanza la cura, que además hay que fabricar y repartir.
- *Two Point Hospital* y *Theme Hospital*: la sala de investigación, donde los médicos investigan tratamientos y máquinas nuevas; más investigadores, más rápido.
- *Potion Craft* y *Skyrim*: los ingredientes tienen propiedades ocultas. En Skyrim, comer un ingrediente revela su primer efecto y los demás se descubren combinando. En Potion Craft, cada ingrediente mueve la mezcla por un mapa y las recetas se descubren explorándolo.
- *Star Wars Galaxies*: los recursos aparecían por temporadas con estadísticas al azar, duraban unos días o semanas y desaparecían. Los artesanos rastreaban los mejores lotes.
- *EVE Online*: la investigación corre en tiempo real, también sin conectarse, y cada laboratorio tiene pocos espacios.
- *Wurm Online*: cada habilidad sube solo usándola, y cada punto cuesta más que el anterior. Llegar arriba lleva años.
- *Animal Crossing* y *Stardew Valley*: peces, insectos, hierbas y cultivos que solo existen en cierta estación, a cierta hora o con cierto clima. El calendario se vuelve parte del juego.
- *RimWorld*: proyectos de investigación en un banco que avanzan con el tiempo, y un suero sanador rarísimo que repone una parte del cuerpo perdida.

---

## 1. La regla: el conocimiento médico se gana

1. **Cada mal tiene un expediente.** Cada enfermedad, herida que deja secuela y mal crónico tiene un expediente que se llena estudiando casos. Sin expediente no hay cura nueva.
2. **Siete etapas, sin atajos.** Observación → Conocimiento → Hipótesis → Ingredientes → Experimentos → Protocolo → Aplicación. No se puede empezar una etapa sin terminar la anterior.
3. **Los ingredientes están en un lugar y en un momento.** Las curas avanzadas piden materiales de un terreno, una región, un yacimiento único, una hora o una estación del año. Ninguna ciudad los tiene todos (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md)).
4. **Tiempo real.** Los estudios corren en tiempo real, también fuera de línea, como en EVE. Lo que se juega (casos, experimentos) tiene tope semanal.
5. **Usa las piezas de [Investigación y maestría](../07-economia/investigacion-y-maestria.md).** Cada nodo del árbol médico es un **proyecto** (§5 de ese documento) que se paga con **Puntos de Investigación ⚕️** (§4). Lo que agrega este documento es lo que va antes del proyecto (casos, expediente, hipótesis, ingredientes) y la escalera que lleva hasta la Regeneración. La regla de novato de ese documento (§5.3: los 3 primeros proyectos salen bien seguro) asegura el éxito del proyecto, pero **no salta** el expediente, la hipótesis ni los ingredientes. Esta escalera es la misma que D-54 extiende a todos los oficios.
6. **Nada se compra con dinero real** (D-43). Ni las Gemas ni el oro saltan una etapa. El acelerador de oficio (ver [Monetización](../07-economia/monetizacion.md)) sube la experiencia de Medicina del 1 al 100 como en cualquier oficio, pero **no toca nada de este documento**: ni los expedientes, ni los PI, ni los proyectos, ni los experimentos, ni la estación del año (igual que en [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §2.2).
7. **Lo básico ya se sabe.** Las enfermedades del catálogo tienen desde el primer día su tratamiento básico (ver [Curación](curacion-y-tratamientos.md) §7). La investigación abre las curas **completas**, las vacunas, las cirugías nuevas y, arriba de todo, la reparación de las secuelas.

### 1.1 Ligero: capa simple y capa profunda (D-44)

| Quién | Qué ve | Cuánto le pide |
|---|---|---|
| **Paciente** (casi todos) | En `/medico`, si existe un tratamiento para lo suyo y quién lo ofrece | Nada. No necesita saber que existe este sistema |
| **Médico de paso** | `/investigar`: una línea por expediente, con su barra y un botón **[🔬 Estudiar]** | Un toque cuando atiende a alguien |
| **Médico investigador** | El expediente completo, las hipótesis, la mesa de experimentos y el árbol | Lo que quiera: es su carrera |

Los experimentos tienen **modo rápido** (un botón, se resuelve con tu nivel y tu expediente) y **modo manual** (un minijuego de 3 a 6 pasos), igual que la fabricación (ver [Fabricación](../07-economia/fabricacion.md) §1).

## 2. La escalera de siete etapas

```
1 OBSERVACIÓN → 2 CONOCIMIENTO → 3 HIPÓTESIS → 4 INGREDIENTES
      → 5 EXPERIMENTOS → 6 PROTOCOLO → 7 APLICACIÓN
```

| Etapa | Qué haces | Qué se llena | Tiempo orientativo (una cura de rango Médico) |
|---|---|---|---|
| 1. **Observación** | Estudiar casos: pacientes, animales, muestras | Puntos de caso | 3 a 7 días |
| 2. **Conocimiento** | Ordenar lo observado | El expediente, por estrellas | Junto con la anterior |
| 3. **Hipótesis** | Elegir qué tipo de remedio podría servir | La hipótesis (una decisión) | Minutos, pero pide expediente ★★★ |
| 4. **Ingredientes** | Conseguir lo que pide la hipótesis | El cofre del proyecto | De 0 a 3 semanas, según la estación |
| 5. **Experimentos** | Ensayar en la mesa de investigación | Avances del protocolo | 3 a 10 días |
| 6. **Protocolo** | Escribir el tratamiento | Un protocolo con tu nombre | Al completar los avances |
| 7. **Aplicación** | Tratar, curar, vacunar, operar | Pacientes curados | Desde entonces |

### 2.1 Observación: estudiar casos

Un caso es una oportunidad de mirar un mal de cerca. Cada caso da **puntos de caso** al expediente de ese mal, y además los **PI ⚕️** que dice [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §4.1 (muestras de enfermos, primer diagnóstico de cada enfermedad, disección). Los puntos de caso solo sirven para ese expediente; los PI pagan los proyectos.

| Fuente | Cómo se consigue | Puntos | Nota |
|---|---|---|---|
| **Paciente jugador** | Diagnosticarlo o tratarlo en una consulta (ver [Curación](curacion-y-tratamientos.md) §6), con su permiso | Altos | **Seguir el caso** da más: cada fase (incubación, síntomas, pico, recuperación) cuenta aparte |
| **Paciente PNJ** | El sanatorio, los asentamientos y el tablón ("*un pastor con fiebre en Ribera Seca*") | Medios | Siempre hay alguno: nadie se queda sin casos |
| **Paciente con secuela** | Un jugador con un miembro perdido, un nervio cortado o un mal crónico ofrece su caso | Altos, y los únicos que sirven para las secuelas | El médico le paga (ver §8). Las secuelas se vuelven valiosas para la ciencia |
| **Animales** | Veterinaria: monturas, ganado y mascotas enfermas (ver [Animales y cultivos](animales-y-cultivos.md)) | Medios | Los primeros ensayos de Regeneración se hacen con monturas (§4.3) |
| **Muestras de monstruos** | Sangre o tejido de un monstruo **Enfermo** (ver [Bestiario](../06-contenido/bestiario.md) §9), y disección con conocimiento ★★★ de la especie | Medios | Las traen los cazadores |
| **Muestras del entorno** | Agua de pantano, esporas, polvo de cristal, aire de miasma, en frascos de muestra (Joyería) | Bajos | Las fuentes de contaminación de [Peligros del entorno](peligros-del-entorno.md) §5.4 |
| **Regeneración natural** | Observar a un **Trol** que regenera, a un **Licántropo** en forma bestial o a un limo que se divide | Altos, solo para la rama Regeneración | El Trol cobra por dejarse estudiar |

**Reglas de los casos:**
- **Variedad:** el mismo paciente da poco la segunda vez en la misma fase. Pacientes de linajes, anillos y fases distintos valen más.
- **Tope semanal** de puntos de caso por médico (40 casos orientativos), como el conocimiento semanal de los oficios (ver [Profesiones](../07-economia/profesiones.md) §5) y el tope de PI. Quien tiene tiempo infinito no se escapa.
- **Contra las trampas:** los casos de tus propios personajes no cuentan (ver [Seguridad y anti-trampas](../01-plataforma/seguridad-y-anti-trampas.md)).

### 2.2 Conocimiento: el expediente

El expediente tiene **seis fichas**. Se abren a medida que suben las estrellas, como el conocimiento del bestiario.

| Nivel | Casos (orientativo, enfermedad común) | Ficha que se abre | Qué te da |
|---|---|---|---|
| ☆ **Desconocida** | 0 | — | Solo ves síntomas sueltos |
| ★ **Observada** | 5 | **Síntomas** | Diagnóstico más preciso (ver [Curación](curacion-y-tratamientos.md) §2) |
| ★★ **Descrita** | 15 | **Causa:** de dónde viene y cómo se contagia | Consejos de prevención para tus pacientes |
| ★★★ **Comprendida** | 35 | **Cómo avanza** y **qué la empeora** | Puedes proponer una **hipótesis** (§2.3) |
| ★★★★ **Dominada** | 70 | **Qué la alivia** | Tus tratamientos rinden más; la hipótesis correcta se marca |
| ★★★★★ **Maestra** | 120 + un protocolo propio | **Punto débil** | Abre los nodos altos del árbol (§3) |

- Las secuelas y las enfermedades raras piden más casos; las comunes, menos.
- **Copiar un expediente** (Inscripción) se puede, y se vende. Pero leer un expediente ajeno te lleva como máximo a ★★. **Lo que se lee no reemplaza lo que se ve.**

### 2.3 Hipótesis: qué podría servir

Con el expediente en ★★★, el médico elige **qué tipo de remedio** probar y **qué propiedades** debe tener.

| Tipo de remedio | Para qué | Propiedades que suele pedir |
|---|---|---|
| **Febrífugo** | Fiebres que vuelven | Fría, Amarga |
| **Purga o quelante** | Parásitos, escoria, toxinas | Amarga, Purificante |
| **Antitoxina** | Venenos y tétanos | Purificante, Sedante |
| **Suero** | Mordidas, contagios rápidos | Pura, Mineral |
| **Vacuna** | Prevenir una enfermedad ya investigada | Pura, una muestra de la enfermedad |
| **Injerto** | Piel quemada, tejido perdido | Cicatrizante, Renovadora |
| **Cirugía nueva** | Lo que no se arregla con remedios | Instrumental, Sedante (anestesia) |
| **Tónico de la mente** | Fobias, pesadillas, cordura | Calmante, de Memoria |

- La pantalla ofrece **3 o 4 hipótesis** sacadas de lo que dice el expediente. Elegir mal no castiga: los experimentos fallan más, y **cada fallo descarta una opción**, como en un caso de detective (ver [Investigaciones](../06-contenido/investigaciones.md)).
- Con ★★★★, la hipótesis correcta aparece marcada. La capa simple puede elegir esa y seguir.

### 2.4 Ingredientes: un lugar y un momento

La hipótesis pide propiedades. Cada ingrediente tiene **cuatro propiedades ocultas**: la primera se ve al recogerlo, y las otras se descubren en los experimentos (como en Skyrim). Las curas avanzadas piden ingredientes que **solo existen en cierto lugar y en cierto momento**.

**Los relojes del mundo** (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)):
- **Estación del año:** cambia cada semana real. Cada estación vuelve cada 4 semanas.
- **Día y noche:** un día de juego dura 6 horas reales.
- **Luna llena:** cada 7 días de juego, unos 2 días reales. **Eclipse:** una vez al mes en un anillo (ver [Eventos](../06-contenido/eventos.md)).
- **Clima:** ventisca, tormenta, lluvia, ola de calor.

| Ingrediente | Dónde | Cuándo | Quién lo trae | Propiedades | Sirve para |
|---|---|---|---|---|---|
| **Flor de Ciénaga Tardía** | 🐸 Pantano, anillo IV | Solo en **otoño**, de **noche** | Herborista con máscara de carbón | Fría, Amarga | Cura completa de la Fiebre del Pantano crónica |
| **Musgo de Cumbre Blanca** | 🏔️ Montaña (Picos Helados), anillo VI | Solo en **invierno**, después de una ventisca | Herborista aclimatado, con abrigo 3 | Cálida, Pulmonar | Neumonía, *Pulmón manchado*, Tos del Minero |
| **Glándula de Licántropo** | ❄️ Tundra y 🌲 bosque, anillo VI | Solo en **luna llena** | Cazador con Desuello y conocimiento ★★★★ del Licántropo Salvaje | Regenerativa, Salvaje | Rama Regeneración: el tejido que vuelve a crecer |
| **Agua de fondo del Oasis Hondo** | 🏜️ Desierto, anillo V | Solo en **verano**: cuando el oasis baja, aflora el agua del fondo | Explorador o aguador, con frasco de vidrio de duna | Pura, Mineral | Base de sueros y vacunas |
| **Cristal de Resonancia Profunda** | 🌑 Grietas del Abismo Umbrío, anillo IX · **yacimiento único** | Siempre, pero rinde **1 por día** | Minero con forro de plomo y filtro bendito | Resonante, Ordenadora | Nervios, Mente y el molde de la Regeneración |
| **Raíz de mandrágora tierna** | 🐸 Pantano, anillo IV | **Primavera** | Herborista o cazador con tapones de cera | Sedante, Adormecedora | Anestesia profunda para la cirugía mayor |
| **Lágrima helada** | ❄️ Tundra y pasos, anillo VI (Novia de Escarcha) | Con **ventisca** | Cazadores en grupo | Fría, Conservante | Cámara fría: mantiene vivo un tejido durante días |
| **Corazón de micelio** | 🕳️ Cueva, anillo III (Micelio Andante) | Siempre; **cultivado** en casa rinde más | Cazador, y después Agricultor que lo cultiva | Creciente, Pegajosa | El andamio donde crece el tejido nuevo |
| **Miel negra** | 🏛️ Ruinas y 🌲 bosque, anillo VII (Árbol Hueco) | **Otoño** | Cazador y herborista | Cicatrizante, Dulce | Injertos de piel, quemaduras de grado 3 |
| **Escama de salamandra en muda** | 🌋 Tierras volcánicas, anillo VIII | **Verano**, época de muda | Cazador con capa ignífuga | Cálida, Renovadora | Piel nueva: quemaduras extensas, Podredumbre Gris |
| **Polen de Flor de Difuntos** | 🌾 Llanuras de cualquier anillo | Solo durante el **festival de difuntos** (otoño) | Herborista o agricultor | Calmante, de Memoria | Rama Mente: fobias y pesadillas |
| **Agua de rayo** | 🌸 Tierras flotantes, anillo X | Solo con **tormenta** | Explorador con pararrayos y cuerda | Vivificante, Nerviosa | Despertar un nervio dañado |
| **Sal de Estrellas** | **Yacimiento único** (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md) §2) | De **noche**, con cielo despejado | Minero; quien controla el yacimiento pone la cuota | Purificante, Pura | Vacunas mayores y la cura de la Plaga |
| **Hongo del Eclipse** | 🕳️ Cuevas del anillo en eclipse | Solo en **eclipse** | Herborista con luz | Sombría, Despertadora | Elixir de lucidez (cordura) |
| **Bilis de plaga** | Portadores de la Plaga (ver [Bestiario](../06-contenido/bestiario.md)) | Solo durante una **epidemia** | Cazadores en una *Cacería de plaga* (ver [Cacerías](../06-contenido/cacerias.md)) | Contagiosa | La cura y la vacuna de la Plaga Pálida |

**Reglas de los ingredientes:**
- **Calidad por lote**, como en Star Wars Galaxies: cada lote tiene **Pureza** y **Potencia** (ver [Fabricación](../07-economia/fabricacion.md) §3). Un lote mejor sube la probabilidad de éxito en los experimentos.
- **Algunos caducan.** La Flor de Ciénaga se marchita en 12 horas reales y la Glándula de Licántropo en 2 días. Se conservan con ámbar, frascos de vidrio de duna o lágrimas heladas, o se mandan por correo urgente. Eso le da trabajo al comerciante y al transportista.
- **El calendario se vende.** Los eruditos que predicen lunas llenas y eclipses (Astronomía, ver [Catálogo ampliado](../00-vision/catalogo-ampliado.md)) y los cartógrafos que marcan floraciones venden esa información.
- **Algunos se descubren por rumores** (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §7): "*dicen que en verano el Oasis Hondo muestra un agua que no es de este mundo*".
- **Mercado de temporada:** en otoño la Flor de Ciénaga baja de precio; en primavera, quien guardó flores conservadas cobra caro.

### 2.5 Experimentos: la mesa de investigación

La **mesa de investigación** es una estación de oficio. Está en la enfermería de una casa o de un gremio, en el sanatorio y en la Academia del Castillo (ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md)); la del **Anfiteatro anatómico** de la Academia da +5 % de éxito (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §7.1). Pide instrumental (Herrería), frascos (Joyería) y alambique (Alquimia).

**El proyecto.** Con la hipótesis elegida y los ingredientes en el cofre, el médico abre el **proyecto** del nodo: paga sus PI ⚕️, ocupa uno de sus lugares de proyecto y arranca un reloj con un **tiempo mínimo** (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §5). Lo que lo hace avanzar son los experimentos.

- **Modo rápido:** un botón. El resultado sale de tu nivel de Medicina, tu expediente, la calidad de los ingredientes y la mesa.
- **Modo manual:** un minijuego de 3 a 6 pasos con tres barras: **Avance**, **Riesgo** y **Muestra** (la muestra se gasta en cada prueba). Acciones: Mezclar, Calentar, Enfriar, Destilar, Añadir ingrediente, Observar, Anotar, Parar. El modo manual da más avance y más descubrimientos.
- **Tope diario:** 3 experimentos por día y por médico. Por eso la etapa dura días, no minutos.

| Resultado | Qué pasa |
|---|---|
| ✅ **Avance** | Suma al protocolo. Una cura de rango Médico pide unos 5 avances; la Regeneración, decenas |
| 🔎 **Descubrimiento** | Revela una propiedad oculta de un ingrediente. Queda en tu herbario para siempre |
| ❌ **Fallo** | Se pierden los ingredientes de ese ensayo, pero **fallar enseña**: cada fallo descarta una hipótesis o da +15 % al siguiente intento, como la protección contra la mala racha de [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §5.3 |
| ⚠️ **Accidente** (raro, solo si arriesgas) | Algo leve para el médico: Toxicidad, una quemadura de ácido de grado 1 o un contagio menor si trabajaba sin máscara. **Nunca** una herida grave |
| 🧑‍⚕️ **Ensayo con voluntario** | El último paso de una cura: probarla en un paciente que acepta y cobra (pago en custodia). Puede dejar un efecto secundario de horas; **nunca** una secuela |

### 2.6 Protocolo: el tratamiento queda escrito

Con los avances completos nace un **protocolo** con nombre: "*Protocolo de Mara contra la Fiebre del Pantano*". La Gaceta anuncia el primero de cada mal en el servidor.

| Qué se puede hacer con él | Cómo |
|---|---|
| **Usarlo** | El autor trata con él a sus pacientes |
| **Enseñarlo** | A sus aprendices, como cualquier maestro jugador (ver [Profesiones](../07-economia/profesiones.md) §11) |
| **Copiarlo y venderlo** | Copias con usos limitados (Inscripción), como las copias de planos (ver [Fabricación](../07-economia/fabricacion.md) §5). Quien la compra necesita el mismo rango y los mismos ingredientes |
| **Patentarlo** | Con las reglas de [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §8: se registra en la Academia y, durante **12 semanas** (más una renovación de 6), los médicos que lo usan pagan al autor una **regalía** en porcentaje por cada tratamiento. Después **vence** y pasa a la Biblioteca pública (ver [Balance](../03-personaje/balance.md) §5, "patentes que vencen") |
| **Guardarlo en secreto** | Nadie más lo recibe, pero otro médico puede redescubrirlo con su propio expediente, y entonces lo usa sin pagar |
| **Donarlo a la ciudad** | Pasa a la Biblioteca pública y suma Saber a la rama ⚕️ Medicina del árbol de la ciudad (§5.3). El autor gana reputación de Academia y su nombre queda en la biblioteca |

Cuando un protocolo es público, el **sanatorio** también lo usa, a su precio alto de siempre. Así el sanatorio sigue siendo el techo de precios de los médicos jugadores (ver [Curación](curacion-y-tratamientos.md) §5).

### 2.7 Aplicación: qué se puede hacer al final

| Tipo | Qué hace | Quién lo da |
|---|---|---|
| **Tratamiento mejorado** | Frena la gravedad o acelera la inmunidad más que el remedio básico | Médico |
| **Cura completa** | Gana la carrera de una vez o elimina un mal crónico | Médico |
| **Vacuna** | Inmunidad preventiva durante una temporada | Cirujano con Epidemiología |
| **Profilaxis** | Máscaras médicas, pastillas y remedios preventivos que se venden en el mercado | Médico, con alquimistas y sastres |
| **Cirugía nueva** | Una operación nueva en el minijuego de cirugía (ver [Curación](curacion-y-tratamientos.md) §4) | Cirujano |
| **Prótesis mejor** | Implantes que compensan más | Cirujano e ingeniero |
| **Regeneración** | Reponer lo perdido (§4) | Pocos médicos del servidor |

## 3. El árbol de investigación médica

```
                           🌟 REGENERACIÓN
                                  ▲
   ┌──────────┬──────────┬────────┴───┬──────────┬──────────┐
 Fiebres y  Venenos y  Heridas y     Mente     Plagas de  Prótesis
 contagios  toxinas    cirugía                 animales y
                                               cultivos
```

Cada rama tiene **4 nodos**. Cada nodo pide un nivel de Medicina, a veces una especialización, y expedientes con estrellas. Los rangos son los de [Curación](curacion-y-tratamientos.md) §0: **Enfermero** (1-30), **Médico** (31-70) y **Cirujano** (71-100); las especializaciones, las de [Profesiones](../07-economia/profesiones.md) §2.3, más **Veterinaria**, que figura como rama de Medicina en [Profundidad de un oficio](../07-economia/profundidad-de-un-oficio.md) §3. Un nodo es un **proyecto**: pasa por las siete etapas, con las cifras de su rango. Los **saberes combinados** de [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §3 ayudan: Farmacología a Venenos y toxinas, Ortopedia a Prótesis, Anatomía comparada a los casos de monstruos.

Los nodos I piden Medicina 21, el rango desde el que se puede investigar (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §5). Antes de eso, un enfermero ya junta casos y estrellas de expediente.

**Tiempos orientativos por nodo** (un médico solo): I, 3 a 5 días · II, 2 a 3 semanas · III, 1 a 2 meses · IV, 2 a 3 meses.

### 3.1 Fiebres y contagios (Epidemiología)

| Nodo | Requisito | Desbloquea |
|---|---|---|
| I · Registro de síntomas | Medicina 21 | Diagnóstico por síntomas más preciso; expedientes de Gripe de Escarcha y Disentería con la mitad de casos |
| II · Febrífugos | Medicina 40 · Fiebre del Pantano ★★★ | Cura completa de la Fiebre del Pantano crónica (con Flor de Ciénaga Tardía); caldos febrífugos con los cocineros |
| III · Cuarentena y profilaxis | Medicina 60 · Epidemiología · 2 expedientes ★★★★ | Máscaras médicas mejores, pastillas preventivas; una cuarentena declarada baja el doble el contagio |
| IV · Vacunas mayores | Medicina 80 · Epidemiología · 3 expedientes ★★★★★ | Vacunas de una temporada para las enfermedades investigadas; ver venir un brote en la Gaceta antes de que se propague |

### 3.2 Venenos y toxinas (Farmacia)

| Nodo | Requisito | Desbloquea |
|---|---|---|
| I · Antídotos comunes | Medicina 21 | Reconocer la familia de un veneno; antídotos más baratos |
| II · Antitoxinas específicas | Medicina 40 · Farmacia | Tétanos de Óxido sin espasmos crónicos; veneno del Escorpión de Vidrio; quelante del Mal de Escoria |
| III · Desintoxicación profunda | Medicina 65 · Farmacia | Baja la Toxicidad y la dependencia de una vez (ver [Condiciones](condiciones.md)) |
| IV · Anestesia profunda y triaca | Medicina 85 · Farmacia | La **anestesia profunda** que pide la cirugía mayor (con raíz de mandrágora), y una triaca que cura cualquier veneno ya investigado |

### 3.3 Heridas y cirugía (Cirugía)

| Nodo | Requisito | Desbloquea |
|---|---|---|
| I · Suturas finas | Medicina 21 | Menos infección después de suturar; cicatrices más pequeñas |
| II · Injertos de piel | Medicina 50 · Quemadura ★★★ | Injerto para quemaduras de grado 3 y la cicatriz extensa de la Podredumbre Gris (con miel negra o escama de salamandra) |
| III · Cirugía de secuelas | Medicina 75 · Cirugía · Fractura y Nervio dañado ★★★★ | Cura del todo los males crónicos de hueso y nervio (*Rodilla mala*, temblor que vuelve). **Compensa** una rodilla destrozada o un nervio cortado como un equipo Excelente (queda el 45 %, ver [Secuelas](secuelas-y-muerte.md) §2.4), sin pasar nunca el piso del 25 %. Repararlos del todo es cosa de la Regeneración |
| IV · Cirugía mayor | Medicina 90 · Cirugía | Operaciones de varias sesiones con **hasta 2 médicos asistentes**, cada uno a cargo de una barra. La pide la Regeneración |

### 3.4 Mente (sin especialización; Farmacia ayuda)

| Nodo | Requisito | Desbloquea |
|---|---|---|
| I · Calmantes | Medicina 21 | Remedios que bajan un poco el estrés y dan sueño reparador |
| II · Tratar aflicciones | Medicina 45 | Acortan las aflicciones (ver [Mente](mente.md)); trabajan junto al bardo y la taberna |
| III · Terapia de fobias | Medicina 65 · 3 fobias ★★★ | Quitar una fobia o una manía con un tratamiento de varias sesiones (ver [Rasgos adquiridos](rasgos-adquiridos.md)), con Polen de Flor de Difuntos |
| IV · Elixir de lucidez | Medicina 80 · Farmacia | Más cordura en el Abismo y en las Pesadillas (con Hongo del Eclipse). **La Corrupción no se cura con medicina:** es una elección, y la limpia el templo |

### 3.5 Plagas de animales y cultivos (Epidemiología o Veterinaria)

| Nodo | Requisito | Desbloquea |
|---|---|---|
| I · Veterinaria básica | Medicina 21 | Cojera, parásitos y heridas de montura (ver [Animales y cultivos](animales-y-cultivos.md)) |
| II · Fiebre del establo | Medicina 40 | Remedio y cuarentena de establo; vacuna para el ganado |
| III · Sanidad del campo | Medicina 60 · trabajo junto a un agricultor y un alquimista | Tratamientos contra el tizón y la langosta; semillas resistentes junto con la hibridación |
| IV · Brotes en la fauna | Medicina 80 · Epidemiología | Cebos medicados que frenan un brote en una especie de monstruo antes de que se vuelva epidemia (ver [Bestiario](../06-contenido/bestiario.md) §10.7) |

### 3.6 Prótesis (Cirugía, con Ingeniería)

| Nodo | Requisito | Desbloquea |
|---|---|---|
| I · Muletas y férulas | Medicina 21 | La muleta baja la penalización de una pierna perdida; férulas mejores |
| II · Implante simple | Medicina 50 | Implantar prótesis simples con el minijuego (ver [Secuelas y muerte](secuelas-y-muerte.md) §2) |
| III · Prótesis articulada | Medicina 75 · Cirugía | Menos tiempo de adaptación; prótesis de obra maestra con mejor implante |
| IV · Prótesis con nervio | Medicina 90 · Cirugía · Nervio dañado ★★★★★ | La mejor prótesis posible, que se mueve con los nervios: compensa casi todo, **nunca del todo** (D-51) |

## 4. Regeneración: la cima del árbol

### 4.1 Qué repone y qué no

| Repone | No repone |
|---|---|
| Dedos, orejas y piel perdidos | La **Corrupción**: es una elección (ver [Mente](mente.md)) |
| Manos, pies y ojos | Las **cicatrices-trofeo**: se quedan si el jugador quiere |
| Brazos y piernas | La muerte del **Juramento de Hierro**: caer es caer |
| Un **nervio cortado** o una **rodilla destrozada**, del todo | Nada en el momento: siempre hay cirugía, internación y rehabilitación |
| Un órgano dañado (*Pulmón dañado*, *Hígado castigado*), la *Sordera parcial* y la *Piel marcada* | Los males **crónicos**: esos ya se curan con un tratamiento largo (nodos III, ver [Secuelas](secuelas-y-muerte.md) §3) |

### 4.2 Qué pide investigarla

Cuatro nodos, uno sobre otro. El primero pide **todo esto**:
- **Medicina muy alta:** Gran Maestro de Medicina (96-100). Quien no es de Cirugía puede hacer R1 y R2 junto a un Maestro de Cirugía (81 o más); R3 y R4 piden la rama Cirugía en 100 y después su Maestría.
- **Nodos IV** de Heridas y cirugía y de Venenos y toxinas (anestesia profunda), y al menos el nodo III de otras dos ramas.
- **Expedientes ★★★★★** de Gangrena, Congelación, Fractura y Nervio dañado, y de al menos tres enfermedades más. Además, el expediente de **tejido que se regenera**, que solo se llena observando a trols, licántropos y limos (§2.1).
- **Ingredientes de varias zonas y estaciones** (§2.4): glándula de licántropo (luna llena), corazón de micelio (cueva), lágrima helada (ventisca), cristal de resonancia profunda (Abismo, 1 por día), agua de fondo (verano), raíz de mandrágora (primavera) y miel negra (otoño). Las cuatro estaciones: como mínimo un año entero del mundo (4 semanas reales), y en la práctica más.
- **Una instalación:** el **Quirófano mayor** del Sanatorio del Castillo, o una **Enfermería mayor** de gremio u orden. Es una obra que dirige un Maestro de obras (ver [Sistema de construcción](../09-construccion/sistema-de-construccion.md)), con mesa de cirugía de obra maestra (Herrería), cámara fría (Ingeniería y lágrimas heladas), luces de cristal (Joyería) y lienzos limpios (Sastrería).

| Nodo | Requisito extra | Desbloquea | Tiempo (orden de médicos) |
|---|---|---|---|
| R1 · Tejido vivo | Lo de arriba | Entender cómo vuelve a crecer un tejido; la cámara fría | 4 a 6 semanas |
| R2 · Regeneración menor | R1 · ensayos en monturas | Dedos, orejas, piel | 4 a 6 semanas |
| R3 · Regeneración mayor | R2 · Medicina 100 y la rama Cirugía en 100 | Manos, pies, ojos; nervios y huesos de una zona | 6 a 8 semanas |
| R4 · Regeneración completa | R3 · **Maestría M10 en Cirugía** (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §2.2) | Brazos, piernas, órganos dañados | 8 a 10 semanas |

**Total:** de **5 a 7 meses** para la primera orden de médicos del servidor que lo intente, y más para un médico solo. Esto se suma a los meses de llegar a Gran Maestro (alrededor de un año, ver [Profesiones](../07-economia/profesiones.md) §4). La M10 lleva unos 2 meses más, que corren a la par de R1 a R3.

### 4.3 Primero un dedo, después una pierna

Los ensayos van de menor a mayor, y cada paso es un protocolo:
1. **Monturas:** reponer la pata de una montura herida (con su dueño de acuerdo y veterinaria).
2. **Voluntarios con dedos perdidos** por congelación: pagados, con consentimiento.
3. **Manos y ojos.**
4. **Brazos y piernas.**

### 4.4 La cirugía mayor

Usa el minijuego de cirugía (ver [Curación](curacion-y-tratamientos.md) §4) con una barra más, **Vitalidad del tejido**, que baja cada ronda; la cámara fría la frena. Tiene tres partes:

| Parte | Cómo es | Quién |
|---|---|---|
| **1. Preparación** | Una sesión de unas 10 rondas: anestesia profunda, limpiar, abrir | El cirujano y un asistente de Farmacia (lleva el Dolor y la Estabilidad) |
| **2. Siembra** | Una sesión de 12 a 15 rondas con tres acciones nuevas: **Implantar el andamio** (corazón de micelio), **Infundir** (glándula de licántropo) y **Alinear** (cristal de resonancia). Ocupan el lugar de Incisión, Extraer e Implantar durante esa sesión: la pantalla no crece | El cirujano y dos asistentes; cada uno ve sus botones en el mismo mensaje vivo |
| **3. Crecimiento** | El paciente queda internado de 7 a 14 días reales. Un enfermero hace una cura diaria (un toque). Saltarse una cura lo alarga, no lo arruina | Enfermero de la orden |

Después viene la **rehabilitación**: el miembro nuevo empieza débil, con la mitad de la penalización de no tenerlo, y la pierde en 2 a 4 semanas de uso, como la aclimatación.

**Si sale mal:** el paciente queda como estaba, nunca peor, y se pierden los materiales de la sesión fallida.

### 4.5 Cuánto cuesta y quién la da

**Materiales de una pierna** (orientativo): 1 glándula de licántropo, 2 corazones de micelio, 3 lágrimas heladas, 1 cristal de resonancia profunda, 4 aguas de fondo, 2 raíces de mandrágora, 1 miel negra, vendas de seda (Sastrería) e hilo de tendón (Desuello). Más los honorarios del cirujano y sus asistentes, la internación y el desgaste del instrumental.

- **No es barata:** cada pieza es rara, de temporada o de un yacimiento con cuota. El precio lo pone el mercado.
- **Es un servicio de pocos:** al principio, ninguno; después, unos pocos Gran Maestros por servidor.
- **Topes:** cada Gran Maestro hace como máximo **una regeneración mayor o completa por semana**, y cada personaje recibe como máximo **una por temporada**.
- **El sanatorio PNJ no la ofrece.** Solo alquila el Quirófano mayor. Es un servicio de jugadores.

### 4.6 Cómo encaja con D-51

D-51 dice que las secuelas **perduran o son definitivas**, que se compensan en parte y nunca del todo. D-53 dice que se pueden **reponer** con medicina avanzada. Las dos se cumplen así:
- **En el juego normal, la secuela es definitiva.** Ninguna poción, hechizo, PNJ, oro ni Gemas la quita. Lo que tiene el jugador a mano (prótesis, muletas, adaptación, cirugía de secuelas) compensa en parte, nunca del todo.
- **La Regeneración no es un remedio: es la obra máxima de la medicina del servidor.** Solo existe cuando alguien la investigó durante meses, un Gran Maestro acepta el caso, se juntaron ingredientes de las cuatro estaciones, existe la instalación y la cirugía sale bien. Durante buena parte del primer año, seguramente nadie podrá hacerla: las secuelas serán definitivas de hecho.
- **No borra la historia.** Las semanas con la secuela, el oro y los materiales ya se pagaron. El perfil guarda la cicatriz y suma una **marca de regeneración** ("*pierna regenerada por Mara de Ribera, Lejanía 4*").
- **No vuelve barato el descuido.** La cadena de descuidos que lleva a perder un miembro sigue costando caro. Reponerlo es un proyecto, casi una misión propia.

## 5. Investigar solo o en conjunto

### 5.1 Un médico solo

Avanza despacio: su tope semanal de casos, su mesa, sus propios ingredientes. Llega a los nodos IV con paciencia. La Regeneración, en la práctica, no la hace solo: la cirugía mayor pide asistentes.

### 5.2 Una orden de médicos

Una **orden de médicos** es un gremio, o un grupo dentro de un gremio, que se registra como tal en la Academia del Castillo. Es la institución de Medicina que nombra [Profundidad de un oficio](../07-economia/profundidad-de-un-oficio.md) §3 (Orden de Médicos). Comparte:
- un **expediente común**: los casos de cada miembro suman al mismo expediente;
- las mesas, la biblioteca (la biblioteca de gremio ya acelera la investigación, ver [Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md)) y el almacén de ingredientes;
- los nodos, que corren como **proyecto de grupo** de 2 a 5 investigadores que suman sus PI (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §5.2);
- los protocolos, que puede usar cada miembro con el rango que piden.

**Rendimiento decreciente:** cada miembro que aporta en la semana suma +20 % de velocidad, con un tope de +100 %. Una orden de 50 no va diez veces más rápido que una de 5. Y **nada acelera la estación del año**: si falta la flor de otoño, se espera al otoño.

### 5.3 La ciudad

La **Academia** del Castillo guarda el conocimiento de la ciudad: el **árbol de conocimiento de la ciudad**, con su rama ⚕️ Medicina (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §6). Un protocolo donado:
- pasa a la Biblioteca pública: los médicos con el rango que pide lo usan gratis, y el sanatorio también;
- suma Saber a la rama ⚕️ Medicina de la ciudad, que abre servicios para todos: Antisépticos, Vacunación pública, Cuarentena ordenada y, en la cumbre, **Rehabilitación** (que también acortaría la rehabilitación después de una Regeneración, §4.4) o **Escuela de epidemiólogos**;
- el **Catedrático de Medicina** de la Academia (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §7.2) propone qué males investiga la ciudad primero, y los residentes votan.

Los médicos que no son de la ciudad aprovechan sus servicios pagando la tasa, como cualquier visitante.

### 5.4 En una epidemia, la investigación es de todos

Durante una epidemia de servidor (ver [Enfermedades](enfermedades.md) §4 y [Eventos](../06-contenido/eventos.md)), la cura sigue las mismas siete etapas, pero **en una sola barra para todo el servidor**, como en Plague Inc.:
1. **Observación:** cada caso, cada muestra de bilis de plaga y cada paciente que se deja estudiar suma al **expediente común del servidor**. La Gaceta publica el porcentaje.
2. **Hipótesis votada:** los tres médicos que más aportaron proponen una; los demás médicos votan.
3. **Ingredientes:** la hipótesis pide uno de yacimiento (por ejemplo, Sal de Estrellas), de la estación en curso o de la propia epidemia (bilis de plaga), **nunca uno fuera de estación**: la epidemia no espera un mes. Todo el servidor sale a buscarlo.
4. **Experimentos:** cualquier médico con rango ensaya, y cada avance suma a la barra común.
5. **Protocolo público:** las curas de una epidemia **no se patentan** (ver [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §8.2). Pasan a todos los médicos y al sanatorio a la vez.
6. **Aplicación:** se fabrica en cadena (ver [Investigaciones](../06-contenido/investigaciones.md) §2.1) y llega la vacuna. Los que más aportaron ganan el título.

## 6. Ritmo: cuánto lleva y por qué no se salta

| Qué | Tiempo real orientativo | Qué lo limita |
|---|---|---|
| Expediente ★★★ de una enfermedad común | 1 a 2 semanas | Tope semanal de casos; casos variados |
| Expediente ★★★★★ | 1 a 2 meses | Casos raros y un protocolo propio |
| Esperar un ingrediente de temporada | 0 a 3 semanas | La estación vuelve cada 4 semanas reales |
| Experimentos de una cura de rango Médico | 3 a 10 días | 3 experimentos por día |
| Nodo I · II · III · IV | 3-5 días · 2-3 semanas · 1-2 meses · 2-3 meses | Todo lo anterior, sumado |
| Regeneración, la primera del servidor | 5 a 7 meses de investigación, después de llegar a Gran Maestro | Cuatro nodos, cuatro estaciones, un yacimiento con cuota, la instalación |
| Cada regeneración después de eso | 4 a 7 semanas | Juntar materiales, cirugía, internación y rehabilitación |

**Por qué no se puede saltar:**
- **D-43:** nada de esto se vende. Ni Gemas ni aceleradores tocan los expedientes, los experimentos ni las estaciones.
- **Relojes del mundo:** la estación del año, la luna y el clima no se adelantan.
- **Topes semanales y diarios:** el tiempo infinito no compra ventaja infinita.
- **Lo que se lee no reemplaza lo que se ve:** un expediente copiado llega a ★★.
- **Por qué conviene:** pediste que no fuera de la noche a la mañana. Un médico que repone piernas tiene que haber pasado meses estudiando, y eso vale oro y prestigio de verdad.

## 7. Cómo se ve

**La capa simple (`/investigar`):**

```
🔬 Tus investigaciones
Fiebre del Pantano ★★★  ▓▓▓▓▓▓░░ protocolo 3/5
Gangrena           ★★   ▓▓▓░░░░░ casos 18/35
Orden de San Bram · Vacuna de Gripe ▓▓▓▓▓▓▓░ 71 %
Casos esta semana: 22/40

[📂 Expedientes] [🧪 Mesa] [🌳 Árbol]
```

**El expediente:**

```
📂 Expediente — Fiebre del Pantano
★★★☆☆ Comprendida · 46/70 casos para ★★★★
✅ Síntomas: fiebre en brotes, Aguante bajo
✅ Causa: picadura del Mosquito de Ciénaga
✅ Avanza: incubación 6 h · vuelve cada semana
✅ La empeora: lluvia, verano, miasma
🔒 La alivia (★★★★)  🔒 Punto débil (★★★★★)
💡 Hipótesis: febrífugo frío y amargo
🌿 Falta: Flor de Ciénaga Tardía (otoño, noche)
📅 El otoño empieza en 2 días

[🔬 Estudiar caso] [🧪 Experimentar] [📜 Copiar]
```

**Un experimento (modo manual):**

```
🧪 Mesa · Enfermería del gremio Arena Roja
Fiebre del Pantano · febrífugo · protocolo 3/5
Avance  ▓▓▓▓▓▓░░░░ 60 %
Riesgo  ▓▓░░░░░░░░ bajo
Muestra ●●○
Paso 3: la mezcla se enturbia ⚠️

[🔥 Calentar]     [❄️ Enfriar]
[🌿 Añadir flor]  [👁 Observar]
[📝 Anotar]       [⛔ Parar]
```

Al terminar: `✅ Avance: protocolo 4/5. Descubriste: la Flor de Ciénaga es Fría.`

## 8. A quién le da trabajo

| Quién | Qué hace aquí |
|---|---|
| **Médicos** (enfermero, médico, cirujano) | Investigan, firman protocolos, cobran regalías de patentes, curas, vacunas y regeneraciones |
| **Pacientes** | Cobran por ser casos de estudio y voluntarios de ensayos. Quien tiene una secuela es buscado por las órdenes |
| **Herboristas** | Flores, musgos y raíces de temporada y de noche |
| **Cazadores** (Desuello, Orden de Cazadores) | Glándulas, lágrimas heladas, muestras de monstruos enfermos, bilis de plaga |
| **Exploradores y cartógrafos** | Encuentran floraciones, oasis y yacimientos; venden mapas y calendarios |
| **Mineros** | Cristal de resonancia profunda, Sal de Estrellas |
| **Alquimistas** | Bases, destilados y la fabricación en serie de cada cura |
| **Joyeros** | Frascos de muestra, viales y frascos de vidrio de duna que conservan; luces de cristal |
| **Herreros** | Instrumental fino y mesas de cirugía de obra maestra |
| **Ingenieros** | Cámara fría; prótesis con nervio |
| **Sastres** | Vendas de seda, lienzos limpios, máscaras médicas |
| **Agricultores y ganaderos** | Cultivan corazón de micelio y hierbas medicinales; monturas para los primeros ensayos |
| **Constructores** | Mesas de investigación, enfermerías mayores, el Quirófano mayor |
| **Escribas** (Inscripción) | Copias de expedientes y protocolos |
| **Comerciantes y transportistas** | Llevan lo que caduca antes de que se eche a perder |
| **Eruditos** | Calendarios de lunas llenas y eclipses |

**Su fila en la [Red de sistemas](../00-vision/red-de-sistemas.md):**

| Sistema | Consume | Produce | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|---|
| **Investigación médica** | Casos (pacientes, animales, muestras), ingredientes de lugar y estación, instrumental, frascos, mesas, enfermerías, tiempo real | Protocolos (curas, vacunas, cirugías, prótesis, Regeneración), expedientes y copias vendibles, regalías, demanda de materiales de temporada, títulos | Hierbas, glándulas, cristales, sal, agua, muestras | Frascos, instrumental, cámara fría, vendas, remedios en serie, enfermerías | Rango y especialización de Medicina, nodos del árbol, estrellas de los expedientes |

## 9. Límites para que no frustre

1. **Nadie espera a la ciencia para lo básico.** Todo mal del catálogo tiene su tratamiento básico desde el primer día.
2. **Nadie queda fuera.** Los protocolos públicos llegan al sanatorio.
3. **Fallar enseña.** Cada fallo descarta algo o suma al siguiente intento.
4. **Sin accidentes graves.** Lo peor que le pasa a un médico es leve; a un voluntario, un efecto de horas.
5. **Siempre con permiso.** Ningún jugador es caso de estudio ni voluntario sin aceptar y cobrar.
6. **Fuera de línea cuenta.** Los estudios largos y la internación avanzan sin conectarse.
7. **Todo cabe en una pantalla.** `/investigar` resume; el expediente y la mesa se piden.

## 10. Orden de construcción sugerido

Junto con el orden de [Salud](README.md):
1. **v2** (Medicina como oficio): expedientes con estrellas y casos de pacientes.
2. **v3** (enfermedades): hipótesis, mesa en modo rápido, protocolos y nodos I y II.
3. **v4:** ingredientes de lugar y estación, modo manual, patentes, órdenes de médicos.
4. **v5** (secuelas): nodos III y IV, cirugía mayor y Regeneración; investigación comunitaria en epidemias.

## 11. Ediciones pendientes en otros documentos

No se hicieron: otros procesos están editando esos documentos.

- [x] **[Secuelas y muerte](secuelas-y-muerte.md)** §2.1, §2.7, §2.8, §3 y §5.4: la Regeneración médica, la secuela definitiva en el juego normal y los nodos III (hecho).
- [ ] **[Secuelas y muerte](secuelas-y-muerte.md)** §2.4: sumar a la tabla la fila "Cirugía de secuelas (nodo III de Heridas y cirugía): rodilla destrozada y nervio cortado, 45 %", junto a la de la prótesis con nervio.
- [ ] **[Curación](curacion-y-tratamientos.md)**: §0, agregar qué investiga cada rango (nodos I a IV); §3, la fila Vacuna enlaza aquí; §5, sumar la mesa de investigación, la enfermería mayor y el Quirófano mayor; §7, "Miembro perdido" ya dice que se compensa y que reponerlo es la Regeneración médica (hecho); §8, los ingredientes de temporada enlazan a §2.4; §9, sumar la carrera de investigador.
- [ ] **[Enfermedades](enfermedades.md)**: §1, decir que las curas completas salen de un protocolo; §3, nota de que cada enfermedad tiene expediente; §4 (Respuesta), enlazar a §5.4 (la cura comunitaria por etapas, sin patente).
- [ ] **[README de Salud](README.md)**: la fila en la tabla de documentos ya está (hecho). Falta: en "Las siete capas", Secuelas se cura con "Prótesis, adaptación y, en la cima de la medicina, Regeneración"; sumar esta línea al orden de construcción (§10) y a "A quién le da trabajo" (pacientes de estudio, exploradores, eruditos).
- [ ] **[Investigación y maestría](../07-economia/investigacion-y-maestria.md)**: §5.2, enlazar aquí desde la fila "Remedio" y aclarar que un proyecto médico pide antes expediente ★★★, hipótesis e ingredientes; §4, decir que los puntos de caso del expediente son un contador aparte de los PI ⚕️; §6.2, en la cumbre Rehabilitación, sumar la rehabilitación después de una Regeneración; §7.1, el Anfiteatro anatómico tiene mesa de investigación médica.
- [ ] **[Profesiones](../07-economia/profesiones.md)**: §2.3, en Medicina sumar "protocolos e investigación médica" y sumar **Veterinaria** a sus especializaciones, como ya dicen [Profundidad de un oficio](../07-economia/profundidad-de-un-oficio.md) §3 y [Animales y cultivos](animales-y-cultivos.md); §5, los expedientes son el conocimiento de Medicina; §9, rol de investigador médico; §10, fila "Reponer una pierna"; §12, regalías de patentes y pago a pacientes de estudio.
- [ ] **[Decisiones](../00-vision/decisiones.md)** D-53: enlazar este documento y [Investigación y maestría](../07-economia/investigacion-y-maestria.md), que ya existe, en lugar de "Investigación y maestría (en redacción)".
- [ ] **[Creación de personaje](../03-personaje/creacion-de-personaje.md)**, tabla de razas (fila Trol) y "Por qué conviene": el Trol recupera "*incluso un miembro perdido, muy despacio (semanas)*" y "*lo recupera en semanas*", lo que choca con D-51. Dejarlo como ya propone [Secuelas](secuelas-y-muerte.md) §2.7: regenera dedos, orejas y dientes, hace la rehabilitación y la adaptación en la mitad del tiempo y es el mejor caso de estudio, pero un brazo, una pierna o un ojo le piden la Regeneración médica.
- [ ] **[Profundidad de un oficio](../07-economia/profundidad-de-un-oficio.md)** §3, fila Medicina: en "Conocimiento del material", sumar "expedientes"; la Orden de Médicos enlaza a §5.2 de este documento.
- [ ] **[Investigación y maestría](../07-economia/investigacion-y-maestria.md)** §11: la pantalla `/investigar` muestra también las líneas de los expedientes (§7 de este documento), para que haya una sola pantalla.
- [ ] **[Decisiones](../00-vision/decisiones.md)** D-54: cuando exista el documento de la escalera de conocimiento, que cite esta escalera como su modelo médico.
- [ ] **[Investigaciones](../06-contenido/investigaciones.md)** §2.1: sumar la fila "Investigación médica" y enlazar aquí desde "Investigación de la cura".
- [ ] **[Red de sistemas](../00-vision/red-de-sistemas.md)** §3: sumar la fila de §8.
- [ ] **[Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md)**: enlazar las **patentes** de [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §8, que usan su tasa autodeclarada en la renovación.
- [ ] **[Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)** §4: en cada estación, nombrar 2 o 3 ingredientes médicos que solo salen entonces.
- [ ] **[Geografía y recursos](../02-mundo/geografia-y-recursos.md)** §2-3: sumar el Cristal de Resonancia Profunda (Abismo) y el Oasis Hondo como yacimientos únicos; ubicar la Sal de Estrellas.
- [ ] **[Bestiario](../06-contenido/bestiario.md)**: Licántropo Salvaje deja glándula; Micelio Andante, corazón de micelio para la Regeneración; Novia de Escarcha, lágrimas heladas para la cámara fría.
- [ ] **[Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md)** y **[Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md)**: Quirófano mayor (mejora del Sanatorio), mesa de investigación en la Academia, Enfermería mayor y Orden de médicos.
- [ ] **[Monetización](../07-economia/monetizacion.md)** §3: sumar que los aceleradores no tocan expedientes, PI, proyectos ni investigación médica (ya lo dice [Investigación y maestría](../07-economia/investigacion-y-maestria.md) §2.2).
- [ ] **[Glosario](../00-vision/glosario.md)**: expediente, puntos de caso, protocolo, mesa de investigación, orden de médicos, Enfermería mayor, Quirófano mayor, Regeneración y marca de regeneración.
- [ ] **[Preguntas abiertas](../00-vision/preguntas-abiertas.md)**: sumar las preguntas de abajo, con el siguiente número P-xx libre (hoy el más alto es P-70).

**Preguntas para el dueño:**
1. ¿Una regeneración por personaje y por temporada es buen tope, o debería ser una sola vez por miembro?
2. ¿El Trol conserva su regeneración natural de miembros completos, o la limitamos como propone esta lista?
3. ¿El expediente lleva su propio contador de casos, como propone este documento, o se simplifica y todo se paga solo con PI ⚕️?
