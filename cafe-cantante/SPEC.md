# SPEC — «Calle Rosario, 4»

GOAL:    que quien lo vea entienda que el café cantante le dio al flamenco un escenario público, y
         que fue Silverio Franconetti quien lo llevó a su punto más alto; termina con ganas de compartirlo.
OUTPUT:  HyperFrames, 1080×1920 (9:16, Instagram Reels), 30 fps.
TIME:    ~90 s × 30 = ~2700 frames. La voz marca el tiempo; la duración final la da la narración.
VOICE:   Piper (local, gratis); voz por confirmar. Velocidad ~0.9 (length_scale 1.1).
SAFE:    todo texto entre y 288–1248 px y x 120–888 px (zona libre de Reels). Subtítulos con
         su borde inferior en y ≤ 1248. Fuera de esa banda solo textura y decoración.

## LOOK — un cartel de café del siglo XIX recortado y pegado

- **Papel de fondo:** estraza #C9A77C con fibra al 6 % (ruido SVG), sin degradados.
- **Papel de recorte:** papel de periódico #E6DCC3 en tiras con borde rasgado (máscara SVG
  irregular, 6–14 px de diente) y sombra de despegue 0 6 px 0 rgba(27,23,18,.35).
- **Tinta:** #1B1712 en todo texto legible, líneas y grabados.
- **Acento (rojo albero, #B8432F):** solo en los años (1881, 1889), en la entrada de la calle
  Rosario y en la frase final. Una sola zona de acento por plano.
- **Grabados:** imágenes de dominio público pasadas a semitono (puntos de 6 px a 1080) en tinta
  sobre papel; nunca fotos a color.
- **Cinta adhesiva:** rectángulos #F2E6C4 al 70 % con bordes dentados, girados ±4–9°.
- **Tipos:** titulares en League Gothic 400, 150–210 px, tracking +1 %, en mayúsculas, como en
  los carteles de época; texto y subtítulos en EB Garamond 600, 46 px; años en League Gothic a 260 px.
- **Luz y profundidad:** sin viñeta ni brillo; 3 capas de papel con parallax 1 : 0.6 : 0.3.

## OBJECTS

- La **entrada / el boleto**: papel rasgado con troquel, «CALLE ROSARIO, 4 · SEVILLA».
- La **puerta del café**: dos hojas de madera recortadas en papel que se abren hacia la cámara.
- Las **mesas**: veladores de mármol con copas y humo de papel de seda.
- El **tablao**: tarima de tablas con una silla de anea y una guitarra.
- **Silverio**: su fotografía de época (dominio público) en semitono, recortada.
- **Antonio Chacón**: silueta de muchacho recortada entre el público (sin cara inventada).
- El **mapa de Andalucía**: recorte con chinchetas rojas que se multiplican.
- La **silla vacía**: la misma silla del tablao, sola, con un foco de papel.

## MOTION

- Entrada de recortes: «slap» (de escala 1.25 a 1.0 en 8 f, back.out(1.6)); nada aparece con fundido.
- Movimientos de cámara: power2.inOut, empujes de 60–90 f; la cámara atraviesa las capas de papel
  (la puerta, las mesas, el humo), nunca corta en seco dentro de la toma continua.
- Las tiras de texto se «pegan» con un giro de 6° a 0° en 10 f; escalonado de 4 f.
- Salidas: el papel se levanta y se va de cuadro (y −120 px, rotación 8°, 12 f).
- Una sola acción protagonista por plano; las secundarias a 50–70 % de recorrido y 3–6 f después.

## SHOTS (guion · ~158 palabras)

| # | Frames aprox. | Acción protagonista | Voz |
|---|---|---|---|
| 1 | 0–180 | El boleto «CALLE ROSARIO, 4 · SEVILLA» choca contra la cámara (fotograma 0 ya legible). | Hubo un tiempo en que el flamenco no tenía escenario. |
| 2 | 180–480 | Patio y taberna en grabado; la cámara se asoma por una ventana de papel. | Se cantaba en patios, en tabernas, en fiestas privadas. Para unos pocos, y a puerta cerrada. |
| 3 | 480–810 | La puerta del café se abre hacia la cámara: mesas, copas, el tablao. | Hasta que en Sevilla llegaron los cafés cantantes. Mesas, copas, un tablao… y un público que pagaba por escuchar. |
| 4 | 810–1140 | «1881» en rojo se pega; empuje hasta el cartel del café. | El más famoso estaba en la calle Rosario, número cuatro. Lo abrió un cantaor en 1881: Silverio Franconetti. |
| 5 | 1140–1500 | La foto de Silverio se rasga en dos mitades: Italia / Morón; aparecen los versos de Lorca. | Hijo de padre italiano y madre andaluza, creció en Morón de la Frontera. Lorca escribiría: «la densa miel de Italia con el limón nuestro». |
| 6 | 1500–1830 | Travelling por el público hasta la silueta del muchacho. | En su café cantaban las grandes figuras de su tiempo. Y entre el público, un muchacho de Jerez: Antonio Chacón. |
| 7 | 1830–2160 | Zoom fuera: el café se vuelve una chincheta en el mapa; se multiplican. | Fue la Edad de Oro del flamenco. Los cafés se extendieron por Andalucía, y el cante se hizo oficio. |
| 8 | 2160–2460 | «1889» en rojo; el tablao se vacía, queda la silla. | Silverio murió en 1889. Su silla quedó vacía, pero el escenario ya no se iba a cerrar. |
| 9 | 2460–2700 | Cierre: la frase final se pega sobre el boleto del principio. | Silverio Franconetti le dio al cante un escenario. |

Sonido: guitarra por soleá, seca, que entra cuando se abre la puerta (plano 3); palmas solo en el
tablao (planos 3–6); se queda en silencio en la silla vacía (plano 8) y vuelve para el cierre.
Fuente de la música: por decidir. Sin fuente gratuita, el reel se entrega solo con voz.

## Datos y su fuente

- Calle Rosario, 4, de Sevilla, 1881: andalucia.org, Expoflamenco (hay fuentes que dan 1870).
- Padre italiano, madre andaluza, infancia en Morón: andalucia.com, Biografías y Vidas.
- Muere en 1889: todas las fuentes.
- El joven Antonio Chacón pasó por su café: andalucia.org.
- Edad de Oro y declive hacia los teatros en los años veinte: andalucia.org.
- Versos: Federico García Lorca, «Retrato de Silverio Franconetti», *Poema del cante jondo*
  (dominio público en España desde 2017).

BANNED: fondo oscuro con elementos flotando; brillos, partículas y destellos; degradados morados o
azules; papel crema con serif en cursiva y etiquetas en mono; todo centrado; todo apareciendo con
fundido o subiendo; texto que se mueve mientras se lee; tres tarjetas en fila; caras o fotos
inventadas de personas reales; banderas o tópicos de postal (lunares, peinetas, abanicos).

QA:      f0 legible como portada; f600 la puerta abierta; f1000 «1881» en rojo; f1300 Silverio
         partido en dos; f1700 la silueta de Chacón; f2000 el mapa con chinchetas; f2350 la silla
         vacía; f2650 la frase final. Todo texto dentro de la zona segura de Reels.
