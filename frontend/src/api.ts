import type { Filters } from './types';

export async function fetchJson<T>(path: string, signal: AbortSignal): Promise<T> {
  const response = await fetch(path, { signal, headers: { Accept: 'application/json' } });
  if (!response.ok) {
    const body = await response.json().catch(() => null) as { error?: { message?: string } } | null;
    throw new Error(body?.error?.message ?? `请求失败（HTTP ${response.status}），请稍后重试。`);
  }
  return response.json() as Promise<T>;
}

export function filterQuery(filters: Filters): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value !== '' && value !== false) params.set(key, String(value));
  }
  return params.toString();
}
