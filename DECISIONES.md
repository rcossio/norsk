# Estado y decisiones

Este archivo explica **por qué la app es como es**. El README explica los criterios;
este explica el origen de cada uno.

## Estado actual

| | |
|---|---|
| Vocabulario | 120 palabras, tres niveles anidados (25 / 61 / 120) |
| Frases | 1050 generadas, 50 plantillas, tope de 10% por plantilla |
| Audio | 3301 mp3: Piper normal y lento, más la voz de Google, 41 MB |
| Juegos | 10, más Reglas y la Lista |
| Dependencias | ninguna; un archivo HTML |
| Persistencia | ninguna; el nivel viaja en el hash de la URL |
| Externo | solo la pestaña Hablá (voz del navegador + Google) |

**Funciona:** todo lo listado, verificado en producción.
**Sabido y aceptado:** el contador de práctica se pierde al recargar; los endpoints
de Google no son oficiales y pueden caerse (hay respaldo local).
**Pendiente:** pasado, posesivos, niveles 250/500, diálogo de dos turnos.

---

## Solicitudes, en orden

Cada línea es una petición del usuario y lo que produjo. Las marcadas con ⚑ son
correcciones del usuario a errores del modelo.

### Contenido inicial

1. 50 palabras comunes ancladas a inglés, italiano, francés, portugués o castellano → método de anclas.
2. Las mismas separadas por comas, para pegar en un traductor.
3. Tabla de tres columnas: noruego, pronunciación, castellano → nace la estructura de datos.
4. 50 palabras más, orientadas a verbos, cortesía y viaje → vocabulario de 100.

### La app

5. Sitio con ~10 pestañas, un juego por pestaña, publicado en GitHub Pages → nace Ankeret.
6. Token entregado, repo `norsk`, hacerlo directamente.
7. No insistir con la seguridad del token → se deja de mencionar.
8. Audio con botón de play → 115 grabaciones con Piper, no TTS del navegador.

### Anclas propuestas por el usuario

9. *kjøtt* → chota, el pedazo de carne.
10. *trenger* → necesito una tregua.
11. *heter* → inglés *I hate*.
12. *spiser* → inglés *spice*.
13. *bor* → Boris la re vivía.
14. *kjøper* → sumar *shopper* al *cheap* existente.
15. *beklager* → tiré la cerveza *lager*.

Las anclas del usuario resultaron mejores que las del modelo. Por eso el README
las documenta como trabajo manual y no automatizable.

### Pronunciación

16. ¿*morgen* debería ser "morgn"? → se verifica: *morn* es correcto, no se cambia.
17. Pedido de revisar la escritura fonética, con la instrucción de **no tocar si hay dudas** → se corrigen solo dos: *gir* (yir se leería *shir* en rioplatense) y *penger*.
18. Idea de marcar las letras mudas → campo `sil`, en línea aparte para no romper la lectura de la fonética.
19. ⚑ *jeg* suena más "iei" que "iai" → correcto: el diptongo *ei* es [æi] y "jai" es el acento de extranjero típico. Se corrigen *jeg*, *hei* y *nei*.
20. ⚑ *sier* suena a "si" → se mide: el archivo tenía un artefacto de 0.4 s. Se regenera y se documenta que la *-er* es genuinamente débil.

### Ajustes de interfaz

21. En Elegí, botón de play en la pregunta.
22. En Escribí, esperar a que el usuario pulse Siguiente en vez de avanzar solo.
23. ⚑ En Pares se oyen dos voces → el mp3 se cortaba a sí mismo y el `AbortError` disparaba el sintetizador del navegador.
24. En Sonido, ocultar la transcripción tras un botón de revelado.
25. Eliminar el juego Ancla.
26. Banderas 🇳🇴 🇪🇸 en vez de "no" y "es"… ⚑ pero solo en esos dos botones: *mezclado* vuelve a su etiqueta.
27. En Escribí, quitar la dirección noruego → castellano.
28. Botón Siguiente neutro, sin color de acento.
29. Botón de velocidad lenta también en Sonido → se generaliza `playBtn` en vez de duplicar código.

### Muestreo

30. Las palabras se repiten demasiado → se propone mazo.
31. ⚑ No quiero mazo ni azar puro → rechazo con tope, O(1), sin tabla.
32. Tope de 3 en vez de 2… y después de 2 otra vez.
33. ⚑ "Vi cuatro repeticiones" → se auditan dos fugas reales: un off-by-one y una escapatoria tras 40 intentos.

### Hablá

34. Grabar la voz del usuario, transcribir y traducir → Web Speech API + desglose local + Google.
35. Play de la versión modelo para comparar.
36. Versión lenta y botón de palabra al azar para improvisar.
37. ⚑ "Volviste a las palabras sueltas" → no; el modo lento de Google inserta pausas.
38. ⚑ "El normal suena igual que el lento" → cierto: `ttsspeed` frena solo 18% y el `playbackRate` se perdía al cargar el recurso. Se pasa a `playbackRate` con `defaultPlaybackRate`.
39. ⚑ "Están sonando tus mp3, no Google" → cierto: una regla del modelo prefería la grabación local si el texto coincidía. Se elimina y se avisa en pantalla cuando entra el respaldo.
40. ⚑ "Google no responde" → cierto: 404 por `Referer`. Se agrega `<meta name="referrer" content="no-referrer">`.

### Frases

41. En Sonido, submodo de frases con ~500 frases generadas.
42. ⚑ "¿Las revisaste una por una?" → no. La auditoría encuentra siete defectos, entre ellos *må ikke* mal traducido y *kommer her*, que no existe.
43. ⚑ "¿Agregaste a la lista las palabras que usaste en las frases?" → no. Faltaban *ikke* (en 104 frases), *i* y *nå*.
44. ⚑ "Las frases tienen sesgo: nunca el sujeto es un sustantivo" → cierto y medible: 0 de 500 tenían sujeto nominal, 346 empezaban con pronombre, 36 palabras no aparecían nunca.
45. ⚑ "La cortesía sí entra en oraciones" → cierto. Siete plantillas nuevas con sus ejemplos: *Jeg vil ha en ost, vær så snill*.
46. Dos rondas de scouting del modelo para diversificar → atributivos, plurales, imperativo, subordinadas, identificación, dos cláusulas con sujetos distintos.

### Niveles

47. Diagnóstico previo, sin tocar código, sobre cómo hacer niveles de vocabulario.
48. ⚑ "Elegir por cobertura es intratable" → parcialmente: el greedy es barato, pero **sería circular**. Se adopta la propuesta del usuario: la frecuencia manda, la cobertura verifica.
49. Implementar 25 / 60 / 120 conservando las palabras ya construidas → el nivel 3 son las 114 existentes más 6, así que hubo que escribir 6 anclas nuevas y no 120.

### Audio, segunda vuelta

52. ⚑ "Reproducir más lento no sirve; el problema son las pausas entre palabras. ¿Estás usando Google de verdad?" → **no**: en Sonido sonaban los mp3 de Piper; Google solo se usaba en Hablá. Y el diagnóstico era correcto: lo que cuesta al escuchar es segmentar, no la velocidad. Se genera una segunda grabación `-lento` por cada texto, con comas entre palabras para forzar pausas reales.
53. ⚑ "No te pedí que tocaras Hablá" → cierto, fue un cambio no pedido. Hablá se revierte: sigue yendo siempre a Google, porque ahí el texto lo inventa el usuario y no hay grabación propia; encadenar palabras sueltas no funciona.

54. Botón **G** en Sonido, a la izquierda del play y simétrico con el ½×, para pedir una segunda voz a Google bajo demanda → se mantiene el audio local por defecto y se evita depender de una API no oficial, pero queda la ayuda cuando hace falta contrastar.

### Reglas

55. Sección de reglas gramaticales y de pronunciación, con las de pronunciación mudadas desde la Lista, repartidas en tres niveles y **practicables, no solo enunciadas** → 22 reglas con 48 preguntas de opción múltiple; cada respuesta explica el porqué y suma al marcador general.

56. Segunda voz de Google, bajada en cinco etapas para verificar que no bloquee → 1128 archivos, 0 fallos. Después, a pedido, Google pasa a voz principal (▶₁) y Piper a segunda (▶₂).
57. ⚑ "El orden de la Lista desapareció y yo no lo pedí" → cierto: un borrado por rango se llevó el selector, y el JS huérfano cortaba la ejecución del script entero. El mismo error había borrado antes `playBtn`. Se restauran, `$()` se blinda y se agrega un simulador de DOM que corre el script completo, porque `node --check` solo valida sintaxis.
58. Poder escuchar la propia grabación en Hablá, sin que quede guardada → se intentó con MediaRecorder en paralelo al reconocimiento. **No funcionó**: en Android los dos consumidores del micrófono se pisan y el reconocedor aborta sin avisar. Serializar la toma del micrófono tampoco alcanzó. Revertido a pedido del usuario; queda pendiente hasta tener el error de consola.

### Documentación

50. README con los criterios de construcción → se detecta que el generador de frases vivía fuera del repo y el corpus no era reproducible.
51. Este archivo.

---

## Lo que estas correcciones cambiaron en el diseño

- **El usuario audita mejor de oído que el modelo por medición.** Tres bugs de audio y pronunciación los detectó él escuchando; el modelo solo pudo confirmarlos midiendo después. De ahí que exista el botón lento y el aviso de cuándo entra el respaldo.
- **Nada se da por verificado si no se midió.** Las auditorías de cobertura y de tokens nacieron de dos preguntas del usuario que el modelo había contestado de memoria y mal.
- **Las decisiones de muestreo y de niveles son del usuario.** El modelo propuso mazo y cobertura óptima; ambas se descartaron por buenas razones y lo que quedó es más simple.
- **Nada de refactors grandes sin pedido.** Los cambios se hicieron incrementales y verificados en producción, uno por uno.
