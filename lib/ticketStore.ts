import fs from 'fs';
import path from 'path';

export type Ticket = {
  id: number;
  name: string;
  email: string;
  phone: string;
  address: string;
  issue: string;
  price: number;
  confirmation_number: number;
  created_at: string;
};

type DBShape = { tickets: Ticket[] };

const DATA_DIR = path.join(process.cwd(), 'data');
const DATA_FILE = path.join(DATA_DIR, 'tickets.json');

function ensureStore() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, JSON.stringify({ tickets: [] } as DBShape, null, 2));
}

function readStore(): DBShape {
  ensureStore();
  const raw = fs.readFileSync(DATA_FILE, 'utf8');
  try {
    return JSON.parse(raw) as DBShape;
  } catch {
    return { tickets: [] };
  }
}

function writeStore(db: DBShape) {
  ensureStore();
  fs.writeFileSync(DATA_FILE, JSON.stringify(db, null, 2));
}

export function listTickets(): Ticket[] {
  const db = readStore();
  return db.tickets.slice().sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
}

export function createTicket(t: Omit<Ticket, 'id' | 'created_at'>): { id: number; confirmation_number: number } {
  const db = readStore();
  const id = (db.tickets.at(-1)?.id ?? 0) + 1;
  const created_at = new Date().toISOString();
  const ticket: Ticket = { id, created_at, ...t };
  db.tickets.push(ticket);
  writeStore(db);
  return { id, confirmation_number: ticket.confirmation_number };
}

export function findTicket(name: string, email: string, confirmation_number: number): Ticket | null {
  const db = readStore();
  const lower = (s: string) => s.trim().toLowerCase();
  return db.tickets.find(
    (t) => lower(t.name) === lower(name) && lower(t.email) === lower(email) && t.confirmation_number === confirmation_number,
  ) ?? null;
}

export function updateTicket(id: number, updates: Partial<Pick<Ticket, 'phone' | 'address' | 'issue' | 'price'>>): boolean {
  const db = readStore();
  const idx = db.tickets.findIndex((t) => t.id === id);
  if (idx === -1) return false;
  db.tickets[idx] = { ...db.tickets[idx], ...updates };
  writeStore(db);
  return true;
}


