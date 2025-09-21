import { NextResponse } from 'next/server';
import { getCollection } from '../../../../lib/mongodb';
import { identifyIssue } from '../../../../lib/models';
import { ObjectId } from 'mongodb';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    console.log('[API] POST /api/tickets/update-by-id', { body });
    const { ticket_id, field, value } = body as {
      ticket_id: number;
      field: 'phone' | 'address' | 'issue';
      value: string;
    };

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

    const collection = await getCollection('tickets');
    const result = await collection.updateOne(
      { _id: new ObjectId(ticket_id) },
      { $set: updates }
    );

    if (result.modifiedCount === 0) {
      return NextResponse.json({ success: false, error: 'Update failed' }, { status: 500 });
    }

    return NextResponse.json({ success: true, field, value, ticket_id, message: `Updated ${field}` });
  } catch (e) {
    console.error('[API] POST /api/tickets/update-by-id error', e);
    return NextResponse.json({ success: false, error: 'Server error' }, { status: 500 });
  }
}


