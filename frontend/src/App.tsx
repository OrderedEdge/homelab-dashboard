import { useState } from 'react'
import { useStatus } from './hooks/useStatus'
import { FleetBar } from './components/FleetBar'
import { QuickAccess } from './components/QuickAccess'
import { TabBar } from './components/TabBar'
import { Toolbar } from './components/Toolbar'
import { ServiceGrid } from './components/ServiceGrid'
import { HostSummary } from './components/HostSummary'
import type { ActiveTab, SortBy, StatusFilter } from './types'

const HOSTS = ['cosmos', 'zeus', 'nuc', 'titan', 'forge', 'network', 'smarthome']

export default function App() {
  const { data, loading, error } = useStatus()
  const [activeTab, setActiveTab] = useState<ActiveTab>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all')
  const [sortBy, setSortBy] = useState<SortBy>('name')

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <p className="text-slate-400">Loading dashboard...</p>
      </div>
    )
  }

  if (error && !data) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <p className="text-red-400">Error: {error}</p>
      </div>
    )
  }

  if (!data) return null

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200">
      <header className="bg-slate-800 border-b border-slate-700 px-8 py-5 flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">
          Homelab <span className="text-blue-400">Dashboard</span>
        </h1>
        <span className="text-xs text-slate-500">
          Updated {new Date(data.updated_at).toLocaleTimeString()}
        </span>
      </header>

      <FleetBar fleet={data.fleet} hosts={data.hosts} />
      <QuickAccess services={data.services} />
      <TabBar activeTab={activeTab} onTabChange={setActiveTab} services={data.services} hosts={HOSTS} />
      {activeTab !== 'all' && data.hosts[activeTab] && (
        <HostSummary name={activeTab} host={data.hosts[activeTab]} />
      )}
      <Toolbar
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        statusFilter={statusFilter}
        onStatusFilterChange={setStatusFilter}
        sortBy={sortBy}
        onSortChange={setSortBy}
        serviceCount={data.services.length}
      />
      <ServiceGrid
        services={data.services}
        activeTab={activeTab}
        searchQuery={searchQuery}
        statusFilter={statusFilter}
        sortBy={sortBy}
      />
    </div>
  )
}
