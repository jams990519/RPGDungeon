# Hoja de ruta

> **Módulo** [00 · Visión](README.md) · **Estado:** propuesta

**Reglas fijas:** no se escribe código hasta que el dueño lo diga (D-04). No se toca Railway (D-03). No se toca TowerWars (D-01). El juego se monta en @LostRealmsbot (D-02).

---

## 0. El alcance es enorme: cómo no ahogarse

Este diseño describe un juego de años. Construirlo entero antes de que alguien juegue sería un error. La estrategia:

1. **El núcleo primero:** lo que hace único al juego debe estar en la alfa. Eso es la fundación desde cero, el combate por turnos con avisos, el cuerpo que se hiere y los oficios que se estudian.
2. **Todo es un módulo que se enchufa** (ver [Arquitectura](../01-plataforma/arquitectura-modular.md)): cada fase agrega módulos sin reescribir los anteriores.
3. **Las clases y los anillos llegan como en WoW:** por expansiones.
4. **Cada fase se juega con gente real** antes de pasar a la siguiente.

## 1. Fases

### Fase 0 · Diseño (ahora)
- Cerrar las [Preguntas abiertas](preguntas-abiertas.md).
- Elegir el alcance exacto de la alfa.
- Definir tecnología y presupuesto (P-46, P-47).

### Fase 1 · Cimientos técnicos (sin jugadores)
- Núcleo: tiempo, azar con semilla, eventos, idiomas (ES/EN).
- Héroe, linajes y trasfondos.
- Motor de combate por rondas en solitario, con avisos, Aguante, Firmeza, postura y Tácticas.
- Contenido como datos (biomas, jefes, recetas).
- Simulador de balance básico.
- Herramientas de administración (radiografías).
- Adaptador de Telegram mínimo, **preparado** para @LostRealmsbot (no se despliega hasta que el dueño lo diga).

### Fase 2 · Alfa cerrada: "El Claro"
El núcleo que hace único al juego, con pocos jugadores:
- **Fundación desde cero** junto al Claro: del Claro a la Aldea, con las necesidades de la ciudad.
- Recolección: minería, tala, herboristería, caza, **agricultura** y ganadería, con refinado.
- Oficios: Carpintería, Herrería, **Construcción**, **Medicina**, Cocina, con entrenadores PNJ y exámenes.
- Construcción por jornadas con minijuego y paga; casa propia con taller.
- Heridas v1 (7 zonas, 5 tipos) y curación básica.
- 4 clases: Guerrero, Mago, Sacerdote, Pícaro (tanque, daño a distancia, sanador, daño cuerpo a cuerpo).
- Lejanía 1 y 2, con el Guardián de la primera región.
- Mercado con libro de órdenes, encargos, expediciones.
- Dados de taberna.

### Fase 3 · Beta abierta
- Las **9 clases** del lanzamiento.
- Todo el anillo I (Lejanía 1-3), con **la Frontera** y banda del anillo I.
- Mazmorras con buscador de grupos; Profundidades con compañero.
- Curación completa con cirugía; enfermedades v1; estrés.
- **Cacerías**, **investigaciones** (casos rápidos y de la región), **apuestas legales**.
- Zonas amarillas y rojas, karma, arena asíncrona.
- Gobierno de la ciudad (Villa); **propiedad y concesiones** con pujas y tasas.
- **Crisis** básicas: hambruna, incendio, incursión.
- Crimen básico: carterismo, perista, guardia, recompensas.

### Fase 4 · Lanzamiento (1.0)
- Anillos II y III, con **la primera Gran Barrera** (propuesta, al final del anillo III).
- El primer **Castillo** completo con sus alas: entrenadores de rango alto, la Fortuna, sanatorio, prisión.
- **Cisma** habilitado → **guerra de castillos**.
- Bandas por anillo, Mítica+ temporada 1, arenas en vivo, campos de batalla.
- Apuestas ilegales, crimen y justicia con tribunal, defensa de construcciones.
- Rasgos adquiridos, salud de animales y cultivos, Juramento de Hierro.
- Monetización cosmética y Premium de comodidad.
- Del catálogo ampliado: termas, museo, vino que se añeja, mapas del tesoro, libros de jugadores, torneos de oficio.

### Expansiones (cada 4 a 6 meses)

| Expansión | Clase nueva | Anillo | Sistemas grandes |
|---|---|---|---|
| **E1** | Caballero de la Muerte | IV (Pantano) | Zonas negras, territorios y fortalezas, asedios, panteón de dioses, epidemias de servidor, espionaje, idiomas antiguos |
| **E2** | Monje | V (Desierto, **Gran Barrera**) | Talentos de héroe, liga de pelota, justas, música compuesta, linaje familiar |
| **E3** | Cazador de Demonios | VI (Picos Helados) | Clima extremo completo, vampirismo y licantropía |
| **E4** | Evocador | VII (Ruinas y costas) | Barcos, rutas marítimas, piratería, arqueología mayor |
| **E5** | Nigromante | VIII (Ciudadela, **Gran Barrera**) | Corrupción, Pesadillas mayores |
| **E6** | Bardo | IX (Abismo) | Cordura, el Gran Misterio de la Lejanía |
| **Final** | — | X (Jardines) y la Lejanía profunda | El cierre de la primera era |

Con este ritmo, la primera era dura entre 2 y 4 años.

## 2. El producto mínimo que ya sería distinto

Si hubiera que elegir lo más chico que ya se sienta como este juego:
1. Un Claro vacío que la gente convierte en aldea entre todos.
2. Combate por turnos con avisos de jefe al estilo Elden Ring.
3. Heridas por zona que curan médicos que estudiaron.
4. Tres oficios con profundidad real (Carpintería, Construcción, Medicina).
5. El Guardián de la primera región.

Eso solo ya no existe en ningún juego de Telegram.

## 3. Riesgos

| Riesgo | Cómo se enfrenta |
|---|---|
| **Alcance** (muy grande para un equipo chico) | Fases, módulos, producto mínimo |
| **Límites de Telegram** | Mensaje vivo, rondas, lotes de eventos (ver [Telegram](../01-plataforma/telegram.md)) |
| **Balance de 46 specs** | Lanzamiento escalonado, simulador, registro de balance |
| **Bots y multicuentas** | Diseño sin nada que farmear pulsando, retos contextuales (ver [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md)) |
| **Costos del servidor** | Definir presupuesto antes de la alfa; base de datos que aguante concurrencia |
| **Comunidad y moderación** | Moderadores voluntarios, plantillas, herramientas |
| **Nombres y propiedad intelectual** | Mundo propio (ver [Referencias](../99-referencias/referencias.md)) |
| **Economía que se rompe** | Sumideros en porcentaje, informe mensual, palancas de ajuste |

## 4. Reglas de trabajo (heredadas de TowerWars)

- Antes de cada subida: correr las pruebas **y** arrancar el bot.
- Todo número de balance que se mueve va al registro, con su antes → después y la medición.
- Notas de versión en idioma de resultado, en español y en inglés.
- Credenciales: nombres de variables sí, valores jamás.
- Nada en Railway sin permiso del dueño.
