import { useCallback, useEffect, useState } from 'react'
import type { DashboardStatus } from '../types'

const POLL_INTERVAL = 30_000

export function useStatus() {
  const [data, setData] = useState<DashboardStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStatus = useCallback(async () => {
    try {
      const resp = await fetch('/api/status')
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const json = await resp.json()
      setData(json)
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [fetchStatus])

  return { data, loading, error, refetch: fetchStatus }
}
