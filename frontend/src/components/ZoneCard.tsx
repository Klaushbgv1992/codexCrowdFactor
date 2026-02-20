export default function ZoneCard({ title, value, unit }: { title: string; value: number; unit: string }) {
  return <div className="bg-[#111827] rounded-xl p-4 border border-slate-700"><div className="text-slate-400 text-sm">{title}</div><div className="text-3xl font-semibold">{value}</div><div className="text-xs text-slate-500">{unit}</div></div>;
}
