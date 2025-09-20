import { NextResponse } from 'next/server';
import { identifyIssue } from '../../../../lib/issues';
import { findTicket, updateTicket } from '../../../../lib/ticketStore';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    console.log('[API] POST /api/tickets/update', { body });
    const { name, email, confirmation_number, field, value } = body as {
      name: string;
      email: string;
      confirmation_number: number;
      field: 'phone' | 'address' | 'issue';
      value: string;
    };

    const ticket = findTicket(name, email, confirmation_number);
    if (!ticket) {
      return NextResponse.json({ success: false, error: 'Not found' }, { status: 404 });
    }

    const updates: any = {};
    if (field === 'issue') {
      const match = identifyIssue(value);
      if (!match) {
        return NextResponse.json({ success: false, error: 'Unsupported issue' }, { status: 400 });
      }
      updates.issue = match.description;
      updates.price = match.price;
    } else if (field === 'phone') {
      updates.phone = value;
    } else if (field === 'address') {
      updates.address = value;
    } else {
      return NextResponse.json({ success: false, error: 'Invalid field' }, { status: 400 });
    }

    const ok = updateTicket(ticket.id, updates);
    if (!ok) {
      return NextResponse.json({ success: false, error: 'Update failed' }, { status: 500 });
    }

    return NextResponse.json({ success: true, field, value, ticket_id: ticket.id, message: `Updated ${field}` });
  } catch (e) {
    console.error('[API] POST /api/tickets/update error', e);
    return NextResponse.json({ success: false, error: 'Server error' }, { status: 500 });
  }
}


