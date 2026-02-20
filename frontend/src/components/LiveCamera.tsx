import { YOUTUBE_EMBED_ID } from '@/lib/constants';

export default function LiveCamera() {
  return <div className="bg-[#111827] rounded-xl p-4 border border-slate-700"><h3 className="mb-3">Live Dania Beach Pier Cam</h3><iframe className="w-full aspect-video" src={`https://www.youtube.com/embed/${YOUTUBE_EMBED_ID}`} allowFullScreen /></div>;
}
