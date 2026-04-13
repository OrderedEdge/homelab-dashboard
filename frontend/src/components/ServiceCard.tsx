import type { Service } from '../types'
import { Sparkline } from './Sparkline'

interface Props {
  service: Service
}

const CATEGORY_COLOURS: Record<string, string> = {
  monitoring: 'bg-blue-500/20 text-blue-400',
  security: 'bg-red-500/20 text-red-400',
  media: 'bg-purple-500/20 text-purple-400',
  network: 'bg-cyan-500/20 text-cyan-400',
  storage: 'bg-amber-500/20 text-amber-400',
  web: 'bg-green-500/20 text-green-400',
  infra: 'bg-slate-500/20 text-slate-400',
  iot: 'bg-pink-500/20 text-pink-400',
}

function sparklineColour(cpu: number | null): string {
  if (cpu === null) return '#64748b'
  if (cpu < 30) return '#22c55e'
  if (cpu < 60) return '#3b82f6'
  if (cpu < 85) return '#f59e0b'
  return '#ef4444'
}

export function ServiceCard({ service: s }: Props) {
  const isDown = s.status === 'down'
  const catClass = CATEGORY_COLOURS[s.category] || CATEGORY_COLOURS.infra

  return (
    <div className={`bg-slate-800 border rounded-xl p-4 transition-all hover:border-slate-600 ${isDown ? 'border-l-2 border-l-red-500 border-t-slate-700 border-r-slate-700 border-b-slate-700' : 'border-slate-700'}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${s.status === 'up' ? 'bg-green-500 shadow-[0_0_6px_#22c55e80]' : s.status === 'down' ? 'bg-red-500 shadow-[0_0_6px_#ef444480]' : 'bg-slate-500'}`} />
          <span className="font-semibold">{s.name}</span>
        </div>
        <span className="text-xs text-slate-500">CT {s.ct}</span>
      </div>

      <div className="flex items-center gap-2 mb-3">
        <span className="text-xs text-slate-500">{s.host}</span>
        <span className={`text-xs px-1.5 py-0.5 rounded ${catClass}`}>{s.category}</span>
      </div>

      <div className="mb-3">
        <Sparkline data={s.cpu_sparkline} colour={sparklineColour(s.cpu_pct)} />
      </div>

      <div className="flex items-center justify-between text-xs">
        {isDown ? (
          <span className="text-red-400">Target down</span>
        ) : (
          <span className="text-slate-500">
            {s.cpu_pct !== null ? `CPU ${s.cpu_pct}%` : 'No metrics'}
          </span>
        )}
        {s.link && (
          <a
            href={s.link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300"
            onClick={e => e.stopPropagation()}
          >
            Open ↗
          </a>
        )}
      </div>
    </div>
  )
}
