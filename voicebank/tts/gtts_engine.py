from gtts import gTTS
import os
from typing import Optional


def synthesize_speech(text: str, lang: str = 'en') -> Optional[bytes]:
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            audio_bytes = f.read()
        os.remove("response.mp3")
        return audio_bytes
    except Exception:
        return None
