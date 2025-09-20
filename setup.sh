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
pip3 install -r requirements.txt
cd ..

# Create environment files if they don't exist
echo "⚙️  Setting up environment files..."

if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/env.example backend/.env
    echo "⚠️  Please edit backend/.env with your LiveKit credentials"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend/.env.local from template..."
    cp frontend/env.example frontend/.env.local
    echo "⚠️  Please edit frontend/.env.local if needed"
fi

# Make scripts executable
chmod +x backend/run_agent.py
chmod +x backend/run_server.py

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit backend/.env with your LiveKit credentials:"
echo "   - LIVEKIT_URL=wss://your-project.livekit.cloud"
echo "   - LIVEKIT_API_KEY=your-api-key"
echo "   - LIVEKIT_API_SECRET=your-api-secret"
echo ""
echo "2. Start the development servers:"
echo "   npm run dev"
echo ""
echo "3. Or start them separately:"
echo "   Backend: cd backend && python run_server.py"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see the README.md file"
