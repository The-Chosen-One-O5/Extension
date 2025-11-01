# Telegram Voice Call Bot

A Telegram userbot that can join voice calls and interact using AI with Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities.

## Features

- 🎤 **Voice Call Integration**: Join and manage Telegram voice calls
- 🗣️ **Text-to-Speech**: Unlimited free TTS using EdgeTTS
- 👂 **Speech-to-Text**: Fast transcription using Whisper
- 🤖 **AI Responses**: Intelligent conversation using OpenAI-compatible API
- 🐳 **Docker Ready**: Containerized with ffmpeg support
- 💚 **Health Check**: Built-in health endpoint for UptimeRobot monitoring
- 🔄 **Auto-reconnect**: Robust error handling and reconnection logic

## Tech Stack

- **Telethon**: Telegram userbot framework
- **pytgcalls**: Voice call handling
- **EdgeTTS**: Text-to-speech generation
- **openai-whisper**: Speech-to-text transcription
- **OpenAI Client**: AI response generation
- **aiohttp**: Health check server
- **Docker**: Containerization with ffmpeg

## Commands

| Command | Description |
|---------|-------------|
| `/joincall` | Join the voice call in current chat |
| `/leavecall` | Leave the voice call |
| `/callstatus` | Check voice call status |
| `/speak <text>` | Make the bot speak text in voice call |
| `/reset` | Reset conversation history |
| `/help` | Show help message |

## Setup

### Environment Variables

Create a `.env` file with the following variables:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
SESSION_STRING=your_session_string
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://your-api-endpoint.com/v1/chat/completions
MODEL_ID=your-model-id
```

### Local Development

1. Install Python 3.11+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install ffmpeg (required for audio processing):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

### Docker Deployment

Build and run with Docker:

```bash
docker build -t telegram-voice-bot .
docker run -p 8080:8080 --env-file .env telegram-voice-bot
```

### Render Deployment

1. Create a new Web Service on Render
2. Connect your repository
3. Set the following:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: 8080
4. Add environment variables from your `.env` file
5. Deploy

The bot includes a health check endpoint at `http://your-service.onrender.com/health` for UptimeRobot monitoring.

## Architecture

```
main.py                 # Entry point, command handlers
├── config.py           # Configuration management
├── voice_handler.py    # Voice call management
├── ai_handler.py       # AI response generation
├── tts_handler.py      # Text-to-speech conversion
├── stt_handler.py      # Speech-to-text transcription
└── health_server.py    # Health check endpoint
```

## How It Works

1. **Join Call**: Bot joins voice chat using pytgcalls
2. **Listen**: Continuously listens to audio in the call
3. **Transcribe**: Converts speech to text using Whisper
4. **Process**: Sends transcribed text to AI API
5. **Generate Speech**: Converts AI response to audio using EdgeTTS
6. **Speak**: Streams audio back to the voice call

## Voice Options

EdgeTTS supports multiple voices. Default is `en-US-AndrewNeural`. You can modify the voice in `tts_handler.py`:

```python
self.voice = "en-US-AndrewNeural"  # Male voice
# Or
self.voice = "en-US-JennyNeural"   # Female voice
```

## Troubleshooting

### Bot can't join voice call
- Ensure there's an active voice chat in the group
- Check that the userbot has permission to access the chat
- Verify pytgcalls is properly installed

### No audio output
- Ensure ffmpeg is installed in the container
- Check audio file generation in the `temp_audio` directory
- Verify EdgeTTS is working properly

### STT not working
- Check that audio files are being captured
- Ensure Whisper model downloaded successfully
- Verify audio file format is supported

### Health check failing
- Ensure port 8080 is exposed and accessible
- Check that the health server started successfully
- Verify firewall settings

## Performance Notes

- **Whisper Model**: Uses `base` model for speed/accuracy balance
- **AI Responses**: Limited to 150 tokens for faster responses
- **Conversation History**: Keeps last 10 message pairs
- **Audio Cleanup**: Automatically removes temporary audio files

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
