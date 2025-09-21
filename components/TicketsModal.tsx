'use client';

import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';

type Ticket = {
  _id: string;
  name: string;
  email: string;
  phone: string;
  address: string;
  issue: string;
  price: number;
  confirmation_number: number;
  created_at: string;
};

interface TicketsModalProps {
  open: boolean;
  onClose: () => void;
}

export default function TicketsModal({ open, onClose }: TicketsModalProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    if (!open) return;
    const fetchTickets = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('[UI] fetching /api/tickets');
        const res = await fetch('/api/tickets', { cache: 'no-store' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('[UI] /api/tickets ->', data);
        setTickets(data.tickets ?? []);
      } catch (e: any) {
        console.error('[UI] tickets fetch error', e);
        setError('Failed to load tickets');
      } finally {
        setLoading(false);
      }
    };
    fetchTickets();
  }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[100]">
      {/* backdrop */}
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />

      {/* modal */}
      <div className="bg-background text-foreground absolute left-1/2 top-1/2 w-[95vw] max-w-5xl -translate-x-1/2 -translate-y-1/2 rounded-lg border p-4 shadow-xl md:p-6">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Support Tickets</h2>
          <Button variant="secondary" onClick={onClose}>Close</Button>
        </div>

        {loading && <p className="text-sm opacity-80">Loading…</p>}
        {error && <p className="text-sm text-red-500">{error}</p>}

        {!loading && !error && (
          <div className="max-h-[70vh] overflow-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="border-b bg-muted/40 text-left">
                  <th className="p-2">ID</th>
                  <th className="p-2">Name</th>
                  <th className="p-2">Email</th>
                  <th className="p-2">Phone</th>
                  <th className="p-2">Address</th>
                  <th className="p-2">Issue</th>
                  <th className="p-2">Price</th>
                  <th className="p-2">Confirm #</th>
                  <th className="p-2">Created</th>
                </tr>
              </thead>
              <tbody>
                {tickets.length === 0 && (
                  <tr>
                    <td className="p-3 text-center opacity-70" colSpan={9}>No tickets yet</td>
                  </tr>
                )}
                {tickets.map((t) => (
                  <tr key={t._id} className="border-b last:border-0">
                    <td className="p-2 align-top">{t._id.slice(-6)}</td>
                    <td className="p-2 align-top">{t.name}</td>
                    <td className="p-2 align-top">{t.email}</td>
                    <td className="p-2 align-top">{t.phone}</td>
                    <td className="p-2 align-top">{t.address}</td>
                    <td className="p-2 align-top">{t.issue}</td>
                    <td className="p-2 align-top">${t.price}</td>
                    <td className="p-2 align-top">{t.confirmation_number}</td>
                    <td className="p-2 align-top">{new Date(t.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}


