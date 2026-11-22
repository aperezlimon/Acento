# Revisión — «Calle Rosario, 4», versión 2

Reel vertical 1080×1920 a 30 fps, 61,4 s, 9 escenas. Narración con Kokoro (voz Dora) y
música de fondo de El Mochuelo. Rehecho a partir de las notas sobre la versión 1: voz Kokoro,
imágenes en alta definición, sin fondo de estraza ni puertas dibujadas, estilo de reportaje de
revista y unos 60 s.

## Decisiones creativas

- **Fotografía de archivo real como protagonista.** La foto de Emilio Beauchy de un café
  cantante sevillano (h. 1885) abre, explica y cierra la pieza. El grabado de Doré, el de
  Alarcón, las dos fotos de Silverio y el plano de Sevilla de 1868 cubren el resto.
- **Lenguaje de revista:** página negra, titulares en Archivo Black sobre caja, una o dos
  palabras resaltadas en amarillo albero por plano, etiquetas y círculos sobre las fotos,
  créditos en cursiva.
- **Guion recortado a 9 frases.** La historia es la misma que en la versión 1.
- **Chacón sin cara:** la escena señala al público en general, no a una persona concreta,
  y da su nombre y fechas. No hay foto suya en el café y su retrato no se pudo descargar
  (Wikimedia devolvió 429).
- **Silla vacía:** es la silla real del tablao del grabado de Alarcón, con su crédito.
  Ilustra la frase; no es la silla de Silverio.
- **Mapa de Andalucía** con datos geográficos reales (es-atlas), no dibujado a mano.

## Qué se midió y qué solo se miró

- `hyperframes check --safe-zone reels`: ok. Queda un aviso de contraste que dura 3
  fotogramas, mientras una palabra resaltada cambia de color.
- Snapshots de las 9 escenas y de los momentos clave; las imágenes se leen nítidas.
- **Audio medido, no escuchado:** la música queda entre 12 y 17 dB por debajo de la voz
  mientras se habla y sube a unos −31 dBFS en las pausas y a −25 dBFS en el cierre.

## Puntos débiles

- Las dos fotos de Silverio son originales muy pequeños (165×250 y 449×355). Están
  ampliadas con grano de copia antigua y se ven blandas comparadas con la de Beauchy.
- La grabación de El Mochuelo tiene cante, no solo guitarra. Bajo la voz suena como el
  ambiente del café, pero si molesta habría que buscar una pista solo de guitarra.
- No hay efectos de sonido.

## Pendiente o posible

- El retrato de Antonio Chacón (`Chacon 03.jpg` en Commons), si Wikimedia deja de bloquear.
- Unas palmas de fondo en las escenas del café (`tools/mix_music.sh` ya las mezcla si existe
  `assets/audio/palmas-src.ogg`).
