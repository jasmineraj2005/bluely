#!/bin/bash
# Setup script for Bluely STT-TTS System

echo "🚀 Setting up Bluely STT-TTS System"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️ No .env file found. Creating from template..."
    cat > .env << EOF
# Environment Variables for Bluely STT-TTS System
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
SAMPLE_RATE=16000
CHUNK_SIZE=1024
RECORD_SECONDS=5
EOF
    echo "📝 Created .env file. Please edit it with your API keys."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the system: python run.py"
echo ""
echo "To activate virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate virtual environment:"
echo "  deactivate"
