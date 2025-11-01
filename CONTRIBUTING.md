# Contributing to Telegram Voice Call Bot

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Describe the feature clearly
- Explain the use case
- Consider implementation complexity

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/telegram-voice-bot.git
cd telegram-voice-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (if any)
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

## Code Style

- Follow PEP 8 guidelines
- Use async/await for I/O operations
- Add type hints where beneficial
- Keep functions focused and small
- Use descriptive variable names
- Add docstrings to functions and classes

## Testing

Before submitting a PR:

1. Test all commands: `/joincall`, `/leavecall`, `/callstatus`, `/speak`, `/reset`, `/help`
2. Test error handling (invalid inputs, network failures, etc.)
3. Verify health check endpoint works
4. Check Docker build: `docker build -t test .`
5. Run syntax check: `python -m py_compile *.py`

## Documentation

- Update README.md if needed
- Update DEPLOYMENT.md for deployment changes
- Add inline comments for complex logic
- Update docstrings

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add voice pitch control for TTS
fix: Handle network timeout in AI handler
docs: Update deployment guide for Render
refactor: Simplify audio cleanup logic
test: Add unit tests for STT handler
```

## Project Structure

```
main.py                 # Entry point, command handlers
config.py               # Configuration management
voice_handler.py        # Voice call orchestration
ai_handler.py          # AI API integration
tts_handler.py         # Text-to-speech
stt_handler.py         # Speech-to-text
health_server.py       # Health check server
```

## Areas for Contribution

### High Priority
- Improved error handling and recovery
- Better audio quality optimization
- More comprehensive testing
- Performance optimization

### Medium Priority
- Additional TTS voices and languages
- Configurable Whisper models
- Enhanced conversation context
- Admin commands

### Nice to Have
- Web dashboard for monitoring
- Multiple AI model support
- Voice activity detection improvements
- Audio effects and filters

## Questions?

Feel free to open an issue for any questions about contributing!
