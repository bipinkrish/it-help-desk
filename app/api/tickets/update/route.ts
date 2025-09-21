import { NextResponse } from 'next/server';
import { getCollection } from '../../../../lib/mongodb';
import { identifyIssue } from '../../../../lib/models';

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

    const collection = await getCollection('tickets');
    const ticket = await collection.findOne({
      name: { $regex: new RegExp(`^${name}$`, 'i') },
      email: { $regex: new RegExp(`^${email}$`, 'i') },
      confirmation_number: confirmation_number
    });

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

    const result = await collection.updateOne(
      { _id: ticket._id },
      { $set: updates }
    );

    if (result.modifiedCount === 0) {
      return NextResponse.json({ success: false, error: 'Update failed' }, { status: 500 });
    }

    return NextResponse.json({ success: true, field, value, ticket_id: ticket._id.toString(), message: `Updated ${field}` });
  } catch (e) {
    console.error('[API] POST /api/tickets/update error', e);
    return NextResponse.json({ success: false, error: 'Server error' }, { status: 500 });
  }
}


