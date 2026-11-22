# SPEC — «Calle Rosario, 4» (versión 2, revista)

GOAL:    que quien lo vea entienda que el café cantante le dio al flamenco un escenario
         público, y que Silverio Franconetti fue su gran figura.
OUTPUT:  HyperFrames, 1080×1920 (9:16, Reels), 30 fps.
TIME:    61,4 s × 30 = 1842 frames. La voz marca el tiempo (timings.json).
VOICE:   Kokoro-82M, voz ef_dora, velocidad 0,92 (tools/build_vo.py, frases en caché).
MUSIC:   «Soleares», El Mochuelo (CC BY-SA 4.0), en ducking bajo la voz y subiendo en las
         pausas (tools/mix_music.sh).
SAFE:    texto entre y 288–1248 y x 120–888; subtítulos con el borde inferior en y 1240.

## LOOK — reportaje de revista con fotografía de archivo

- **Página:** negro #111111, sin textura.
- **Fotografía:** imágenes de archivo reales a sangre o en «copia» con marco #F2ECE0 de 18 px
  y sombra 0 18 px 40 px al 45 %. Virado cálido de dos tintas (#16130F → #EFE6D4) y grano
  del 3–7 %. Nada de semitono ni de ilustración dibujada.
- **Titulares:** Archivo Black, 64–100 px, interlineado 1,04, tracking −1,5 %, papel #F2ECE0
  sobre caja negra.
- **Resaltado:** barra amarilla albero #F2C230 que se dibuja detrás de una o dos palabras por
  plano; la palabra pasa a negro.
- **Antetítulos y etiquetas:** Oswald 600 en mayúsculas, tracking 0,1–0,16 em; etiquetas negras
  sobre albero.
- **Anotaciones:** círculos y líneas albero de 7 px que se dibujan sobre la foto.
- **Citas y créditos:** EB Garamond cursiva, 28–74 px.
- **Subtítulos:** Montserrat 600, 40 px, papel sobre caja negra al 86 %.

## MOTION

- Los titulares se imprimen con un barrido de izquierda a derecha (12 f, power2.out); nunca
  aparecen con fundido ni suben.
- Las etiquetas entran con un ligero rebote de escala (6 f, back.out 1.7).
- Sobre cada foto, la cámara se mueve despacio (sine.inOut, de 1,0 a 1,08–1,22 de escala).
- Los cortes entre escenas son secos; el ritmo lo marcan la voz y la música.

## SHOTS

| # | Escena | Imagen | Acción |
|---|---|---|---|
| 1 | El flamenco, sin escenario | Beauchy, café cantante, h. 1885 | Portada; el resaltado se dibuja |
| 2 | Cante para unos pocos | Doré, academia de baile, 1874 | Etiquetas: patios, tabernas, fiestas privadas |
| 3 | Los cafés cantantes | Beauchy completa | Del tablao al café entero; círculos en mesas, tablao y público |
| 4 | Calle Rosario, Sevilla · 1881 | Plano de Sevilla, 1868 | El año en albero; entra la copia de Silverio con guitarra |
| 5 | Lorca | Retrato de Silverio, h. 1875 | Padre italiano / madre andaluza; cita de Lorca |
| 6 | Las grandes figuras | Público de la foto de Beauchy | Círculo en el público; ficha de Antonio Chacón |
| 7 | La Edad de Oro | Mapa de Andalucía (es-atlas) | Sevilla, Jerez, Cádiz y Málaga |
| 8 | 1889 | Silverio → silla vacía del grabado de Alarcón | Barrido a la silla vacía; silencio |
| 9 | Le dio al cante un escenario | Beauchy (vuelta al principio) | Cierre que se mantiene en pantalla |

BANNED: estraza o corcho; puertas y siluetas dibujadas; semitono; imágenes pixeladas o
ampliadas más de 3,2×; fondo oscuro con elementos pequeños flotando; brillos y partículas;
todo apareciendo con fundido o subiendo; texto que se mueve mientras se lee; tres tarjetas en
fila; caras inventadas de personas reales; tópicos de postal (lunares, peinetas, abanicos);
señalar a una persona concreta de una foto como alguien que no es.

QA:      f0 legible como portada; el resaltado de cada escena; 1881 y 1889 en albero; la cita de
         Lorca completa; los cuatro puntos del mapa; la silla vacía reconocible.
