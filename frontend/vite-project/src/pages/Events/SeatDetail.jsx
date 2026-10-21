import { useEffect } from 'react'
import { useParams, useSearchParams } from 'react-router'

function SeatDetail() {
    const params = useParams();
    const [searchParams, setSearchParams] = useSearchParams();
    
    useEffect(() => {
        async function logBooking() {
            let res = await fetch("http://localhost:8000/api/bookings", {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({"seat_id": params.seatId, "user_id": localStorage.getItem("userId")})
            })
        }
        logBooking();
        async function cancelOtherBookings() {
            let res = await fetch(`http://localhost:8000/api/bookings?seat_id=${params.seatId}&user_id=${localStorage.getItem("userId")}`, {
                method: "PUT"
            })
        }
        cancelOtherBookings();
    }, [])


    return (
        <div id="seat-details-container">
            <p>{searchParams.get("eventTitle")}</p>
            <p>{searchParams.get("row")}</p>
            <p>{searchParams.get("number")}</p>
            <p>{searchParams.get("price")}</p>
        </div>
    )
}

export default SeatDetail;