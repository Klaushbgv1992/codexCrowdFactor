export default function BookingCTA({ text }: { text: string }) {
  return <div className="bg-[#F5E6D3] text-slate-900 rounded-xl p-6"><p>{text}</p><a href="https://vibesurfschool.com/book" className="inline-block mt-3 bg-slate-900 text-white px-4 py-2 rounded">Book a Lesson</a></div>;
}
