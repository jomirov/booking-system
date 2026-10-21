import Event from './Event'
import { useState, useEffect } from 'react'

function EventList() {
    const [events, setEvents] = useState([]);
    useEffect(() => {
        async function fetchEvents() {
            let res = await fetch("http://localhost:8000/api/events");
            setEvents(await res.json());
        }
        fetchEvents();
    }, []);

    return (
        <>
            <ul id="events-list">
                {events.map((event) => (
                    <Event key={event.id} event={event}/>
                ))}
            </ul>
        </>
    )
}

export default EventList;