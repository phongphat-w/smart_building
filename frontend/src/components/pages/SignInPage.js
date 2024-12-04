import React, { useState } from 'react';
import axios from 'axios';
import { jwtDecode } from "jwt-decode";

const LoginPage = () => {
  // State variables for the form fields and error messages
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');

    // Create the payload
    const data = { email, password };

    try {
        const response = await axios.post(`http://127.0.0.1:8000/api/login_guest/`, data, {
            headers: {
            'Content-Type': 'application/json',
            },
        });
        // Response contains a token
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token); 
        
        console.log('DEBUG: Access Token:', localStorage.getItem('access_token'));
        console.log('DEBUG: Refresh Token:', localStorage.getItem('refresh_token'));

        const token = localStorage.getItem('access_token')
        const decodedToken = jwtDecode(token); // jwtDecode is a function you can use from the 'jwt-decode' library
        console.log("DEBUG: SignIn - Token expiry: ", new Date(decodedToken.exp * 1000)); // Convert from seconds to milliseconds

        setLoading(false);

        // Redirect landing page
        window.location.href = '/dashboards';
    } catch (error) {
        setLoading(false);
        setErrorMessage(error.response ? error.response.data.error : 'Error during login');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="text-center mb-4">Login</h2>
              <form onSubmit={handleSubmit}>
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}

                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group mt-3">
                  <label htmlFor="password">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>

                <div className="d-flex justify-content-between mt-3">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                  </button>
                  <a href="/signup" className="btn btn-link">Sign Up</a>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
