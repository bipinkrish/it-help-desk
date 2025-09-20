# IT Help Desk Voice Bot

A real-time IT Help Desk Voice Bot that handles support calls through natural voice conversations using LiveKit Cloud and AI models.

## 🎯 Features

- 🎤 **Real-time voice conversation** using LiveKit Cloud
- 🤖 **AI-powered conversation** (STT → LLM → TTS pipeline)
- 💰 **Fixed pricing** for 4 supported IT issues
- 🌐 **Modern React frontend** with shadcn/ui
- ☁️ **Cloud-based deployment** (no local server needed)

## 📋 Supported IT Issues & Pricing

| Issue | Price | Description |
|-------|-------|-------------|
| Wi-Fi problems | $20 | Network connectivity issues |
| Email login issues | $15 | Password reset and login problems |
| Slow laptop performance | $25 | CPU upgrade and optimization |
| Printer problems | $10 | Hardware and driver issues |

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- LiveKit Cloud account (free)
- API keys for Groq, Deepgram, and Cartesia

### 1. Get API Keys

**Groq (Free LLM):**
- Go to [console.groq.com](https://console.groq.com)
- Sign up (no credit card required)
- Create API key

**Deepgram (Speech-to-Text):**
- Go to [deepgram.com](https://deepgram.com)
- Sign up and get API key

**Cartesia (Text-to-Speech):**
- Go to [cartesia.ai](https://cartesia.ai)
- Sign up and get API key

**LiveKit Cloud:**
- Go to [cloud.livekit.io](https://cloud.livekit.io)
- Create project and get credentials

### 2. Configure Secrets

Create `backend/secrets.env`:
```env
# LiveKit Cloud Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# AI Provider Configuration
GROQ_API_KEY=your_groq_key
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key
```

### 3. Deploy Everything

Run the deployment script:
```bash
./deploy.sh
```

This will:
1. ✅ Deploy the agent to LiveKit Cloud
2. ✅ Start the React frontend
3. ✅ Open http://localhost:3000

## 🎮 Usage

1. **Open** http://localhost:3000
2. **Click** "Start Call" 
3. **Talk** to the IT Help Desk bot
4. **Follow** the conversation flow to create support tickets

## 🏗️ Architecture

```
[ React Frontend ] ←→ [ LiveKit Cloud ] ←→ [ Python Agent ]
     (Port 3000)         (Real-time)         (Groq + Deepgram + Cartesia)
```

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Deploy agent
cd backend
lk agent deploy --secrets-file secrets.env

# Start frontend  
cd ../frontend
npm install
npm run dev
```

## 📁 Project Structure

```
it-help-desk/
├── backend/                    # Python agent (deployed to LiveKit Cloud)
│   ├── src/                   # Agent source code (logic only)
│   │   ├── agent.py          # Main agent logic
│   │   ├── models.py         # Database models
│   │   └── tools.py          # Agent tools
│   ├── config/               # Configuration files
│   │   └── agent_instructions.py # Agent prompts & settings
│   ├── secrets.env           # API keys (not committed)
│   └── Dockerfile            # For deployment
├── frontend/                  # Official LiveKit React starter
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   └── .env.local           # Frontend config (auto-created)
├── deploy.sh                 # One-click deployment script
└── README.md                # This file
```

## 🆘 Troubleshooting

**Agent not responding?**
- Check `lk agent logs` for errors
- Verify API keys in `backend/secrets.env`

**Frontend not connecting?**
- Ensure agent is deployed: `lk agent status`
- Check browser console for errors

**No audio?**
- Allow microphone permissions in browser
- Check if agent is running: `lk agent status`

## 📚 Learn More

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Cloud](https://cloud.livekit.io/)
- [Groq API](https://console.groq.com/)
- [Deepgram API](https://deepgram.com/)
- [Cartesia API](https://cartesia.ai/)

## 📄 License

MIT License - see LICENSE file for details.