

# CLIENTE DE API PARA LM STUDIO CON SOPORTE DE VOZ

Este proyecto permite enviar preguntas a una instancia local de LM Studio mediante una interfaz asíncrona y con soporte para entrada y salida por voz. Utiliza reconocimiento de voz, síntesis de texto a voz y llamadas a la API local de LM Studio.

---

## CARACTERÍSTICAS

- Envío de preguntas a LM Studio mediante API local.
- Caché de respuestas para evitar peticiones repetidas.
- Reconocimiento de voz con `SpeechRecognition`.
- Conversión de texto a voz con `pyttsx3`.
- Configuración flexible mediante archivo `config.json`.

---

## ARCHIVOS PRINCIPALES

- `api_client.py`: Cliente asíncrono para interactuar con LM Studio.
- `config.json`: Archivo de configuración general.
- `requirements.txt`: Lista de dependencias necesarias.

---
![Captura de pantalla 2025-05-11 163322](https://github.com/user-attachments/assets/e65774e2-a9a0-46bf-9dae-45a67d0826e1)

## INSTALACIÓN

1. Clona el repositorio o descarga los archivos en tu máquina local.
2. Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```
---

## CONFIGURACIÓN

Edita el archivo `config.json` para personalizar el comportamiento del cliente:

```json
{
  "model_name": "tiny",
  "lm_studio_api_url": "http://localhost:1234/v1/chat/completions",
  "speech_rate": 150,
  "supported_languages": ["es", "en"]
}
```
---

## EJECUCIÓN

Para ejecutar la aplicación, asegúrate de tener LM Studio iniciado localmente y luego corre el archivo principal con:

```bash
python main.py
```
