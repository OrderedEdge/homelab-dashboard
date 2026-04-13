import type { ActiveTab, Service } from '../types'

interface Props {
  activeTab: ActiveTab
  onTabChange: (tab: ActiveTab) => void
  services: Service[]
  hosts: string[]
}

const HOST_ICONS: Record<string, string> = {
  all: '◆',
  cosmos: '🖥️',
  zeus: '⚡',
  nuc: '📦',
  titan: '🤖',
  forge: '🔥',
  network: '🌐',
  smarthome: '🏠',
}

export function TabBar({ activeTab, onTabChange, services, hosts }: Props) {
  const tabs = ['all', ...hosts]

  return (
    <div className="flex gap-2 px-6 py-3 bg-slate-800 border-b border-slate-700 overflow-x-auto">
      {tabs.map(tab => {
        const count = tab === 'all' ? services.length : services.filter(s => s.host === tab).length
        const isActive = activeTab === tab
        return (
          <button
            key={tab}
            onClick={() => onTabChange(tab)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-medium whitespace-nowrap transition-all ${
              isActive
                ? 'bg-blue-600 border-blue-600 text-white'
                : 'bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-500 hover:text-slate-200'
            }`}
          >
            <span>{HOST_ICONS[tab] || '◆'}</span>
            <span className="capitalize">{tab}</span>
            <span className={`text-xs px-1.5 py-0.5 rounded-full ${isActive ? 'bg-white/20' : 'bg-slate-700'}`}>
              {count}
            </span>
          </button>
        )
      })}
    </div>
  )
}
