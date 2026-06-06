import { create } from 'zustand'

interface ViewerState {
  activeWindowId: string | null
  setWindow: (id: string) => void
}

export const useViewerStore = create<ViewerState>(set => ({
  activeWindowId: null,
  setWindow: id => set({ activeWindowId: id }),
}))
