import { useViewerStore } from '../../store/viewerStore'

interface Window { id: string; label: string | null; photo_count: number; status: string }
interface Props { windows: Window[] }

export default function TimelineScrubber({ windows }: Props) {
  const { activeWindowId, setWindow } = useViewerStore()
  const maxCount = Math.max(...windows.map(w => w.photo_count), 1)

  return (
    <div className="absolute bottom-0 left-0 right-0 bg-slate-900/80 backdrop-blur px-4 pb-4 pt-2">
      <div className="flex gap-1 items-end h-12">
        {windows.map(w => (
          <button
            key={w.id}
            onClick={() => setWindow(w.id)}
            title={w.label ?? w.id}
            className={`flex-1 rounded-t transition-all ${
              w.id === activeWindowId ? 'bg-violet-500' : 'bg-slate-600 hover:bg-slate-500'
            }`}
            style={{ height: `${Math.max(20, (w.photo_count / maxCount) * 100)}%` }}
          />
        ))}
      </div>
      <div className="flex justify-between text-xs text-slate-400 mt-1">
        <span>{windows[0]?.label}</span>
        <span>{windows[windows.length - 1]?.label}</span>
      </div>
    </div>
  )
}
