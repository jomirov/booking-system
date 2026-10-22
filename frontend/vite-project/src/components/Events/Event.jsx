import { useState, useEffect } from 'react'
import { Link } from 'react-router'

function Event({event}) {
    return (
        <>
            <li>
                <p id="event-title">{event.title}</p>
                <p id="event-date">{event.date}</p>
                <p id="event-location">{event.location}</p>
                <Link id="event-details-btn" to={`/events/${event.id}`}>Қарау</Link>
            </li>
        </>
    )
}

export default Event