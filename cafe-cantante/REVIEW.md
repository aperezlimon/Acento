# Revisión — «Calle Rosario, 4»

Reel vertical 1080×1920 a 30 fps, 81,9 s, 9 escenas. Narración en español con la voz Piper
`es_ES-davefx-medium`. Historia A de `STORYLINES.md`; las otras dos (B «Entre italiano y flamenco»
y C «Del patio al teatro») no se han construido.

## Decisiones creativas

- **Collage de cartel de café del siglo XIX:** estraza, recortes de periódico, cinta adhesiva,
  y grabados y fotos de época pasados a semitono de una sola tinta. El rojo albero queda
  reservado para los años, la calle Rosario y la frase final.
- **Imágenes reales de dominio público** en lugar de ilustraciones: la escena de Doré, el café
  de Alarcón y las dos fotos de Silverio. Para Chacón uso una silueta recortada, porque no hay
  imagen suya en el café y no quería inventarle una cara.
- **Escena 7:** el mapa de Andalucía del SPEC se convirtió en sellos con nombres de ciudades.
  Un contorno de mapa dibujado a mano habría quedado poco fiable.
- **Duración:** 82 s y no 90. La voz dura 57 s; los respiros (la puerta, el desgarro, el mapa,
  la silla vacía y el cierre) llevan el resto. Ralentizar más la voz la hacía sonar pesada.

## Qué se midió y qué solo se miró

- `hyperframes check --safe-zone reels`: sin errores de lint, ejecución, audio ni contraste
  graves. Quedan 3 avisos de oclusión entre recortes girados, que en los fotogramas se leen
  enteros; los marqué con `data-layout-allow-occlusion`.
- Snapshots de cada escena, de cada corte (±0,2 s) y en ancho de móvil (360 px). Todo el
  texto se lee a 360 px.
- **El sonido no lo ha escuchado nadie:** la voz se generó y midió, pero no se oyó. La música
  aún no está mezclada (ver abajo).

## Puntos débiles

- **Escena 3:** la puerta es un plano marrón muy plano durante 0,5 s antes de abrirse.
  Con más tiempo le daría textura de madera y un cartel en el dintel.
- **Escena 6:** la silueta de Chacón es esquemática; funciona como recorte, pero es la imagen
  menos rica de la película.
- **Subtítulos:** cuatro de los 36 grupos pasan de 30 caracteres y ocupan dos líneas.

## Avisos que mantengo a propósito

- `duplicate_media_discovery_risk`: la escena 5 usa la misma foto dos veces para las dos
  mitades del retrato rasgado.
- `timeline_track_too_dense` en `captions.html`: el archivo de subtítulos tiene 36 grupos.
- `outside_safe_zone` solo para TikTok: el reel está compuesto para la zona segura de Reels.

## Pendiente

- **Música:** «Soleares por El Mochuelo» (CC BY-SA 4.0) y unas palmas (CC0) de Wikimedia
  Commons. `upload.wikimedia.org` responde 429 a las descargas de audio. Cuando estén en
  `assets/audio/`, ejecuta `tools/mix_music.sh` y añade
  `<audio id="musica" src="assets/audio/musica.wav" ...>` a `index.html`.
