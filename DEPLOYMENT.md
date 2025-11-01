# Deployment Guide

This guide provides detailed instructions for deploying the Telegram Voice Call Bot to various platforms.

## Table of Contents

1. [Render Deployment](#render-deployment)
2. [Docker Hub Deployment](#docker-hub-deployment)
3. [Local Development](#local-development)
4. [Environment Variables](#environment-variables)
5. [UptimeRobot Setup](#uptimerobot-setup)
6. [Troubleshooting](#troubleshooting)

## Render Deployment

### Option 1: Using render.yaml (Recommended)

1. Fork or clone this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml`
6. Add the required environment variables:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `SESSION_STRING`
   - `OPENAI_API_KEY`
7. Click "Apply" to deploy

### Option 2: Manual Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your repository
4. Configure:
   - **Name**: telegram-voice-bot
   - **Environment**: Docker
   - **Dockerfile Path**: ./Dockerfile
   - **Plan**: Free
   - **Port**: 8080
5. Add environment variables (see [Environment Variables](#environment-variables))
6. Click "Create Web Service"

### Post-Deployment

Once deployed, your bot will be available at:
```
https://your-service-name.onrender.com
```

Health check endpoint:
```
https://your-service-name.onrender.com/health
```

## Docker Hub Deployment

### Build and Push

```bash
# Build the image
docker build -t your-username/telegram-voice-bot:latest .

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push your-username/telegram-voice-bot:latest

# Run the container
docker run -d \
  --name telegram-voice-bot \
  -p 8080:8080 \
  --env-file .env \
  your-username/telegram-voice-bot:latest
```

### Using Docker Compose

```bash
# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

## Local Development

### Prerequisites

- Python 3.11 or higher
- ffmpeg installed on your system
- Virtual environment (recommended)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd telegram-voice-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env
# Edit .env with your actual values

# Run the bot
python main.py
```

### Testing Locally

1. Start the bot: `python main.py`
2. Open Telegram and find your userbot
3. Create or join a group with voice chat
4. Start a voice chat in the group
5. Send `/joincall` command
6. Test other commands: `/speak`, `/callstatus`, etc.

## Environment Variables

### Required Variables

```env
API_ID=your_api_id                  # Get from https://my.telegram.org
API_HASH=your_api_hash              # Get from https://my.telegram.org
BOT_TOKEN=your_bot_token            # Optional, for bot functionality
SESSION_STRING=your_session_string  # Generated Telethon session string
OPENAI_API_KEY=your_api_key        # AI API key
OPENAI_BASE_URL=https://your-api-endpoint.com/v1/chat/completions
MODEL_ID=your-model-id             # AI model identifier
GROQ_API_KEY=gsk_free              # Groq API key (free tier default)
```

### Optional Variables

```env
PORT=8080                           # Health check server port (default: 8080)
```

### Getting API_ID and API_HASH

1. Go to https://my.telegram.org
2. Login with your phone number
3. Click "API development tools"
4. Create a new application
5. Copy your `api_id` and `api_hash`

### Generating SESSION_STRING

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = your_api_id
API_HASH = "your_api_hash"

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Session String:", client.session.save())
```

## UptimeRobot Setup

Keep your Render service alive with UptimeRobot:

1. Go to [UptimeRobot](https://uptimerobot.com/)
2. Create a free account
3. Add New Monitor:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Telegram Voice Bot
   - **URL**: `https://your-service.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
4. Save the monitor

UptimeRobot will ping your service every 5 minutes to keep it alive.

## Troubleshooting

### Bot won't start

**Check logs:**
```bash
# Docker
docker logs telegram-voice-bot

# Docker Compose
docker-compose logs -f

# Render
View logs in Render dashboard
```

**Common issues:**
- Invalid SESSION_STRING
- Missing environment variables
- API credentials expired

### Can't join voice call

**Symptoms:** `/joincall` fails

**Solutions:**
1. Ensure there's an active voice chat in the group
2. Check bot has permission to access the group
3. Verify pytgcalls is properly initialized
4. Check logs for specific errors

### No audio output

**Symptoms:** Bot joins but doesn't speak

**Solutions:**
1. Verify ffmpeg is installed (check Dockerfile)
2. Check EdgeTTS is working: `edge-tts --list-voices`
3. Ensure audio files are being generated in `temp_audio/`
4. Check file permissions

### STT not transcribing

**Symptoms:** Bot doesn't respond to speech

**Solutions:**
1. Ensure Groq API key is set correctly (default: gsk_free)
2. Check internet connectivity for API access
3. Check audio input format is supported
4. Verify microphone permissions in group call
5. Test with `/speak` command first

### Health check failing

**Symptoms:** UptimeRobot shows service down

**Solutions:**
1. Verify port 8080 is exposed and accessible
2. Check health server started: Look for "Health check server started" in logs
3. Test manually: `curl https://your-service.onrender.com/health`
4. Check firewall/network settings

### Memory issues

**Symptoms:** Bot crashes with OOM errors

**Solutions:**
1. Upgrade Render plan for more memory (Note: Groq API significantly reduces memory usage)
2. Reduce conversation history limit
3. Clean up temporary audio files more aggressively
4. Monitor memory usage in Render dashboard

### API rate limiting

**Symptoms:** AI responses fail intermittently

**Solutions:**
1. Check API quota and limits
2. Add retry logic with exponential backoff
3. Reduce AI response frequency
4. Consider caching responses

## Monitoring

### Logs

Always monitor logs to diagnose issues:

```bash
# Docker
docker logs -f telegram-voice-bot

# Docker Compose
docker-compose logs -f bot

# Render
Dashboard → Your Service → Logs tab
```

### Health Check

Test the health endpoint:

```bash
curl https://your-service.onrender.com/health
```

Expected response: `OK` with status `200`

## Performance Tips

1. **Groq Whisper API** provides fast cloud-based transcription with no model loading
2. **Limit conversation history** to 10 messages to save memory
3. **Clean up audio files** after use to save disk space
4. **Use async operations** everywhere (already implemented)
5. **Monitor resource usage** in Render dashboard

## Security Best Practices

1. **Never commit .env** to version control (already in .gitignore)
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Limit bot permissions** to minimum required
5. **Monitor access logs** for suspicious activity

## Support

For issues and questions:
- Check logs first
- Review this troubleshooting guide
- Open an issue on GitHub
- Check Telethon and pytgcalls documentation

## Useful Links

- [Telethon Documentation](https://docs.telethon.dev/)
- [pytgcalls Documentation](https://pytgcalls.github.io/)
- [EdgeTTS Documentation](https://github.com/rany2/edge-tts)
- [Render Documentation](https://render.com/docs)
- [Groq Documentation](https://console.groq.com/docs)
