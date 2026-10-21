import './index.css'
import { Routes, Route } from 'react-router'
import Login from './pages/Authentication/Login'
import Signup from './pages/Authentication/Signup'
import Events from './pages/Events/Events'
import EventDetail from './pages/Events/EventDetail'
import SeatDetail from './pages/Events/SeatDetail'
import Header from './components/Header'

function App() {
    return (
        <>
            <Header/>
            <Routes>
                <Route path="login" element={<Login/>}/>
                <Route path="signup" element={<Signup/>}/>
                <Route path="/" element={<Events/>}/>
                <Route path="events/:eventId" element={<EventDetail/>}/>
                <Route path="events/:eventId/seats/:seatId" element={<SeatDetail/>}/>
            </Routes>
        </>
    )
}

export default App