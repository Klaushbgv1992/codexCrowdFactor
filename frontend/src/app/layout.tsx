import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Dania Beach Crowd Checker — Live Beach & Pier Crowds | Vibe Surf School',
  description: 'Check how crowded Dania Beach is right now. Live parking, pier, beach & water crowd levels updated every 30 seconds. Plan your perfect beach day.',
  alternates: { canonical: 'https://vibesurfschool.com/tools/crowd-checker' },
  openGraph: {
    title: 'Dania Beach Crowd Checker',
    description: 'Live Dania Beach crowd levels for parking, pier, beach, and water.',
    type: 'website',
    url: 'https://vibesurfschool.com/tools/crowd-checker'
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const ld = {
    '@context': 'https://schema.org', '@type': 'WebApplication',
    name: 'Dania Beach Crowd Checker', applicationCategory: 'TravelApplication',
    description: metadata.description
  };
  return <html lang="en"><body><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }} />{children}</body></html>;
}
