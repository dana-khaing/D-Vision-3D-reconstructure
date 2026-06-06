import { useParams } from 'react-router-dom'
import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

export default function UploadFlow() {
  const { eventId } = useParams<{ eventId: string }>()
  const [uploading, setUploading] = useState(false)
  const [uploaded, setUploaded] = useState(0)
  const [total, setTotal] = useState(0)

  const onDrop = useCallback(async (accepted: File[]) => {
    setUploading(true)
    setTotal(accepted.length)
    setUploaded(0)

    const BATCH = 10
    for (let i = 0; i < accepted.length; i += BATCH) {
      const batch = accepted.slice(i, i + BATCH)
      const fd = new FormData()
      batch.forEach(f => fd.append('files', f))
      await axios.post(`/api/v1/events/${eventId}/photos`, fd)
      setUploaded(prev => prev + batch.length)
    }
    setUploading(false)
  }, [eventId])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png', '.heic', '.heif'] },
    multiple: true,
  })

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Upload Photos</h1>
      <div {...getRootProps()} className={`border-2 border-dashed rounded-xl p-16 text-center cursor-pointer transition ${
        isDragActive ? 'border-violet-400 bg-violet-900/20' : 'border-slate-600 hover:border-slate-400'}`}>
        <input {...getInputProps()} />
        <p className="text-xl mb-2">Drop photos here</p>
        <p className="text-slate-400">or click to select from your camera roll</p>
      </div>
      {uploading && (
        <div className="mt-6">
          <div className="flex justify-between text-sm text-slate-400 mb-2">
            <span>Uploading...</span>
            <span>{uploaded} / {total}</span>
          </div>
          <div className="h-2 bg-slate-700 rounded-full">
            <div className="h-2 bg-violet-500 rounded-full transition-all"
              style={{ width: `${total ? (uploaded / total) * 100 : 0}%` }} />
          </div>
        </div>
      )}
      {!uploading && uploaded > 0 && (
        <p className="mt-6 text-green-400 text-center">
          {uploaded} photos uploaded successfully!
        </p>
      )}
    </div>
  )
}
