import Seat from './Seat'
import { useEffect, useState } from 'react'

function SeatList({eventId, eventTitle}) {
    const [seats, setSeats] = useState([]);
    
    useEffect(() => {
        async function fetchSeatsForEvent() {
            let res = await fetch(`http://localhost:8000/api/seats?event_id=${eventId}`)
            let data = await res.json();
            setSeats(await data);
        }
        
        fetchSeatsForEvent();
    }, [eventId])

    return (
        <>
            <ul id="seats-list">
                {seats.map((seat) => (
                    <Seat key={seat.id} seat={seat} eventTitle={eventTitle}/>
                ))}
            </ul>
        </>
    )
}

export default SeatList;