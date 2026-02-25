import type { Skill, SkillPayload } from '../types/skill'
import { apiRequest, JSON_HEADERS } from './apiUtils'

const BASE = '/api/skills'

export function listSkills(query?: string): Promise<Skill[]> {
  const url = query ? `${BASE}?q=${encodeURIComponent(query)}` : BASE
  return apiRequest<Skill[]>(url)
}

export function getSkill(id: string): Promise<Skill> {
  return apiRequest<Skill>(`${BASE}/${encodeURIComponent(id)}`)
}

export function createSkill(payload: SkillPayload): Promise<Skill> {
  return apiRequest<Skill>(BASE, {
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify(payload),
  })
}

export function updateSkill(id: string, payload: SkillPayload): Promise<Skill> {
  return apiRequest<Skill>(`${BASE}/${encodeURIComponent(id)}`, {
    method: 'PUT',
    headers: JSON_HEADERS,
    body: JSON.stringify(payload),
  })
}

export function deleteSkill(id: string): Promise<void> {
  return apiRequest<void>(`${BASE}/${encodeURIComponent(id)}`, { method: 'DELETE' })
}
