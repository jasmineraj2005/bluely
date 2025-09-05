#!/usr/bin/env python3
"""
Setup script for Real-Time STT-TTS Flow with OpenAI Agent
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"✅ {env_file} already exists")
        return True
        
    print(f"\n📝 Creating {env_file} template...")
    
    env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB

# Audio Configuration (optional)
SAMPLE_RATE=16000
CHUNK_SIZE=1024
RECORD_SECONDS=5
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ {env_file} created successfully")
        print("⚠️  Please edit .env file and add your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create {env_file}: {e}")
        return False

def check_audio_system():
    """Check audio system requirements"""
    print("\n🔊 Checking audio system...")
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("✅ macOS detected - audio should work with PyAudio")
    elif system == "linux":
        print("✅ Linux detected - ensure ALSA/PulseAudio is installed")
    elif system == "windows":
        print("✅ Windows detected - audio should work with PyAudio")
    else:
        print(f"⚠️  Unknown system: {system}")
        
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    required_modules = [
        "pyaudio",
        "openai", 
        "elevenlabs",
        "pygame",
        "numpy",
        "requests"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All imports successful")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Real-Time STT-TTS Flow with OpenAI Agent")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n❌ Setup failed at .env file creation")
        sys.exit(1)
    
    # Check audio system
    check_audio_system()
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed at import testing")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your API keys:")
    print("   - OpenAI API key: https://platform.openai.com/api-keys")
    print("   - ElevenLabs API key: https://elevenlabs.io/app/settings/api-keys")
    print("\n2. Test the system:")
    print("   python main.py test")
    print("\n3. Start a conversation:")
    print("   python main.py")
    print("\n4. Read README.md for detailed instructions")
    print("=" * 60)

if __name__ == "__main__":
    main()
