#!/usr/bin/env python3
"""
Real-Time STT-TTS Flow with OpenAI Agent
Main application that orchestrates the entire conversation flow
"""

import os
import sys
import time
import signal
import threading
from typing import Optional
from config import Config
from audio_capture import AudioCapture
from stt_service import STTService
from openai_agent import OpenAIAgent, IntentProcessor
from tts_service import TTSService
from debug_logger import debug_logger

class RealTimeConversationApp:
    """Main application class for real-time voice conversation"""
    
    def __init__(self):
        self.config = Config()
        self.is_running = False
        self.audio_capture = None
        self.stt_service = None
        self.openai_agent = None
        self.tts_service = None
        self.intent_processor = None
        
        # Conversation state
        self.conversation_active = False
        self.last_activity = time.time()
        self.silence_timeout = 30  # seconds of silence before ending conversation
        
    def initialize_services(self) -> bool:
        """Initialize all required services"""
        try:
            print("Initializing services...")
            
            # Validate configuration
            self.config.validate()
            print("✓ Configuration validated")
            
            # Initialize audio capture
            self.audio_capture = AudioCapture()
            print("✓ Audio capture initialized")
            
            # Initialize STT service
            self.stt_service = STTService()
            if not self.stt_service.is_available():
                print("✗ STT service not available")
                return False
            print("✓ STT service initialized")
            
            # Initialize OpenAI agent
            self.openai_agent = OpenAIAgent()
            if not self.openai_agent.is_available():
                print("✗ OpenAI service not available")
                return False
            print("✓ OpenAI agent initialized")
            
            # Initialize TTS service
            self.tts_service = TTSService()
            if not self.tts_service.is_available():
                print("✗ TTS service not available")
                return False
            print("✓ TTS service initialized")
            
            # Initialize intent processor
            self.intent_processor = IntentProcessor(self.openai_agent)
            print("✓ Intent processor initialized")
            
            return True
            
        except Exception as e:
            print(f"Error initializing services: {e}")
            return False
            
    def start_conversation(self):
        """Start the real-time conversation loop"""
        if not self.initialize_services():
            print("Failed to initialize services. Exiting.")
            return
            
        print("\n" + "="*50)
        print("🎤 Real-Time Voice Conversation Started")
        print("="*50)
        print("Speak naturally - I'll listen and respond!")
        print("Say 'goodbye' or 'exit' to end the conversation")
        print("Press Ctrl+C to stop the application")
        print("="*50 + "\n")
        
        # Welcome message
        self.tts_service.speak("Hello! I'm ready to chat. What would you like to talk about?")
        
        self.is_running = True
        self.conversation_active = True
        
        try:
            # Start audio capture
            self.audio_capture.start_recording()
            
            # Main conversation loop
            self._conversation_loop()
            
        except KeyboardInterrupt:
            print("\n\nStopping conversation...")
        except Exception as e:
            print(f"Error in conversation loop: {e}")
        finally:
            self._cleanup()
            
    def _conversation_loop(self):
        """Main conversation processing loop"""
        while self.is_running and self.conversation_active:
            try:
                # Get latest audio file (no queue, no timeout)
                audio_file = self.audio_capture.get_latest_audio_file()
                
                if audio_file:
                    print(f"🎤 Processing latest audio: {audio_file}")
                    debug_logger.log_audio_capture(audio_file)
                    
                    # Transcribe audio to text
                    transcribed_text = self.stt_service.transcribe(audio_file)
                    debug_logger.log_transcription(audio_file, transcribed_text)
                    
                    if transcribed_text and transcribed_text.strip():
                        print(f"👤 You said: {transcribed_text}")
                        
                        # Check for exit commands
                        if self._is_exit_command(transcribed_text):
                            debug_logger.log_system_event("exit_command_detected", {"text": transcribed_text})
                            self._handle_exit()
                            break
                            
                        # Process with OpenAI agent
                        intent, ai_response = self.intent_processor.process_with_intent(transcribed_text)
                        debug_logger.log_ai_response(transcribed_text, ai_response, intent)
                        print(f"🤖 AI Response: {ai_response}")
                        
                        # Convert response to speech
                        tts_success = self.tts_service.speak(ai_response)
                        debug_logger.log_tts_output(ai_response, success=tts_success)
                        
                        # Update activity timestamp
                        self.last_activity = time.time()
                        
                    else:
                        print("🔇 No speech detected")
                        debug_logger.log_system_event("no_speech_detected")
                    
                    # Clear the processed file
                    self.audio_capture.clear_latest_audio()
                        
                else:
                    # Check for conversation timeout
                    if time.time() - self.last_activity > self.silence_timeout:
                        print("⏰ Conversation timeout - no activity detected")
                        self.tts_service.speak("It seems quiet. I'll be here when you're ready to chat!")
                        self.last_activity = time.time()
                        
            except Exception as e:
                print(f"Error in conversation loop: {e}")
                time.sleep(1)
                
    def _is_exit_command(self, text: str) -> bool:
        """Check if the text contains an exit command"""
        exit_commands = ["goodbye", "exit", "quit", "stop", "bye", "see you later"]
        return any(cmd in text.lower() for cmd in exit_commands)
        
    def _handle_exit(self):
        """Handle exit command"""
        print("👋 Ending conversation...")
        self.tts_service.speak("Goodbye! It was great talking with you!")
        self.conversation_active = False
        
    def _cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        debug_logger.log_system_event("cleanup_started")
        
        if self.audio_capture:
            self.audio_capture.cleanup()
            
        if self.tts_service:
            self.tts_service.stop_all()
            
        # Save debug logs
        debug_logger.save_logs()
        
        self.is_running = False
        print("Cleanup complete.")
        
    def test_services(self):
        """Test all services individually"""
        print("Testing services...")
        
        if not self.initialize_services():
            return False
            
        # Test STT
        print("\n1. Testing STT service...")
        test_audio = "test_audio.wav"  # You would need a test audio file
        if os.path.exists(test_audio):
            result = self.stt_service.transcribe(test_audio)
            print(f"STT Result: {result}")
        else:
            print("No test audio file found, skipping STT test")
            
        # Test OpenAI
        print("\n2. Testing OpenAI agent...")
        test_response = self.openai_agent.process_input("Hello, this is a test.")
        print(f"OpenAI Response: {test_response}")
        
        # Test TTS
        print("\n3. Testing TTS service...")
        success = self.tts_service.speak("This is a test of the text to speech service.")
        print(f"TTS Success: {success}")
        
        return True

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print("\nReceived interrupt signal. Shutting down...")
    sys.exit(0)

def main():
    """Main entry point"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run the application
    app = RealTimeConversationApp()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            app.test_services()
            return
        elif sys.argv[1] == "help":
            print("Usage:")
            print("  python main.py          - Start real-time conversation")
            print("  python main.py test     - Test all services")
            print("  python main.py help     - Show this help")
            return
            
    # Start the conversation
    app.start_conversation()

if __name__ == "__main__":
    main()
