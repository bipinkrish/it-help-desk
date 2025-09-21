# IT Help Desk Voice Bot 🎤

A real-time AI-powered IT Help Desk that handles support calls through natural voice conversations using LiveKit Cloud and modern AI models.

## ✨ Features

- 🎤 **Real-time voice conversation** using LiveKit Cloud
- 🤖 **AI-powered conversation** (STT → LLM → TTS pipeline)
- 🌐 **Modern React frontend** with Next.js and shadcn/ui
- ☁️ **Cloud-based deployment** (no local server needed)

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- LiveKit Cloud account (free)
- API keys for Groq, Deepgram

## 🏗️ Architecture

```
[ React Frontend ] ←→ [ LiveKit Cloud ] ←→ [ Python Agent ]
     (Port 3000)         (Real-time)         (Groq + Deepgra)
```

## Get API Keys

**Groq (Free LLM):**
- Go to [console.groq.com](https://console.groq.com)
- Sign up and Create API key

**Deepgram (Speech-to-Text and Text-to-Speech):**
- Go to [deepgram.com](https://deepgram.com)
- Sign up and get API key

**LiveKit Cloud:**
- Go to [cloud.livekit.io](https://cloud.livekit.io)
- Create project and get credentials

## 📁 Project Structure

```
it-help-desk/
├── agent/                       # Python agent (deployed to LiveKit Cloud)
│   ├── src/                    # Agent source code
│   │   ├── agent.py           # Main agent logic
│   │   ├── models.py          # Database models
│   │   └── tools.py           # Agent tools (create_ticket, edit_ticket)
│   ├── config/                # Configuration files
│   │   └── agent_config.py    # Model settings and Agent prompts
│   ├── env.example           # Environment template
│   ├── Dockerfile            # For deployment
│   └── livekit.toml          # LiveKit configuration
├── app/                       # Next.js frontend
│   ├── api/                  # API routes
│   └── components/           # React components
├── components/               # Shared UI components
├── .github/workflows/        # GitHub Actions
├── .env.example             # Environment template
├── deploy.sh                # One-click deployment
└── README.md               # This file
```

## 🔧 Manual Setup

If you prefer manual setup:

```bash
# Deploy agent
./deploy.sh

# Install dependencies
npm install

# Start frontend  
npm run dev
```

## 🆘 Troubleshooting

**Agent not responding?**
- Check `lk agent logs` for errors
- Verify API keys in `.env`
- Ensure agent is deployed: `lk agent status`

**Frontend not connecting?**
- Ensure agent is deployed: `lk agent status`
- Check browser console for errors
- Verify LiveKit credentials

**No audio?**
- Allow microphone permissions in browser
- Check if agent is running: `lk agent status`
- Verify STT/TTS API keys

## 📚 Learn More

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Cloud](https://cloud.livekit.io/)
- [Groq API](https://console.groq.com/)
- [Deepgram API](https://deepgram.com/)