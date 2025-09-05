#!/usr/bin/env python3
"""
Example usage of the Real-Time STT-TTS Flow components
This script demonstrates how to use individual components
"""

import os
import time
from config import Config
from audio_capture import AudioCapture
from stt_service import STTService
from openai_agent import OpenAIAgent
from tts_service import TTSService

def example_audio_capture():
    """Example of using audio capture"""
    print("🎤 Audio Capture Example")
    print("-" * 30)
    
    with AudioCapture() as audio:
        print("Recording for 5 seconds...")
        audio.start_recording()
        time.sleep(5)
        audio.stop_recording()
        
        # Get recorded audio
        audio_file = audio.get_audio_file(timeout=2.0)
        if audio_file:
            print(f"✅ Audio saved to: {audio_file}")
            return audio_file
        else:
            print("❌ No audio captured")
            return None

def example_stt(audio_file):
    """Example of using STT service"""
    if not audio_file:
        print("❌ No audio file for STT")
        return None
        
    print("\n🗣️ Speech-to-Text Example")
    print("-" * 30)
    
    stt = STTService()
    if stt.is_available():
        text = stt.transcribe(audio_file)
        if text:
            print(f"✅ Transcribed: {text}")
            return text
        else:
            print("❌ Transcription failed")
    else:
        print("❌ STT service not available")
    return None

def example_openai(text):
    """Example of using OpenAI agent"""
    if not text:
        print("❌ No text for OpenAI processing")
        return None
        
    print("\n🤖 OpenAI Agent Example")
    print("-" * 30)
    
    agent = OpenAIAgent()
    if agent.is_available():
        response = agent.process_input(text)
        print(f"✅ AI Response: {response}")
        return response
    else:
        print("❌ OpenAI service not available")
    return None

def example_tts(text):
    """Example of using TTS service"""
    if not text:
        print("❌ No text for TTS")
        return
        
    print("\n🔊 Text-to-Speech Example")
    print("-" * 30)
    
    tts = TTSService()
    if tts.is_available():
        success = tts.speak(text)
        if success:
            print("✅ Speech played successfully")
        else:
            print("❌ Speech playback failed")
    else:
        print("❌ TTS service not available")

def example_conversation_flow():
    """Example of the complete conversation flow"""
    print("\n🔄 Complete Conversation Flow Example")
    print("=" * 50)
    
    # Step 1: Capture audio
    audio_file = example_audio_capture()
    
    # Step 2: Transcribe audio
    text = example_stt(audio_file)
    
    # Step 3: Process with OpenAI
    response = example_openai(text)
    
    # Step 4: Convert to speech
    example_tts(response)
    
    # Cleanup
    if audio_file and os.path.exists(audio_file):
        os.unlink(audio_file)
        print(f"\n🧹 Cleaned up: {audio_file}")

def example_voice_settings():
    """Example of configuring voice settings"""
    print("\n🎛️ Voice Settings Example")
    print("-" * 30)
    
    tts = TTSService()
    if tts.is_available():
        voice_info = tts.get_voice_info()
        print("Available voice information:")
        for key, value in voice_info.items():
            print(f"  {key}: {value}")
    else:
        print("❌ TTS service not available")

def example_conversation_context():
    """Example of conversation context management"""
    print("\n💬 Conversation Context Example")
    print("-" * 30)
    
    agent = OpenAIAgent()
    if agent.is_available():
        # First exchange
        response1 = agent.process_input("Hello, my name is John")
        print(f"AI: {response1}")
        
        # Second exchange (should remember the name)
        response2 = agent.process_input("What's my name?")
        print(f"AI: {response2}")
        
        # Show conversation context
        context = agent.get_conversation_context()
        print(f"\nConversation Context:\n{context}")
    else:
        print("❌ OpenAI service not available")

def main():
    """Main example function"""
    print("📚 Real-Time STT-TTS Flow Examples")
    print("=" * 50)
    
    # Check configuration
    try:
        Config.validate()
        print("✅ Configuration validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set up your .env file with API keys")
        return
    
    # Run examples
    try:
        # Individual component examples
        example_voice_settings()
        example_conversation_context()
        
        # Complete flow example (uncomment to test)
        # example_conversation_flow()
        
        print("\n✅ Examples completed successfully!")
        print("\nTo run the complete flow example, uncomment the line in main()")
        print("To start the real-time conversation, run: python main.py")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
