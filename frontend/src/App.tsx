import { useState } from 'react'
import SkillList from './components/SkillList'
import MCPMarket from './components/MCPMarket'
import './App.css'

type Tab = 'skills' | 'mcp'

export default function App() {
  const [tab, setTab] = useState<Tab>('skills')

  return (
    <div className="app">
      <header>
        <h1>Harano</h1>
        <p>Skill &amp; MCP Marketplace</p>
        <nav>
          <button
            onClick={() => setTab('skills')}
            style={{ fontWeight: tab === 'skills' ? 'bold' : 'normal', marginRight: '1rem' }}
          >
            Skills
          </button>
          <button
            onClick={() => setTab('mcp')}
            style={{ fontWeight: tab === 'mcp' ? 'bold' : 'normal' }}
          >
            MCP Market
          </button>
        </nav>
      </header>

      <main>
        {tab === 'skills' && <SkillList />}
        {tab === 'mcp' && <MCPMarket />}
      </main>
    </div>
  )
}
