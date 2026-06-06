import { BrowserRouter, Routes, Route } from 'react-router-dom'
import EventList from './pages/EventList'
import EventDetail from './pages/EventDetail'
import UploadFlow from './pages/UploadFlow'
import Viewer from './pages/Viewer'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<EventList />} />
        <Route path="/events/:eventId" element={<EventDetail />} />
        <Route path="/events/:eventId/upload" element={<UploadFlow />} />
        <Route path="/view/:eventId" element={<Viewer />} />
      </Routes>
    </BrowserRouter>
  )
}
