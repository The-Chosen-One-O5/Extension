import logging
import os
import whisper
from typing import Optional

logger = logging.getLogger(__name__)

class STTHandler:
    def __init__(self):
        try:
            logger.info("Initializing Whisper model (base)...")
            self.model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            self.model = None
    
    async def transcribe_audio(self, audio_file: str) -> Optional[str]:
        try:
            if not self.model:
                logger.error("Whisper model not initialized")
                return None
            
            if not os.path.exists(audio_file):
                logger.error(f"Audio file does not exist: {audio_file}")
                return None
            
            logger.info(f"Transcribing audio file: {audio_file}")
            
            result = self.model.transcribe(
                audio_file,
                language="en"
            )
            
            transcribed_text = result["text"]
            
            if transcribed_text.strip():
                logger.info(f"Transcription: {transcribed_text}")
                return transcribed_text.strip()
            else:
                logger.info("No speech detected in audio")
                return None
                
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    def is_ready(self) -> bool:
        return self.model is not None
