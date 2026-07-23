import os

from dotenv import load_dotenv
from manim_voiceover.services.openai import OpenAIService

load_dotenv()


def get_speech_service() -> OpenAIService:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to your .env file."
        )
    return OpenAIService(voice="alloy", model="tts-1", transcription_model=None)
