import { useEffect, useRef, useState } from 'react'

interface ProgressEvent {
  job_id: string
  stage: string
  pct: number
  msg: string
  ts: string
}

export function useJobWebSocket(jobId: string | null) {
  const [progress, setProgress] = useState<ProgressEvent | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!jobId) return

    let retryDelay = 1000
    let stopped = false

    function connect() {
      if (stopped) return
      const ws = new WebSocket(`ws://localhost:8000/ws/jobs/${jobId}`)
      wsRef.current = ws

      ws.onmessage = e => {
        try { setProgress(JSON.parse(e.data)) } catch {}
      }

      ws.onclose = () => {
        if (!stopped) setTimeout(connect, Math.min(retryDelay *= 2, 30_000))
      }
    }

    connect()
    return () => { stopped = true; wsRef.current?.close() }
  }, [jobId])

  return progress
}
