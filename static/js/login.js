import axios from "axios"

const submitButton = document.getElementById('submitButton');
const form = document.getElementById('loginForm');

submitButton.addEventListener('click', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(form); // Create a FormData object from the form

    const res = await axios.post("http://localhost:8000/login/",
        formData,
        {
            headers: {
                'Content-Type':'application/x-www-form-urlencoded'
            }
        }
    );

    if (!res.ok) {
        // Handle error response
        console.error('Error sending data:', res.status);
        return;
    }

    const response = await res.json(); // Parse the JSON response
    if (response.token) {
        // Store the token in local storage or a secure mechanism
        localStorage.setItem('jwtToken', response.token);
        console.log('Token received:', response.token);

        // Redirect to the desired page after successful login
        window.location.href = '/home';
    } else {
        // Handle login failure
        console.error('Login failed:', response.message);
    }
});
