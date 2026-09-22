import { useEffect, useState } from 'react';
import { fetchJson } from '../api';

export interface Resource<T> { data: T | null; loading: boolean; error: string | null }

/** Abort plus an active guard prevents an old response from replacing a new query. */
export function useResource<T>(path: string | null, revision = 0): Resource<T> {
  const [resource, setResource] = useState<Resource<T>>({ data: null, loading: !!path, error: null });
  useEffect(() => {
    if (!path) { setResource({ data: null, loading: false, error: null }); return; }
    const controller = new AbortController();
    let active = true;
    setResource({ data: null, loading: true, error: null });
    fetchJson<T>(path, controller.signal).then(data => {
      if (active) setResource({ data, loading: false, error: null });
    }).catch((error: unknown) => {
      if (active && !controller.signal.aborted) {
        setResource({ data: null, loading: false, error: error instanceof Error ? error.message : '网络请求失败，请重试。' });
      }
    });
    return () => { active = false; controller.abort(); };
  }, [path, revision]);
  return resource;
}
