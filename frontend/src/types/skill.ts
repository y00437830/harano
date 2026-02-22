/** Parameter type accepted by a Skill. */
export type ParameterType = 'string' | 'integer' | 'float' | 'boolean' | 'object' | 'array'

/** A single input parameter accepted by a Skill. */
export interface SkillParameter {
  name: string
  type: ParameterType
  description: string
  required: boolean
  defaultValue?: unknown
}

/** A Skill registered in the platform. */
export interface Skill {
  id: string
  name: string
  version: string
  description: string
  parameters: SkillParameter[]
  tags: string[]
}

/** Payload for creating or updating a Skill. */
export type SkillPayload = Omit<Skill, 'id'> & { id?: string }
