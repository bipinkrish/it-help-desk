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

let DATA_DIR = process.env.TICKET_DATA_DIR || path.join(process.cwd(), 'data');
let DATA_FILE = path.join(DATA_DIR, 'tickets.json');

// In-memory fallback for read-only or ephemeral environments
let MEMORY_DB: DBShape | null = null;

function tryEnsureDir(dir: string) {
  try {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    return true;
  } catch {
    return false;
  }
}

function tryWrite(file: string, data: string) {
  try {
    fs.writeFileSync(file, data);
    return true;
  } catch {
    return false;
  }
}

function ensureStore() {
  // Primary location
  if (tryEnsureDir(DATA_DIR)) {
    if (!fs.existsSync(DATA_FILE)) {
      if (tryWrite(DATA_FILE, JSON.stringify({ tickets: [] } as DBShape, null, 2))) return;
    } else {
      return;
    }
  }

  // Fallback to /tmp for Vercel/serverless
  const tmpDir = '/tmp';
  const tmpFile = path.join(tmpDir, 'tickets.json');
  if (tryEnsureDir(tmpDir)) {
    DATA_DIR = tmpDir;
    DATA_FILE = tmpFile;
    if (!fs.existsSync(DATA_FILE)) {
      if (tryWrite(DATA_FILE, JSON.stringify({ tickets: [] } as DBShape, null, 2))) return;
    } else {
      return;
    }
  }

  // Final fallback: in-memory
  if (!MEMORY_DB) MEMORY_DB = { tickets: [] };
}

function readStore(): DBShape {
  ensureStore();
  if (MEMORY_DB) return MEMORY_DB;
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw) as DBShape;
  } catch {
    return { tickets: [] };
  }
}

function writeStore(db: DBShape) {
  ensureStore();
  if (MEMORY_DB) {
    MEMORY_DB = db;
    return;
  }
  tryWrite(DATA_FILE, JSON.stringify(db, null, 2));
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


