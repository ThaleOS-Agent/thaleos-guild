const base =
  (import.meta as any).env?.VITE_API_BASE ||
  "http://localhost:8080";

export async function getJSON<T>(path: string): Promise<T> {
  const url = path.startsWith("http") ? path : `${base}${path}`;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return (await r.json()) as T;
}

export async function postJSON<T>(path: string, body: any): Promise<T> {
  const url = path.startsWith("http") ? path : `${base}${path}`;
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return (await r.json()) as T;
}