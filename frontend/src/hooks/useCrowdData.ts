'use client';
import { useEffect, useState } from 'react';

export function useCrowdData() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    let active = true;
    async function load() {
      const res = await fetch('/api-proxy/current').then(r => r.json());
      if (active) setData(res);
    }
    load();
    const i = setInterval(load, 30000);
    return () => {
      active = false;
      clearInterval(i);
    };
  }, []);
  return data;
}
