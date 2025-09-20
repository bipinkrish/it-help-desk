import { NextResponse } from 'next/server';
import { findTicket } from '../../../../lib/ticketStore';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    console.log('[API] POST /api/tickets/lookup', { body });
    const { name, email, confirmation_number } = body as {
      name: string;
      email: string;
      confirmation_number: number;
    };

    const ticket = findTicket(name, email, confirmation_number);
    if (!ticket) {
      return NextResponse.json({ success: false, error: 'Not found' }, { status: 404 });
    }

    return NextResponse.json({ success: true, ticket, message: `Found your ticket! Your issue is: ${ticket.issue} for $${ticket.price}` });
  } catch (e) {
    console.error('[API] POST /api/tickets/lookup error', e);
    return NextResponse.json({ success: false, error: 'Server error' }, { status: 500 });
  }
}


