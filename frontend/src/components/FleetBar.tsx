import type { FleetSummary, HostMetrics } from '../types'

interface Props {
  fleet: FleetSummary
  hosts: Record<string, HostMetrics>
}

export function FleetBar({ fleet, hosts }: Props) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-6 bg-slate-800 border-b border-slate-700">
      <Stat label="Uptime" value={`${fleet.uptime_pct}%`} colour={fleet.uptime_pct > 95 ? 'text-green-400' : 'text-amber-400'} />
      <Stat label="Services" value={String(fleet.total_services)} colour="text-blue-400" />
      <Stat label="Alerts" value={String(fleet.alerts)} colour={fleet.alerts > 0 ? 'text-red-400' : 'text-green-400'} />
      <div className="text-center">
        <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Hosts</div>
        <div className="flex justify-center gap-2">
          {Object.entries(hosts).map(([name, h]) => (
            <span key={name} className="flex items-center gap-1 text-sm">
              <span className={`w-2 h-2 rounded-full ${h.status === 'up' ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-slate-400 text-xs">{name}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

function Stat({ label, value, colour }: { label: string; value: string; colour: string }) {
  return (
    <div className="text-center">
      <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">{label}</div>
      <div className={`text-2xl font-bold tabular-nums ${colour}`}>{value}</div>
    </div>
  )
}
