import { useNavigate, useParams } from 'react-router'


export default function Header () {
    const navigate = useNavigate();
    const params = useParams();
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
    function goBack() {
        if (window.location.pathname.includes("/seats")) navigate(-1); 
        else if (window.location.pathname.includes("/events")) navigate("/");
        else navigate(-1);
    }
    let backBtn = (window.location.pathname != "/") ? (<button id="header-back-btn" onClick={goBack}>Артқа</button>) : (<div></div>)
    let header;
    if (!(window.location.pathname === "/login" || window.location.pathname === "/signup")) {
        if (!localStorage.getItem("userId")) {
            header = (
                <header>
                    {backBtn}
                    <button id="header-login-btn" onClick={goToLogin}>Кіру</button>
                </header>
            )
        } else header = <header>{backBtn}<button id="header-logout-btn" onClick={logOut}>Шығу</button></header>
    }
    return (
        <>{ header }</>
    )
}