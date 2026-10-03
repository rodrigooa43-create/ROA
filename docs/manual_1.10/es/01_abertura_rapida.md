# Abrir el programa (pantalla de apertura)

> Manual del Usuario → Capítulo "Instalación y primera ejecución" → después de "Abrir el programa".

Al abrir el ROA aparece una pequeña pantalla con el logo y una línea de señal
dibujándose. Debajo de ella, en palabras, el programa dice lo que está
haciendo ("Cargando las bibliotecas…", "Montando la pantalla inicial…"). Esa
pantalla desaparece sola en cuanto la pantalla inicial está lista; no hace
falta hacer clic en nada.

**Primera apertura después de instalar o actualizar.** El programa se prepara
una vez (la pantalla dice "Preparando el programa por primera vez…") y guarda
el resultado en la carpeta `.roa_cache`, junto al programa. Las veces
siguientes la apertura es mucho más rápida. Si la carpeta del programa no
permite escritura (por ejemplo, en `Archivos de programa`), la caché va a la
carpeta del usuario (`%LOCALAPPDATA%\ROA\cache`). Borrar esa carpeta no causa
problemas: se rehace en la apertura siguiente.

**Si la pantalla de apertura estorba** (por ejemplo, en una automatización o
en un equipo con problemas de vídeo), abra el programa con la opción
`--sem-splash` o defina la variable de entorno `ROA_SEM_SPLASH=1`.

**Actualizaciones.** En *Ayuda → Buscar actualizaciones* el programa sigue
descargando solo su propio código, sin enviar nunca sus datos. A partir de
esta versión también puede actualizar el lanzador (`EEG_Data_Collector.py`)
cuando la actualización traiga una versión nueva de él; si no lo consigue,
avisa y el programa sigue funcionando con el lanzador actual.
