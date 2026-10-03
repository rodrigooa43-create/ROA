# Replay: ver la grabación como una animación

> Manual del Usuario → Capítulo "Revisar una grabación" → nueva sección "Replay" (después de "Informe PDF").

Al abrir una grabación de **músculos**, **corazón** u **ojos**, el botón
**▶ Reproducción** queda disponible (queda desactivado para grabaciones de
cerebro). Abre una ventana con un reproductor común a los tres exámenes:
**▶ Reproducir / ⏸ Pausar**, **⏮ Inicio**, la línea de tiempo arrastrable y
el reloj "0:05 / 0:30". En el Completo hay también la velocidad (0,25× a 4×)
y *Repetir*.

> La animación **simula** lo que se grabó: no es el vídeo de la persona, y no
> es informe ni diagnóstico. El sello en lo alto de la ventana lo repite.

## Músculos

Una figura articulada vista de lado (tronco, hombro, codo, antebrazo, muñeca,
mano con dedos) rehace el **movimiento marcado** en la línea de tiempo, y
cada músculo se enciende con la intensidad medida en ese instante. La
supinación y la pronación son inconfundibles: la palma clara vuelta hacia
arriba o el dorso vuelto hacia abajo, con el texto "palma hacia arriba/abajo".

La línea de tiempo (2 a 4 pistas) nace de los **marcadores y fases** de la
grabación ("Flexión", "Extensión", "Reposo"…); sin marcador, las
**contracciones detectadas** se convierten en tramos "por definir". Las
pistas en el mismo instante se **suman** (por ejemplo, cerrar la mano
mientras el codo se flexiona). Movimientos disponibles: flexión y extensión
de codo, supinación, pronación, flexión y extensión de muñeca, abrir y cerrar
la mano, pinza, flexión y extensión de hombro, reposo.

En el **Simple** usted ve el reproductor, la figura y la lista de tramos. En
el **Completo** la línea de tiempo es editable: arrastre un bloque para
moverlo, tire del borde para estirarlo, haga clic derecho para *Cambiar el
movimiento*, *Dividir aquí*, *Borrar*, *Añadir pista/Eliminar pista*; Ctrl+Z
deshace. *Tarea predefinida* inserta, a partir del cursor, una secuencia con
el objeto agarrado con la mano: **levantar la mancuerna**, **abrir/cerrar la
puerta con la llave**, **tomar el vaso de la mesa y llevarlo a la boca**.
Cuando los músculos activos no coinciden con el movimiento elegido (por
ejemplo, tríceps activo en un tramo de flexión), aparece un aviso. *Guardar*
graba `movimentos.json` junto a la grabación; el programa pregunta si hay
marcas sin guardar al cerrar.

## Corazón

Un corazón dibujado **late al ritmo grabado**, junto al trazado con el cursor
y a los latidos por minuto. La franja de abajo muestra **todos** los latidos:
el regular es un trazo fino; el **latido adelantado** es un triángulo
naranja; la **pausa mayor** es un rectángulo hueco rojo (color y forma, para
quien no distingue colores). La lista en palabras ("0:13 latido adelantado",
"0:25 pausa mayor (1,7 s)") se puede pulsar y lleva el reproductor hasta ahí.
Los latidos son los mismos del informe PDF. En el Completo, el clic derecho
en la franja permite **corregir** (eliminar latido, añadir latido aquí,
marcar como regular / adelantado / pausa mayor); *Guardar* graba
`batidas.json`.

## Ojos

Dos ojos dibujados **parpadean en los parpadeos y miran** hacia donde mandan
las señales. *Invertir horizontal* e *Invertir vertical* intercambian los
lados, por si los electrodos se colocaron al revés. La línea de tiempo dice
en palabras lo que ocurrió ("0:03 parpadeó", "0:05 miró a la derecha") y los
contadores suman parpadeos y movimientos hacia los lados y hacia arriba/abajo.
En el Completo, el clic derecho en la lista elimina un evento o cambia la
dirección; *Guardar* graba `olhos.json`.
