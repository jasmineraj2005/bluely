import requests
import json
import os
import tempfile
import pygame
import threading
import queue
from typing import Optional, Dict, Any
from config import Config
import elevenlabs

class ElevenLabsTTS:
    """Text-to-Speech service using ElevenLabs API"""
    
    def __init__(self, api_key: str = None, voice_id: str = None):
        self.api_key = api_key or Config.ELEVENLABS_API_KEY
        self.voice_id = voice_id or Config.ELEVENLABS_VOICE_ID
        
        # Set the API key for ElevenLabs
        elevenlabs.set_api_key(self.api_key)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
    def text_to_speech(self, text: str, voice_id: str = None, model_id: str = "eleven_monolingual_v1") -> Optional[str]:
        """Convert text to speech and return audio file path"""
        try:
            voice = voice_id or self.voice_id
            
            # Use ElevenLabs library to generate speech
            audio = elevenlabs.generate(
                text=text,
                voice=voice,
                model=model_id
            )
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(audio)
                return temp_file.name
                
        except Exception as e:
            print(f"Error in TTS conversion: {e}")
            return None
            
    def speak_text(self, text: str, voice_id: str = None, blocking: bool = True) -> bool:
        """Convert text to speech and play it immediately"""
        try:
            # Generate audio file
            audio_file = self.text_to_speech(text, voice_id)
            if not audio_file:
                return False
                
            # Play the audio
            success = self.play_audio_file(audio_file, blocking)
            
            # Clean up temporary file
            try:
                os.unlink(audio_file)
            except:
                pass
                
            return success
            
        except Exception as e:
            print(f"Error in speak_text: {e}")
            return False
            
    def play_audio_file(self, audio_file_path: str, blocking: bool = True) -> bool:
        """Play audio file using pygame"""
        try:
            # Load and play audio
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.play()
            
            if blocking:
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                    
            return True
            
        except Exception as e:
            print(f"Error playing audio file: {e}")
            return False
            
    def stop_audio(self):
        """Stop current audio playback"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
            
    def get_available_voices(self) -> Optional[Dict[str, Any]]:
        """Get list of available voices"""
        try:
            voices = elevenlabs.voices()
            return {"voices": [{"voice_id": voice.voice_id, "name": voice.name} for voice in voices]}
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return None
            
    def is_available(self) -> bool:
        """Check if TTS service is available"""
        try:
            # Test with a simple request
            voices = self.get_available_voices()
            return voices is not None
        except:
            return False

class TTSService:
    """Main TTS service with queue management for real-time playback"""
    
    def __init__(self, primary_provider: str = "elevenlabs"):
        self.primary_provider = primary_provider
        self.elevenlabs_tts = ElevenLabsTTS()
        self.audio_queue = queue.Queue()
        self.is_playing = False
        self.playback_thread = None
        
    def speak(self, text: str, voice_id: str = None, blocking: bool = True) -> bool:
        """Convert text to speech and play it"""
        if self.primary_provider == "elevenlabs":
            return self.elevenlabs_tts.speak_text(text, voice_id, blocking)
        else:
            return False
            
    def queue_speech(self, text: str, voice_id: str = None):
        """Queue text for speech (non-blocking)"""
        self.audio_queue.put((text, voice_id))
        if not self.is_playing:
            self._start_playback_thread()
            
    def _start_playback_thread(self):
        """Start the playback thread"""
        if self.playback_thread and self.playback_thread.is_alive():
            return
            
        self.is_playing = True
        self.playback_thread = threading.Thread(target=self._playback_worker)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
    def _playback_worker(self):
        """Worker thread for processing queued speech"""
        while self.is_playing:
            try:
                # Get next item from queue
                text, voice_id = self.audio_queue.get(timeout=1.0)
                
                # Convert and play
                self.speak(text, voice_id, blocking=True)
                
                # Mark task as done
                self.audio_queue.task_done()
                
            except queue.Empty:
                # No more items in queue, stop playing
                self.is_playing = False
                break
            except Exception as e:
                print(f"Error in playback worker: {e}")
                self.is_playing = False
                break
                
    def stop_all(self):
        """Stop all audio playback and clear queue"""
        self.is_playing = False
        self.elevenlabs_tts.stop_audio()
        
        # Clear the queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
                self.audio_queue.task_done()
            except queue.Empty:
                break
                
    def is_available(self) -> bool:
        """Check if TTS service is available"""
        if self.primary_provider == "elevenlabs":
            return self.elevenlabs_tts.is_available()
        else:
            return False
            
    def get_voice_info(self) -> Dict[str, Any]:
        """Get information about available voices"""
        if self.primary_provider == "elevenlabs":
            voices = self.elevenlabs_tts.get_available_voices()
            if voices:
                return {
                    "current_voice": self.elevenlabs_tts.voice_id,
                    "available_voices": len(voices.get("voices", [])),
                    "voices": voices.get("voices", [])[:5]  # First 5 voices
                }
        return {"error": "No voice information available"}

class AudioPlayer:
    """Simple audio player for testing and fallback"""
    
    def __init__(self):
        pygame.mixer.init()
        
    def play_file(self, file_path: str) -> bool:
        """Play audio file"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
            return True
        except Exception as e:
            print(f"Error playing audio file: {e}")
            return False
            
    def stop(self):
        """Stop audio playback"""
        pygame.mixer.music.stop()
