# IT Help Desk Voice Bot

A real-time IT Help Desk Voice Bot that handles support calls through natural voice conversations using LiveKit, AI models, and a modern web interface.

## Features

- 🎤 Real-time voice conversation using LiveKit
- 🤖 AI-powered conversation handling (STT → LLM → TTS)
- 📋 Automatic ticket creation and management
- 💰 Fixed pricing for 4 supported IT issues
- ✏️ Ability to edit details before confirmation
- 🌐 Modern React frontend with shadcn/ui

## Supported IT Issues & Pricing

- Wi-Fi not working: $20
- Email login issues (password reset): $15
- Slow laptop performance (CPU change): $25
- Printer problems (power plug change): $10

## Architecture

```
[ React Frontend ] (Vercel)
         |
         v
  [ LiveKit Cloud ]  <--- Real-time audio streaming
         |
         v
  [ Python Backend ] (Railway)
         |
         v
  [ SQLite Database ] (Ticket storage)
```

## Tech Stack

### Backend
- Python with LiveKit Agents SDK
- Hugging Face Whisper (Speech-to-Text)
- Hugging Face Mistral-7B (Language Model)
- Coqui XTTS (Text-to-Speech)
- SQLite (Ticket database)
- FastAPI (Token endpoint)

### Frontend
- React with TypeScript
- shadcn/ui components
- LiveKit Client SDK
- Tailwind CSS

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- LiveKit Cloud account (free trial available)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd it-help-desk-bot
```

2. Install all dependencies:
```bash
npm run install:all
```

3. Set up environment variables:
```bash
# Copy example env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

4. Get your LiveKit Cloud credentials and configure them in `backend/.env`:
   - Go to [LiveKit Cloud](https://cloud.livekit.io/)
   - Create a new project or use existing one
   - Copy your Project URL, API Key, and API Secret
   - Update `backend/.env` with your credentials:
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

5. Start development servers:
```bash
# Terminal 1: Backend server
cd backend && source venv/bin/activate && python run_server.py

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: LiveKit agent
cd backend && source venv/bin/activate && python run_agent.py
```

This will start:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- LiveKit Agent: Connected to LiveKit Cloud

## Usage

1. Open the frontend in your browser
2. Click "Join Call" to start the voice conversation
3. Follow the bot's prompts to:
   - Provide your name and email
   - Give your phone number and address
   - Describe your IT issue
   - Confirm ticket creation
4. Receive your confirmation number

## Example Conversation

**Bot:** "Welcome to IT Help Desk. May I have your name and email?"

**User:** "I'm Alice, alice@example.com."

**Bot:** "Thanks, Alice. What's your phone number and address?"

**User:** "555-1234, 10 Main Street."

**Bot:** "Got it. What issue are you facing?"

**User:** "My laptop is slow."

**Bot:** "That's a supported issue. The service fee is $25. Should I create a ticket?"

**User:** "Yes."

**Bot:** "Ticket created. Your confirmation number is 42. You'll get a confirmation at alice@example.com. Thank you!"

## Project Structure

```
it-help-desk-bot/
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── lib/
│   ├── package.json
│   └── ...
├── backend/            # Python backend
│   ├── app.py         # FastAPI server
│   ├── agent.py       # LiveKit agent
│   ├── models.py      # Database models
│   ├── tools.py       # Bot tools (create_ticket, edit_ticket)
│   ├── requirements.txt
│   └── ...
├── package.json       # Root package.json
└── README.md
```

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set build command: `cd frontend && npm run build`
3. Set output directory: `frontend/dist`
4. Add environment variables for LiveKit configuration

### Backend (Railway)
1. Connect your GitHub repository to Railway
2. Set start command: `cd backend && python app.py`
3. Add environment variables for LiveKit and database configuration
4. Enable persistent volume for SQLite database

## Development

### Backend Development
```bash
cd backend
python app.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
