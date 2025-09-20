#!/bin/bash

# IT Help Desk Voice Bot - Simple Deployment Script
set -e

echo "🚀 IT Help Desk Voice Bot - Deployment"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "agent/src/agent.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."

if ! command_exists "lk"; then
    echo "❌ LiveKit CLI not found. Installing..."
    if command_exists "brew"; then
        brew install livekit-cli
    else
        echo "Please install LiveKit CLI manually: https://docs.livekit.io/cli/"
        exit 1
    fi
fi

echo "✅ Dependencies OK"

# Deploy the agent to LiveKit Cloud
echo "🤖 Deploying agent to LiveKit Cloud..."
cd agent

# Check if secrets.env exists
if [ ! -f "../.env" ]; then
    echo "❌ .env not found in root directory"
    echo "Please create agent/secrets.env with your API keys:"
    exit 1
fi

# Deploy agent
lk agent deploy --secrets-file ../.env

echo "✅ Agent deployed successfully!"

# Go back to root and start frontend
cd ..
echo "🌐 Starting frontend..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    if command_exists "pnpm"; then
        pnpm install
    else
        npm install
    fi
fi

# Start the Web App
if command_exists "pnpm"; then
    pnpm start
else
    npm run start
fi
