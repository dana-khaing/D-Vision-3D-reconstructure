import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../lib/api'

export default function EventDetail() {
  const { eventId } = useParams<{ eventId: string }>()
  const qc = useQueryClient()

  const { data: event } = useQuery({
    queryKey: ['event', eventId],
    queryFn: () => api.get(`/api/v1/events/${eventId}`).then(r => r.data),
  })

  const process = useMutation({
    mutationFn: () => api.post(`/api/v1/events/${eventId}/process`, { quality: 'standard' }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['event', eventId] }),
  })

  if (!event) return <div className="p-8 text-slate-400">Loading...</div>

  return (
    <div className="max-w-4xl mx-auto p-8">
      <Link to="/" className="text-slate-400 hover:text-white mb-6 block">← All events</Link>
      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-3xl font-bold">{event.name}</h1>
          {event.description && <p className="text-slate-400 mt-1">{event.description}</p>}
        </div>
        <div className="flex gap-3">
          <Link to={`/events/${eventId}/upload`}
            className="bg-slate-700 px-4 py-2 rounded-lg hover:bg-slate-600">
            Upload Photos
          </Link>
          {event.status === 'done' && (
            <Link to={`/view/${eventId}`}
              className="bg-violet-600 px-4 py-2 rounded-lg hover:bg-violet-500">
              View 3D Scene
            </Link>
          )}
          {event.status === 'created' && (
            <button onClick={() => process.mutate()}
              className="bg-cyan-600 px-4 py-2 rounded-lg hover:bg-cyan-500">
              Build 3D Scene
            </button>
          )}
        </div>
      </div>
      <div className="bg-slate-800 rounded-xl p-6">
        <p className="text-slate-400">Status: <span className="text-white font-medium">{event.status}</span></p>
      </div>
    </div>
  )
}
