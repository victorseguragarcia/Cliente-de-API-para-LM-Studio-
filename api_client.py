import aiohttp
import asyncio
from urllib3.util.retry import Retry
from config import Config

class APIClient:
    def __init__(self):
        self.is_thinking = False
        self.response_cache = {}  # Caché de respuestas

    async def ask_lm_studio(self, question, max_retries=3):
        """Envía una pregunta al servidor de LM Studio de forma asíncrona."""
        if question in self.response_cache:
            return self.response_cache[question]

        self.is_thinking = True
        async with aiohttp.ClientSession() as session:
            retries = Retry(total=max_retries, backoff_factor=0.5, status_forcelist=[502, 503, 504])
            try:
                payload = {
                    "model": "lmstudio-community/qwen2.5-7b-instruct",
                    "messages": [{"role": "user", "content": question}]
                }
                async with session.post(Config.LM_STUDIO_API_URL, json=payload, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    answer = data["choices"][0]["message"]["content"]
                    self.response_cache[question] = answer
                    return answer
            except aiohttp.ClientResponseError as e:
                return f"Error HTTP: {e.status} - {e.message}"
            except asyncio.TimeoutError:
                return "Error: La solicitud al servidor tomó demasiado tiempo."
            except Exception as e:
                return f"Error inesperado: {e}"
            finally:
                self.is_thinking = False