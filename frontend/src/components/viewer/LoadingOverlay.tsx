interface Props { message?: string }

export default function LoadingOverlay({ message = 'Loading...' }: Props) {
  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-slate-950 text-white">
      <div className="w-12 h-12 border-4 border-violet-500 border-t-transparent rounded-full animate-spin mb-4" />
      <p className="text-slate-300">{message}</p>
    </div>
  )
}
