import { describe, it, expect } from 'vitest'
import type { Skill } from '../types/skill'
import type { MCPServer } from '../types/mcp'

describe('Skill type', () => {
  it('can represent a valid skill object', () => {
    const skill: Skill = {
      id: 'greet',
      name: 'Greet',
      version: '1.0.0',
      description: 'Returns a greeting.',
      parameters: [
        { name: 'name', type: 'string', description: 'Target name', required: true },
      ],
      tags: ['greeting'],
    }
    expect(skill.id).toBe('greet')
    expect(skill.parameters).toHaveLength(1)
    expect(skill.parameters[0].required).toBe(true)
  })

  it('supports all parameter types', () => {
    const types: Skill['parameters'][0]['type'][] = [
      'string', 'integer', 'float', 'boolean', 'object', 'array',
    ]
    types.forEach(t => {
      const param: Skill['parameters'][0] = { name: 'p', type: t, description: '', required: true }
      expect(param.type).toBe(t)
    })
  })
})

describe('MCPServer type', () => {
  it('can represent an available server', () => {
    const server: MCPServer = {
      id: 'weather',
      name: 'Weather API',
      version: '1.0.0',
      description: 'Fetches weather data.',
      author: 'acme',
      tags: ['weather', 'api'],
      status: 'AVAILABLE',
    }
    expect(server.status).toBe('AVAILABLE')
    expect(server.tags).toContain('weather')
  })

  it('can represent an installed server', () => {
    const server: MCPServer = {
      id: 'weather',
      name: 'Weather API',
      version: '1.0.0',
      description: 'Fetches weather data.',
      author: 'acme',
      tags: [],
      status: 'INSTALLED',
    }
    expect(server.status).toBe('INSTALLED')
  })

  it('homepage is optional', () => {
    const server: MCPServer = {
      id: 's1',
      name: 'S1',
      version: '0.1.0',
      description: '',
      author: '',
      tags: [],
      status: 'AVAILABLE',
    }
    expect(server.homepage).toBeUndefined()
  })
})
