import logging
import os
from groq import Groq
from typing import Optional
from config import GROQ_API_KEY

logger = logging.getLogger(__name__)

class STTHandler:
    def __init__(self):
        try:
            logger.info("Initializing Groq client for Whisper API...")
            self.client = Groq(api_key=GROQ_API_KEY)
            logger.info("Groq client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Groq client: {e}")
            self.client = None
    
    async def transcribe_audio(self, audio_file: str) -> Optional[str]:
        try:
            if not self.client:
                logger.error("Groq client not initialized")
                return None
            
            if not os.path.exists(audio_file):
                logger.error(f"Audio file does not exist: {audio_file}")
                return None
            
            logger.info(f"Transcribing audio file: {audio_file}")
            
            with open(audio_file, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_file, file.read()),
                    model="whisper-large-v3",
                    response_format="text",
                    language="en"
                )
            
            transcribed_text = transcription.strip() if isinstance(transcription, str) else str(transcription).strip()
            
            if transcribed_text:
                logger.info(f"Transcription: {transcribed_text}")
                return transcribed_text
            else:
                logger.info("No speech detected in audio")
                return None
                
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    def is_ready(self) -> bool:
        return self.client is not None
