import { useEffect, useRef } from 'react'
import * as THREE from 'three'

interface Props { plyUrl: string | null }

export default function SplatViewer({ plyUrl }: Props) {
  const canvasRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!canvasRef.current || !plyUrl) return

    // Dynamic import keeps the heavy GS library out of the initial bundle
    let viewer: any = null
    import('@mkkellogg/gaussian-splats-3d').then(({ Viewer: GsViewer }) => {
      viewer = new GsViewer({
        rootElement: canvasRef.current!,
        cameraUp: [0, -1, 0],
        initialCameraPosition: [0, 2, 5],
        initialCameraLookAt: [0, 0, 0],
      })
      viewer.addSplatScene(plyUrl, { showLoadingUI: false })
        .then(() => viewer.start())
    })

    return () => {
      viewer?.stop?.()
      viewer?.dispose?.()
    }
  }, [plyUrl])

  return <div ref={canvasRef} className="w-full h-full" />
}
