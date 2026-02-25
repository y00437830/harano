import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import {
  listSkills,
  getSkill,
  createSkill,
  updateSkill,
  deleteSkill,
} from '../api/skillApi'
import type { Skill } from '../types/skill'

const mockSkill: Skill = {
  id: 'greet',
  name: 'Greet',
  version: '1.0.0',
  description: 'A greeting skill',
  parameters: [],
  tags: ['test'],
}

function mockFetch(data: unknown, status = 200) {
  return vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(data),
  })
}

beforeEach(() => {
  vi.stubGlobal('fetch', mockFetch([mockSkill]))
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('skillApi', () => {
  it('listSkills fetches /api/skills', async () => {
    vi.stubGlobal('fetch', mockFetch([mockSkill]))
    const skills = await listSkills()
    expect(skills).toHaveLength(1)
    expect(skills[0].id).toBe('greet')
  })

  it('listSkills with query appends ?q=', async () => {
    const spy = mockFetch([mockSkill])
    vi.stubGlobal('fetch', spy)
    await listSkills('weather')
    expect(spy).toHaveBeenCalledWith('/api/skills?q=weather')
  })

  it('getSkill fetches /api/skills/:id', async () => {
    vi.stubGlobal('fetch', mockFetch(mockSkill))
    const skill = await getSkill('greet')
    expect(skill.name).toBe('Greet')
  })

  it('createSkill posts to /api/skills', async () => {
    const spy = mockFetch(mockSkill, 201)
    vi.stubGlobal('fetch', spy)
    const { id: _id, ...payload } = mockSkill
    const created = await createSkill(payload)
    expect(created.id).toBe('greet')
    expect(spy).toHaveBeenCalledWith('/api/skills', expect.objectContaining({ method: 'POST' }))
  })

  it('updateSkill puts to /api/skills/:id', async () => {
    const spy = mockFetch(mockSkill)
    vi.stubGlobal('fetch', spy)
    const { id: _id, ...payload } = mockSkill
    await updateSkill('greet', payload)
    expect(spy).toHaveBeenCalledWith('/api/skills/greet', expect.objectContaining({ method: 'PUT' }))
  })

  it('deleteSkill calls DELETE /api/skills/:id', async () => {
    const spy = vi.fn().mockResolvedValue({ ok: true, status: 204 })
    vi.stubGlobal('fetch', spy)
    await deleteSkill('greet')
    expect(spy).toHaveBeenCalledWith('/api/skills/greet', expect.objectContaining({ method: 'DELETE' }))
  })

  it('throws on non-ok response', async () => {
    vi.stubGlobal('fetch', mockFetch(null, 404))
    await expect(getSkill('nonexistent')).rejects.toThrow()
  })
})
