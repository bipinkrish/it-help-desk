# IT Help Desk Voice Bot 🎤

A real-time AI-powered IT Help Desk that handles support calls through natural voice conversations using LiveKit Cloud and modern AI models.

## ✨ Features

- 🎤 **Real-time voice conversation** using LiveKit Cloud
- 🤖 **AI-powered conversation** (STT → LLM → TTS pipeline)
- 💰 **Fixed pricing** for 4 supported IT issues
- 🌐 **Modern React frontend** with Next.js and shadcn/ui
- ☁️ **Cloud-based deployment** (no local server needed)
- 🔄 **Auto-deployment** via GitHub Actions

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
- Python 3.11+
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

### 2. Configure Environment

Copy the example environment file:
```bash
cp env.example .env
```

Edit `.env` with your API keys:
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

## 🔄 Auto-Deployment

The project includes GitHub Actions for automatic deployment:

- **Trigger**: Push to `main` branch
- **Action**: Automatically deploys agent to LiveKit Cloud
- **Setup**: Add secrets to GitHub repository

### Required GitHub Secrets:
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `DEEPGRAM_API_KEY`
- `GROQ_API_KEY`
- `CARTESIA_API_KEY`

## 🔧 Manual Setup

If you prefer manual setup:

```bash
# Install dependencies
npm install

# Deploy agent
cd agent
lk agent deploy --secrets-file ../.env

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
- [Cartesia API](https://cartesia.ai/)

## 📄 License

MIT License - see LICENSE file for details.