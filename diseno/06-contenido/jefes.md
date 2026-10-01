# Jefes: dificultad de Elden Ring, en texto y por turnos

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Combate](../04-combate/README.md) (avisos, postura, partes) · **Alimenta a:** [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (la Frontera, Pioneros), [Equipamiento](../03-personaje/equipamiento.md) (artefactos, Recuerdos) · **Estado:** propuesta

**De dónde sale.**
- *Elden Ring* y *Dark Souls*: jefes que se aprenden muriendo, golpes retrasados, fases con transformación, postura, invocación de otros jugadores, cenizas espirituales, mensajes en el suelo y manchas de sangre.
- *World of Warcraft*: jefes de mundo y avisos de mecánicas.
- *Monster Hunter*: partes rompibles.
- Bots de Telegram: *Ragna* (desde 2017), un jefe que se invoca en cualquier chat para una pelea de 5 minutos con roles; y *ORNEST*, con un jefe mundial semanal.

---

## 1. Tipos de jefe

| Tipo | Dónde | Cuántos | Dificultad | Recompensa |
|---|---|---|---|---|
| **De campo** | Tierras salvajes, a la vista | 2 o 3 por región | Media-alta | Materiales, artefactos menores |
| **Guardián de la región** (jefe de mundo, D-08) | Su guarida | 1 por región | Alta: su caída hace avanzar la Frontera | Recuerdo, artefactos, título de Pionero (solo el primer grupo) |
| **Oculto** | En los secretos de la región (hay que encontrarlo) | 0 o 1 por región | Muy alta | Artefactos únicos, título, historia |
| **Gran Barrera** (propuesta, en ciertos anillos) | Su Gran Barrera | 3 | Extrema; varios grupos a la vez | Lo mejor del anillo |
| **Errante** | Se invoca en cualquier chat de grupo con un **Cuerno de Invocación** | Muchos | Media | Cajas de botín para el chat |
| **Semanal de servidor** | Rota por las regiones | 1 por semana | Vida **compartida por todo el servidor** | Según la contribución; ranking por gremio |

El **Cuerno de Invocación** se fabrica (Inscripción y Joyería), así que el jefe errante también mueve la economía.

## 2. Las diez reglas de un jefe de Elden Ring hecho en texto

1. **Duro pero justo.** Todo golpe grande se avisa (ver [Avisos](../04-combate/avisos-y-tacticas.md)). Nadie muere por azar puro.
2. **Repertorio fijo.** Entre 8 y 12 movimientos por jefe, con variaciones. Se aprende.
3. **Castiga la codicia.** Golpes retrasados, combos de varios golpes y fintas en las últimas fases.
4. **Fases.** Al 66 % y al 33 % de vida, cada una con movimientos nuevos. La última cambia el tono: "*el Coloso se parte, y de adentro sale algo más pequeño y mucho más rápido*".
5. **Postura.** Romperla abre la ventana de golpes críticos. Es lo que acorta una pelea larga si el grupo juega bien.
6. **Partes.** Romperlas le quita movimientos (ver [Daño y estados](../04-combate/dano-y-estados.md)).
7. **No escala con tu nivel.** Subir de nivel de más ayuda, como en Souls, pero la mecánica mata igual.
8. **Invocaciones.** Puedes pedir ayuda (§3).
9. **Conocimiento.** El Bestiario registra lo aprendido.
10. **Aprendes de los muertos.** Las manchas de sangre muestran las últimas rondas de quienes cayeron ahí.

## 3. Pedir ayuda al estilo Souls, sin estar conectados a la vez

- **Signos de invocación.** Quien ya venció a un jefe puede dejar su **signo** en la guarida, y quien está peleando puede invocarlo:
  - Si el dueño del signo está conectado, le llega un aviso y **entra a la pelea de verdad**.
  - Si no lo está, entra su **Eco**: una copia de su héroe que pelea con sus [Tácticas](../04-combate/avisos-y-tacticas.md).
  - Los dos cobran recompensa. El ayudante recibe una moneda de "Ayuda" que compra cosméticos y consumibles.
- **Espíritus.** Aliados PNJ coleccionables (las *cenizas espirituales* de Elden Ring). Se consiguen de jefes o los fabrican nigromantes y encantadores. Máximo uno por pelea.
- **Escalado.** Cada ayudante sube la vida del jefe, aunque menos que en proporción, y hace que el jefe reparta la atención.
- **Notas en el suelo.** Los jugadores dejan mensajes en los nodos con frases de plantilla ("*cuidado con el golpe retrasado*", "*tesoro adelante*", "*prueba a esquivar*"), y otros los valoran. Como en Elden Ring: humor, ayuda y trampas. Las plantillas impiden usar las notas para insultar.

## 4. Ejemplo completo: el Guardián del Mar de Dunas, Wyrm de las Dunas

**Datos:**
- **Vida:** escala con los participantes. **Postura:** alta.
- **Débil** a escarcha y a perforación en el vientre. **Resiste** fuego y corte.
- **Partes rompibles:** la cola (le quita *Barrido*), las alas (le quita *Tormenta de Arena*) y el vientre, que solo queda expuesto después de *Zambullida*.

**Repertorio:**

| Movimiento | Aviso | Respuesta correcta | Si fallas |
|---|---|---|---|
| **Mordisco** | "*clava la mirada en X*" | X esquiva, o el tanque provoca | Herida profunda |
| **Barrido de cola** | "*la cola se enrosca hacia la retaguardia*" | La retaguardia cambia de fila o esquiva | Derribo y contusión |
| **Tormenta de Arena** (canalizada) | "*bate las alas y el aire se llena de arena*" | **Interrumpir** en esa ronda | Ceguera 3 rondas (precisión −50 %) |
| **Zambullida** | "*se hunde en la arena…*" (una ronda sin objetivo) | Agruparse en el centro. En la ronda siguiente sale y expone el vientre | Quien quede disperso recibe el golpe entero |
| **Aliento de Vidrio** (retrasado) | "*inhala… y retiene el aire*" | **Esperar**, y esquivar en la ronda siguiente | Quemadura de grado 2 en una fila |
| **Fase 2 (66 %): Enjambre** | "*de su lomo caen escorpiones*" | Cambiar de objetivo y cuidar a los sanadores | Veneno acumulado |
| **Fase 3 (33 %): Tormenta Perpetua** | "*el cielo se oscurece*" | — | Por el resto del combate hay poca visibilidad y los avisos llegan con menos detalle |

**Recompensas:**
- **Primera muerte del servidor:** título "Pionero del Mar de Dunas" y un cosmético único.
- **Recuerdo:** *Garra de las Dunas* (arma) o *Escamas del Wyrm* (pecho de malla).
- **Artefactos posibles:** Colmillo de Vidrio, Glándula de Arena.

## 5. Cómo se prueba que un jefe es justo

- Todo jefe nuevo pasa por el **simulador** con grupos de PNJ que juegan "bien" (siguen todos los avisos) y "mal" (ignoran los retrasados).
- Un grupo que juega bien tiene que poder ganarle con equipo del anillo sin mejoras. Si no puede, el jefe está roto.
- Un grupo que juega mal tiene que perder aunque tenga equipo de dos anillos más lejos. Si gana, el jefe es aburrido.
- Los números de cada jefe y cada cambio van al registro de balance (ver [Balance](../03-personaje/balance.md)).
