import requests
import json
import os
from typing import Optional, Dict, Any
from config import Config

class ElevenLabsSTT:
    """Speech-to-Text service using ElevenLabs API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
    def transcribe_audio_file(self, audio_file_path: str, model_id: str = "scribe_v1") -> Optional[str]:
        """Transcribe audio file to text using ElevenLabs STT"""
        try:
            # Read the audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                
            # Prepare the request
            url = f"{self.base_url}/speech-to-text"
            
            # ElevenLabs STT API expects multipart/form-data with model_id
            files = {
                'file': ('audio.wav', audio_data, 'audio/wav')
            }
            
            data = {
                'model_id': model_id
            }
            
            headers = {
                "xi-api-key": self.api_key
            }
            
            # Make the API request
            response = requests.post(url, files=files, data=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '').strip()
            else:
                print(f"STT API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in STT transcription: {e}")
            return None
            
    def transcribe_audio_data(self, audio_data: bytes, sample_rate: int = 16000) -> Optional[str]:
        """Transcribe raw audio data to text"""
        try:
            # Save audio data to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
                
            # Transcribe the temporary file
            result = self.transcribe_audio_file(temp_path)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return result
            
        except Exception as e:
            print(f"Error in audio data transcription: {e}")
            return None
            
    def is_available(self) -> bool:
        """Check if the STT service is available"""
        try:
            # Test the API with a simple request to voices endpoint
            url = f"{self.base_url}/voices"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False

class GoogleSTT:
    """Alternative STT service using Google Speech-to-Text (fallback)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://speech.googleapis.com/v1/speech:recognize"
        
    def transcribe_audio_file(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file using Google Speech-to-Text"""
        try:
            import base64
            
            # Read and encode audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_content = base64.b64encode(audio_file.read()).decode('utf-8')
                
            # Prepare request body
            request_body = {
                "config": {
                    "encoding": "LINEAR16",
                    "sampleRateHertz": 16000,
                    "languageCode": "en-US",
                    "enableAutomaticPunctuation": True
                },
                "audio": {
                    "content": audio_content
                }
            }
            
            # Make API request
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, json=request_body)
            
            if response.status_code == 200:
                result = response.json()
                if 'results' in result and len(result['results']) > 0:
                    return result['results'][0]['alternatives'][0]['transcript']
                return ""
            else:
                print(f"Google STT error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in Google STT transcription: {e}")
            return None

class STTService:
    """Main STT service that can use multiple providers"""
    
    def __init__(self, primary_provider: str = "elevenlabs"):
        self.primary_provider = primary_provider
        self.elevenlabs_stt = ElevenLabsSTT()
        self.google_stt = GoogleSTT()  # Fallback if needed
        
    def transcribe(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file using the configured provider"""
        if self.primary_provider == "elevenlabs":
            result = self.elevenlabs_stt.transcribe_audio_file(audio_file_path)
            if result is None and self.google_stt.api_key:
                print("ElevenLabs STT failed, trying Google STT...")
                result = self.google_stt.transcribe_audio_file(audio_file_path)
            return result
        else:
            return self.google_stt.transcribe_audio_file(audio_file_path)
            
    def is_available(self) -> bool:
        """Check if STT service is available"""
        if self.primary_provider == "elevenlabs":
            return self.elevenlabs_stt.is_available()
        else:
            return self.google_stt.api_key is not None
