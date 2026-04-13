import type { SortBy, StatusFilter } from '../types'

interface Props {
  searchQuery: string
  onSearchChange: (q: string) => void
  statusFilter: StatusFilter
  onStatusFilterChange: (f: StatusFilter) => void
  sortBy: SortBy
  onSortChange: (s: SortBy) => void
  serviceCount: number
}

export function Toolbar({
  searchQuery, onSearchChange,
  statusFilter, onStatusFilterChange,
  sortBy, onSortChange,
  serviceCount,
}: Props) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 px-6 py-3">
      <div className="flex items-center gap-3">
        <span className="font-semibold">{serviceCount} services</span>
        <input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={e => onSearchChange(e.target.value)}
          className="px-3 py-1.5 rounded-md border border-slate-700 bg-slate-900 text-slate-200 text-sm placeholder-slate-500 w-40 focus:outline-none focus:border-blue-500"
        />
      </div>
      <div className="flex items-center gap-2">
        {(['all', 'up', 'down'] as StatusFilter[]).map(f => (
          <button
            key={f}
            onClick={() => onStatusFilterChange(f)}
            className={`px-3 py-1 rounded-md border text-xs capitalize ${
              statusFilter === f
                ? 'bg-blue-600 border-blue-600 text-white'
                : 'border-slate-700 bg-slate-800 text-slate-400'
            }`}
          >
            {f}
          </button>
        ))}
        <span className="text-slate-600 mx-1">|</span>
        {(['name', 'host', 'ct', 'status'] as SortBy[]).map(s => (
          <button
            key={s}
            onClick={() => onSortChange(s)}
            className={`px-3 py-1 rounded-md border text-xs capitalize ${
              sortBy === s
                ? 'bg-blue-600 border-blue-600 text-white'
                : 'border-slate-700 bg-slate-800 text-slate-400'
            }`}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}
