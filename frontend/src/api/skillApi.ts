import type { Skill, SkillPayload } from '../types/skill'

const BASE = '/api/skills'

export async function listSkills(query?: string): Promise<Skill[]> {
  const params = new URLSearchParams()
  if (query) params.set('q', query)
  const url = params.size ? `${BASE}?${params.toString()}` : BASE
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Failed to list skills: ${res.status}`)
  return res.json() as Promise<Skill[]>
}

export async function getSkill(id: string): Promise<Skill> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}`)
  if (!res.ok) throw new Error(`Skill not found: ${id}`)
  return res.json() as Promise<Skill>
}

export async function createSkill(payload: SkillPayload): Promise<Skill> {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(`Failed to create skill: ${res.status}`)
  return res.json() as Promise<Skill>
}

export async function updateSkill(id: string, payload: SkillPayload): Promise<Skill> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(`Failed to update skill: ${res.status}`)
  return res.json() as Promise<Skill>
}

export async function deleteSkill(id: string): Promise<void> {
  const res = await fetch(`${BASE}/${encodeURIComponent(id)}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`Failed to delete skill: ${res.status}`)
}
