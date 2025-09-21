import { NextResponse } from 'next/server';
import { getCollection } from '../../../lib/mongodb';
import { identifyIssue, type Ticket } from '../../../lib/models';

export async function GET() {
  try {
    console.log('[API] GET /api/tickets');
    const collection = await getCollection('tickets');
    const tickets = await collection.find({}).sort({ created_at: -1 }).toArray();
    console.log('[API] Found tickets:', tickets.length);
    return NextResponse.json({ success: true, tickets });
  } catch (error) {
    console.error('[API] GET /api/tickets error:', error);
    return NextResponse.json({ success: false, error: 'Database error' }, { status: 500 });
  }
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
          error: "Unsupported issue. We handle Wi‑Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10).",
        },
        { status: 400 },
      );
    }

    const collection = await getCollection('tickets');
    const confirmation_number = Math.floor(10000 + Math.random() * 90000);
    
    const ticket: Omit<Ticket, '_id'> = {
      name,
      email,
      phone,
      address,
      issue: issue.description,
      price: issue.price,
      confirmation_number,
      created_at: new Date(),
    };

    const result = await collection.insertOne(ticket);
    console.log('[API] Ticket created:', result.insertedId);

    return NextResponse.json({
      success: true,
      ticket_id: result.insertedId.toString(),
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


