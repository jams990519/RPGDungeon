# Daño, estados y partes del cuerpo

> **Módulo** [04 · Combate](README.md) · **Depende de:** [Ronda y acciones](ronda-y-acciones.md) · **Alimenta a:** [Heridas](../05-salud/heridas.md), [Jefes](../06-contenido/jefes.md), [Fabricación](../07-economia/fabricacion.md) (materiales de partes rotas) · **Estado:** propuesta, con D-46 (6 botones) aplicada

**De dónde sale.** *Elden Ring* y *Monster Hunter* (estados por acumulación), *Fallout* (apuntar partes del cuerpo con V.A.T.S.), *Fear & Hunger* (miembros que se pierden en combate por turnos), *Monster Hunter* (partes rompibles con materiales propios), *Divinity: Original Sin 2* (armadura física y mágica separadas).

---

## 1. Tipos de daño

| Familia | Tipos | Qué heridas deja (ver [Heridas](../05-salud/heridas.md)) |
|---|---|---|
| **Física** | Corte · Perforación · Contundente | Corte: laceraciones y sangrado. Perforación: heridas profundas y hemorragia interna. Contundente: contusiones, fracturas, conmoción |
| **Elemental** | Fuego · Escarcha · Naturaleza · Rayo | Fuego: quemaduras. Escarcha: congelación. Naturaleza: veneno |
| **Mística** | Arcano · Sombra · Sagrado · Vacío | Sombra y Vacío: estrés y corrupción. Arcano: Quemadura de Maná en quien lo abusa |

Cada tipo de armadura resiste distinto. Las placas frenan el corte pero no el contundente; el cuero frena la perforación a medias y deja pasar el fuego. **Elegir la armadura según el jefe del piso** es parte de la preparación, igual que llevar en el cinturón la **poción de resistencia** del tipo que más pega (ver [Ronda y acciones](ronda-y-acciones.md)). Los jefes tienen debilidades y resistencias por tipo, que el Bestiario va revelando (ver [Avisos y tácticas](avisos-y-tacticas.md)).

**Mitigación.** La armadura absorbe `def / (def + K)`, un porcentaje y no una resta (ver [Balance](../03-personaje/balance.md)).

## 2. Estados por acumulación

En lugar de "35 % de probabilidad de envenenar", cada golpe **suma** a una barra del objetivo. Cuando la barra se llena, el estado **revienta** y la barra se vacía. Así el azar no decide todo: el jugador ve cuánto falta y planifica.

**Ligero en pantalla (D-44).** La barra de un estado solo aparece cuando pasa de la mitad, con su icono: `🩸▓▓▓▓▓▓▓░░░`. Mientras tanto, no ocupa lugar.

| Estado | Al llenarse | Cómo se quita en combate | Desde |
|---|---|---|---|
| 🩸 **Sangrado** | Pierde de golpe un porcentaje de su vida máxima y le queda una laceración | 🩹 Venda o 💊 coagulante; curas que cierran heridas | El principio |
| 🟢 **Veneno** | Daño por ronda durante 5 rondas y menos curación recibida | 💊 Antídoto; habilidades que curan veneno | El principio |
| 🔥 **Quemadura** | Daño por ronda, y puede dejar una quemadura en una zona del cuerpo | 💊 Ungüento para quemaduras | El principio |
| ❄️ **Congelación** | Pierde su siguiente turno y recibe más daño físico | 💊 Tónico caliente; recibir fuego | El principio |
| 🟤 **Podredumbre** | Daño por ronda grande y largo, que necesita una cura específica. Alto riesgo de secuela | Solo su remedio propio (Alquimia de nivel alto) o una cura de enfermedad | Pisos altos |
| 🌀 **Locura** | Pierde recurso y le sube el estrés. Un enemigo con locura ataca al azar durante una ronda | 💊 Sales de calma; habilidades que disipan | Pisos altos |
| 💤 **Sueño** | Se salta turnos hasta que recibe daño | Recibir daño; un aliado lo despierta con Levantar | Pisos altos |
| ☠️ **Maldición** | Efecto propio de cada jefe, por ejemplo "muere en 5 rondas si no se disipa" | Disipar (habilidad de clase) o un pergamino de purificación (Inscripción) | Jefes |

- **Capa simple primero.** En los primeros pisos solo aparecen los cuatro de arriba (sangrado, veneno, quemadura y congelación), que son los que se curan con lo que ya llevas en el cinturón. Los otros llegan con los pisos altos y los jefes.
- **Quitar un estado gasta la ronda**, sea con un remedio de la 🎒 Mochila o con una habilidad. Por eso conviene vaciarlo antes de que reviente, no después.
- **Disipar** magia, curar veneno y curar enfermedad lo tienen al menos 4 clases cada uno, y siempre hay un consumible fabricado que hace lo mismo (ver [Balance](../03-personaje/balance.md)).
- La resistencia a los estados sale del equipo, los consumibles y el linaje (el Goblin resiste veneno).
- **El daño por ronda no pasa por la armadura, pero la acumulación sí**: la armadura hace que la barra se llene más despacio. Esto cierra una duda que TowerWars tiene abierta (si el veneno y la quemadura deberían pasar por la armadura).

## 3. Apuntar a partes del cuerpo

Apuntar ya **no es un botón ni una acción aparte** (D-46). Se hace de dos formas, las dos sin sumar botones:

1. **Como efecto de habilidades** (la forma normal). Algunas pegan siempre a una parte (*Golpe de Escudo* a la cabeza, *Tajo a las Corvas* a las piernas, *Desarmar* a los brazos) y otras dejan elegir la parte sin penalización (*Apuntar*, del Cazador de Puntería).
2. **Dentro de ⚔️ Atacar (opcional, capa profunda).** Por defecto, Atacar va al torso sin preguntar. Si activas "apuntar con Atacar" en tus opciones, contra enemigos con partes (monstruos grandes, jefes, y jugadores en PvP) al tocar Atacar aparece el teclado con sus partes: `Coloso · torso`, `Coloso · brazo der.`, `Coloso · cola`. La parte elegida se recuerda, así que repetir cuesta un toque.

**Por qué así.** Es la forma más ligera (D-44): el jugador nuevo nunca ve el menú de partes, y quien quiere romper partes lo tiene a un ajuste de distancia, sin sumar botones (ver [Clases](../03-personaje/clases-y-especializaciones.md) §4). Las [Tácticas](avisos-y-tacticas.md) también pueden apuntar ("mientras la cola esté entera, Atacar a la cola").

| Parte (humanoides) | Precisión | Si impacta | Si la rompes (monstruos grandes) |
|---|---|---|---|
| **Cabeza** | −25 % | +50 % de probabilidad de crítico; puede aturdir; más probabilidad de herida grave | Pierde su aliento o su grito; material de cabeza |
| **Brazos** | −10 % | El objetivo pega menos 2 rondas; puede desarmarlo | Pierde un ataque con garra o arma; material |
| **Piernas** | −10 % | Pierde iniciativa y no puede huir | Cae al suelo una ronda (su postura se rompe más fácil) |
| **Torso** | Normal | Daño normal | — |
| **Parte especial** (cola, alas, cuernos, núcleo) | Varía | Según el monstruo | Material exclusivo; el monstruo pierde una mecánica entera |

- El Cazador de Puntería apunta sin penalización de precisión.
- Los jugadores también reciben golpes en partes concretas: es lo que alimenta el sistema de [Heridas](../05-salud/heridas.md).
- En PvP, apuntar a la cabeza sube el riesgo para los dos: el que recibe puede quedar herido de gravedad y el que apunta falla más.

**Por qué conviene.** Cada monstruo grande se vuelve un rompecabezas ("¿le cortamos la cola primero para que deje de barrer la retaguardia?"). Además, la economía recibe materiales únicos: la cola del Wyrm de las Dunas solo existe si alguien se la cortó.

## 4. Interrupciones y control

- **Interrumpir ✋ es un efecto**, no un botón: lo tienen ciertas habilidades (*Golpe de Escudo*, *Patada*, *Contrahechizo*) y la 💣 bomba de destello. En la barra, la habilidad lleva la marca ✋.
- **Una canalización avisada termina al final de la ronda siguiente al aviso.** Cualquier ✋ que caiga en esa ronda la corta, sin importar la iniciativa. Si el enemigo no canalizaba, la habilidad hace su efecto normal (si pega, pega), pero el ✋ se pierde y entra en enfriamiento.
- Toda spec tiene una interrupción o algo equivalente en su repertorio (ver [Balance](../03-personaje/balance.md)); llevarla en una de las 3 casillas es decisión de cada uno según el enemigo.
- El control (aturdir, silenciar, derribar, congelar) llena la **Firmeza** del objetivo (ver [Ronda y acciones](ronda-y-acciones.md)).
- Los jefes tienen Firmeza muy alta. El control sirve contra sus invocaciones y para ganar una ronda en el momento justo, no para dejarlos quietos toda la pelea.
