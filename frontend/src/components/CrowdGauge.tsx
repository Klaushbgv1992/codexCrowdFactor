export default function CrowdGauge({ score, label, color }: { score: number; label: string; color: string }) {
  return (
    <div className="rounded-2xl bg-[#111827] p-6 border border-slate-700">
      <p className="text-sm text-slate-400">Overall Crowd Factor</p>
      <div className="text-5xl font-bold mt-2" style={{ color }}>{score}</div>
      <div className="uppercase text-sm tracking-wider mt-1" style={{ color }}>{label}</div>
      <div className="w-full bg-slate-700 rounded-full h-3 mt-4"><div className="h-3 rounded-full" style={{ width: `${score}%`, background: color }} /></div>
    </div>
  );
}
