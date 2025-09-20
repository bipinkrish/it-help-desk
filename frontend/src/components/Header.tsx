import React from 'react'
import { Badge } from './ui/badge'

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">IT</span>
              </div>
              <h1 className="text-xl font-semibold text-gray-900">
                IT Help Desk
              </h1>
            </div>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              AI Voice Assistant
            </Badge>
          </div>
          <div className="text-sm text-gray-500">
            Powered by LiveKit & AI
          </div>
        </div>
      </div>
    </header>
  )
}
