import React, { useState, useEffect, useRef } from 'react'
import { Room, RoomEvent, Track, RemoteTrack, RemoteParticipant } from 'livekit-client'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Progress } from './ui/progress'
import { Badge } from './ui/badge'
import { Mic, MicOff, Phone, PhoneOff, Volume2, VolumeX } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CallState {
  status: 'idle' | 'connecting' | 'connected' | 'disconnected' | 'error'
  isMuted: boolean
  isSpeaking: boolean
  volume: number
  error?: string
}

interface TicketInfo {
  id?: number
  confirmationNumber?: number
  email?: string
  issue?: string
  price?: number
}

export const VoiceCall: React.FC = () => {
  const [callState, setCallState] = useState<CallState>({
    status: 'idle',
    isMuted: false,
    isSpeaking: false,
    volume: 0
  })
  
  const [ticketInfo, setTicketInfo] = useState<TicketInfo | null>(null)
  const [conversationStage, setConversationStage] = useState<string>('')
  
  const roomRef = useRef<Room | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const volumeIntervalRef = useRef<number | null>(null)

  // Initialize audio element for playback
  useEffect(() => {
    audioRef.current = new Audio()
    audioRef.current.autoplay = true
    
    return () => {
      if (audioRef.current) {
        audioRef.current.pause()
        audioRef.current = null
      }
    }
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (volumeIntervalRef.current) {
        clearInterval(volumeIntervalRef.current)
      }
      disconnect()
    }
  }, [])

  const connect = async () => {
    try {
      setCallState(prev => ({ ...prev, status: 'connecting', error: undefined }))
      
      // Get access token from backend
      const tokenResponse = await fetch('/api/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          room_name: 'it-help-desk',
          participant_name: `user-${Date.now()}`
        })
      })

      if (!tokenResponse.ok) {
        throw new Error('Failed to get access token')
      }

      const { token, url } = await tokenResponse.json()

      // Create room and connect
      const room = new Room({
        adaptiveStream: true,
        dynacast: true,
      })

      roomRef.current = room

      // Set up event listeners
      room.on(RoomEvent.Connected, () => {
        console.log('Connected to room')
        setCallState(prev => ({ ...prev, status: 'connected' }))
        setConversationStage('Connected - Bot is greeting you...')
      })

      room.on(RoomEvent.Disconnected, (reason) => {
        console.log('Disconnected from room:', reason)
        setCallState(prev => ({ ...prev, status: 'disconnected' }))
        setConversationStage('')
      })

      room.on(RoomEvent.TrackSubscribed, (track: RemoteTrack, publication, participant: RemoteParticipant) => {
        console.log('Track subscribed:', track.kind)
        
        if (track.kind === Track.Kind.Audio) {
          // Attach audio track to audio element for playback
          const audioElement = audioRef.current
          if (audioElement) {
            track.attach(audioElement)
          }
        }
      })

      room.on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack, publication, participant: RemoteParticipant) => {
        console.log('Track unsubscribed:', track.kind)
        track.detach()
      })

      room.on(RoomEvent.DataReceived, (payload: Uint8Array, participant?: RemoteParticipant) => {
        try {
          const data = JSON.parse(new TextDecoder().decode(payload))
          console.log('Received data:', data)
          
          // Handle conversation stage updates
          if (data.type === 'stage_update') {
            setConversationStage(data.stage)
          }
          
          // Handle ticket creation
          if (data.type === 'ticket_created') {
            setTicketInfo({
              id: data.ticket_id,
              confirmationNumber: data.confirmation_number,
              email: data.email,
              issue: data.issue,
              price: data.price
            })
          }
        } catch (error) {
          console.error('Error parsing data:', error)
        }
      })

      // Connect to room
      await room.connect(url, token)
      // Enable microphone
      await room.localParticipant.setMicrophoneEnabled(true)

      // Start volume monitoring
      startVolumeMonitoring(room)

    } catch (error) {
      console.error('Connection error:', error)
      setCallState(prev => ({ 
        ...prev, 
        status: 'error', 
        error: error instanceof Error ? error.message : 'Unknown error'
      }))
    }
  }

  const disconnect = async () => {
    if (roomRef.current) {
      await roomRef.current.disconnect()
      roomRef.current = null
    }
    
    if (volumeIntervalRef.current) {
      clearInterval(volumeIntervalRef.current)
      volumeIntervalRef.current = null
    }
    
    setCallState(prev => ({ ...prev, status: 'idle', volume: 0 }))
    setConversationStage('')
    setTicketInfo(null)
  }

  const toggleMute = async () => {
    if (roomRef.current) {
      const isCurrentlyMuted = roomRef.current.localParticipant.isMicrophoneEnabled
      await roomRef.current.localParticipant.setMicrophoneEnabled(!isCurrentlyMuted)
      setCallState(prev => ({ ...prev, isMuted: !isCurrentlyMuted }))
    }
  }

  const startVolumeMonitoring = (room: Room) => {
    volumeIntervalRef.current = setInterval(() => {
      if (room && room.localParticipant) {
        // Get audio level from local participant
        const audioLevel = room.localParticipant.audioLevel || 0
        setCallState(prev => ({ 
          ...prev, 
          volume: audioLevel,
          isSpeaking: audioLevel > 0.1
        }))
      }
    }, 100)
  }

  const getStatusColor = () => {
    switch (callState.status) {
      case 'connected': return 'bg-green-500'
      case 'connecting': return 'bg-yellow-500'
      case 'error': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusText = () => {
    switch (callState.status) {
      case 'idle': return 'Ready to connect'
      case 'connecting': return 'Connecting...'
      case 'connected': return 'Connected'
      case 'disconnected': return 'Disconnected'
      case 'error': return 'Connection error'
      default: return 'Unknown status'
    }
  }

  return (
    <div className="space-y-6">
      {/* Main Voice Call Card */}
      <Card className="max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Start Voice Call</CardTitle>
          <CardDescription>
            Click "Join Call" to start talking with our AI assistant
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Status and Controls */}
          <div className="flex items-center justify-center space-x-4">
            {/* Status Indicator */}
            <div className="flex items-center space-x-2">
              <div className={cn("w-3 h-3 rounded-full", getStatusColor())} />
              <span className="text-sm font-medium">{getStatusText()}</span>
            </div>
            
            {/* Volume Indicator */}
            {callState.status === 'connected' && (
              <div className="flex items-center space-x-2">
                <div className="w-20">
                  <Progress value={callState.volume * 100} className="h-2" />
                </div>
                {callState.isSpeaking ? (
                  <Volume2 className="w-4 h-4 text-green-500" />
                ) : (
                  <VolumeX className="w-4 h-4 text-gray-400" />
                )}
              </div>
            )}
          </div>

          {/* Main Action Button */}
          <div className="text-center">
            {callState.status === 'idle' || callState.status === 'disconnected' || callState.status === 'connecting' ? (
              <Button 
                onClick={connect} 
                size="lg" 
                className="w-full max-w-xs"
                disabled={callState.status === 'connecting'}
              >
                <Phone className="w-5 h-5 mr-2" />
                {callState.status === 'connecting' ? 'Connecting...' : 'Join Call'}
              </Button>
            ) : (
              <div className="flex items-center justify-center space-x-4">
                <Button 
                  onClick={toggleMute}
                  variant={callState.isMuted ? "destructive" : "outline"}
                  size="lg"
                >
                  {callState.isMuted ? (
                    <MicOff className="w-5 h-5" />
                  ) : (
                    <Mic className="w-5 h-5" />
                  )}
                </Button>
                <Button 
                  onClick={disconnect} 
                  variant="destructive" 
                  size="lg"
                >
                  <PhoneOff className="w-5 h-5 mr-2" />
                  End Call
                </Button>
              </div>
            )}
          </div>

          {/* Error Display */}
          {callState.error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-sm">{callState.error}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Conversation Status */}
      {conversationStage && (
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle className="text-lg">Conversation Status</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">{conversationStage}</p>
          </CardContent>
        </Card>
      )}

      {/* Ticket Information */}
      {ticketInfo && (
        <Card className="max-w-2xl mx-auto border-green-200 bg-green-50">
          <CardHeader>
            <CardTitle className="text-lg text-green-800">Ticket Created Successfully!</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium text-gray-700">Confirmation Number:</span>
                <p className="text-lg font-bold text-green-600">{ticketInfo.confirmationNumber}</p>
              </div>
              <div>
                <span className="font-medium text-gray-700">Service Fee:</span>
                <p className="text-lg font-bold text-green-600">${ticketInfo.price}</p>
              </div>
              <div className="col-span-2">
                <span className="font-medium text-gray-700">Issue:</span>
                <p className="text-gray-700">{ticketInfo.issue}</p>
              </div>
              <div className="col-span-2">
                <span className="font-medium text-gray-700">Confirmation Email:</span>
                <p className="text-gray-700">{ticketInfo.email}</p>
              </div>
            </div>
            <div className="mt-4 p-3 bg-green-100 rounded-lg">
              <p className="text-green-800 text-sm">
                You will receive a confirmation email at {ticketInfo.email} with your ticket details.
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
