import { useEffect } from 'react'
import { Link, useNavigate } from 'react-router'


async function getToken() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let form_data = new FormData();
    form_data.append("username", email);
    form_data.append("password", password);
    
    let response = await fetch("http://localhost:8000/token", {
        method: "POST",
        body: form_data,
        credentials: 'include'
    });
    
    if (!response.ok) {
        return false;
    }
    return true;
}

async function fetchToken() {
    let response = await fetch("http://localhost:8000/users/me", {method: "GET", credentials: 'include'});
    let data = await response.json();
    
    if (!response.ok) {
        return false
    }

    localStorage.setItem("userId", data.current_user_id);
    localStorage.setItem("userEmail", data.current_user_email);

    return true;
}

export function isLogged() {
    return localStorage.getItem("userId");
}

function Login() {
    const navigate = useNavigate();

    useEffect(() => {
        if (isLogged()) {
            alert("You're already logged in!");
            navigate("/");
        }
    }, []);

    async function handleLoginSubmit(e) {
        e.preventDefault();
        let isToken = await getToken();
        if (!isToken) {
            alert("Invalid email or password");
            navigate(0);
        } else {
            await fetchToken();
            navigate("/");
        }
    }
    
    return (
        <>
            <form id='form-login' className='form-authentication' onSubmit={handleLoginSubmit}>
                <h4>Аккаунтқа кіру</h4>
                <label htmlFor='email'>Электронды пошта</label>
                <input type='email' id="email" required></input>
                <label htmlFor='password'>Құпия сөз</label>
                <input type='password' id='password' required></input>
                <button type='submit'>Кіру</button>
                <Link to="/signup">Аккаунт құру</Link>
            </form>
        </>
    )
}

export default Login;