import type { HostMetrics } from '../types'
import { Sparkline } from './Sparkline'

interface Props {
  name: string
  host: HostMetrics
}

function metricColour(pct: number): string {
  if (pct < 50) return 'text-green-400'
  if (pct < 75) return 'text-amber-400'
  return 'text-red-400'
}

function barColour(pct: number): string {
  if (pct < 50) return '#22c55e'
  if (pct < 75) return '#f59e0b'
  return '#ef4444'
}

export function HostSummary({ name: _name, host }: Props) {
  return (
    <div className="bg-slate-800 border-b border-slate-700">
      {/* Metrics bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 px-6 py-4">
        <div className="text-center">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">CPU</div>
          <div className={`text-3xl font-bold tabular-nums ${metricColour(host.cpu_pct)}`}>
            {host.cpu_pct}%
          </div>
        </div>
        <div className="text-center">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">RAM</div>
          <div className={`text-3xl font-bold tabular-nums ${metricColour(host.ram_pct)}`}>
            {host.ram_pct}%
          </div>
        </div>
        <div className="text-center">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Disk</div>
          <div className={`text-3xl font-bold tabular-nums ${metricColour(host.disk_pct)}`}>
            {host.disk_pct}%
          </div>
        </div>
        <div className="text-center">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-1">Status</div>
          <div className="flex items-center justify-center gap-2">
            <span className={`w-3 h-3 rounded-full ${host.status === 'up' ? 'bg-green-500 shadow-[0_0_8px_#22c55e80]' : 'bg-red-500 shadow-[0_0_8px_#ef444480]'}`} />
            <span className={`text-lg font-semibold capitalize ${host.status === 'up' ? 'text-green-400' : 'text-red-400'}`}>
              {host.status}
            </span>
          </div>
        </div>
      </div>

      {/* Sparkline charts */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 px-6 pb-4">
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">CPU History (1h)</div>
          <Sparkline data={host.cpu_sparkline} height={80} colour={barColour(host.cpu_pct)} />
        </div>
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">RAM History (1h)</div>
          <Sparkline data={host.ram_sparkline} height={80} colour={barColour(host.ram_pct)} />
        </div>
      </div>
    </div>
  )
}
