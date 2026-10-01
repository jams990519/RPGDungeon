"""Pure game engine: rules only, no client code.

The engine never imports Telegram, web or mobile code. Clients send commands
and receive neutral views (engine.messaging).

[ES]
Para qué sirve: es el motor del juego; aquí viven todas las reglas.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §1
Módulo: todos (cada subpaquete es un módulo M1-M25)
Depende de: ninguno (solo la biblioteca estándar y PyYAML para leer contenido)
Lo usan: adapters/telegram, adapters/cli, tests
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. El motor no sabe que existe Telegram, la web ni la app (D-40, D-41).
Si cambias esto, revisa:
    - Adaptadores: adapters/ — importan desde engine.service
    - Pruebas: tests/
"""
