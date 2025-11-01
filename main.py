import asyncio
import logging
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION_STRING
from voice_handler import VoiceCallHandler
from health_server import HealthCheckServer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

client = None
voice_handler = None
health_server = None

async def main():
    global client, voice_handler, health_server
    
    try:
        logger.info("Starting Telegram Voice Bot...")
        
        client = TelegramClient(
            StringSession(SESSION_STRING),
            API_ID,
            API_HASH
        )
        
        await client.start()
        logger.info("Telegram client started successfully")
        
        me = await client.get_me()
        logger.info(f"Logged in as: {me.first_name} (@{me.username})")
        
        voice_handler = VoiceCallHandler(client)
        await voice_handler.start()
        
        health_server = HealthCheckServer()
        await health_server.start()
        
        @client.on(events.NewMessage(pattern='/joincall'))
        async def join_call_handler(event):
            try:
                logger.info("Received /joincall command")
                
                chat = await event.get_chat()
                chat_id = event.chat_id
                
                success = await voice_handler.join_call(chat_id)
                
                if success:
                    await event.respond("✅ Joined the voice call! I'm ready to listen and respond.")
                else:
                    await event.respond("❌ Failed to join the voice call. Make sure there's an active voice chat.")
                    
            except Exception as e:
                logger.error(f"Error in join_call_handler: {e}")
                await event.respond(f"❌ Error: {str(e)}")
        
        @client.on(events.NewMessage(pattern='/leavecall'))
        async def leave_call_handler(event):
            try:
                logger.info("Received /leavecall command")
                
                success = await voice_handler.leave_call()
                
                if success:
                    await event.respond("✅ Left the voice call.")
                else:
                    await event.respond("❌ Not currently in a voice call.")
                    
            except Exception as e:
                logger.error(f"Error in leave_call_handler: {e}")
                await event.respond(f"❌ Error: {str(e)}")
        
        @client.on(events.NewMessage(pattern='/callstatus'))
        async def status_handler(event):
            try:
                logger.info("Received /callstatus command")
                
                status = voice_handler.get_status()
                
                status_text = f"""
📊 **Voice Call Status**

🔊 In Call: {'Yes' if status['in_call'] else 'No'}
💬 Chat ID: {status['chat_id'] if status['chat_id'] else 'N/A'}
🎤 STT Ready: {'Yes' if status['stt_ready'] else 'No'}
                """
                
                await event.respond(status_text)
                
            except Exception as e:
                logger.error(f"Error in status_handler: {e}")
                await event.respond(f"❌ Error: {str(e)}")
        
        @client.on(events.NewMessage(pattern='/speak'))
        async def speak_handler(event):
            try:
                logger.info("Received /speak command")
                
                text = event.message.text.replace('/speak', '').strip()
                
                if not text:
                    await event.respond("❌ Please provide text to speak. Usage: /speak <text>")
                    return
                
                if not voice_handler.is_in_call:
                    await event.respond("❌ Not currently in a voice call. Use /joincall first.")
                    return
                
                success = await voice_handler.process_and_speak(text)
                
                if success:
                    await event.respond("✅ Message spoken in the voice call.")
                else:
                    await event.respond("❌ Failed to speak in the voice call.")
                    
            except Exception as e:
                logger.error(f"Error in speak_handler: {e}")
                await event.respond(f"❌ Error: {str(e)}")
        
        @client.on(events.NewMessage(pattern='/reset'))
        async def reset_handler(event):
            try:
                logger.info("Received /reset command")
                voice_handler.ai_handler.reset_conversation()
                await event.respond("✅ Conversation history reset.")
            except Exception as e:
                logger.error(f"Error in reset_handler: {e}")
                await event.respond(f"❌ Error: {str(e)}")
        
        @client.on(events.NewMessage(pattern='/help'))
        async def help_handler(event):
            help_text = """
🤖 **Voice Bot Commands**

/joincall - Join the voice call in current chat
/leavecall - Leave the voice call
/callstatus - Check voice call status
/speak <text> - Make the bot speak text in voice call
/reset - Reset conversation history
/help - Show this help message

**Features:**
🎤 Speech-to-Text (Whisper)
🔊 Text-to-Speech (EdgeTTS)
🤖 AI Responses (OpenAI-compatible)
            """
            await event.respond(help_text)
        
        logger.info("Bot is ready and listening for commands...")
        logger.info("Available commands: /joincall, /leavecall, /callstatus, /speak, /reset, /help")
        
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        raise
    finally:
        if voice_handler:
            await voice_handler.cleanup()
        if health_server:
            await health_server.stop()
        if client:
            await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        sys.exit(1)
