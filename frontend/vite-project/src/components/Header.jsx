import { useNavigate } from 'react-router'


export default function Header () {
    const navigate = useNavigate();
    async function logOut() {
        let res = await fetch("http://localhost:8000/token", {method: "DELETE", credentials: 'include'});
        if (!res.ok) {
            alert("Something wrong happened while logging out");
        }
        localStorage.removeItem("userId");
        localStorage.removeItem("userEmail");
        navigate(0);
    }
    function goToLogin() {
        navigate('/login');
    }
    let header;
    if (!(window.location.pathname === "/login" || window.location.pathname === "/signup")) {
        if (!localStorage.getItem("userId")) {
            header = (
                <header>
                    <button id="header-login-btn" onClick={goToLogin}>Кіру</button>
                </header>
            )
        } else header = <header><button id="header-logout-btn" onClick={logOut}>Шығу</button></header>
    }
    return (
        <>{ header }</>
    )
}