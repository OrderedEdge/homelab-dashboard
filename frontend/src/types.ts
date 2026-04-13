export interface FleetSummary {
  uptime_pct: number
  total_services: number
  alerts: number
  hosts: number
}

export interface HostMetrics {
  status: string
  cpu_pct: number
  ram_pct: number
  disk_pct: number
  cpu_sparkline: number[]
  ram_sparkline: number[]
}

export interface Service {
  name: string
  host: string
  ct: number
  ip: string
  instance: string
  link: string | null
  linkLabel: string | null
  category: string
  pinned: boolean
  status: string
  cpu_pct: number | null
  cpu_sparkline: number[]
}

export interface DashboardStatus {
  fleet: FleetSummary
  hosts: Record<string, HostMetrics>
  services: Service[]
  updated_at: string
}

export type ActiveTab = 'all' | string
export type StatusFilter = 'all' | 'up' | 'down'
export type SortBy = 'name' | 'host' | 'ct' | 'status'
