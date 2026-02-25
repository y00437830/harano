import type { MCPServer, MCPServerPayload } from '../types/mcp'
import { apiRequest, JSON_HEADERS } from './apiUtils'

const BASE = '/api/mcp'

export function listMCPServers(query?: string, availableOnly = false): Promise<MCPServer[]> {
  const params = new URLSearchParams()
  if (query) params.set('q', query)
  if (availableOnly) params.set('availableOnly', 'true')
  const url = params.size ? `${BASE}?${params.toString()}` : BASE
  return apiRequest<MCPServer[]>(url)
}

export function getMCPServer(id: string): Promise<MCPServer> {
  return apiRequest<MCPServer>(`${BASE}/${encodeURIComponent(id)}`)
}

export function publishMCPServer(payload: MCPServerPayload): Promise<MCPServer> {
  return apiRequest<MCPServer>(BASE, {
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify(payload),
  })
}

export function unpublishMCPServer(id: string): Promise<void> {
  return apiRequest<void>(`${BASE}/${encodeURIComponent(id)}`, { method: 'DELETE' })
}

export function listInstalledMCPServers(): Promise<MCPServer[]> {
  return apiRequest<MCPServer[]>(`${BASE}/installed`)
}

export function installMCPServer(id: string): Promise<MCPServer> {
  return apiRequest<MCPServer>(`${BASE}/${encodeURIComponent(id)}/install`, { method: 'POST' })
}

export function uninstallMCPServer(id: string): Promise<void> {
  return apiRequest<void>(`${BASE}/${encodeURIComponent(id)}/install`, { method: 'DELETE' })
}
