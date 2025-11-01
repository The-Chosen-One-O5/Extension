import asyncio
import logging
import os
import time
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import AudioPiped, Update
from pytgcalls.exceptions import GroupCallNotFound, AlreadyJoinedError
from telethon import TelegramClient
from typing import Optional
from ai_handler import AIHandler
from tts_handler import TTSHandler
from stt_handler import STTHandler

logger = logging.getLogger(__name__)

class VoiceCallHandler:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.pytgcalls = PyTgCalls(client)
        self.ai_handler = AIHandler()
        self.tts_handler = TTSHandler()
        self.stt_handler = STTHandler()
        
        self.current_chat_id: Optional[int] = None
        self.is_in_call = False
        self.temp_dir = "temp_audio"
        
        os.makedirs(self.temp_dir, exist_ok=True)
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.pytgcalls.on_stream_end()
        async def on_stream_end(client: PyTgCalls, update: Update):
            logger.info("Audio stream ended")
    
    async def start(self):
        try:
            await self.pytgcalls.start()
            logger.info("PyTgCalls started successfully")
        except Exception as e:
            logger.error(f"Error starting PyTgCalls: {e}")
    
    async def join_call(self, chat_id: int) -> bool:
        try:
            if self.is_in_call:
                logger.warning("Already in a call")
                return False
            
            logger.info(f"Attempting to join voice call in chat {chat_id}")
            
            silence_file = await self._create_silence_audio()
            
            await self.pytgcalls.join_group_call(
                chat_id,
                AudioPiped(silence_file),
                stream_type=StreamType().pulse_stream
            )
            
            self.current_chat_id = chat_id
            self.is_in_call = True
            logger.info(f"Successfully joined voice call in chat {chat_id}")
            
            return True
            
        except AlreadyJoinedError:
            logger.warning("Already joined this call")
            self.is_in_call = True
            self.current_chat_id = chat_id
            return True
        except GroupCallNotFound:
            logger.error("No active group call found in this chat")
            return False
        except Exception as e:
            logger.error(f"Error joining call: {e}")
            return False
    
    async def leave_call(self) -> bool:
        try:
            if not self.is_in_call or not self.current_chat_id:
                logger.warning("Not currently in a call")
                return False
            
            await self.pytgcalls.leave_group_call(self.current_chat_id)
            
            self.is_in_call = False
            chat_id = self.current_chat_id
            self.current_chat_id = None
            
            logger.info(f"Left voice call in chat {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error leaving call: {e}")
            return False
    
    async def process_and_speak(self, text: str) -> bool:
        try:
            if not self.is_in_call or not self.current_chat_id:
                logger.warning("Not in a call, cannot speak")
                return False
            
            logger.info(f"Processing text: {text}")
            
            ai_response = await self.ai_handler.get_response(text)
            
            output_file = os.path.join(self.temp_dir, f"response_{int(time.time())}.mp3")
            audio_file = await self.tts_handler.text_to_speech(ai_response, output_file)
            
            if not audio_file:
                logger.error("Failed to generate TTS audio")
                return False
            
            await self.pytgcalls.change_stream(
                self.current_chat_id,
                AudioPiped(audio_file)
            )
            
            logger.info("Audio streamed to voice call")
            
            await asyncio.sleep(5)
            
            try:
                os.remove(audio_file)
            except:
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Error in process_and_speak: {e}")
            return False
    
    async def listen_and_respond(self, audio_file: str) -> bool:
        try:
            if not self.stt_handler.is_ready():
                logger.error("STT handler not ready")
                return False
            
            transcribed_text = await self.stt_handler.transcribe_audio(audio_file)
            
            if transcribed_text:
                logger.info(f"Heard: {transcribed_text}")
                await self.process_and_speak(transcribed_text)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in listen_and_respond: {e}")
            return False
    
    async def _create_silence_audio(self) -> str:
        silence_file = os.path.join(self.temp_dir, "silence.mp3")
        
        if not os.path.exists(silence_file):
            await self.tts_handler.text_to_speech(".", silence_file)
        
        return silence_file
    
    def get_status(self) -> dict:
        return {
            "in_call": self.is_in_call,
            "chat_id": self.current_chat_id,
            "stt_ready": self.stt_handler.is_ready()
        }
    
    async def cleanup(self):
        try:
            if self.is_in_call:
                await self.leave_call()
            
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                try:
                    os.remove(file_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
