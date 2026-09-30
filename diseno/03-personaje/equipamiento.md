# Equipamiento

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Fabricación](../07-economia/fabricacion.md), [Jefes](../06-contenido/jefes.md) · **Alimenta a:** [Combate](../04-combate/README.md), [Heridas](../05-salud/heridas.md), [Economía](../07-economia/economia.md) · **Estado:** propuesta

**De dónde sale.**
- *World of Warcraft*: 16 ranuras, tipos de armadura, calidades por color, nivel de objeto, conjuntos, gemas, encantamientos, pistas de mejora y Gran Tesoro semanal.
- *Albion Online*: tiers de T1 a T8, encantamiento de .1 a .4, calidad al fabricar, durabilidad y destrucción. Casi todo lo fabrican jugadores, y los jefes sueltan **artefactos** que sirven de ingrediente.
- *Elden Ring*: la carga de equipo decide cómo te mueves, y el **Recuerdo** del jefe se cambia por un objeto concreto.
- *Diablo* y *Path of Exile*: afijos.
- *Star Wars Galaxies*: el nombre del artesano grabado en el objeto.

---

## 1. Ranuras

Son las 16 de WoW, agrupadas para que se lean bien en un teléfono. Cada ranura de armadura está atada a la zona del cuerpo que protege (ver [Heridas](../05-salud/heridas.md)).

| Grupo | Ranura | Protege |
|---|---|---|
| **Armas** | Mano principal · Mano secundaria (o arma a dos manos) | — |
| **Armadura** | Cabeza | Cabeza |
| | Hombros · Pecho | Torso |
| | Cintura | Abdomen |
| | Muñecas · Manos | Brazos |
| | Piernas · Pies | Piernas |
| | Espalda (capa) | Clima (frío, calor, lluvia) |
| **Joyas** | Cuello · Anillo ×2 | — |
| **Abalorios** | Abalorio ×2 | Efecto activable o pasivo |
| **Utilidad** | Herramienta de oficio ×2 · Mochila · Montura | — |
| **Cosmético** | Tabardo · Camisa · Apariencias | — |

Se puede lanzar con 10 ranuras (armas, cabeza, hombros, pecho, manos, piernas, pies, capa, anillo, cuello) y llegar a las 16 en la beta.

## 2. Tipos de armadura y carga

| Tipo | Clases que la dominan | Protege mejor contra | Peso |
|---|---|---|---|
| **Tela** | Mago, Sacerdote, Brujo, Nigromante | Daño místico | Ligero |
| **Cuero** | Pícaro, Druida, Monje, Cazador de Demonios, Bardo | Perforación; elemental a medias | Medio-ligero |
| **Malla** | Cazador, Chamán, Evocador | Corte, perforación | Medio |
| **Placas** | Guerrero, Paladín, Caballero de la Muerte | Corte (mucho), perforación | Pesado |

- **Dominio:** tu clase domina un tipo de armadura y recibe un bono si llevas todo el conjunto de ese tipo, como la especialización de armadura de WoW.
- **Libertad con costo:** puedes ponerte cualquier armadura, pero sin dominio no recibes el bono y el **peso** te castiga. Un mago en placas es posible, y es lento.
- **Carga** (Elden Ring): el peso del equipo frente a tu capacidad (que sale de la raza y el aguante).

  | Carga | Efecto |
  |---|---|
  | Ligera (<30 %) | +iniciativa; esquivar cuesta menos Aguante |
  | Media (30-70 %) | Normal |
  | Pesada (70-100 %) | −iniciativa; Aguante máximo −1 |
  | Sobrecargado (>100 %) | No puedes esquivar |

## 3. Qué define a un objeto

Cada objeto tiene siete propiedades. En la pantalla se ven dos o tres; el resto está en el detalle.

| Propiedad | Valores | De dónde sale | Qué decide |
|---|---|---|---|
| **Tramo** | T1 a T10, uno por tramo de 10 pisos | Albion (tiers) | La base de sus números y el material con que se hace |
| **Calidad** (si es fabricado) | Normal · Buena · Notable · Excelente · Obra Maestra | Albion (calidad al fabricar) | Bono sobre la base; sale de la [fabricación](../07-economia/fabricacion.md) |
| **Rareza** (si es botín) | Común · Poco común · Raro · Épico · Legendario · Reliquia | WoW (colores) | Cuántos afijos tiene |
| **Encantamiento** | +0 a +4 | Albion (.1 a .4) | Cada nivel sube el Poder de Objeto como un tramo parcial. Se hace infundiendo runas, almas y reliquias |
| **Mejoras** | 0 a 3 | Pistas de mejora de WoW | Cada mejora cuesta Esencia y material, y nunca llega a la base del tramo siguiente |
| **Afijos** | 0 a 4 líneas | WoW (secundarias), Diablo | Crítico, Celeridad, Maestría, Versatilidad, resistencias, protección de zona, robo de vida… |
| **Engarces** | 0 a 2 | WoW (gemas) | Gemas de joyería |

Además: **durabilidad** (actual y máxima), **peso**, **atadura** y **firma del artesano**.

### Poder de Objeto (PO)

Todo lo anterior se resume en un número, el **Poder de Objeto** (como el nivel de objeto de WoW o el *item power* de Albion). Lo usan el buscador de grupos para los requisitos mínimos y el mercado para ordenar.

```
⚔️ Espada Larga de Acero Estelar   [PO 412]
T5 · Excelente · +2 · Mejoras 1/3
Forjada por Lisbeth la Herrera ✒️
+38 Fuerza · +Crítico · +Protección de brazo
Técnica: Tajo Circular (golpea a toda la vanguardia)
Durabilidad 84/100 (máx. 96) · 4,2 kg · Libre
```

## 4. Durabilidad: el equipo se gasta de verdad

**De dónde sale.** En Albion y EVE el equipo se pierde, se rompe y se reemplaza, y eso sostiene la economía durante años. En WoW casi nunca se pierde, y la fabricación depende de que llegue la próxima expansión.

- Cada objeto tiene **durabilidad actual**, que baja al combatir y al caer, y **durabilidad máxima**.
- **Reparar** devuelve la actual, cuesta oro (sumidero) y **baja un poco la máxima**. Un herrero de mucho nivel repara perdiendo menos máxima, así que su servicio vale más que el del PNJ.
- Cuando la máxima llega a 0, el objeto se rompe **para siempre**. Se puede desmontar para recuperar parte del material.
- Resultado: una pieza normal dura varias semanas de uso intenso. Siempre hay demanda de armas y armaduras, **aunque no salga contenido nuevo**.

## 5. Atadura

| Tipo | Regla | Para qué objetos |
|---|---|---|
| **Libre** | Se puede comerciar siempre | Casi todo lo fabricado, materiales, consumibles, **artefactos de jefe** |
| **Ligado al equipar** | Libre hasta que alguien se lo pone | Piezas fabricadas con artefactos (armas únicas) |
| **Ligado al recoger** | No se comercia | Solo recompensas de prestigio: cosméticos de Pionero, títulos, objetos de logro |

La mayor parte del poder se **fabrica y se comercia**. El jefe no te da la espada: te da el **artefacto** para que un herrero la haga.

## 6. De dónde sale el equipo

| Fuente | Qué da | Por qué |
|---|---|---|
| **Artesanos** | La mayoría de las piezas de todos los tramos | La economía gira alrededor de ellos (Albion) |
| **Jefes** | **Artefactos** (la Garra del Wyrm, el Corazón del Coloso), que son ingredientes de armas y armaduras únicas con técnicas propias; **planos** raros; materiales de partes rotas (ver [Daño y estados](../04-combate/dano-y-estados.md)) | Une el botín de jefe de WoW con la fabricación de Albion: importa matar al jefe, y también el herrero |
| **Recuerdos del Guardián** | La primera victoria contra cada Guardián da un Recuerdo **garantizado**, que se cambia por una de dos piezas icónicas de ese jefe | Elden Ring: recompensa determinista para lo más importante |
| **Mercado Negro** | Las piezas que sueltan los monstruos comunes **las fabricaron jugadores** y el Mercado Negro las compró | Albion: hasta el botín del mundo depende de los artesanos (ver [Economía](../07-economia/economia.md)) |
| **Tienda PNJ** | Equipo básico T1 y T2 | Para empezar |
| **Vendedores de reputación y PvP** | Piezas con afijos específicos | Metas de largo plazo |

## 7. Técnicas de equipo

Cada tipo de arma da **una técnica** y cada pecho o par de botas da **otra** (ver la barra de 8 en [Clases](clases-y-especializaciones.md)).

| Pieza | Técnica |
|---|---|
| Espada larga | *Tajo Circular*: golpea a toda la vanguardia |
| Lanza | *Estocada Profunda*: alcanza la retaguardia desde la vanguardia |
| Maza | *Quebrantahuesos*: mucho daño a la postura y más probabilidad de fractura |
| Hacha | *Hendidura*: abre una herida que sangra |
| Dagas | *Puñalada Trapera*: crítico garantizado por la espalda (si el objetivo mira a otro) |
| Arco largo | *Flecha Clavadora*: el objetivo no puede cambiar de fila |
| Ballesta | *Virote Perforante*: ignora parte de la armadura |
| Bastón | *Remanso*: recupera maná y baja el estrés propio |
| Varita | *Chispa*: ataque a distancia gratis que acumula estado elemental |
| Escudo torre | *Muro*: la fila entera recibe menos daño una ronda |
| Pecho de placas | *Resistir*: ignora el siguiente derribo |
| Pecho de malla | *Cota Tensa*: la próxima herida baja un nivel de gravedad |
| Pecho de cuero | *Capa de Humo*: esquiva garantizada una ronda |
| Túnica | *Barrera Rúnica*: escudo que absorbe magia |
| Botas de placas | *Carga*: cambia de fila y pega en la misma acción |
| Botas de cuero | *Paso Ligero*: +iniciativa durante 2 rondas |

Las armas de artefacto tienen técnicas únicas. La Garra del Wyrm da *Barrido de Dunas*: arena que ciega a la vanguardia.

## 8. Suerte, pero con red

**El problema de WoW:** semanas sin el objeto que necesitas.

1. **Protección contra mala racha.** Cada vez que un jefe no te da nada útil, sube tu probabilidad la próxima vez. WoW la agregó en 2013 a sus tiradas extra.
2. **Recuerdos del Guardián**, deterministas (§6).
3. **Tesoro Semanal.** Según lo que hiciste en la semana (mazmorras, bandas, Profundidades, PvP) se abren hasta 9 casillas y eliges **una** recompensa. Si ninguna te sirve, te llevas su valor en Esencia. Es el Gran Tesoro de WoW.
4. **Mejoras con Esencia.** Lo que no sale, se mejora.
5. **Tirada a la vista.** En grupo, "Necesidad / Codicia" se tira con el 🎲 nativo en el chat (ver [Gremios y social](../08-social/gremios-y-social.md)).

## 9. Apariencias y colecciones

- **Apariencias textuales.** Cada pieza tiene una descripción visual, y puedes ponerle a tu equipo la apariencia de otra pieza que hayas tenido (la transfiguración de WoW). Todo esto se ve en tu perfil y en las citas de combate.
- **Colección de apariencias** compartida por toda la cuenta.
- **Tarjeta de perfil** en imagen (fase tardía): tu equipo, tus cicatrices y tus títulos en una carta lista para reenviar.

Ver P-14 y P-34 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
