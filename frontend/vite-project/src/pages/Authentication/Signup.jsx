import { useEffect } from 'react'
import { Link, useNavigate } from 'react-router'
import { isLogged } from './Login'

async function signupRequest() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let response = await fetch("http://localhost:8000/api/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"email": email, "password": password})
    });
    if (!response.ok) {
        alert(`${response.status} ${response.statusText}`);
        return false;
    }
    return true;
}

async function handleSignupSubmit(e) {
    e.preventDefault();
    let isSuccess = await signupRequest();
    if (!isSuccess) {
        alert("Something wrong is happened while signup");
        return;
    }  
    alert("Аккаунт сәтті құрылды");
    window.location.href = "/login";
}

function Signup() {
    const navigate = useNavigate();
    useEffect(() => {
        
        if (isLogged()) {
            alert("You're already logged in!");
            navigate("/");
        }
    }, [])
    return (
        <>
            <form id="form-signup" className="form-authentication" onSubmit={handleSignupSubmit}>
                <h4>Аккаунтты құру</h4>
                <label htmlFor="email">Электронды пошта</label>
                <input type="email" id="email" placeholder="example@test.com" required></input>
                <label htmlFor="password">Құпия сөз</label>
                <input type="text" id='password' minLength='8' required></input>
                <button type='submit'>Аккаунт құру</button>
                <Link to='/login'>Кіру</Link>
            </form>
        </>
    )
}

export default Signup;