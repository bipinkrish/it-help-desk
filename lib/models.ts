export interface Ticket {
  _id?: string;
  name: string;
  email: string;
  phone: string;
  address: string;
  issue: string;
  price: number;
  confirmation_number: number;
  created_at: Date;
}

export interface SupportedIssue {
  type: string;
  name: string;
  description: string;
  price: number;
  keywords: string[];
}

export const SUPPORTED_ISSUES: SupportedIssue[] = [
  {
    type: 'wifi',
    name: 'Wi-Fi not working',
    description: 'Network connectivity issues',
    price: 20,
    keywords: ['wifi', 'wi-fi', 'wireless', 'internet', 'connection', 'network', 'connectivity']
  },
  {
    type: 'email',
    name: 'Email login issues',
    description: 'Password reset and login problems',
    price: 15,
    keywords: ['email', 'login', 'password', 'reset', 'account', 'access', 'signin']
  },
  {
    type: 'performance',
    name: 'Slow laptop performance',
    description: 'CPU change and optimization',
    price: 25,
    keywords: ['laptop', 'slow', 'performance', 'cpu', 'speed', 'computer', 'pc', 'optimization']
  },
  {
    type: 'printer',
    name: 'Printer problems',
    description: 'Power plug or driver issues',
    price: 10,
    keywords: ['printer', 'printing', 'power', 'plug', 'cable', 'hardware', 'driver']
  }
];

export function identifyIssue(description: string): SupportedIssue | null {
  const text = description.toLowerCase();
  
  for (const issue of SUPPORTED_ISSUES) {
    if (issue.keywords.some(keyword => text.includes(keyword))) {
      return issue;
    }
  }
  
  return null;
}
