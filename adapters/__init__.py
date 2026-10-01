"""Client adapters (Telegram, console) and storage implementations.

[ES]
Para qué sirve: lo que conecta el motor con el mundo: el bot de Telegram, la consola
de pruebas y el guardado en disco. Aquí sí puede haber aiogram; en el motor, nunca.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §2 (adaptadores)
Módulo: adaptadores
Depende de: engine.service
Lo usan: el proceso que arranca el bot
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Ningún adaptador agrega reglas de juego: solo traduce órdenes y dibuja vistas.
Si cambias esto, revisa:
    - Pruebas: tests/
"""
