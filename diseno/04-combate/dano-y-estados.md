# Daño, estados y partes del cuerpo

> **Módulo** [04 · Combate](README.md) · **Alimenta a:** [Heridas](../05-salud/heridas.md), [Jefes](../06-contenido/jefes.md), [Fabricación](../07-economia/fabricacion.md) (materiales de partes rotas) · **Estado:** propuesta

**De dónde sale.** *Elden Ring* y *Monster Hunter* (estados por acumulación), *Fallout* (apuntar partes del cuerpo con V.A.T.S.), *Fear & Hunger* (miembros que se pierden en combate por turnos), *Monster Hunter* (partes rompibles con materiales propios), *Divinity: Original Sin 2* (armadura física y mágica separadas).

---

## 1. Tipos de daño

| Familia | Tipos | Qué heridas deja (ver [Heridas](../05-salud/heridas.md)) |
|---|---|---|
| **Física** | Corte · Perforación · Contundente | Corte: laceraciones y sangrado. Perforación: heridas profundas y hemorragia interna. Contundente: contusiones, fracturas, conmoción |
| **Elemental** | Fuego · Escarcha · Naturaleza · Rayo | Fuego: quemaduras. Escarcha: congelación. Naturaleza: veneno |
| **Mística** | Arcano · Sombra · Sagrado · Vacío | Sombra y Vacío: estrés y corrupción. Arcano: Quemadura de Maná en quien lo abusa |

Cada tipo de armadura resiste distinto. Las placas frenan el corte pero no el contundente; el cuero frena la perforación a medias y deja pasar el fuego. **Elegir la armadura según el jefe del piso** es parte de la preparación. Los jefes tienen debilidades y resistencias por tipo, que el Bestiario va revelando (ver [Avisos y tácticas](avisos-y-tacticas.md)).

**Mitigación.** La armadura absorbe `def / (def + K)`, un porcentaje y no una resta (ver [Balance](../03-personaje/balance.md)).

## 2. Estados por acumulación

En lugar de "35 % de probabilidad de envenenar", cada golpe **suma** a una barra del objetivo. Cuando la barra se llena, el estado **revienta** y la barra se vacía. Así el azar no decide todo: el jugador ve cuánto falta y planifica.

| Estado | Al llenarse |
|---|---|
| 🩸 **Sangrado** | Pierde de golpe un porcentaje de su vida máxima y le queda una laceración |
| 🟢 **Veneno** | Daño por ronda durante 5 rondas y menos curación recibida |
| 🟤 **Podredumbre** | Daño por ronda grande y largo, que necesita una cura específica. Alto riesgo de secuela |
| ❄️ **Congelación** | Pierde su siguiente turno y recibe más daño físico |
| 🔥 **Quemadura** | Daño por ronda, y puede dejar una quemadura en una zona del cuerpo |
| 🌀 **Locura** | Pierde recurso y le sube el estrés. Un enemigo con locura ataca al azar durante una ronda |
| 💤 **Sueño** | Se salta turnos hasta que recibe daño |
| ☠️ **Maldición** | Efecto propio de cada jefe, por ejemplo "muere en 5 rondas si no se disipa" |

- La resistencia a los estados sale del equipo, los consumibles y el linaje (el Goblin resiste veneno).
- **El daño por ronda no pasa por la armadura, pero la acumulación sí**: la armadura hace que la barra se llene más despacio. Esto cierra una duda que TowerWars tiene abierta (si el veneno y la quemadura deberían pasar por la armadura).

## 3. Apuntar a partes del cuerpo

Como **acción rápida**, puedes apuntar tu próxima acción a una parte:

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

- **Interrumpir** es una reacción preparada: si el enemigo empieza a canalizar en esa ronda, se corta. Si no canaliza, se pierde el Aguante.
- El control (aturdir, silenciar, derribar, congelar) llena la **Firmeza** del objetivo (ver [Ronda y acciones](ronda-y-acciones.md)).
- Los jefes tienen Firmeza muy alta. El control sirve contra sus invocaciones y para ganar una ronda en el momento justo, no para dejarlos quietos toda la pelea.
