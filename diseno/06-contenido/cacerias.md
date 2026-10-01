# Cacerías

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Combate](../04-combate/README.md) (partes rompibles), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (ecología, día y noche, clima) · **Alimenta a:** [Fabricación](../07-economia/fabricacion.md) (materiales de partes), [Progresión](../03-personaje/progresion.md) (bestiario, trofeos), [Casa propia](../09-construccion/casa-propia.md) (sala de trofeos) · **Estado:** §0 está en el juego (🏹 Cazar en la zona y 🏹 Partida de caza del campamento, capa simple, D-106 provisional); lo demás es propuesta

**De dónde sale.**
- *Monster Hunter*: rastrear a la presa, romper sus partes, capturarla viva o matarla, y fabricar equipo con lo que rompiste.
- *Midnight* (WoW, 2026): el sistema **Prey**, que caza objetivos en dificultad Normal, Difícil o Pesadilla.
- *Red Dead Redemption 2* y *theHunter*: calidad de la pieza (una piel perfecta vale más que una rota), cebos, rastreo por huellas, animales legendarios.
- *The Witcher 3*: contratos de monstruos del tablón, con investigación previa (ver [Investigaciones](investigaciones.md)).
- *Skyrim*: licántropos y vampiros como presas y cazadores.
- *Pokémon* y *Monster Hunter*: capturar vivo en lugar de matar.

**Por qué conviene.** La cacería es el puente entre explorar, pelear y fabricar. Da materiales que no salen de ningún otro lado, le da uso a la ecología del mundo y es una forma de jugar solo o en grupos chicos que no depende de horarios.

---

## 0. En el juego (D-106, provisional)

**Qué pidió el dueño** (por voz, 1-oct-2026). "Agregar el formato de cacería en la misma zona: no solo misiones, sino un formato de cacería para atacar solo mobs". Y: "una vez creas el campamento y agregas más personas, esas personas pueden ir contigo a las misiones y a las cacerías".

**Cómo se tomó** (D-106, provisional, en [decisiones.md](../00-vision/decisiones.md)). La **capa simple** de este documento (D-44): cazar es pelear en la zona donde estás, sin explorar ni recolectar; y la **partida de caza** junta a los miembros de un campamento que están en la misma zona, con un bono y una cuenta de presas común. La forma y los números son interpretación de Claude. Todo lo que sigue después de §0 (contratos, rastreo, acecho, partes, calidad de la pieza, captura viva, herramientas, Bestiario, ecología, rangos) **sigue siendo propuesta**: la capa profunda.

### 0.1 🏹 Cazar en la zona

- **Dónde está el botón:** 🧭 Explorar → **🏹 Cazar**. 🧭 Explorar sigue con 4 botones (D-75): 🔎 Explorar · 🪓 Recolectar · 🏹 Cazar · 🗺️ Mapa. Para hacerle lugar, **📒 Lugares se mudó adentro de 🗺️ Mapa** (🗺️ Mapa → 📒 Lugares, y su ↩️ Volver vuelve al mapa).
- **La pantalla 🏹 Cazar** muestra qué enemigos rondan la zona (los mismos de los encuentros: del bioma y del nivel de la zona, nunca jefes), cuánto cuesta cada presa, que no suma exploración ni recursos, y tu vida y energía. Botones: **🏹 Buscar presa · ⚡2**, **🏹 Partida de caza** o **🏹 Unirme** (solo con campamento) y ↩️ Volver.
- **🏹 Buscar presa** cobra **2 de energía** (`hunt.energy`; lo fijó D-108 para que cazar dé una experiencia por ⚡ parecida a explorar y recolectar; la pelea en sí no gasta, D-78) y empieza **enseguida** una pelea normal, de 1 contra 1, contra un enemigo común de la zona. Su nivel es el de la zona, +1 con 30 % de probabilidad, como en los encuentros.
- **Qué da:** solo lo de la pelea: experiencia, monedas, botín (las bestias sueltan 🍖 carne para la despensa; equipo con la probabilidad de siempre) y la victoria cuenta para el gremio (D-97). **Nunca da exploración ni recursos.**
- **Al ganar**, la pantalla final ofrece **🏹 Otra presa** (si te queda energía) antes de ▶️ Continuar, y 🏹 Partida de caza o 🏹 Unirme si corresponde: 3 botones como máximo. Al perder o huir, solo ▶️ Continuar.
- **Dónde no se caza:** en el Claro (su bioma no tiene peligro: no hay presas) y en la guarida del Guardián (solo está él: ⚔️ Desafiar al Guardián sigue en 🧭 Explorar, que ahí queda con 3 botones). **Sí se caza en el territorio de un campamento**: la tierra protege de las emboscadas al llegar, explorar o recolectar (D-81), pero salir a buscar una presa es a propósito.
- **Cuándo no:** malherido (🤕: primero hay que curarse, y el juego lo dice), ocupado (viajando, explorando, recolectando o durmiendo: una actividad a la vez) o sin energía. Se avisa y no se cobra nada.

### 0.2 🏹 Partida de caza con tu campamento

- **Quién la convoca:** cualquier miembro de un campamento de jugadores, desde 🏹 Cazar o desde el final de una presa, en una zona donde se pueda cazar y sin estar malherido. No gasta energía.
- **A quién avisa:** solo a los miembros del campamento **presentes en esa misma zona**: los mismos que salen en 👥 de 📍 Zona (tocaron un botón en los últimos 15 minutos, o exploran, recolectan o duermen ahí, D-96). El aviso trae **🏹 Unirme**. A los que están en otra zona no les llega nada: no hay teletransporte. Quien llega después se une desde 🏹 Cazar.
- **Una por campamento a la vez**, y dura **30 minutos** (`hunt.party.minutes`). Si ya hay una en tu zona, convocar te une.
- **Unirse:** solo los miembros, y solo desde la zona de la partida. Se puede aunque estés explorando o recolectando ahí (para cazar, primero hay que terminar o parar).
- **Bono de grupo:** cada presa que gana un cazador de la partida en esa zona da **+10 % de experiencia y de probabilidad de botín** (carne, equipo) **por cada otro cazador de la partida presente en la zona, hasta +30 %**. Nunca más monedas. Cazar solo rinde lo de siempre.
- **Cuenta común:** la partida suma las presas de todos. La pantalla 🏹 Cazar y el final de cada presa la muestran ("🏹 Partida de caza: 4/6 presas entre todos · bono de esta presa +10 %").
- **Cierre:** reloj perezoso, como las oleadas (D-99): cuando terminó la ventana y un miembro del campamento juega, la partida se cierra y **todos sus cazadores reciben un informe** (presas juntas y las de cada uno). Solo cuentan las presas ganadas antes de que termine la ventana.
- **Premio:** si se unieron **al menos 2 cazadores** y juntaron **3 presas por cazador**, cada cazador con al menos 1 presa gana **40 de experiencia y 20 🥉**. Unirse sin cazar no cobra nada, y una partida de uno solo nunca da premio.
- **Sin pelea compartida:** cada uno pelea su presa, de 1 contra 1. "Ir juntos" es cazar en la misma zona a la misma hora, con el bono y la cuenta común.

| Número | Valor | Dónde |
|---|---|---|
| Energía por presa | 2 (D-108) | `hunt.energy` |
| Duración de la partida | 30 minutos | `hunt.party.minutes` |
| Bono por compañero presente | +10 % de experiencia y de probabilidad de botín | `hunt.party.bonus_per_companion` |
| Tope del bono | +30 % | `hunt.party.bonus_cap` |
| Meta | 3 presas por cazador (contando al menos 2) | `hunt.party.prey_per_hunter`, `min_hunters` |
| Premio | 40 de experiencia y 20 🥉 a cada cazador con al menos 1 presa | `hunt.party.reward` |

### 0.3 Lo que todavía no tiene

- **Las misiones con los miembros del campamento** ("pueden ir contigo a las misiones") quedan para la tarea de misiones, que está en cola: la partida de caza solo cubre las cacerías.
- La capa profunda de este documento (contratos, rastreo, acecho, partes rompibles, calidad de la pieza, captura viva, herramientas, Bestiario, ecología y rangos de cazador) sigue como propuesta.

**Dónde está.** Código: `engine/service/game.py` (sección "hunting", y ganchos en `_explore_menu`, `_start_combat` y `_end_combat`) y `engine/social/hunting.py` (las cuentas de la partida). Números: `content/balance.yaml` → `hunt`. Textos: `hunt.*` en `content/locales/es.yaml`. Pruebas: `tests/test_hunt.py`. Registro de balance: [Balance](../03-personaje/balance.md) §7.

**De dónde sale.** Cazar monstruos en la zona es el bucle más viejo de los juegos de rol en línea, también en los de texto de Telegram como *Chat Wars*. El bono por compañero viene de los MMORPG clásicos (*Lineage II*, *Ragnarok Online*) que dan más experiencia al cazar en grupo; la cuenta común, de las cacerías en grupo de *Monster Hunter*.

---

## 1. El bucle de una cacería

```
CONTRATO ──> RASTREO ──> ACECHO ──> COMBATE ──> DESPIECE ──> TROFEO
(tablón,     (huellas,    (cebo,     (romper     (calidad    (bestiario,
 rumor,       rastros,     trampa,    partes,     de la       sala de
 avistamiento) clima)      emboscada) capturar)   pieza)      trofeos)
```

1. **Contrato.** Del tablón del asentamiento, de un rumor en la taberna, de un avistamiento en el chat de la región o de un encargo de otro jugador.
2. **Rastreo.** Recorres los nodos de la región siguiendo **rastros**: huellas, sangre, restos de comida, ramas rotas, olor. Cada rastro dice algo: hacia dónde fue, hace cuánto, si está herida. El clima borra rastros (la lluvia los borra rápido) y la noche los esconde.
3. **Acecho.** Cuando la encuentras, eliges cómo empezar: **emboscada** (ataque sorpresa, si tu sigilo gana), **cebo** (la atraes a un nodo que tú elegiste), **trampa** (colocada antes) o **de frente**.
4. **Combate.** Con el combate normal (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)), pero la presa **huye** si se asusta o si está herida, y hay que seguirla. Romper partes cambia qué deja.
5. **Despiece.** Desuello y caza (ver [Profesiones](../07-economia/profesiones.md)) decide cuánto se aprovecha y con qué calidad.
6. **Trofeo.** La pieza va al Bestiario, y la cabeza o el cuerno pueden ir a tu sala de trofeos.

## 2. Formatos de cacería

| Formato | Para quién | Cómo es | Qué da |
|---|---|---|---|
| **Contrato del tablón** | Solo o grupo de 2 a 4 | Presa concreta con recompensa en oro y reputación. Rotan cada día | Oro, reputación, materiales |
| **Presa (estilo Prey)** | Solo | Un objetivo marcado en tres dificultades: Normal, Difícil y Pesadilla. En Pesadilla la presa **también te caza a ti**: puede emboscarte mientras exploras | Materiales raros, cosméticos de cazador |
| **Caza mayor** | Grupo de 2 a 5 | Monstruos grandes con muchas partes rompibles, estilo Monster Hunter | Materiales de partes para equipo temático |
| **Bestia legendaria** | Grupo; a veces el servidor entero la persigue | Una por anillo y por temporada: una criatura única con nombre ("el Ciervo de Ceniza de Lejanía 17"). Aparece, se mueve por la región, deja rastros y desaparece si nadie la caza | Un trofeo único en el servidor y un título |
| **Caza nocturna** | Solo o grupo | Presas que solo salen de noche (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)); con farol o con un Elfo Sombrío en el grupo | Materiales nocturnos |
| **Trampero** | Solo, juego pasivo | Colocas trampas en nodos y vuelves horas después a ver qué cayó. A veces cae algo que no esperabas, y a veces un jugador te roba la trampa en zona roja | Pieles y materiales básicos |
| **Captura viva** | Solo o grupo | Debilitar sin matar, y usar red, sedante o jaula. La presa capturada sirve para **doma** (monturas, mascotas de combate) o se vende a un criador | Monturas, mascotas, cría |
| **Cacería de plaga** | Grupo | Durante una epidemia, cazar a las criaturas portadoras frena el contagio (ver [Enfermedades](../05-salud/enfermedades.md)) | Reputación de sanador, materiales para la cura |
| **Temporada de caza** | Todos | Evento por estación: una especie se multiplica y el tablón paga el doble por ella. Si se sobrecaza, escasea la temporada siguiente | Ranking de cazadores |
| **Caza de licántropos y vampiros** | Grupo | Presas que son jugadores o PNJ malditos (ver [Enfermedades](../05-salud/enfermedades.md)). Con PNJ es PvE; con jugadores malditos, solo con consentimiento o en PvP | Plata bendita, reputación |
| **Recompensas por jugadores** | PvP | Ver [PvP](pvp.md) (cazarrecompensas y karma) | Oro |

## 3. Calidad de la pieza

**De dónde sale.** *Red Dead Redemption 2*: una piel de tres estrellas vale mucho más que una rota por un escopetazo.

- Cada pieza tiene una **calidad** (de una a tres estrellas) que depende de:
  - **cómo la mataste:** con el arma adecuada y sin destrozar el cuerpo; un golpe limpio a la cabeza con arco da la mejor piel;
  - **qué partes rompiste:** romper la cola da el material de la cola, pero la piel sale peor;
  - **tu nivel de Desuello.**
- Las piezas de tres estrellas son las que piden las recetas de equipo excelente (ver [Fabricación](../07-economia/fabricacion.md)).

**Por qué conviene.** No gana el que pega más fuerte sino el que caza mejor. Es una habilidad propia.

## 4. Herramientas del cazador

| Herramienta | Qué hace | Quién la fabrica |
|---|---|---|
| **Cebos** | Atraen a una especie a un nodo | Cocina, Alquimia |
| **Trampas** (cepo, red, foso) | Inmovilizan, dañan o capturan | Herrería, Carpintería, Ingeniería |
| **Sedantes y venenos de caza** | Capturar vivo, debilitar | Alquimia |
| **Silbato de rastreo** | Revela el rastro más fresco | Carpintería |
| **Farol de caza** | Permite rastrear de noche | Herrería |
| **Capa de camuflaje** | Mejora la emboscada | Sastrería |

El Cazador (la clase) y los linajes Licántropo (olfato, rastreo) y Elfo Sombrío (visión nocturna) tienen ventajas propias, pero **cualquiera puede cazar**.

## 5. Bestiario y conocimiento

- Cada especie cazada suma al **Bestiario**: hábitat, horario, debilidades, partes rompibles, qué deja cada parte.
- Cazar varias veces la misma especie sube tu **conocimiento** de ella: rastros más claros, más probabilidad de pieza de tres estrellas, ves cuándo está por huir.
- Las fichas de caza se pueden vender (ver el Informante en [Profesiones](../07-economia/profesiones.md)).

## 6. Ecología: cazar cambia el mundo

- Cazar baja la población de una especie en la región (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)). Si se sobrecaza, escasea y su material sube de precio. Si nadie la caza, crece e invade zonas seguras.
- Los depredadores siguen a sus presas: sobrecazar ciervos hace que los lobos bajen al asentamiento (y eso se convierte en evento).
- **El tablón paga más por las especies que sobran** y deja de pagar por las que escasean.

## 7. Rangos de cazador

Un camino de reputación propio con la **Orden de Cazadores**:

| Rango | Qué abre |
|---|---|
| Rastreador | Contratos básicos, trampas simples |
| Montero | Caza mayor, cebos avanzados |
| Batidor | Presas en dificultad Difícil, captura viva |
| Cazador Mayor | Presas en Pesadilla, bestias legendarias |
| Leyenda de la Lejanía | Título, apariencia de cazador, tu nombre en la sala de trofeos de la Orden |

## 8. Cómo se ve en Telegram

```
🐾 Cacería — Wyrm Joven de las Dunas (Difícil)
Lejanía 13 · Desierto Ardiente · 🌙 Noche · Viento del sur

Rastro: surcos profundos en la arena, todavía tibios.
Fue hacia el Oasis Seco hace menos de una hora.
Está herido (manchas de sangre oscura).

[👣 Seguir el rastro]   [🪤 Poner trampa aquí]
[🍖 Dejar cebo]         [🗺 Ver mapa]
```
