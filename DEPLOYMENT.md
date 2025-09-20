# Deployment Guide

This guide covers deploying the IT Help Desk Voice Bot to production.

## Prerequisites

- LiveKit Cloud account (free trial available)
- Vercel account (for frontend)
- Railway account (for backend)
- GitHub repository

## Step 1: LiveKit Cloud Setup

1. Go to [LiveKit Cloud](https://cloud.livekit.io/)
2. Create a new project
3. Note down your:
   - Project URL (e.g., `wss://your-project.livekit.cloud`)
   - API Key
   - API Secret

## Step 2: Backend Deployment (Railway)

1. Go to [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Create a new project from your repository
4. Select the backend service
5. Set the following environment variables:
   ```
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   DATABASE_URL=sqlite:///./tickets.db
   PORT=8000
   HOST=0.0.0.0
   ```
6. Set the start command: `python run_server.py`
7. Deploy the service
8. Note the deployed URL (e.g., `https://your-backend.railway.app`)

## Step 3: Frontend Deployment (Vercel)

1. Go to [Vercel](https://vercel.com/)
2. Import your GitHub repository
3. Set the build settings:
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `frontend/dist`
   - Install Command: `npm install && cd frontend && npm install`
4. Set environment variables:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
5. Deploy the frontend
6. Note the deployed URL (e.g., `https://your-frontend.vercel.app`)

## Step 4: Running the LiveKit Agent

The LiveKit agent needs to run continuously to handle voice conversations. You can run it on Railway as a separate service:

1. Create a new service in Railway
2. Use the same repository
3. Set environment variables (same as backend)
4. Set the start command: `python run_agent.py`
5. Deploy the service

## Step 5: Testing the Deployment

1. Open your frontend URL
2. Click "Join Call"
3. Allow microphone access
4. Test the voice conversation flow
5. Verify ticket creation works

## Production Considerations

### Security
- Use environment variables for all sensitive data
- Enable HTTPS for all services
- Consider rate limiting for API endpoints
- Implement proper CORS policies

### Performance
- Monitor LiveKit usage and costs
- Consider using a production database (PostgreSQL) instead of SQLite
- Implement proper logging and monitoring
- Set up health checks

### Scaling
- LiveKit Cloud handles scaling automatically
- Consider multiple agent instances for high availability
- Implement database connection pooling
- Use a CDN for frontend assets

## Troubleshooting

### Common Issues

1. **Agent not responding**: Check if the agent service is running and connected to LiveKit
2. **Token generation fails**: Verify LiveKit credentials and API endpoint
3. **Audio not working**: Check browser permissions and LiveKit connection
4. **Database errors**: Ensure database file permissions and persistence

### Monitoring

- Check Railway logs for backend issues
- Monitor LiveKit Cloud dashboard for connection issues
- Use browser developer tools for frontend debugging
- Check Vercel function logs for API issues

## Cost Optimization

- LiveKit Cloud: Pay per usage (free tier available)
- Vercel: Free tier for frontend hosting
- Railway: Pay per usage for backend hosting
- Monitor usage and optimize as needed

## Support

For issues with:
- LiveKit: Check [LiveKit documentation](https://docs.livekit.io/)
- Railway: Check [Railway documentation](https://docs.railway.app/)
- Vercel: Check [Vercel documentation](https://vercel.com/docs)
