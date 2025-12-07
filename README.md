# VAQUEROMON  
### A LAN-Based Turn Combat Game

Vaqueromon es un juego de combate por turnos inspirado en mecánicas clásicas de RPG, diseñado para funcionar mediante **conexiones LAN**.  
Dos jugadores pueden unirse a una partida generando un número de sala (*Room Number*) y conectándose mediante la dirección IP del host.

---

## Características Principales

- **Batallas LAN en tiempo real** usando sockets TCP.  
- **Selección de equipo**: cada jugador elige 4 Vaqueromons.  
- **Sistema de combate por turnos** sincronizado entre host y cliente.  
- **Animaciones de ataque** y UI personalizada.  
- **Efectos de sonido y música ambiental**.  
- **Sprites personalizados** (front/back) para cada Vaqueromon.

---

## Cómo Funciona la Conexión

1. El host inicia una sala ingresando un número de 4 dígitos.  
2. Se genera un puerto dinámico basado en ese número.  
3. El cliente ingresa el mismo número y escribe la IP del host.  
4. Ambos jugadores seleccionan sus Vaqueromons.  
5. Comienza la batalla sincronizada por TCP.

La comunicación usa un protocolo propio basado en JSON, asegurando que cada mensaje llegue completo y en orden.
