# Real-Time STT-TTS Flow with OpenAI Agent

A complete real-time voice conversation system that captures audio, converts speech to text, processes it with OpenAI GPT-4, and responds with natural speech using ElevenLabs TTS.

## 🎯 Features

- **Real-time Audio Capture**: Continuous microphone input with voice activity detection
- **Speech-to-Text**: ElevenLabs STT API for accurate transcription
- **AI Processing**: OpenAI GPT-4 with conversation context management
- **Text-to-Speech**: ElevenLabs TTS for natural voice responses
- **Intent Processing**: Smart intent detection and response generation
- **Conversation Management**: Maintains context across the conversation

## 🏗️ Architecture

```
Audio Input → STT → OpenAI GPT-4 → TTS → Audio Output
     ↑                                    ↓
     └─────────── Conversation Loop ──────┘
```

### Components

1. **Audio Capture** (`audio_capture.py`): Real-time microphone input with PyAudio
2. **STT Service** (`stt_service.py`): ElevenLabs Speech-to-Text integration
3. **OpenAI Agent** (`openai_agent.py`): GPT-4 with conversation management
4. **TTS Service** (`tts_service.py`): ElevenLabs Text-to-Speech integration
5. **Main Application** (`main.py`): Orchestrates the entire flow

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Microphone access
- OpenAI API key
- ElevenLabs API key

### Installation

1. **Clone or download the project**

   ```bash
   cd /Users/jasminebaldevraj/Desktop/bluey-test
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:

   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # ElevenLabs Configuration
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ELEVENLABS_VOICE_ID=your_voice_id_here

   # Audio Configuration (optional)
   SAMPLE_RATE=16000
   CHUNK_SIZE=1024
   RECORD_SECONDS=5
   ```

4. **Get API Keys**

   - **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **ElevenLabs**: Get your API key from [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)

5. **Run the application**
   ```bash
   python main.py
   ```

## 🎮 Usage

### Starting a Conversation

```bash
python main.py
```

The system will:

1. Initialize all services
2. Play a welcome message
3. Start listening for your voice
4. Respond naturally to your speech

### Commands

- **Start conversation**: `python main.py`
- **Test services**: `python main.py test`
- **Show help**: `python main.py help`

### Ending a Conversation

Say any of these phrases to end the conversation:

- "goodbye"
- "exit"
- "quit"
- "stop"
- "bye"
- "see you later"

Or press `Ctrl+C` to stop the application.

## ⚙️ Configuration

### Audio Settings

Edit `config.py` or set environment variables:

```python
# Audio Configuration
SAMPLE_RATE = 16000        # Audio sample rate
CHUNK_SIZE = 1024          # Audio chunk size
RECORD_SECONDS = 5         # Recording duration
```

### Conversation Settings

```python
# Conversation Configuration
MAX_CONVERSATION_HISTORY = 10  # Keep last 10 exchanges
```

### Voice Settings

```python
# ElevenLabs Voice Configuration
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Default voice
```

## 🔧 Troubleshooting

### Common Issues

1. **PyAudio Installation Issues**

   ```bash
   # On macOS
   brew install portaudio
   pip install pyaudio

   # On Ubuntu/Debian
   sudo apt-get install python3-pyaudio
   pip install pyaudio

   # On Windows
   pip install pipwin
   pipwin install pyaudio
   ```

2. **Microphone Permission Issues**

   - Grant microphone access to your terminal/IDE
   - Check system audio settings

3. **API Key Issues**

   - Verify your API keys are correct
   - Check API key permissions and quotas
   - Ensure environment variables are loaded

4. **Audio Playback Issues**
   - Install pygame: `pip install pygame`
   - Check system audio output
   - Verify audio drivers

### Testing Services

Run the test command to verify all services:

```bash
python main.py test
```

This will test:

- STT service availability
- OpenAI API connection
- TTS service functionality

## 📁 Project Structure

```
bluey-test/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── audio_capture.py     # Real-time audio capture
├── stt_service.py       # Speech-to-Text service
├── openai_agent.py      # OpenAI GPT-4 integration
├── tts_service.py       # Text-to-Speech service
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔄 Real-Time Flow

1. **Audio Capture**: Continuously captures microphone input
2. **Voice Activity Detection**: Detects when you start/stop speaking
3. **Speech-to-Text**: Converts audio to text using ElevenLabs STT
4. **Intent Processing**: Analyzes the text for user intent
5. **AI Response**: GPT-4 generates contextual response
6. **Text-to-Speech**: Converts response to natural speech
7. **Audio Output**: Plays the response through speakers
8. **Context Update**: Maintains conversation history

## 🎛️ Advanced Configuration

### Custom Voice Settings

```python
# In config.py or .env
ELEVENLABS_VOICE_ID = "your_custom_voice_id"

# Available voices can be found at:
# https://elevenlabs.io/app/voice-library
```

### Custom System Prompt

```python
# In openai_agent.py
self.system_prompt = """Your custom system prompt here..."""
```

### Audio Quality Settings

```python
# In config.py
SAMPLE_RATE = 44100      # Higher quality
CHUNK_SIZE = 2048        # Larger chunks
```

## 🚨 Important Notes

- **API Costs**: This system uses paid APIs (OpenAI and ElevenLabs)
- **Privacy**: Audio is processed by external services
- **Internet Required**: All services require internet connection
- **Microphone Access**: System needs microphone permissions

## 📝 License

This project is for educational and development purposes. Please ensure you comply with the terms of service for OpenAI and ElevenLabs APIs.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this system.

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Run `python main.py test` to diagnose problems
3. Verify your API keys and internet connection
4. Check system audio settings and permissions
