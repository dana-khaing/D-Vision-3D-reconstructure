import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import api from '../lib/api'

export default function EventList() {
  const { data: events, isLoading } = useQuery({
    queryKey: ['events'],
    queryFn: () => api.get('/api/v1/events').then(r => r.data),
  })

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-violet-400">Memoir3D</h1>
        <Link to="/events/new" className="bg-violet-600 px-4 py-2 rounded-lg text-white hover:bg-violet-500">
          New Event
        </Link>
      </div>

      {isLoading ? (
        <p className="text-slate-400">Loading events...</p>
      ) : events?.length === 0 ? (
        <div className="text-center py-24 text-slate-500">
          <p className="text-xl mb-2">No events yet</p>
          <p>Create your first event to get started.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {events?.map((event: any) => (
            <Link key={event.id} to={`/events/${event.id}`}
              className="bg-slate-800 rounded-xl p-6 hover:bg-slate-700 transition">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-xl font-semibold">{event.name}</h2>
                  {event.description && <p className="text-slate-400 mt-1">{event.description}</p>}
                </div>
                <span className={`text-sm px-2 py-1 rounded ${
                  event.status === 'done' ? 'bg-green-800 text-green-200' :
                  event.status === 'processing' ? 'bg-yellow-800 text-yellow-200' :
                  'bg-slate-700 text-slate-300'}`}>
                  {event.status}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
