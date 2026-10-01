# Investigaciones

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Misiones](misiones-y-exploracion.md), [Mundo](../02-mundo/README.md) · **Alimenta a:** [Enfermedades](../05-salud/enfermedades.md) (curas), [Fabricación](../07-economia/fabricacion.md) (recetas y planos), [Jefes](jefes.md) (jefes ocultos), [PvP](pvp.md) (karma) · **Estado:** propuesta

"Investigar" significa aquí dos cosas, y las dos entran:
- **Investigación detectivesca:** resolver casos con pistas, interrogatorios y deducción.
- **Investigación de conocimiento:** estudiar para descubrir algo nuevo (una cura, una receta, un secreto del lore, la debilidad de un jefe).

**De dónde sale.**
- *Sherlock Holmes: Consulting Detective* (juego de mesa) y *Return of the Obra Dinn*: resolver un caso cruzando pistas y responder quién, cómo y por qué.
- *Disco Elysium*: interrogatorios con opciones de diálogo, y un "gabinete de ideas" que se investiga con el tiempo.
- *L.A. Noire*: interrogar y detectar mentiras.
- *The Witcher 3*: investigar antes del contrato de monstruo, con los sentidos de brujo, para saber qué es y cómo matarlo.
- *Pathologic 2*: investigar el origen de la plaga.
- *Fallen London*: historias de texto con cualidades que se acumulan.
- *Arqueología* de WoW: excavar y completar piezas para desbloquear historias.
- *EVE Online*: investigación de planos que lleva días.
- *Destiny* y *Elden Ring*: secretos que la comunidad resuelve junta.

**Por qué conviene.** Es contenido **de cabeza**, no de reflejos ni de equipo, y encaja perfecto en texto. Además, da un camino completo a quien le gusta leer, deducir y descubrir.

---

## 1. Casos: el formato detectivesco

### 1.1 Cómo funciona un caso

1. **El encargo.** Un PNJ (o el tablón) plantea un caso: "*Alguien envenenó el pozo de Ribera Seca*".
2. **La escena.** Recorres lugares (nodos) y encuentras **pistas**, que van a tu **Tablero de corcho**.
3. **Los testigos.** Interrogas a PNJ con opciones de diálogo. Algunos mienten; cruzar su testimonio con las pistas revela la mentira ("*dijo que estaba en el molino, pero la harina de su bota es de la panadería*").
4. **La deducción.** Cuando crees saberlo, respondes tres preguntas: **quién**, **cómo** y **por qué** (como en *Obra Dinn*), eligiendo entre opciones que ya descubriste.
5. **El veredicto.**
   - Acertar las tres da la recompensa completa.
   - Acertar parte da una recompensa parcial.
   - Acusar a un inocente tiene consecuencias en la historia de la región: el culpable escapa, o el pueblo desconfía de ti.

### 1.2 El Tablero de corcho

```
🧷 Tablero — El pozo envenenado (Ribera Seca, Lejanía 4)
Pistas (5/8):
 • Frasco roto con olor a almendra amarga (junto al pozo)
 • Huellas de bota pequeña en el barro
 • El molinero dice que estuvo en el molino toda la noche
 • Harina de centeno en la bota del molinero ⚠️ contradice su testimonio
 • La herborista vendió "raíz de almendra" hace dos días

[🔍 Seguir investigando]  [🗣 Interrogar]
[⚖️ Acusar]               [📜 Notas]
```

### 1.3 Formatos de caso

| Formato | Duración | Qué es |
|---|---|---|
| **Caso rápido** | 5-10 minutos | Del tablón diario, con 3 o 4 pistas |
| **Caso de la región** | Una sesión | Parte de la campaña de la región; su final cambia el asentamiento |
| **Caso semanal del servidor** | Una semana | El mismo caso para todos; quien lo resuelve primero sale en la Gaceta, y las pistas se pueden intercambiar o vender |
| **Caso de gremio** | Varios días | Las pistas están repartidas: cada miembro ve solo algunas y tienen que juntarlas en el chat del gremio |
| **Caso de jugadores** | Varía | Crímenes reales entre jugadores (quién mató a un verde en zona roja, quién robó una trampa): el sistema de karma deja rastros que un investigador puede seguir para cobrar una recompensa (ver [PvP](pvp.md)) |
| **Caso de brujo** | Antes de una cacería | Investigar los ataques en un pueblo para saber qué monstruo es y su debilidad; si aciertas, empiezas la cacería con ventaja (ver [Cacerías](cacerias.md)) |
| **Asesinato en la taberna** | Evento | Un PNJ "muere" en la taberna y los presentes investigan juntos; mezcla con La Máscara (ver [Minijuegos](../08-social/minijuegos-y-formatos-telegram.md)) |

### 1.4 Rangos de investigador

Reputación con la **Guardia de la Región** o con una **Agencia de Investigadores**: Curioso, Sabueso, Inspector, Detective, Maestro Detective. Los rangos altos abren casos más complejos, pistas ocultas y el título.

## 2. Investigación de conocimiento

### 2.1 Formatos

| Formato | Qué se investiga | Cómo | Qué da |
|---|---|---|---|
| **Investigación de la cura** | Una enfermedad nueva durante una epidemia | Médicos y alquimistas estudian muestras de pacientes (jugadores enfermos), prueban combinaciones y comparten avances; la cura se descubre entre todos (ver [Enfermedades](../05-salud/enfermedades.md)) | La receta de la cura, título para quien más aportó |
| **Investigación de recetas** | Combinaciones nuevas de alquimia y cocina | Descubrimiento por experimentación (ver [Fabricación](../07-economia/fabricacion.md)) | Recetas con tu nombre como descubridor |
| **Investigación de planos** | Mejorar un plano | Días de estudio en una estación (estilo EVE) | Planos más eficientes y copias vendibles |
| **Arqueología** | Ruinas del mundo viejo | Excavar, catalogar fragmentos, completar piezas | Lore, curiosidades, monturas, historias del mundo antes del Colapso |
| **Estudio de monstruos** | Debilidades y movimientos de jefes | Observar peleas, leer manchas de sangre, disecar partes | Pistas en los avisos (ver [Avisos](../04-combate/avisos-y-tacticas.md)), fichas vendibles |
| **Gabinete de ideas** | Tu propio héroe | Estilo *Disco Elysium*: "piensas" una idea durante horas reales (por ejemplo, "El peso de la armadura") y al terminar te da un rasgo pequeño y permanente, con pros y contras | Rasgos de personaje (identidad, no poder) |
| **Secretos de la región** | Jefes ocultos, pasadizos, finales alternativos | Pistas repartidas en textos, inscripciones, notas y conversaciones de la región | Acceso al jefe oculto, logros |
| **Gran Misterio de la Lejanía** | ¿Qué causó el Colapso? ¿Qué hay muy lejos del Claro? | Un misterio de años para toda la comunidad, estilo *Destiny* o los secretos de *Elden Ring*: cada región esconde una pieza, y la comunidad la une en sus chats | Historia, títulos únicos para quienes descubren piezas clave |

### 2.2 El Erudito

Investigar sube una reputación propia, la **Academia**, y el oficio de **Inscripción** (rama de Cartografía y Pergaminos) sirve para registrar descubrimientos. El Erudito y el Informante (ver [Profesiones](../07-economia/profesiones.md)) venden conocimiento: fichas de monstruos, mapas, notas de casos, traducciones de inscripciones antiguas.

## 3. Reglas para que funcione en texto

1. **Cada caso tiene una solución lógica** que se puede deducir solo con las pistas. Nada de "adivina lo que pensó el guionista".
2. **Los casos se escriben como datos** (pistas, testigos, contradicciones, solución), así se pueden producir muchos (ver [Arquitectura](../01-plataforma/arquitectura-modular.md), "el contenido son datos").
3. **Casos generados:** además de los escritos a mano, un generador combina culpables, motivos, métodos y pistas para los casos rápidos del tablón, así nunca se acaban.
4. **Contra las trampas:** en los casos del servidor, los detalles cambian un poco para cada jugador (el nombre del testigo, el lugar de la pista), así una respuesta copiada no sirve tal cual. Pero la lógica es la misma, y compartir el razonamiento está permitido.
5. **Sin penalización dura por equivocarse** en los casos rápidos. En los grandes, equivocarse cambia la historia, no te quita progreso.

Ver P-49 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
