import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Wifi, Mail, Laptop, Printer } from 'lucide-react'

const issues = [
  {
    type: 'wifi',
    title: 'Wi-Fi Issues',
    description: 'Wireless internet connection problems',
    price: 20,
    icon: Wifi,
    keywords: ['wifi', 'wi-fi', 'wireless', 'internet', 'connection', 'network']
  },
  {
    type: 'email',
    title: 'Email Login Issues',
    description: 'Password reset and account access problems',
    price: 15,
    icon: Mail,
    keywords: ['email', 'login', 'password', 'reset', 'account', 'access']
  },
  {
    type: 'laptop',
    title: 'Slow Laptop Performance',
    description: 'CPU optimization and performance improvements',
    price: 25,
    icon: Laptop,
    keywords: ['laptop', 'slow', 'performance', 'cpu', 'speed', 'computer', 'pc']
  },
  {
    type: 'printer',
    title: 'Printer Problems',
    description: 'Hardware issues and power connection problems',
    price: 10,
    icon: Printer,
    keywords: ['printer', 'printing', 'power', 'plug', 'cable', 'hardware']
  }
]

export const SupportedIssues: React.FC = () => {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 text-center">
        Supported IT Issues
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {issues.map((issue) => {
          const Icon = issue.icon
          return (
            <Card key={issue.type} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Icon className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{issue.title}</CardTitle>
                    <Badge variant="outline" className="mt-1">
                      ${issue.price}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm text-gray-600">
                  {issue.description}
                </CardDescription>
              </CardContent>
            </Card>
          )
        })}
      </div>
      <p className="text-center text-sm text-gray-500">
        Simply describe your issue and our AI assistant will identify the problem and provide a quote.
      </p>
    </div>
  )
}
