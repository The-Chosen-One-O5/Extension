import edge_tts
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

class TTSHandler:
    def __init__(self):
        self.voice = "en-US-AndrewNeural"
        self.rate = "+0%"
        self.volume = "+0%"
        
    async def text_to_speech(self, text: str, output_file: str) -> Optional[str]:
        try:
            logger.info(f"Converting text to speech: {text[:50]}...")
            
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate,
                volume=self.volume
            )
            
            await communicate.save(output_file)
            
            if os.path.exists(output_file):
                logger.info(f"TTS audio saved to {output_file}")
                return output_file
            else:
                logger.error("TTS file was not created")
                return None
                
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return None
    
    def set_voice(self, voice: str):
        self.voice = voice
        logger.info(f"Voice changed to: {voice}")
    
    async def get_available_voices(self):
        try:
            voices = await edge_tts.list_voices()
            return voices
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
