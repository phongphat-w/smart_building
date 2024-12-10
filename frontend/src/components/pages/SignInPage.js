import React, { useState } from 'react';
import axios from 'axios';
import { jwtDecode } from "jwt-decode";

const API_URL = process.env.REACT_APP_SB_API_URL + ":" + process.env.REACT_APP_SB_API_PORT;

const LoginPage = () => {
  // State variables for the form fields, error messages, and user info
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [userInfo, setUserInfo] = useState(null);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page refresh
    setLoading(true);
    setErrorMessage('');

    // Create the payload
    const data = { email, password };

    try {
      const response = await axios.post(`${API_URL}/api/login_guest/`, data, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Extract user info and tokens
      const userInfo = response.data.data.sb_user_info;
      setUserInfo(userInfo);
      console.log("DEBUG: First Name:", userInfo[0].first_name);

      localStorage.setItem('sb_access_token', response.data.data.sb_access_token);
      localStorage.setItem('sb_refresh_token', response.data.data.sb_refresh_token);
      localStorage.setItem('sb_user_info', JSON.stringify(userInfo)); // Store as JSON string

      console.log('DEBUG: Access Token:', localStorage.getItem('sb_access_token'));
      console.log('DEBUG: Refresh Token:', localStorage.getItem('sb_refresh_token'));
      console.log('DEBUG: User Info:', JSON.parse(localStorage.getItem('sb_user_info')));

      // Decode and log token expiration
      const token = response.data?.data?.sb_access_token;
      const decodedToken = jwtDecode(token);
      console.log("DEBUG: Token expiry:", new Date(decodedToken.exp * 1000)); // Convert from seconds to milliseconds

      setLoading(false);

      // Redirect to the dashboard
      window.location.href = '/dashboard';

    } catch (error) {
      setLoading(false);
      setErrorMessage(error.response?.data?.error || 'Error during login');
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
