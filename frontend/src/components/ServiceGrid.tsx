import type { Service, SortBy, StatusFilter } from '../types'
import { ServiceCard } from './ServiceCard'

interface Props {
  services: Service[]
  activeTab: string
  searchQuery: string
  statusFilter: StatusFilter
  sortBy: SortBy
}

function sortServices(services: Service[], by: SortBy): Service[] {
  return [...services].sort((a, b) => {
    switch (by) {
      case 'name': return a.name.localeCompare(b.name)
      case 'host': return a.host.localeCompare(b.host) || a.name.localeCompare(b.name)
      case 'ct': return a.ct - b.ct
      case 'status': {
        const order = { down: 0, unknown: 1, up: 2 }
        return (order[a.status as keyof typeof order] ?? 1) - (order[b.status as keyof typeof order] ?? 1)
      }
      default: return 0
    }
  })
}

export function ServiceGrid({ services, activeTab, searchQuery, statusFilter, sortBy }: Props) {
  let filtered = services

  if (activeTab !== 'all') {
    filtered = filtered.filter(s => s.host === activeTab)
  }

  if (searchQuery) {
    const q = searchQuery.toLowerCase()
    filtered = filtered.filter(s =>
      s.name.toLowerCase().includes(q) ||
      s.host.toLowerCase().includes(q) ||
      s.category.toLowerCase().includes(q)
    )
  }

  if (statusFilter !== 'all') {
    filtered = filtered.filter(s => s.status === statusFilter)
  }

  const sorted = sortServices(filtered, sortBy)

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-6">
      {sorted.map(s => (
        <ServiceCard key={s.name} service={s} />
      ))}
      {sorted.length === 0 && (
        <p className="text-slate-500 col-span-full text-center py-12">No services match filters</p>
      )}
    </div>
  )
}
