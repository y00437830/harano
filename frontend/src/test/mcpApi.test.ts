import { describe, it, expect, vi, afterEach } from 'vitest'
import {
  listMCPServers,
  getMCPServer,
  publishMCPServer,
  unpublishMCPServer,
  listInstalledMCPServers,
  installMCPServer,
  uninstallMCPServer,
} from '../api/mcpApi'
import type { MCPServer } from '../types/mcp'

const mockServer: MCPServer = {
  id: 'weather',
  name: 'Weather API',
  version: '1.0.0',
  description: 'Weather data',
  author: 'acme',
  tags: ['weather'],
  status: 'AVAILABLE',
}

const installedServer: MCPServer = { ...mockServer, status: 'INSTALLED' }

function mockFetch(data: unknown, status = 200) {
  return vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(data),
  })
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('mcpApi', () => {
  it('listMCPServers fetches /api/mcp', async () => {
    vi.stubGlobal('fetch', mockFetch([mockServer]))
    const servers = await listMCPServers()
    expect(servers).toHaveLength(1)
    expect(servers[0].id).toBe('weather')
  })

  it('listMCPServers with query', async () => {
    const spy = mockFetch([mockServer])
    vi.stubGlobal('fetch', spy)
    await listMCPServers('weather')
    expect(spy).toHaveBeenCalledWith('/api/mcp?q=weather')
  })

  it('listMCPServers with availableOnly', async () => {
    const spy = mockFetch([mockServer])
    vi.stubGlobal('fetch', spy)
    await listMCPServers(undefined, true)
    expect(spy).toHaveBeenCalledWith('/api/mcp?availableOnly=true')
  })

  it('getMCPServer fetches /api/mcp/:id', async () => {
    vi.stubGlobal('fetch', mockFetch(mockServer))
    const server = await getMCPServer('weather')
    expect(server.name).toBe('Weather API')
  })

  it('publishMCPServer posts to /api/mcp', async () => {
    const spy = mockFetch(mockServer, 201)
    vi.stubGlobal('fetch', spy)
    const { status: _s, ...payload } = mockServer
    await publishMCPServer(payload)
    expect(spy).toHaveBeenCalledWith('/api/mcp', expect.objectContaining({ method: 'POST' }))
  })

  it('unpublishMCPServer deletes /api/mcp/:id', async () => {
    const spy = vi.fn().mockResolvedValue({ ok: true, status: 204 })
    vi.stubGlobal('fetch', spy)
    await unpublishMCPServer('weather')
    expect(spy).toHaveBeenCalledWith('/api/mcp/weather', expect.objectContaining({ method: 'DELETE' }))
  })

  it('listInstalledMCPServers fetches /api/mcp/installed', async () => {
    const spy = mockFetch([installedServer])
    vi.stubGlobal('fetch', spy)
    const servers = await listInstalledMCPServers()
    expect(servers[0].status).toBe('INSTALLED')
    expect(spy).toHaveBeenCalledWith('/api/mcp/installed')
  })

  it('installMCPServer posts to /api/mcp/:id/install', async () => {
    const spy = mockFetch(installedServer)
    vi.stubGlobal('fetch', spy)
    const server = await installMCPServer('weather')
    expect(server.status).toBe('INSTALLED')
    expect(spy).toHaveBeenCalledWith('/api/mcp/weather/install', expect.objectContaining({ method: 'POST' }))
  })

  it('uninstallMCPServer deletes /api/mcp/:id/install', async () => {
    const spy = vi.fn().mockResolvedValue({ ok: true, status: 204 })
    vi.stubGlobal('fetch', spy)
    await uninstallMCPServer('weather')
    expect(spy).toHaveBeenCalledWith('/api/mcp/weather/install', expect.objectContaining({ method: 'DELETE' }))
  })

  it('throws on non-ok response', async () => {
    vi.stubGlobal('fetch', mockFetch(null, 404))
    await expect(getMCPServer('nonexistent')).rejects.toThrow()
  })
})
