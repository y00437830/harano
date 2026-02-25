import type { MCPServer, MCPServerPayload } from '../types/mcp'

const BASE = '/api/mcp'

export async function listMCPServers(query?: string, availableOnly = false): Promise<MCPServer[]> {
  const params = new URLSearchParams()
  if (query) params.set('q', query)
  if (availableOnly) params.set('availableOnly', 'true')
  const url = params.size ? `${BASE}?${params.toString()}` : BASE
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Failed to list MCP servers: ${res.status}`)
  return res.json() as Promise<MCPServer[]>
}

export async function getMCPServer(id: string): Promise<MCPServer> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}`)
  if (!res.ok) throw new Error(`MCP server not found: ${id}`)
  return res.json() as Promise<MCPServer>
}

export async function publishMCPServer(payload: MCPServerPayload): Promise<MCPServer> {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(`Failed to publish MCP server: ${res.status}`)
  return res.json() as Promise<MCPServer>
}

export async function unpublishMCPServer(id: string): Promise<void> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`Failed to unpublish MCP server: ${res.status}`)
}

export async function listInstalledMCPServers(): Promise<MCPServer[]> {
  const res = await fetch(`${BASE}/installed`)
  if (!res.ok) throw new Error(`Failed to list installed MCP servers: ${res.status}`)
  return res.json() as Promise<MCPServer[]>
}

export async function installMCPServer(id: string): Promise<MCPServer> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}/install`, { method: 'POST' })
  if (!res.ok) throw new Error(`Failed to install MCP server: ${res.status}`)
  return res.json() as Promise<MCPServer>
}

export async function uninstallMCPServer(id: string): Promise<void> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}/install`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`Failed to uninstall MCP server: ${res.status}`)
}
