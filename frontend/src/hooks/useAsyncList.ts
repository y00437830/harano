import { useCallback, useEffect, useState } from 'react'

/**
 * Reusable hook for loading a searchable list of items asynchronously.
 * Eliminates the duplicated loading/error/search state management
 * between SkillList and MCPMarket components.
 */
export function useAsyncList<T>(fetcher: (query?: string) => Promise<T[]>) {
  const [items, setItems] = useState<T[]>([])
  const [query, setQuery] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const load = useCallback(
    (q: string) => {
      setLoading(true)
      setError(null)
      fetcher(q || undefined)
        .then(setItems)
        .catch((e: unknown) => setError(e instanceof Error ? e.message : String(e)))
        .finally(() => setLoading(false))
    },
    [fetcher],
  )

  useEffect(() => {
    load('')
  }, [load])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    load(query)
  }

  return { items, setItems, query, setQuery, error, setError, loading, load, handleSearch }
}
