import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useRef } from 'react'
import api from '../lib/api'
import SplatViewer from '../components/viewer/SplatViewer'
import TimelineScrubber from '../components/viewer/TimelineScrubber'
import LoadingOverlay from '../components/viewer/LoadingOverlay'
import { useViewerStore } from '../store/viewerStore'

export default function Viewer() {
  const { eventId } = useParams<{ eventId: string }>()
  const activeWindowId = useViewerStore(s => s.activeWindowId)

  const { data: scene, isLoading } = useQuery({
    queryKey: ['scene', eventId],
    queryFn: () => api.get(`/events/${eventId}/scene`).then(r => r.data),
  })

  if (isLoading || !scene) return <LoadingOverlay message="Loading scene..." />

  const activeWindow = scene.windows.find((w: any) => w.id === activeWindowId) ?? scene.windows[0]
  const plyUrl = activeWindow?.ply_url ?? null

  return (
    <div className="relative w-full h-screen bg-slate-950 overflow-hidden">
      <SplatViewer plyUrl={plyUrl} />
      <div className="absolute top-4 left-4 text-white font-semibold text-lg drop-shadow">
        {scene.event_name}
      </div>
      <TimelineScrubber windows={scene.windows} />
    </div>
  )
}
