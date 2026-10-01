# Fabricación: el minijuego, la calidad y los planos

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Profesiones](profesiones.md), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (vetas) · **Alimenta a:** [Equipamiento](../03-personaje/equipamiento.md) · **Estado:** propuesta

---

## 1. Dos formas de fabricar

| Modo | Cómo | Techo de calidad | Para qué |
|---|---|---|---|
| **Manual** | Un minijuego por turnos (§2) | Obra Maestra | Piezas importantes, pedidos, obras maestras |
| **Rápida** | Un botón; se resuelve con tu nivel y tu maestría | Notable | Cantidad: 50 vendas, 20 lingotes, pociones comunes |

**Por qué las dos.** El minijuego premia la habilidad y hace que fabricar sea jugar. La fabricación rápida respeta el tiempo de quien necesita volumen. Es el mismo principio que las [Tácticas](../04-combate/avisos-y-tacticas.md) en el combate.

## 2. El minijuego

**De dónde sale.** *Final Fantasy XIV*: cada fabricación tiene **Progreso**, **Calidad**, **Durabilidad**, **Puntos de Artesanía** y una **Condición** que cambia en cada paso (Normal, Buena, Excelente, Pobre). Cada acción gasta durabilidad; si llega a 0 sin completar el progreso, se pierden los materiales. Ya es un juego por turnos, así que encaja perfecto en Telegram.

**Las barras:**
- **Progreso:** cuando se llena, el objeto está hecho.
- **Calidad:** decide si sale Normal, Buena, Notable, Excelente u Obra Maestra.
- **Durabilidad:** cada acción la gasta; si llega a 0 antes de terminar, se pierden los materiales.
- **Puntos de Artesanía (PA):** el recurso para las acciones especiales. Salen de tu nivel y tu equipo de oficio.
- **Condición:** cambia al azar en cada paso. *Buena* y *Excelente* multiplican la calidad; *Pobre* la reduce.

**Acciones** (máximo 8 botones, como en el combate):

| Acción | Efecto | Costo |
|---|---|---|
| Síntesis firme | +Progreso | Durabilidad |
| Toque básico | +Calidad | Durabilidad, pocos PA |
| Toque preciso | +Calidad grande; solo con condición Buena o Excelente | Durabilidad, PA |
| Manipulación | Recupera durabilidad durante varios pasos | PA |
| Veneración | +50 % de progreso durante 4 pasos | PA |
| Innovación | +50 % de calidad durante 4 pasos | PA |
| Observar | No hace nada, pero permite ver la condición del paso siguiente | PA mínimos |
| Síntesis final | Termina el progreso de golpe; arriesgado si falta mucho | Mucha durabilidad |

Cada oficio agrega una o dos acciones propias. El herrero tiene *Templar* (la calidad sube más si el paso anterior fue un toque); el alquimista tiene *Destilar* (convierte progreso en calidad).

**Cómo se ve:**

```
⚒️ Forja — Espada Larga de Acero Estelar (T5)
Progreso  ▓▓▓▓▓▓░░░░  620/1.000
Calidad   ▓▓▓▓░░░░░░  1.840/4.500  → Notable
Durabilidad ●●●○○   PA 212/480
Condición: ✨ EXCELENTE

[🔨 Síntesis firme]   [✋ Toque básico]
[💎 Toque preciso]    [🔧 Manipulación]
[📈 Innovación]       [👁 Observar]
[⚡ Síntesis final]   [📜 Receta]
```

## 3. Calidad de los recursos: cada veta es distinta

**De dónde sale.** *Star Wars Galaxies*. Los recursos aparecían por temporadas con estadísticas al azar, así que un lote servía para unas recetas y no para otras. Los artesanos rastreaban los mejores lotes y los guardaban.

**Cómo funciona.**
- Cada veta, planta o criatura da materiales con **atributos**: Pureza, Dureza, Flexibilidad, Conductividad, Resonancia.
- Cada receta pondera atributos distintos. A una espada le importan la Dureza y la Flexibilidad; a una varita, la Conductividad y la Resonancia.
- Las vetas **rotan** por los pisos cada semana (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)).
- **Prospectar** muestra los atributos de una veta; el Enano los ve sin prospectar.
- Los materiales conservan sus atributos al refinarse (un lingote de mineral de pureza 870 es un lingote de pureza 870).

**Por qué conviene.** No todo el hierro es igual. Una veta excelente es noticia, se vende información sobre ella y los lotes buenos se especulan. Esto da profundidad durante años sin inventar materiales nuevos.

## 4. Recetas

| Fuente | Ejemplo |
|---|---|
| Entrenador del asentamiento | Recetas básicas de cada tramo |
| Reputación | Recetas de facción y de órdenes |
| Botín de jefes | Planos raros, piezas de artefacto |
| **Descubrimiento** | Combinar ingredientes sin receta y descubrir el resultado |
| Especialización | Recetas exclusivas de una rama |

**Descubrimiento** (*Skyrim* y *Guild Wars 2*). Cada ingrediente de alquimia y cocina tiene efectos ocultos. Combinarlos los revela, y a veces sale una receta nueva que queda registrada con tu nombre como descubridor. La primera persona del servidor que descubre una receta sale en la Gaceta.

**Experimentación** (*Star Wars Galaxies*). Al fabricar manualmente en rango Maestro, puedes repartir unos pocos puntos de experimentación para inclinar el objeto: más daño y menos durabilidad, o más protección de zona y más peso.

## 5. Planos e investigación

**De dónde sale.** *EVE Online*: los planos se investigan para gastar menos material y tiempo, y se copian para vender copias con usos limitados.

- Las recetas de piezas importantes vienen como **planos**.
- Un plano se puede **investigar** (lleva días reales) para que gaste menos material y menos tiempo.
- Un plano investigado se puede **copiar**: la copia tiene 10 usos y se vende en el mercado.
- **Por qué conviene:** nace un mercado de conocimiento. El artesano que investigó a fondo un plano vive de vender copias.

## 6. Estaciones y ciudades

- Fabricar requiere una **estación**: forja, alambique, telar, mesa de cirugía. Las hay públicas en los asentamientos (con tasa de uso, un sumidero), en las casas y en los salones de gremio.
- **Cada capital tiene una especialidad** (como las ciudades de Albion): en una la herrería rinde un 15 % más de retorno de material, en otra la alquimia. Esto mueve a los artesanos y a los materiales entre ciudades.
- Las estaciones de gremio y de territorio pueden tener bonos propios (ver [PvP](../06-contenido/pvp.md), territorios).

## 7. Trabajadores

**De dónde sale.** Los trabajadores de *Black Desert* y los obreros de las islas de Albion.

- En tu casa o en el territorio de tu gremio puedes tener **trabajadores PNJ** que recolectan o refinan mientras no juegas, poco y lento.
- Se contratan, se alimentan (Cocina) y suben de nivel.
- Juego pasivo que se revisa en un toque: perfecto para Telegram.

## 8. Firma y obras maestras

- Todo objeto fabricado lleva la **firma del artesano**: "Forjada por Lisbeth la Herrera".
- Una **Obra Maestra** permite al artesano **ponerle nombre** al objeto ("*Susurro del Alba*"), y queda en un registro público de obras maestras del servidor.
- Los artesanos con más obras maestras aparecen en un ranking.

## 9. Desmontar y reciclar

- **Desmontar** equipo roto o viejo devuelve parte del material.
- **Desencantar** (Encantamiento) convierte objetos mágicos en esencias.
- **Reciclar** es también un sumidero: se devuelve menos de lo que costó.

## 10. Ejemplo completo: una espada larga T5

1. **Minería.** La minera Kira encuentra una veta de mineral estelar con pureza 870 y dureza 790 en las tierras salvajes del piso 44. Arriesga una zona roja para sacarlo.
2. **Fundición.** Vende el mineral al fundidor Tor, que lo convierte en lingotes (conservan los atributos).
3. **Curtiduría.** El curtidor Ansel vende cuero de wyrm para el mango.
4. **Pedido de fabricación.** El guerrero Bram compra los lingotes y el cuero y le manda un pedido a Lisbeth, Gran Maestra herrera con maestría alta en espadas largas, con una comisión.
5. **Minijuego.** Lisbeth forja a mano, aprovecha dos condiciones Excelentes y la espada sale **Excelente**.
6. **Encantamiento.** El encantador Vael infunde una runa y la deja en +2.
7. **Joyería.** La joyera Nim talla un rubí para el engarce.
8. **Uso.** Bram usa la espada seis semanas. La repara tres veces con Lisbeth (pierde poca durabilidad máxima) y una vez con un PNJ (pierde más).
9. **Final.** Bram la pierde en una zona negra. El que lo mató se la lleva y la vende. Bram vuelve a hacerle un pedido a Lisbeth.

En esa historia comieron siete jugadores, se quemó oro en impuestos y reparaciones, y el ciclo empieza de nuevo.
