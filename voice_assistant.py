import threading
from voice_processing import VoiceProcessor
from api_client import APIClient
from config import Config

class VoiceAssistant:
    def __init__(self):
        self.voice_processor = VoiceProcessor()
        self.api_client = APIClient()

    async def ejecutar_conversacion(self, output_text, status_label, entrada_texto=None):
        """Ejecuta una conversación por voz o texto de forma asíncrona."""
        try:
            if entrada_texto is None:
                texto_usuario, lang, error = self.voice_processor.record_audio()
                if error:
                    output_text(f"❌ {error}\n")
                    return
            else:
                texto_usuario = entrada_texto.strip()
                lang = "es"
                if not texto_usuario:
                    return

            output_text(f"🧍 Tú ({lang}): {texto_usuario}\n")
            status_label("🤖 IA está pensando...")
            respuesta = await self.api_client.ask_lm_studio(
                f"Responde en {'inglés' if lang == 'en' else 'español'} de manera clara y concisa: {texto_usuario}"
            )
            output_text(f"🤖 IA: {respuesta}\n\n")
            status_label("")

            threading.Thread(target=self.voice_processor.speak_text, args=(respuesta,), daemon=True).start()

        except Exception as e:
            output_text(f"❌ Error: {e}\n")