import { Link } from 'react-router'


function Seat({seat, eventTitle}) {
    let backgroundColor = "";
    switch(seat.status) {
        case "FREE": backgroundColor = "var(--ocean-blue)"; break;
        case "RESERVED": backgroundColor = "rgb(253, 146, 33)"; break;
        case "BOOKED": backgroundColor = "rgb(253, 43, 43)"; break;
    }
    function SeatView() {
        if (seat.status==="RESERVED" || seat.status==="BOOKED") { 
            return (
                <div id="seat-view">
                    <p>{seat.row} - {seat.number}</p>
                </div>
            ); 
        } else {
            return (
                <Link to={{pathname: `seats/${seat.id}`, search: `?eventTitle=${eventTitle}&row=${seat.row}&number=${seat.number}&price=${seat.price}`}}>
                    <p>{seat.row} - {seat.number}</p>
                </Link>
            )
        }
    }
    
    return (
        <li className="seats" style={{backgroundColor: backgroundColor}}>
            <SeatView/>
        </li>
    )
}

export default Seat;