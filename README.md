# Blue IA — Experimento 001 🔵

Primer laboratorio de Blue Lab Studios: una conversación local en el entorno de Google Colab con el modelo abierto [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct). No utiliza una API comercial, no solicita claves y no entrena el modelo. La personalidad de Blue es una instrucción de texto, no nuevos pesos.

## Abrir desde un celular

1. Descarga en tu celular el archivo [Blue_IA_Experimento_001.ipynb](Blue_IA_Experimento_001.ipynb) de este proyecto. Si lo recibiste dentro de un archivo comprimido, descomprímelo primero.
2. Abre [Google Colab](https://colab.research.google.com/) en el navegador e inicia sesión con tu cuenta de Google. En el diálogo de apertura, elige **Subir** y selecciona el archivo `.ipynb` desde el dispositivo. Si no aparece el diálogo, usa **Archivo → Subir cuaderno**. Si algún control no se ve, activa **Sitio de escritorio** en el menú del navegador.
3. Opcional: en **Entorno de ejecución → Cambiar tipo de entorno de ejecución**, selecciona **GPU**, si está disponible. La GPU gratuita depende de la disponibilidad y de los límites de Colab; el cuaderno también funciona con CPU, aunque más despacio. No hace falta contratar servicios de pago.
4. Conecta el entorno si Colab lo solicita y ejecuta las celdas **en orden** con ▶. Si aparece una advertencia de Colab sobre el origen del cuaderno, revisa el código antes de aceptar su ejecución. La primera instalación y descarga pueden tardar varios minutos y requieren conexión a Internet.
5. En la sección **Hablar con Blue**, cambia el texto dentro de `hablar_con_blue("...")` y vuelve a ejecutar esa celda. También puedes usar la celda de conversación continua y escribir `salir` para terminar. Ejecuta `reiniciar_conversacion()` para borrar la memoria de la sesión.
6. Prueba las celdas de ciencia, matemáticas y tecnología. La sección **Pruebas básicas** hace una generación real y comprueba algunas condiciones; borra el historial antes y después.

También puedes abrir el cuaderno publicado directamente en [Google Colab](https://colab.research.google.com/github/gabrielvillarreta555-code/blue-ia/blob/main/Blue_IA_Experimento_001.ipynb) o subir el `.ipynb` a Google Drive y abrirlo desde allí.

## Cómo funciona

El tokenizador convierte las instrucciones, el historial y tu mensaje en tokens. Qwen usa sus parámetros ya aprendidos para predecir tokens de respuesta durante la **inferencia**. El tokenizador convierte los tokens nuevos de vuelta a texto. Blue conserva como máximo tres intercambios y admite un máximo de 512 tokens de entrada; si no caben, elimina primero los intercambios más antiguos. La respuesta está limitada a 128 tokens nuevos. Un mensaje individual demasiado largo se rechaza para que puedas acortarlo.

El modelo tiene unos 0,5 mil millones de parámetros. Los pesos ocupan aproximadamente 1 GB con precisión de 16 bits en GPU o 2 GB con 32 bits en CPU, además de la memoria para la ejecución y el espacio de los archivos descargados. No se descargan otros modelos. La sesión y la caché de Colab son temporales: si se reinicia el entorno, vuelve a ejecutar las celdas; podría ser necesario descargar los archivos de nuevo. El historial no se guarda en archivos, aunque las salidas visibles sí pueden guardarse en el cuaderno si decides guardarlo.

## Si algo falla

- **Descarga o instalación:** comprueba tu conexión y vuelve a ejecutar la celda que falló. Hugging Face y los repositorios de paquetes deben estar accesibles; no se necesita iniciar sesión ni proporcionar claves para este modelo público.
- **Sin GPU o memoria insuficiente:** cambia a CPU y reinicia el entorno, o vuelve a intentarlo más tarde con una GPU disponible. Cierra otros cuadernos y vuelve a ejecutar desde el inicio. En CPU las respuestas pueden tardar bastante.
- **Error por mensaje largo:** reduce la longitud del mensaje; puedes usar `reiniciar_conversacion()` para borrar el contexto anterior.
- **Una celda dice que falta una variable:** ejecuta de nuevo las celdas anteriores en orden, especialmente la carga del modelo y la definición de `hablar_con_blue`.
- **La entrada continua no funciona en el navegador móvil:** edita y ejecuta la celda de una sola pregunta.

Las respuestas pueden ser imprecisas, especialmente en matemáticas o temas complejos. Comprueba la información importante. No se abre ningún servidor público ni se comparte el entorno mediante este cuaderno.

## Comprobaciones locales

La celda de pruebas del cuaderno requiere descargar y ejecutar el modelo real. Además, `python -m unittest discover -s tests` ejecuta pruebas ligeras sin dependencias externas: comprueba la estructura y la lógica de memoria con objetos de prueba. Estas pruebas locales **no sustituyen** la inferencia real ni comprueban la calidad del modelo.
