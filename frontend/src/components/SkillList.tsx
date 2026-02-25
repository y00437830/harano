import { useCallback, useEffect, useState } from 'react'
import type { Skill } from '../types/skill'
import { listSkills, deleteSkill } from '../api/skillApi'
import { toErrorMessage } from '../utils/errorUtils'

export default function SkillList() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [query, setQuery] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const load = useCallback((q: string) => {
    setLoading(true)
    setError(null)
    listSkills(q || undefined)
      .then(setSkills)
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

  const handleDelete = (id: string) => {
    deleteSkill(id)
      .then(() => load(query))
      .catch((e: unknown) => setError(toErrorMessage(e)))
  }

  return (
    <section>
      <h2>Skills</h2>
      <form onSubmit={handleSearch} style={{ marginBottom: '1rem' }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search skills…"
        />
        <button type="submit">Search</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Loading…</p>}

      {!loading && skills.length === 0 && <p>No skills found.</p>}

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {skills.map(skill => (
          <li key={skill.id} style={{ border: '1px solid #ddd', borderRadius: 6, padding: '0.75rem', marginBottom: '0.5rem' }}>
            <strong>{skill.name}</strong>
            <span style={{ marginLeft: '0.5rem', color: '#666', fontSize: '0.85em' }}>v{skill.version}</span>
            <p style={{ margin: '0.25rem 0', fontSize: '0.9em' }}>{skill.description}</p>
            {skill.tags.length > 0 && (
              <p style={{ margin: '0.25rem 0', fontSize: '0.8em', color: '#555' }}>
                {skill.tags.join(', ')}
              </p>
            )}
            <button onClick={() => handleDelete(skill.id)} style={{ marginTop: '0.5rem' }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
