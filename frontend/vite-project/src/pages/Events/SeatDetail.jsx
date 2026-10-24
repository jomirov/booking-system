import { useEffect } from 'react'
import { useParams, useSearchParams, useNavigate } from 'react-router'
import { checkUser } from './EventDetail'


function SeatDetail() {
    const navigate = useNavigate();
    const params = useParams();
    const [searchParams, setSearchParams] = useSearchParams();

    async function getActiveBooking() {
        let res = await fetch(`http://localhost:8000/api/bookings/active?user_id=${localStorage.getItem("userId")}`)
        let data = await res.json();
        return (await data);
    }
    useEffect(() => {
        checkUser();
        async function logBooking() {
            let activeBooking = await getActiveBooking();
            let currentSeatId = params.seatId;
            localStorage.setItem("currentSeatId", currentSeatId);
            
            if (!activeBooking || (activeBooking.seat_id != currentSeatId)) {
                fetch("http://localhost:8000/api/bookings", {
                    method: 'POST',
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({"seat_id": params.seatId, "user_id": localStorage.getItem("userId")})
                })
            }

        }
        logBooking();
        setTimeout(() => {
            navigate(`/events/${params.eventId}`);
        }, 300000);
    }, [])
    
    async function bookSeat() {
        document.getElementById("seat-details-container").innerHTML = "Loading...";
        setTimeout(() => {
            fetch(`http://localhost:8000/api/bookings/book?user_id=${localStorage.getItem("userId")}`, {method: "PUT"});
            
            alert("Билет сіздің электронды поштаңызға жіберілді!");
            navigate(`/events/${params.eventId}`);
        }, 3000)
    }

    
    return (
        <div id="seat-details-container">
            <p>Іс-шара аты: {searchParams.get("eventTitle")}</p>
            <p>Қатар: {searchParams.get("row")}</p>
            <p>Нөмір: {searchParams.get("number")}</p>
            <p>Бағасы: {searchParams.get("price")} тг.</p>
            <button onClick={bookSeat}>Брондау</button>
        </div>
    )
}
export default SeatDetail;