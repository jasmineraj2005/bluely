#!/usr/bin/env python3
"""
Simple run script for the STT-TTS system
"""

import os
import sys
from main import RealTimeConversationApp

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("❌ No .env file found!")
        print("📝 Create a .env file with:")
        print("OPENAI_API_KEY=your_openai_key")
        print("ELEVENLABS_API_KEY=your_elevenlabs_key")
        print("ELEVENLABS_VOICE_ID=your_voice_id")
        return False
    
    # Check for required API keys
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY', 'ELEVENLABS_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment check passed!")
    return True

def main():
    """Main entry point"""
    print("🚀 Starting Bluely STT-TTS System")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup failed. Please fix the issues above.")
        return
    
    # Create and run the application
    try:
        app = RealTimeConversationApp()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == "test":
                print("🧪 Running service tests...")
                app.test_services()
                return
            elif sys.argv[1] == "debug":
                print("🐛 Running in debug mode...")
                # Debug mode - same as normal but with more logging
                app.start_conversation()
                return
            elif sys.argv[1] == "help":
                print("Usage:")
                print("  python run.py          - Start conversation")
                print("  python run.py test      - Test all services")
                print("  python run.py debug     - Start with debug logging")
                print("  python run.py help      - Show this help")
                return
        
        # Start the conversation
        print("🎤 Starting conversation...")
        app.start_conversation()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check your API keys and microphone permissions")

if __name__ == "__main__":
    main()
