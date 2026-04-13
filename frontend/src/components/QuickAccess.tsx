import type { Service } from '../types'

interface Props {
  services: Service[]
}

export function QuickAccess({ services }: Props) {
  const pinned = services.filter(s => s.pinned && s.link)
  if (pinned.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2 px-6 py-3 bg-slate-800/50 border-b border-slate-700">
      <span className="text-xs uppercase tracking-wider text-slate-500 self-center mr-2">Quick Access</span>
      {pinned.map(s => (
        <a
          key={s.name}
          href={s.link!}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 px-3 py-1 rounded-md bg-slate-900 border border-slate-700 text-sm text-blue-400 hover:border-blue-400 transition-colors"
        >
          <span className={`w-1.5 h-1.5 rounded-full ${s.status === 'up' ? 'bg-green-500' : 'bg-red-500'}`} />
          {s.name}
          <span className="text-slate-500">↗</span>
        </a>
      ))}
    </div>
  )
}
