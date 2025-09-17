#!/bin/bash
# Safe Worlds API Startup Script

echo "🌟 Starting Safe Worlds API Server..."
echo "📝 Features: Emotion Analysis → World Generation → Story → Audio (Murf AI) → Video"
echo ""

# Check if virtual environment exists
if [ ! -d "../svenv" ]; then
    echo "❌ Virtual environment not found at ../svenv"
    echo "   Please activate your virtual environment first"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../svenv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import fastapi, murf, langchain" 2>/dev/null || {
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
}

# Start the server
echo "🚀 Starting FastAPI server on http://127.0.0.1:8004"
echo "📖 API Documentation: http://127.0.0.1:8004/docs"
echo "🔍 Test the API: python test_api.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=" * 50

python main.py
