import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')  # Default voice
    
    # Audio Configuration
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1024))
    RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', 5))
    
    # Conversation Configuration
    MAX_CONVERSATION_HISTORY = 10  # Keep last 10 exchanges
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        required_vars = ['OPENAI_API_KEY', 'ELEVENLABS_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
