import httpx
import logging
from typing import List, Dict
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_ID

logger = logging.getLogger(__name__)

class AIHandler:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = OPENAI_BASE_URL
        self.model = MODEL_ID
        self.conversation_history: List[Dict] = []
        self.max_history = 10
        
    async def get_response(self, user_message: str) -> str:
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-(self.max_history * 2):]
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful AI assistant in a voice call. Keep responses concise and conversational, as they will be spoken aloud. Limit responses to 2-3 sentences unless specifically asked for more detail."
                            },
                            *self.conversation_history
                        ],
                        "temperature": 0.7,
                        "max_tokens": 150
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_message = data["choices"][0]["message"]["content"]
                    
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": ai_message
                    })
                    
                    logger.info(f"AI Response: {ai_message}")
                    return ai_message
                else:
                    logger.error(f"API Error: {response.status_code} - {response.text}")
                    return "I'm sorry, I'm having trouble processing that right now."
                    
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "I apologize, but I encountered an error."
    
    def reset_conversation(self):
        self.conversation_history = []
        logger.info("Conversation history reset")
