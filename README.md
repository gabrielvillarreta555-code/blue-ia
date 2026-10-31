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

## Experimento 002: chat web desde el celular

Esta interfaz usa el mismo Qwen cargado en Colab. Necesita una conexión a Internet para instalar Gradio y crear su túnel temporal; no requiere claves ni servicios de pago. Las respuestas se generan en Colab, no mediante una API comercial de modelos.

1. Abre el [cuaderno en Colab](https://colab.research.google.com/github/gabrielvillarreta555-code/blue-ia/blob/main/Blue_IA_Experimento_001.ipynb). Conecta el entorno y, si está disponible, elige GPU como se explicó arriba; CPU también funciona más despacio.
2. Ejecuta las celdas de **1. Preparar las herramientas** y **2. Descargar y cargar el modelo**. Si ya cargaste el modelo en esta misma sesión, no hace falta repetirlas. Puedes saltarte la consola y los ejemplos.
3. Baja hasta **Experimento 002 — Interfaz web de Blue IA**. Ejecuta en orden las celdas **1. Instalar Gradio**, **2. Conectar Blue**, **3. Construir la interfaz** y **4. Abrir el enlace**. La primera instalación puede tardar unos minutos. Si Colab pide reiniciar el entorno, reinícialo y carga el modelo de nuevo.
4. Espera el mensaje **«Enlace temporal de Blue IA»**, tócalo o cópialo en Chrome en tu teléfono. Escribe una pregunta y toca **Enviar**; en dispositivos compatibles también puedes usar Enter. El botón **Nueva conversación** borra el historial de esa sesión.
5. Para detener la interfaz, vuelve al cuaderno y ejecuta la celda **5. Detener o reiniciar la interfaz**. Para iniciarla otra vez, ejecuta de nuevo **3. Construir la interfaz** y **4. Abrir el enlace**. Si se reinició o detuvo Colab, antes vuelve a ejecutar las celdas de preparación y carga del modelo.

**Privacidad:** el enlace de Gradio permite acceder a cualquiera que lo conozca. No incluyas datos privados y compártelo solo con personas de confianza. El enlace deja de funcionar al detenerse Colab o cuando expira el túnel. Cada sesión web mantiene su propia memoria temporal, separada de la consola; no modifica ni entrena los parámetros del modelo. Las conversaciones no se guardan intencionalmente en archivos del proyecto, pero evita guardar en el cuaderno salidas que incluyan información sensible. Gradio proporciona el túnel para acceder a la interfaz, mientras que la inferencia se ejecuta en tu entorno de Colab.

## Cómo funciona

El tokenizador convierte las instrucciones, el historial y tu mensaje en tokens. Qwen usa sus parámetros ya aprendidos para predecir tokens de respuesta durante la **inferencia**. El tokenizador convierte los tokens nuevos de vuelta a texto. Blue conserva como máximo tres intercambios y admite un máximo de 512 tokens de entrada; si no caben, elimina primero los intercambios más antiguos. La respuesta está limitada a 128 tokens nuevos. Un mensaje individual demasiado largo se rechaza para que puedas acortarlo.

El modelo tiene unos 0,5 mil millones de parámetros. Los pesos ocupan aproximadamente 1 GB con precisión de 16 bits en GPU o 2 GB con 32 bits en CPU, además de la memoria para la ejecución y el espacio de los archivos descargados. No se descargan otros modelos. La sesión y la caché de Colab son temporales: si se reinicia el entorno, vuelve a ejecutar las celdas; podría ser necesario descargar los archivos de nuevo. El historial no se guarda en archivos, aunque las salidas visibles sí pueden guardarse en el cuaderno si decides guardarlo.

## Si algo falla

- **Descarga o instalación:** comprueba tu conexión y vuelve a ejecutar la celda que falló. Hugging Face y los repositorios de paquetes deben estar accesibles; no se necesita iniciar sesión ni proporcionar claves para este modelo público.
- **Sin GPU o memoria insuficiente:** cambia a CPU y reinicia el entorno, o vuelve a intentarlo más tarde con una GPU disponible. Cierra otros cuadernos y vuelve a ejecutar desde el inicio. En CPU las respuestas pueden tardar bastante.
- **Error por mensaje largo:** reduce la longitud del mensaje; puedes usar `reiniciar_conversacion()` para borrar el contexto anterior.
- **Una celda dice que falta una variable:** ejecuta de nuevo las celdas anteriores en orden, especialmente la carga del modelo y la definición de `hablar_con_blue`.
- **La entrada continua no funciona en el navegador móvil:** edita y ejecuta la celda de una sola pregunta.

Las respuestas pueden ser imprecisas, especialmente en matemáticas o temas complejos. Comprueba la información importante. La consola del Experimento 001 no abre un enlace público; el Experimento 002 sí crea un enlace temporal de Gradio al ejecutar su celda de lanzamiento.

## Comprobaciones locales

La celda de pruebas del cuaderno requiere descargar y ejecutar el modelo real. Además, `python -m unittest discover -s tests` ejecuta pruebas ligeras sin dependencias externas: comprueba la estructura y la lógica de memoria con objetos de prueba. También comprueba la adaptación de la memoria web con objetos de prueba. Estas pruebas locales **no sustituyen** la inferencia real ni comprueban la calidad del modelo.
