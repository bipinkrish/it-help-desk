export type SupportedIssueKey = 'wifi' | 'email' | 'performance' | 'printer';

export const SUPPORTED_ISSUES: Record<SupportedIssueKey, { name: string; description: string; price: number; keywords: string[] }> = {
  wifi: {
    name: 'Wi-Fi not working',
    description: 'Network connectivity issues',
    price: 20,
    keywords: ['wifi', 'wi-fi', 'wireless', 'internet', 'connection', 'network', 'connectivity'],
  },
  email: {
    name: 'Email login issues',
    description: 'Password reset and login problems',
    price: 15,
    keywords: ['email', 'login', 'password', 'reset', 'account', 'access', 'signin'],
  },
  performance: {
    name: 'Slow laptop performance',
    description: 'CPU change and optimization',
    price: 25,
    keywords: ['laptop', 'slow', 'performance', 'cpu', 'speed', 'computer', 'pc', 'optimization'],
  },
  printer: {
    name: 'Printer problems',
    description: 'Power plug or driver issues',
    price: 10,
    keywords: ['printer', 'printing', 'power', 'plug', 'cable', 'hardware', 'driver'],
  },
};

export function identifyIssue(description: string): { type: SupportedIssueKey; description: string; price: number } | null {
  const text = description.toLowerCase();
  for (const [key, cfg] of Object.entries(SUPPORTED_ISSUES) as [SupportedIssueKey, (typeof SUPPORTED_ISSUES)['wifi']][]) {
    if (cfg.keywords.some((k) => text.includes(k))) {
      return { type: key, description: cfg.description, price: cfg.price };
    }
  }
  return null;
}


