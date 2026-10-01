"""M10 Missions: story and roleplay, simple layer (D-117, provisional).

[ES]
Para qué sirve: la historia y el rol del juego (capa simple): orígenes del héroe con su cadena de misiones, la
campaña por capítulos (el Capítulo 1 en el Claro), personajes con nombre, tres facciones con reputación, encargos
del tablón (diarios) y del campamento (semanales), el diario del héroe y los gestos entre jugadores. Aquí están las
cuentas puras (rules.py); las pantallas y el guardado están en engine/service/story.py; la historia en sí (misiones,
personajes, facciones, encargos) en content/story.yaml y sus textos en content/locales/es_historia.yaml.
Documento de diseño: diseno/06-contenido/historia-y-rol.md
Módulo: M10 Misiones
Depende de: engine.core (sorteo fijo)
Lo usan: engine/service/story.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. La historia nunca da poder de combate por sí sola: rasgos de origen y premios son de oficio, monedas,
       consumibles, materiales, reputación y títulos.
Si cambias esto, revisa:
    - Servicio: engine/service/story.py
    - Pruebas: tests/test_story.py
"""

from engine.story.rules import EVENT_GOALS, STATE_GOALS, amount, clean_text, daily_pick, matches, rank_index, rank_position, target, weekly_pick

__all__ = ["EVENT_GOALS", "STATE_GOALS", "amount", "clean_text", "daily_pick", "matches", "rank_index", "rank_position", "target", "weekly_pick"]
