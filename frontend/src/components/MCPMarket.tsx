import { useCallback, useEffect, useState } from 'react'
import type { MCPServer } from '../types/mcp'
import {
  listMCPServers,
  listInstalledMCPServers,
  installMCPServer,
  uninstallMCPServer,
} from '../api/mcpApi'
import { toErrorMessage } from '../utils/errorUtils'

export default function MCPMarket() {
  const [servers, setServers] = useState<MCPServer[]>([])
  const [installed, setInstalled] = useState<Set<string>>(new Set())
  const [query, setQuery] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const load = useCallback((q: string) => {
    setLoading(true)
    setError(null)
    Promise.all([listMCPServers(q || undefined), listInstalledMCPServers()])
      .then(([all, inst]) => {
        setServers(all)
        setInstalled(new Set(inst.map(s => s.id)))
      })
      .catch((e: unknown) => setError(toErrorMessage(e)))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    load('')
  }, [load])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    load(query)
  }

  const handleInstall = (id: string) => {
    installMCPServer(id)
      .then(() => load(query))
      .catch((e: unknown) => setError(toErrorMessage(e)))
  }

  const handleUninstall = (id: string) => {
    uninstallMCPServer(id)
      .then(() => load(query))
      .catch((e: unknown) => setError(toErrorMessage(e)))
  }

  return (
    <section>
      <h2>MCP Market</h2>
      <form onSubmit={handleSearch} style={{ marginBottom: '1rem' }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search MCP servers…"
        />
        <button type="submit">Search</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Loading…</p>}

      {!loading && servers.length === 0 && <p>No MCP servers found.</p>}

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {servers.map(server => {
          const isInstalled = installed.has(server.id)
          return (
            <li
              key={server.id}
              style={{
                border: '1px solid #ddd',
                borderRadius: 6,
                padding: '0.75rem',
                marginBottom: '0.5rem',
                background: isInstalled ? '#f0fff4' : 'white',
              }}
            >
              <strong>{server.name}</strong>
              <span style={{ marginLeft: '0.5rem', color: '#666', fontSize: '0.85em' }}>
                v{server.version}
              </span>
              {server.author && (
                <span style={{ marginLeft: '0.5rem', color: '#888', fontSize: '0.85em' }}>
                  by {server.author}
                </span>
              )}
              <p style={{ margin: '0.25rem 0', fontSize: '0.9em' }}>{server.description}</p>
              {server.tags.length > 0 && (
                <p style={{ margin: '0.25rem 0', fontSize: '0.8em', color: '#555' }}>
                  {server.tags.join(', ')}
                </p>
              )}
              {isInstalled ? (
                <button
                  onClick={() => handleUninstall(server.id)}
                  style={{ marginTop: '0.5rem', background: '#fee', borderColor: '#f88' }}
                >
                  Uninstall
                </button>
              ) : (
                <button
                  onClick={() => handleInstall(server.id)}
                  style={{ marginTop: '0.5rem', background: '#efe', borderColor: '#8c8' }}
                >
                  Install
                </button>
              )}
            </li>
          )
        })}
      </ul>
    </section>
  )
}
