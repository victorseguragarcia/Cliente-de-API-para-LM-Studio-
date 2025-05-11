CLIENTE DE API PARA LM STUDIO CON SOPORTE DE VOZ
Este proyecto permite enviar preguntas a una instancia local de LM Studio mediante una interfaz asíncrona y con soporte para entrada y salida por voz. Utiliza reconocimiento de voz, síntesis de texto a voz y llamadas a la API local de LM Studio.

CARACTERÍSTICAS
Envío de preguntas a LM Studio mediante API local.

Caché de respuestas para evitar peticiones repetidas.

Reconocimiento de voz con SpeechRecognition.

Conversión de texto a voz con pyttsx3.

Configuración flexible mediante archivo config.json.

ARCHIVOS PRINCIPALES
api_client.py: Cliente asíncrono para interactuar con LM Studio.

config.json: Archivo de configuración general.

requirements.txt: Lista de dependencias necesarias.

INSTALACIÓN
Clona el repositorio o descarga los archivos en tu máquina local.

Instala las dependencias necesarias ejecutando:

bash
Copiar
Editar
pip install -r requirements.txt
Asegúrate de tener LM Studio ejecutándose en la URL configurada en config.json.

CONFIGURACIÓN
El archivo config.json permite ajustar distintos parámetros de ejecución:

json
Copiar
Editar
{
  "model_name": "tiny",
  "lm_studio_api_url": "http://localhost:1234/v1/chat/completions",
  "speech_rate": 150,
  "supported_languages": ["es", "en"]
}
model_name: Nombre del modelo que se desea usar (informativo).

lm_studio_api_url: URL del servidor local de LM Studio.

speech_rate: Velocidad de lectura del sintetizador de voz.

supported_languages: Idiomas soportados para el reconocimiento de voz.

