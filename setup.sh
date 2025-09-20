#!/bin/bash

# IT Help Desk Voice Bot Setup Script
# This script sets up the development environment for the IT Help Desk Voice Bot

set -e

echo "🚀 Setting up IT Help Desk Voice Bot..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Create environment files if they don't exist
echo "⚙️  Setting up environment files..."

if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cat > backend/.env << 'EOF'
# LiveKit Cloud Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Database
DATABASE_URL=sqlite:///./tickets.db

# OpenAI (optional - for better LLM performance)
# OPENAI_API_KEY=your-openai-key
EOF
    echo "⚠️  Created backend/.env template - YOU MUST UPDATE WITH YOUR LIVEKIT CLOUD CREDENTIALS"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend/.env.local from template..."
    cp frontend/env.example frontend/.env.local
    echo "✅ Created frontend/.env.local"
fi

# Make scripts executable
chmod +x backend/run_agent.py
chmod +x backend/run_server.py

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Get your LiveKit Cloud credentials:"
echo "   - Go to https://cloud.livekit.io/"
echo "   - Create a new project or use existing one"
echo "   - Copy your Project URL, API Key, and API Secret"
echo ""
echo "2. Update backend/.env with your LiveKit Cloud credentials:"
echo "   - LIVEKIT_URL=wss://your-project.livekit.cloud"
echo "   - LIVEKIT_API_KEY=your-api-key"
echo "   - LIVEKIT_API_SECRET=your-api-secret"
echo ""
echo "3. In a new terminal, start the backend server:"
echo "   cd backend && source venv/bin/activate && python run_server.py"
echo ""
echo "4. In another new terminal, start the frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "5. In another new terminal, start the LiveKit agent:"
echo "   cd backend && source venv/bin/activate && python run_agent.py"
echo ""
echo "6. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For production deployment, see DEPLOYMENT.md"
