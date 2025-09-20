import React from 'react'
import { VoiceCall } from './components/VoiceCall.tsx'
import { Header } from './components/Header.tsx'
import { SupportedIssues } from './components/SupportedIssues.tsx'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Hero Section */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-gray-900">
              IT Help Desk Voice Bot
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get instant IT support through natural voice conversation. 
              Our AI assistant can help you with common technical issues.
            </p>
          </div>

          {/* Main Voice Call Component */}
          <VoiceCall />

          {/* Supported Issues */}
          <SupportedIssues />
        </div>
      </main>
    </div>
  )
}

export default App
