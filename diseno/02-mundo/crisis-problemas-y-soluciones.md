# Crisis del mundo: problemas que la comunidad tiene que resolver

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Fundación y cisma](fundacion-y-cisma.md) (necesidades de la ciudad), [Mundo vivo](mundo-vivo-y-viaje.md) · **Se conecta con:** todos los roles (ver [Roles](../00-vision/roles-y-caminos-de-juego.md)) · **Estado:** propuesta

**Qué pediste.** Problemas y soluciones: que el mundo tenga problemas reales y que resolverlos dependa de la gente.

**De dónde sale.**
- *Frostpunk* y *Banished*: la ciudad sufre hambre, frío, enfermedad y descontento, y cada crisis pide una respuesta distinta.
- *RimWorld* y *Dwarf Fortress*: incendios, plagas de cultivos, sequías y animales enfermos que encadenan problemas.
- *Crusader Kings III*: epidemias, hambrunas y revueltas.
- *EVE Online*: la escasez y las guerras de los jugadores mueven los precios de verdad.
- *World of Warcraft*: la Sangre Corrupta, un problema que nadie planeó y del que todos se acuerdan.

**La regla.** Cada crisis tiene **una causa en otro sistema**, **roles que la resuelven** y **consecuencias** si nadie hace nada. Nunca arruina a nadie para siempre; siempre deja historia.

---

## 1. Catálogo de crisis

| Crisis | Causa típica | Señales | Quién la resuelve | Si nadie hace nada |
|---|---|---|---|---|
| **Hambruna** | Pocos agricultores, mala cosecha, plaga de cultivos, invierno largo | La barra de comida de la ciudad cae | Agricultores, ganaderos, cazadores, pescadores, cocineros (conservas), comerciantes que traen comida de otras regiones | Se van los PNJ, la posada no cura, sube el estrés, la ciudad puede bajar de etapa |
| **Plaga de cultivos** (tizón, langosta) | Monocultivo, clima húmedo, no rotar los campos | Cosechas que se pudren | Agricultores que rotan, alquimistas (tratamientos), herboristas, cazadores (si la langosta viene de una criatura) | Hambruna |
| **Epizootia** (enfermedad del ganado y las monturas) | Corrales sucios, animales salvajes enfermos, comercio de animales | Animales débiles, carreras suspendidas | Veterinarios (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md)), ganaderos, cazadores que eliminan portadores | Mueren animales; sube el precio de la carne y las monturas |
| **Epidemia** | Ver [Enfermedades](../05-salud/enfermedades.md) | Contagios en la Gaceta | Médicos, alquimistas, investigadores, guardia (cuarentena) | Semanas de debilidad en media ciudad |
| **Incendio** | Forjas sin mantenimiento, rayos, sabotaje, dragones | "*¡Fuego en el barrio de las forjas!*" | **Cadena de cubos**: todos los presentes cooperan por rondas; constructores reconstruyen; investigadores buscan al culpable si fue sabotaje | Edificios dañados, obras perdidas |
| **Sequía** | Estación seca, clima extremo del anillo | El pozo baja, los cultivos se secan | Ingenieros (acueductos, norias, cisternas), constructores (pozos), alquimistas y sacerdotes (ritual de lluvia) | Hambruna, incendios |
| **Inundación** | Lluvias fuertes, ríos de la región | Nodos bajo el agua, caminos cortados | Constructores (diques), carpinteros (botes) | Almacenes y cosechas perdidos |
| **Invasión o incursión** | Poblaciones de monstruos sin control (ver [Mundo vivo](mundo-vivo-y-viaje.md)), eclipses | Aviso de la torre de vigía | Defensores, guardias, cazadores (antes, controlando la población) | Brecha, robo del almacén, daños (ver [Defensa](../09-construccion/defensa-y-protecciones.md)) |
| **Escasez de un material** | Una veta agotada, sobreexplotación | El precio se dispara | Exploradores y cartógrafos (vetas nuevas), comerciantes (traer de otras regiones), investigadores (sustitutos) | Obras frenadas |
| **Inflación** | Entra más oro del que sale | Todo sube de precio en el informe mensual | El consejo (impuestos, obras públicas que queman oro), el diseño (ajustar sumideros) | La economía pierde sentido |
| **Crimen** | Poca guardia, garitos, forajidos cerca | Robos PNJ, contrabando, recompensas | Guardia, detectives, cazarrecompensas, el consejo (leyes) | Sube el precio de todo por el "impuesto del miedo"; se van residentes |
| **Corrupción política** | Un alcalde que abusa de sus poderes (impuestos altos, licencias a amigos) | Quejas en el grupo de la ciudad | Los residentes: **moción de censura** (votación), cronistas que lo denuncian | Cisma (ver [Fundación y cisma](fundacion-y-cisma.md)) |
| **Revuelta** | Estrés alto en la ciudad, hambruna, impuestos abusivos | Disturbios PNJ | Bardos, cocineros (banquetes), el consejo (bajar impuestos), la guardia | Servicios cerrados unos días |
| **Deuda de la ciudad** | Obras por encima del tesoro | El tesoro en rojo | El consejo, donaciones, comerciantes | Obras paradas, edificios cerrados |
| **Maldición de la región** | Un gremio profanó algo (cripta, templo antiguo) | Efectos raros en toda la región | Sacerdotes, eruditos (investigación), grupos de combate (el origen) | Estrés y corrupción suben en toda la región |
| **Migración de refugiados** | Una región vecina cae ante una invasión | PNJ que llegan pidiendo refugio | Constructores (viviendas), agricultores (más comida), médicos | Hacinamiento, enfermedades |

## 2. Cómo se juega una crisis

1. **Aparece la señal** en `/ciudad` y en el grupo de la ciudad: una barra que baja, un aviso.
2. **La Gaceta la cuenta.** Los cronistas pueden escribir sobre ella.
3. **Se publican pedidos:** "*se necesitan 2.000 de grano en 5 días*", "*se buscan 10 constructores con rango de Albañil para el dique*". Cualquiera puede cubrirlos, con pago y reputación.
4. **Se resuelve por rondas cuando hay acción directa:** la cadena de cubos de un incendio y la defensa de una incursión se juegan por turnos (ver [Defensa](../09-construccion/defensa-y-protecciones.md)).
5. **Final:** si se resolvió, recompensas y títulos ("Héroe del Gran Incendio"); si no, las consecuencias (nunca permanentes para los jugadores, sí para la historia de la ciudad).

## 3. Cadena de cubos (ejemplo por turnos)

```
🔥 ¡Incendio en el barrio de las forjas! · Ronda 3
Fuego ▓▓▓▓▓▓▓░░░   Edificios en riesgo: Forja de Tor, Almacén
Presentes: 9 · Agua en cubos: 14

[🪣 Pasar cubo]     [💧 Sacar agua del pozo]
[🪓 Derribar muro para cortar el fuego]
[🩹 Atender a un herido]   [📢 Organizar la cadena]
```

- Cada jugador elige una acción por ronda.
- Los que "organizan" (constructores y guardias con rango) multiplican lo que hacen los demás.
- Si el fuego llega al 100 %, el edificio queda dañado; si baja a 0, se salva.
- Quien se acerca demasiado puede quemarse (ver [Heridas](../05-salud/heridas.md)).

## 4. Por qué conviene

- **Todo rol tiene su momento:** la hambruna es el momento del agricultor, el incendio el del constructor, la epidemia el del médico, la revuelta el del bardo.
- **Las crisis conectan los sistemas:** una sequía lleva a la hambruna, la hambruna a la revuelta, la revuelta a un cisma.
- **Dan historia:** "el invierno del hambre", "el gran incendio del Claro". Eso es lo que la gente recuerda años después.
