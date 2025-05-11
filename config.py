import json

class Config:
    """Clase para manejar configuraciones externas."""
    @staticmethod
    def load_config():
        with open("config.json", "r") as f:
            return json.load(f)

    CONFIG = load_config()
    MODEL_NAME = CONFIG["model_name"]
    LM_STUDIO_API_URL = CONFIG["lm_studio_api_url"]
    SPEECH_RATE = CONFIG["speech_rate"]
    SUPPORTED_LANGUAGES = set(CONFIG["supported_languages"])