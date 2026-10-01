# Ascendentes (nombre provisional)

**Un MMORPG por turnos y en texto.** Un solo motor y un solo mundo, con tres clientes: el bot de Telegram **@thetowerwarbot**, la web y una app móvil de texto.

- El mundo empieza tras el **Colapso**: todo fue destruido, hay comunidades de PNJ con reglas propias y los jugadores fundan y sostienen sus propios asentamientos hasta construir un castillo.
- Clases igualadas con roles variados (Ataque, Defensa, Curación, Soporte), combate de 6 botones y jefes difíciles pero justos.
- Un cuerpo que se hiere, se enferma y guarda secuelas; oficios profundos que se estudian; una economía de jugadores con lugares escasos; muchos roles para el roleplay.

## Estado

**Versión 0.1 jugable** (D-59): crear héroe (Guerrero, Pícaro o Sacerdote), explorar un mapa infinito donde viajar toma tiempo real, descubrir zonas y pelear por rondas con 6 botones. El resto del diseño se va abriendo por parches (D-60).

## Cómo probarlo

```bash
pip install -r requirements.txt pytest
python -m pytest            # pruebas del motor
python -m adapters.cli.play --fast   # jugar en la consola, con el tiempo acelerado
```

## Cómo desplegarlo en Railway (@thetowerwarbot)

1. **Borrar el juego viejo del bot:** en el proyecto de Railway donde corre hoy @thetowerwarbot, eliminar su servicio y su base de datos o volumen. **Solo el de @thetowerwarbot**, nunca el de TowerWars (@TowerWarsBot).
2. **Servicio nuevo:** desde el repositorio `jams990519/RPGDungeon` (rama `main`). El comando de arranque ya está en `railway.json`.
3. **Volumen:** montar uno en `/data` para que las partidas no se borren al reiniciar.
4. **Variables:** `TELEGRAM_BOT_TOKEN` = el token de @thetowerwarbot; `RPG_DB_PATH` = `/data/ascendentes.sqlite3`. La lista completa está en `.env.example`.

## Dónde está todo

- **Diseño completo:** [diseno/README.md](diseno/README.md), organizado por módulos.
- **Decisiones del dueño:** [diseno/00-vision/decisiones.md](diseno/00-vision/decisiones.md).
- **Preguntas abiertas:** [diseno/00-vision/preguntas-abiertas.md](diseno/00-vision/preguntas-abiertas.md).
- **Instrucciones para la IA que trabaje en el proyecto:** [CLAUDE.md](CLAUDE.md).

## Historia del repositorio

Este repositorio antes contenía un juego de mazmorras por consola (`RPG-0.1` a `RPG-0.9`). Por decisión del dueño, su contenido fue reemplazado por el juego nuevo. Esos archivos siguen en el historial de git por si se quieren recuperar.
