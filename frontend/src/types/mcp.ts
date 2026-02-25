/** Lifecycle status of an MCP server entry. */
export type MCPServerStatus = 'AVAILABLE' | 'INSTALLED' | 'DEPRECATED'

/** An MCP server available in the marketplace. */
export interface MCPServer {
  id: string
  name: string
  version: string
  description: string
  author: string
  homepage?: string
  tags: string[]
  status: MCPServerStatus
  installed?: boolean
}

/** Payload for publishing a new MCP server. */
export type MCPServerPayload = Omit<MCPServer, 'status' | 'installed'>
