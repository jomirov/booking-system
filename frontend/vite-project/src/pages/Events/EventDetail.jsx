import SeatList from '../../components/Seats/SeatList'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import { isLogged } from '../Authentication/Login';

export async function checkUser() {
    if (!(await isLogged())) window.location.href = "/login";
}

function EventDetail() {
    const [event, setEvent] = useState({});
    const params = useParams();

    useEffect(() => {
        checkUser();
        async function fetchEvent() {
            let res = await fetch(`http://localhost:8000/api/events/${params.eventId}`);
            let data = await res.json();
            setEvent(await data);
        }
        fetchEvent();
    }, [])

    return(
        <>
            <div id="event-details-container">
                <p>Іс-шара аты: {event.title}</p>
                <p>Өткізілу күні: {event.date}</p>
                <p>Өту орны: {event.location}</p>
                <h4>Орындар</h4>
                <SeatList eventId={params.eventId} eventTitle={event.title}/>
            </div>
        </>
    )
}

export default EventDetail;