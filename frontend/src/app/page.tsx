import BookingCTA from '@/components/BookingCTA';
import CrowdGauge from '@/components/CrowdGauge';
import Footer from '@/components/Footer';
import LiveCamera from '@/components/LiveCamera';
import TrendChart from '@/components/TrendChart';
import ZoneCard from '@/components/ZoneCard';
import { fetchCurrent, fetchHistory } from '@/lib/api';

export default async function HomePage() {
  const current = await fetchCurrent();
  const history = await fetchHistory(12);

  return (
    <main className="max-w-6xl mx-auto p-4 md:p-8 space-y-6">
      <header><h1 className="text-3xl md:text-5xl font-extrabold">Dania Beach Crowd Checker</h1><p className="text-slate-400">Powered by Vibe Surf School • Live updates</p></header>
      <CrowdGauge score={current.crowd_factor} label={current.crowd_level} color={current.crowd_level_color} />
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <ZoneCard title="Parking" value={current.zones.parking.cars} unit="cars" />
        <ZoneCard title="Pier" value={current.zones.pier.people} unit="people" />
        <ZoneCard title="Beach" value={current.zones.beach.people} unit="people" />
        <ZoneCard title="Water" value={current.zones.water.people} unit="people" />
      </section>
      <TrendChart data={history.data} />
      <LiveCamera />
      <BookingCTA text={current.recommendation} />
      <section className="text-slate-300">How crowded is Dania Beach right now? Use this live Dania Beach pier crowd level checker to plan the best time to visit Dania Beach and avoid parking congestion.</section>
      <Footer />
    </main>
  );
}
