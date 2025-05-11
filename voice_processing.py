import pyttsx3
import speech_recognition as sr
import whisper
import tempfile
import os
import torch
from concurrent.futures import ThreadPoolExecutor
from config import Config

class VoiceProcessor:
    def __init__(self):
        self.model = None  # Carga perezosa
        self.engine = self._initialize_tts()
        self.is_speaking = False
        self.executor = ThreadPoolExecutor(max_workers=1)

    def _initialize_tts(self):
        """Inicializa el motor de texto a voz."""
        engine = pyttsx3.init()
        engine.setProperty("rate", Config.SPEECH_RATE)
        return engine

    def _load_whisper_model(self):
        """Carga el modelo Whisper con soporte para GPU y cuantización."""
        if self.model is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = whisper.load_model(Config.MODEL_NAME, device=device)
            if device == "cuda":
                self.model = self.model.half()  # Cuantización a FP16

    def transcribe_audio(self, audio_file):
        """Transcribe un archivo de audio usando Whisper en un hilo separado."""
        self._load_whisper_model()
        def transcribe():
            try:
                result = self.model.transcribe(audio_file)
                lang = result.get("language", "")
                text = result["text"].strip()
                if not text:
                    return None, lang, "No se detectó texto claro en el audio."
                if lang not in Config.SUPPORTED_LANGUAGES:
                    return None, lang, f"Idioma no soportado: {lang}. Usa español o inglés."
                return text, lang, None
            except Exception as e:
                return None, None, f"Error al transcribir: {e}"

        future = self.executor.submit(transcribe)
        return future.result()

    def record_audio(self):
        """Graba audio desde el micrófono."""
        recognizer = sr.Recognizer()
        tmp_path = None
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Habla ahora...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    return None, None, "No se detectó audio. Por favor, habla más alto o revisa el micrófono."

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                tmp_path = tmpfile.name
                tmpfile.write(audio.get_wav_data())

            texto, lang, error = self.transcribe_audio(tmp_path)
            return texto, lang, error
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def speak_text(self, text):
        """Convierte texto a voz."""
        self.is_speaking = True
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        finally:
            self.is_speaking = False

    def stop_speaking(self):
        """Detiene la reproducción de voz."""
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False