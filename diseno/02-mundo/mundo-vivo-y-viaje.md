# Mundo vivo y viaje

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Mapa infinito y viaje](mapa-infinito-y-viaje.md) · **Alimenta a:** [Economía](../07-economia/economia.md), [Salud](../05-salud/README.md), [Profesiones](../07-economia/profesiones.md) · **Estado:** propuesta; §2 en parte en el juego desde la 0.58 (el reloj del mundo, los recursos por franja y la zona horaria de cada jugador: D-334, provisional)

---

## 1. Moverse por el mapa

Ya no hay Torre ni pisos (D-58): el mundo es un mapa sin borde y moverse entre zonas toma tiempo real. Cómo funciona el viaje hoy (v0.1) y lo que viene por parches (caminos, monturas, postas, carga, eventos del camino, sin teletransporte) está en [El mapa infinito y el viaje](mapa-infinito-y-viaje.md).

## 2. Día y noche

> **Manda D-239.9 (confirmada):** un día del mundo dura **4 días reales**, no las 6 horas que decía este documento antes (era la recomendación vieja de P-11). Con 24 horas o con un múltiplo de ellas, quien juega siempre a la misma hora vería siempre la misma franja; con 96 horas, cada franja dura 32 y se ven las tres (P-86).

### 2.0 En el juego (0.58: D-126 y D-239.9 confirmadas; cómo se aplicó: D-334, provisional)

- **El reloj del mundo:** un día del mundo dura 96 horas reales (`content/balance.yaml` → `world_clock.day_hours`) y empieza en un instante fijo (`world_clock.anchor`: el 20-oct-2026 a las 05:00 UTC). Se parte en tres franjas iguales de 32 horas: ☀️ **día**, 🌇 **tarde** y 🌙 **noche** (`world_clock.bands`). Es una cuenta sobre la hora: no guarda nada y es la misma para todos en el mismo momento, viva donde viva cada uno (D-124). Quien juega todos los días a la misma hora ve las tres en 4 días.
- **Se ve en 📍 Zona**, en la 4.ª línea: "🌇 Es de tarde en el mundo · 🌙 la noche llega en 31 h 14 min (🕐 18:00)". La duración es igual para todos; la hora sale en la zona horaria de cada uno (§2.1). También en la pantalla 🕐 Zona horaria y en ❓ /d05.
- **Cada franja da recursos un poco distintos** (D-126: "cada franja del día da recursos distintos"). Al 🧺 recolectar, el peso de algunos recursos en el sorteo de cada vuelta se multiplica según la franja (`world_clock.weights`); los hallazgos de 🔎 Explorar también (la 🌿 hierba curativa pesa más de noche):

  | Franja | Sale más | Por qué |
  |---|---|---|
  | ☀️ Día | 🪵 madera y 🪨 piedra ×1,25; fibra, lino, mazorca y miel ×1,2; arcilla, bayas, dátiles y sal ×1,15; metal ×1,1 | Lo que se trabaja con luz y lo que crece al sol |
  | 🌇 Tarde | Lo de siempre (la mezcla de antes de la 0.58) | La franja de paso |
  | 🌙 Noche | 🌿 hierba curativa, setas, musgo y 🐟 pescado ×1,3; raíz amarga, nenúfar y flor de escarcha ×1,25; resina ×1,15 | Lo que crece en la sombra y la pesca nocturna |

  Cambia **la mezcla**, nunca cuántas unidades da una vuelta, y ningún peso baja de ×0,5 (`min_weight`): ningún recurso desaparece y nadie está obligado a jugar a una hora. 🪓 Talar y 🎣 Pescar (un solo recurso) rinden igual. 🧭 Explorar dice qué recursos conocidos de la zona salen más ahora ("🌙 De noche, al 🧺 recolectar aquí sale más: 🌿 Hierba curativa").
- **La noche de los 🔥 Braseros** es la 🌙 noche del mundo (`raids.night.source: world`), como decía D-126: la oleada que llega de noche cuenta 1 punto más de 🛡️ Defensa, y el aviso lo dice ("🌙 Es de noche en el mundo: los 🔥 Braseros suman +1 de 🛡️ Defensa"). Antes contaba de 19 a 6 en UTC−5 (la noche de América, 11 horas de cada 24); ahora un tercio del tiempo, igual para todas las zonas horarias. El ritmo de las oleadas (3 por semana), las 🌊 oleadas crecientes del castillo (D-329) y las oleadas ya abiertas no cambian. Con `source: fixed` vuelven las horas de antes (E-277).
- **Todavía no:** que la franja cambie el peligro y el botín (E-64, P-87: de noche, enemigos más fuertes con mejor botín), los monstruos, hierbas y jefes que salen solo de noche y la visión del Elfo Sombrío (abajo). Los monstruos de hoy no cambian con la franja.
- Código: `engine/world/world_clock.py` (la franja y los pesos) y `engine/service/world_time.py` (lo que se ve); los ganchos en `engine/service/game.py` (`_zone_view`, `_explore_menu`, `_gather_step`, `_explore_step`, `_is_night`, `_raid_notice`). Pruebas: `tests/test_zona_horaria_y_dia.py`. Preguntas: E-276 (P-287) y E-277 (P-288).

**De dónde sale.** El día y la noche que cambian lo que hay afuera (*Don't Starve*, *Valheim*, *Minecraft*); el día más largo que el real para que nadie quede siempre en la misma franja (la recomendación de P-86, que confirmó D-239.9).

### 2.1 La zona horaria de cada jugador (0.58: D-124 confirmada; cómo se aplicó: D-334, provisional)

- **D-124:** "Cada jugador elige su zona horaria para ver las horas, pero los horarios de combate y de eventos son los mismos para todos."
- **Dónde:** ⚙️ Opciones → 🕐 Zona horaria (también /hora y /time). Siete zonas de un toque (🇲🇽 México y Centroamérica, 🇨🇴 Colombia, Perú, Ecuador, 🇻🇪 Venezuela, Bolivia, Caribe, 🇨🇱 Chile, 🇦🇷 Argentina, Uruguay, Paraguay, 🇪🇸 España y 🇺🇸 EE. UU. este; las que tienen horario de verano lo siguen solas), 🌐 UTC y ➖ 1 h / ➕ 1 h para cualquier hora entera de UTC−12 a UTC+14 (`content/balance.yaml` → `time_zones`). Cada zona de la pantalla muestra la hora que tiene ahora: se toca la que coincide con tu reloj.
- **Qué cambia:** solo cómo se ven las horas. Junto a las duraciones ("en 40 min", que no cambian) el juego dice a qué hora en tu zona: cuándo cambian el 📜 Tablón y los encargos del campamento, cuándo termina el lote o el viaje, hasta cuándo dura una oleada y cuándo llega (🗼 Torre de vigía), cuándo vence una orden del 🏛️ Mercado, cuándo termina una obra en ⏫ Siguiente nivel y cuándo cambia la franja del mundo; si no es hoy, con la fecha ("23/10 14:32"). La fecha del 📔 Diario también sale en tu zona. Cada aviso a otro jugador llega con su hora.
- **Qué no cambia:** las reglas. El corte del día (medianoche UTC), las oleadas, el mercado, la noche de los Braseros y el reloj del mundo son los mismos para todos. El motor no sabe desde qué país ni desde qué cliente juega nadie (D-40, D-41): la zona la elige cada uno.
- **Quien nunca eligió** ve **UTC**, la hora que el juego ya usaba, con la etiqueta "UTC" al lado de cada hora (E-275, P-286: cuando el dueño diga dónde vive la mayoría de sus jugadores, esa zona puede pasar a ser la de por defecto).
- Se guarda por jugador en el espacio `prefs` (campo `tz`, junto al idioma). Código: `engine/core/timezones.py` y `engine/service/world_time.py`. El informe diario y el chat de 💬 Feedback, que son del equipo, siguen en UTC.

### 2.2 Lo que sigue siendo propuesta

- De noche salen otros monstruos, algunas hierbas solo se cosechan de noche y algunos jefes de campo solo aparecen a esa hora.
- El Elfo Sombrío ve de noche; los demás tienen menos precisión en zonas sin luz, salvo que lleven antorcha o farol.

## 3. Clima

Cada región tiene su clima, que se anuncia en el asentamiento y cambia cada pocas horas:

| Clima | Efecto |
|---|---|
| Lluvia | Suben las enfermedades de pantano; el fuego pierde fuerza |
| Niebla | Baja la precisión a distancia; más emboscadas |
| Tormenta | Caen rayos en zonas abiertas (avisados como un ataque de jefe) |
| Ventisca | Frío (ver [Condiciones](../05-salud/condiciones.md)) |
| Ola de calor | Deshidratación, aguante máximo más bajo |
| Cielo despejado | Mejor visibilidad, cosecha abundante |

## 4. Estaciones

Cada semana real avanza una estación en todo el mundo.
- **Invierno:** sube la gripe y bajan las hierbas.
- **Verano:** sube la fiebre del pantano.
- **Primavera:** vuelven las migraciones.
- **Otoño:** llegan las cosechas grandes y el festival de difuntos.

Las estaciones también cambian qué se pesca, qué se caza y qué se cultiva.

## 5. Ecología

- Cada especie de monstruo tiene una **población por región**.
- Si se sobrecaza, escasea y sus materiales suben de precio. Si nadie la caza, crece, invade las zonas azules y se convierte en evento.
- Los depredadores migran detrás de su presa.
- Origen: los simuladores de ecosistema (Dwarf Fortress) y la escasez de recursos de Albion.

**Por qué conviene.** El mundo reacciona a lo que hacen los jugadores. El precio de la piel de lobo cuenta una historia: cuando está alta, alguien se pasó cazando.

## 6. Vetas y cosechas que se mueven

Los recursos no están siempre en el mismo nodo. Las **vetas** (minerales, hierbas, maderas) aparecen, se agotan y reaparecen en otro lado, y cada una tiene **calidad propia** (ver [Fabricación](../07-economia/fabricacion.md)). Encontrar una veta excelente es una noticia que vale oro, y se vende (el Cartógrafo y el Informante viven de esto).

## 7. Rumores y secretos

- En las tabernas circulan **rumores**: frases que insinúan algo sin decirlo ("*dicen que el curtidor recibe visitas de noche*", "*un cazador vio una cueva detrás de la cascada de la Hondonada Gris*").
- Algunos son falsos. Los verdaderos llevan a **secretos**: jefes ocultos, vetas raras, pasadizos, mapas del tesoro y **oficios secretos**.
- **Oficios secretos:** el oficio de Robo, el Contrabando, la Falsificación y los venenos prohibidos no los enseña ningún entrenador a la vista. Un entrenador puede **insinuarlo**, y el jugador tiene que seguir el rumor hasta encontrar al Gremio de Ladrones o al maestro que se lo enseñe (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)).
- Los rumores se compran a los taberneros y a los informantes, y se pueden vender.

## 8. Eventos del mundo

Invasiones, eclipses, migraciones y epidemias: ver [Eventos](../06-contenido/eventos.md).
