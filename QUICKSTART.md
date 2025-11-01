# Quick Start Guide

Get your Telegram Voice Call Bot running in 5 minutes!

## Prerequisites

- Python 3.11+ (for local) OR Docker (for containerized)
- Telegram account
- Active voice chat in a group

## Step 1: Get Telegram Credentials

### 1.1 Get API_ID and API_HASH

1. Visit https://my.telegram.org
2. Log in with your phone number
3. Click "API development tools"
4. Create an application
5. Copy your `api_id` and `api_hash`

### 1.2 Generate Session String

```bash
# Install dependencies
pip install telethon

# Run the session generator
python generate_session.py
```

Enter your API credentials and phone number when prompted.

## Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

Required variables:
```env
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_STRING=your_session_string
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://your-endpoint.com/v1/chat/completions
MODEL_ID=your-model-id
```

## Step 3: Run the Bot

### Option A: Docker (Recommended)

```bash
# Build the image
docker build -t telegram-voice-bot .

# Run the container
docker run -d \
  --name voice-bot \
  -p 8080:8080 \
  --env-file .env \
  telegram-voice-bot

# View logs
docker logs -f voice-bot
```

### Option B: Docker Compose

```bash
# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### Option C: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (required)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Run the bot
python main.py
```

## Step 4: Test the Bot

1. Open Telegram
2. Go to a group where you have admin access
3. Start a voice chat in the group
4. Send commands to test:

```
/help        - See all commands
/joincall    - Bot joins the voice chat
/callstatus  - Check if bot is in the call
/speak Hello - Bot speaks "Hello" in the voice chat
/leavecall   - Bot leaves the voice chat
```

## Step 5: Deploy to Render (Optional)

### 5.1 Prepare Repository

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/telegram-voice-bot.git
git push -u origin main
```

### 5.2 Deploy on Render

1. Go to https://dashboard.render.com/
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: telegram-voice-bot
   - **Environment**: Docker
   - **Port**: 8080
5. Add environment variables from your .env
6. Click "Create Web Service"

### 5.3 Keep It Alive

1. Sign up at https://uptimerobot.com/
2. Add New Monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://your-service.onrender.com/health`
   - **Interval**: 5 minutes
3. Your bot will stay alive 24/7!

## Troubleshooting

### Bot won't start

**Check:** Logs for error messages
```bash
# Docker
docker logs voice-bot

# Local
Check terminal output
```

**Solution:** Verify all environment variables are correct

### Can't join voice call

**Check:** Is there an active voice chat?

**Solution:** Start a voice chat in the group first, then use `/joincall`

### No audio output

**Check:** Is ffmpeg installed?
```bash
ffmpeg -version
```

**Solution:** Install ffmpeg using your package manager

### Session expired

**Solution:** Generate a new session string using `generate_session.py`

## Common Commands

```bash
# View logs (Docker)
docker logs -f voice-bot

# Restart bot (Docker)
docker restart voice-bot

# Stop bot (Docker)
docker stop voice-bot

# Remove container (Docker)
docker rm voice-bot

# Rebuild after changes (Docker)
docker build -t telegram-voice-bot .
docker stop voice-bot && docker rm voice-bot
docker run -d --name voice-bot -p 8080:8080 --env-file .env telegram-voice-bot
```

## Next Steps

- Read [README.md](README.md) for detailed features
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for advanced deployment options
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Support

- **Issues?** Check [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section
- **Questions?** Open an issue on GitHub
- **Documentation:** Read all .md files in the repository

## Security Reminder

⚠️ **Never commit your .env file or share your credentials!**

The `.gitignore` file already excludes `.env`, but always double-check before pushing to GitHub.

---

Happy bot building! 🤖🎙️
