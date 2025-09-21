# IT Help Desk Voice Bot 🎤

A real-time AI-powered IT Help Desk that handles support calls through natural voice conversations using LiveKit Cloud, modern AI models, and MongoDB for ticket storage.

## ✨ Features

- 🎤 **Real-time voice conversation** using LiveKit Cloud
- 🤖 **AI-powered conversation** (STT → LLM → TTS pipeline)
- 🌐 **Modern React frontend** with Next.js and shadcn/ui
- 💾 **MongoDB ticket storage** with full CRUD operations
- 📊 **Ticket management dashboard** with table view
- ☁️ **Cloud-based deployment** (no local server needed)

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- LiveKit Cloud account (free)
- MongoDB Atlas account (free)
- API keys for Groq, Deepgram

## 🏗️ Architecture

```
[ React Frontend ] ←→ [ LiveKit Cloud ] ←→ [ Python Agent ]
     (Port 3000)         (Real-time)         (Groq + Deepgram)
                           ↓
                    [ MongoDB Atlas ]
                      (Ticket Storage)
```

## Get API Keys

**Groq (Free LLM):**
- Go to [console.groq.com](https://console.groq.com)
- Sign up and Create API key

**Deepgram (Speech-to-Text and Text-to-Speech):**
- Go to [deepgram.com](https://deepgram.com)
- Sign up and get API key

**MongoDB Atlas (Free Database):**
- Go to [mongodb.com/atlas](https://mongodb.com/atlas)
- Create free cluster
- Get connection string

**LiveKit Cloud:**
- Go to [cloud.livekit.io](https://cloud.livekit.io)
- Create project and get credentials

## 📁 Project Structure

```
it-help-desk/
├── agent/                       # Python agent (deployed to LiveKit Cloud)
│   ├── src/                    # Agent source code
│   │   ├── agent.py           # Main agent logic
│   │   ├── agent_types.py     # Type definitions
│   │   ├── agent_config.py    # Model settings and prompts
│   │   ├── models.py          # Issue identification logic
│   │   └── tools.py           # Agent tools (create_ticket, edit_ticket)
│   ├── Dockerfile            # For deployment
│   ├── requirements.txt      # Python dependencies
│   └── secrets.env           # Agent environment variables
├── app/                       # Next.js frontend
│   ├── api/                  # API routes
│   │   └── tickets/          # Ticket CRUD endpoints
│   └── components/           # React components
├── components/               # Shared UI components
│   ├── TicketsModal.tsx     # Ticket management dashboard
│   └── session-view.tsx     # Main voice interface
├── lib/                     # Utilities
│   ├── mongodb.ts           # MongoDB connection
│   └── models.ts            # TypeScript types
├── .github/workflows/        # GitHub Actions
├── .env.example             # Environment template
├── deploy.sh                # One-click deployment
└── README.md               # This file
```

## 🔧 Manual Setup

### 2. Deploy Agent

Deploy the Python agent to LiveKit Cloud:
```bash
./deploy.sh
```

### 3. Start Frontend

Install dependencies and start the development server:
```bash
npm install
npm run dev
```

Visit `http://localhost:3000` to test the voice interface!

## 🔄 Ticket Flow

1. **User calls** the voice bot
2. **Agent collects** user details and issue description
3. **Agent can edit** ticket details before confirmation (in-memory)
4. **Agent creates** ticket via API call to MongoDB
5. **User receives** confirmation number

### Production URLs
- **Frontend**: Deploy to Vercel/Netlify
- **Agent**: Deployed to LiveKit Cloud
- **Database**: MongoDB Atlas

## 📚 Learn More

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Cloud](https://cloud.livekit.io/)
- [Groq API](https://console.groq.com/)
- [Deepgram API](https://deepgram.com/)
- [MongoDB Atlas](https://mongodb.com/atlas)
