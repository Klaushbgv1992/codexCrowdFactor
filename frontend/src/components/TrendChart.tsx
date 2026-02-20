'use client';
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export default function TrendChart({ data }: { data: any[] }) {
  return (
    <div className="bg-[#111827] rounded-xl p-4 border border-slate-700 h-72">
      <h3 className="mb-3">Trend</h3>
      <ResponsiveContainer width="100%" height="90%">
        <AreaChart data={data}>
          <XAxis dataKey="timestamp" hide />
          <YAxis />
          <Tooltip />
          <Area type="monotone" dataKey="crowd_factor" stroke="#22D3EE" fill="#06B6D4" fillOpacity={0.35} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
