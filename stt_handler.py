import logging
import os
from faster_whisper import WhisperModel
from typing import Optional

logger = logging.getLogger(__name__)

class STTHandler:
    def __init__(self):
        try:
            logger.info("Initializing Whisper model (base)...")
            self.model = WhisperModel("base", device="cpu", compute_type="int8")
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
            
            segments, info = self.model.transcribe(
                audio_file,
                beam_size=5,
                language="en",
                vad_filter=True
            )
            
            transcribed_text = " ".join([segment.text for segment in segments])
            
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
