/**
 * Shared helper that performs a fetch request and throws an error on
 * non-2xx responses. Reduces the boilerplate present in every API module.
 */
export async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
  const res = options !== undefined ? await fetch(url, options) : await fetch(url)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  // No-content responses (e.g. 204 DELETE) have no body to parse.
  if (res.status === 204 || res.status === 205) return undefined as T
  return res.json() as Promise<T>
}

export const JSON_HEADERS = { 'Content-Type': 'application/json' } as const
