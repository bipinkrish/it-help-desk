import { NextResponse } from 'next/server';
import { identifyIssue } from '../../../lib/issues';
import { createTicket, listTickets } from '../../../lib/ticketStore';

export async function GET() {
  console.log('[API] GET /api/tickets');
  const tickets = listTickets();
  return NextResponse.json({ success: true, tickets });
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    console.log('[API] POST /api/tickets', { body });
    const { name, email, phone, address, issue_description } = body as {
      name: string;
      email: string;
      phone: string;
      address: string;
      issue_description: string;
    };

    const issue = identifyIssue(issue_description);
    if (!issue) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Unsupported issue. We handle Wi‑Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10).",
        },
        { status: 400 },
      );
    }

    const confirmation_number = Math.floor(10000 + Math.random() * 90000);
    const { id } = createTicket({
      name,
      email,
      phone,
      address,
      issue: issue.description,
      price: issue.price,
      confirmation_number,
    });

    return NextResponse.json({
      success: true,
      ticket_id: id,
      confirmation_number,
      email,
      issue: issue.description,
      price: issue.price,
    });
  } catch (e) {
    console.error('[API] POST /api/tickets error', e);
    return NextResponse.json({ success: false, error: 'Server error' }, { status: 500 });
  }
}


