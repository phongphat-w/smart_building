import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import { useNavigate } from 'react-router-dom';

const DeviceDashboard = () => {
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Function to get the token from localStorage
  const getAuthToken = () => localStorage.getItem('access_token');
  const getRefreshToken = () => localStorage.getItem('refresh_token');

  console.log('DEBUG: Onload() getAuthToken = ' + getAuthToken());
  console.log('DEBUG: Onload() getRefreshToken = ' + getRefreshToken());

  // SignOut function - used to remove tokens from localStorage
  const signOut = useCallback(() => {
    console.log("DEBUG: signOut() - is working")
    //localStorage.removeItem('access_token');  // Remove access token
    //localStorage.removeItem('refresh_token');  // Remove refresh token
    console.log("DEBUG: 2 tokens are removed")
    //navigate('/signin');  // Redirect to Sign In page
  //}, [navigate]);
  }, []);

  // Redirect to SignIn if there's no auth token, useEffect ensures this is only triggered on page load
  useEffect(() => {
    console.log("DEBUG: useEffect() - is working")
    const token = getAuthToken();

    console.log("DEBUG: useEffect() -  token = " + token)

    if (!token) {
      //navigate('/signin'); // Redirect if no token
      console.log("DEBUG: useEffect() -  if (!token) = " + token)
    }
  //}, [navigate]);
  }, []);

  // Memoized function to refresh the token
  const refreshAuthToken = useCallback(async () => {
    try {
      const refreshToken = getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      console.log("DEBUG: refreshAuthToken() - Sending refresh token:", refreshToken);

      const response = await axios.post(`http://127.0.0.1:8000/api/token/refresh/`, { 
        headers: { Authorization: `Bearer ${refreshToken}` },
        refresh: refreshToken 
      });

      if (response.data && response.data.access) {
        const { access } = response.data;  // .data is an object of access token from the response
        localStorage.setItem('access_token', access); // Store the new access token
        return access;
      } else {
        console.error('Invalid response from refresh token endpoint');
        throw new Error('Invalid response from refresh token endpoint');
      }
    } catch (error) {
      console.error('Error refreshing token:', error);
      throw new Error('Unable to refresh token');
    }
  }, []);

  // Memoized function to fetch devices with token expiration handling
  const fetchDevices = useCallback(async () => {
    console.log('fetchDevices() is working')
    setLoading(true); // Set loading state to true while fetching data
    try {
      const token = getAuthToken();
      if (!token) {
        setErrorMessage('No authorization token found');
        setLoading(false);  // Set loading state to false after handling the error
        return;
      }
      console.log('DEBUG: auth_token still not expire')
      // First attempt to fetch devices with the current token
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/get_user_devices/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDevices(response.data.data);  // Set devices if request is successful
        setLoading(false);  // Set loading state to false after fetching devices

        console.log('DEBUG: fetchDevices() - auth_token still not expire')

      } catch (error) {
        if (error.response && error.response.status === 401) {
          console.log('DEBUG: Token expired, attempting to refresh...');
          try {
            const newToken = await refreshAuthToken();
            // Retry the device fetch with the new token
            const response = await axios.get(`http://127.0.0.1:8000/api/get_user_devices/`, {
              headers: { Authorization: `Bearer ${newToken}` },
            });
            setDevices(response.data.data);  // Update devices state
            setLoading(false);  // Set loading state to false after retrying
          } catch (refreshError) {
            setErrorMessage('Unable to refresh token');
            console.error('Error refreshing token:', refreshError);
            signOut();  // Log out the user and redirect to login
            setLoading(false);  // Set loading state to false after refresh failure
          }
        } else {
          setErrorMessage('Error fetching devices');
          console.error('Error fetching devices:', error);
          setLoading(false);  // Set loading state to false after error
        }
      }
    } catch (error) {
      setErrorMessage('Error fetching devices');
      console.error('Error fetching devices:', error);
      setLoading(false);  // Set loading state to false after handling the error
    }
  }, [refreshAuthToken, signOut]);

  // Fetch devices after login or token change
  useEffect(() => {
    fetchDevices();
  }, [fetchDevices]);  // Now correctly tracks fetchDevices as a stable function

  // Handle device control (e.g., changing temperature)
  const handleDeviceControl = (device) => {
    setSelectedDevice(device);
  };

  const handleTemperatureChange = async () => {
    try {
      const token = getAuthToken();
      const response = await axios.post(
        `http://127.0.0.1:8000/api/control_device/${selectedDevice.id}/`,
        { headers: { Authorization: `Bearer ${token}` } },
        { temperature: selectedDevice.temperature }        
      );
      setSelectedDevice(response.data.device); // Update device data with new value
    } catch (error) {
      setErrorMessage('Error updating device');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Device Dashboard</h2>
      {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}

      {/* Loading Indicator */}
      {loading && <div>Loading...</div>}

      {/* Sign out button */}
      <button className="btn btn-danger" onClick={signOut} style={{ position: 'absolute', top: '10px', right: '10px' }}>
        Sign Out
      </button>

      <div className="row">
        {devices.map((device) => (
          <div className="col-md-4" key={device.id}>
            <div className="card mb-4">
              <div className="card-body">
                <h5 className="card-title">{device.name}</h5>
                <p>Current Temperature: {device.temperature}°C</p>
                <p>Status: {device.status}</p>
                <button className="btn btn-primary" onClick={() => handleDeviceControl(device)}>
                  Configure
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Device Configuration Modal */}
      {selectedDevice && (
        <Modal isOpen={true} onRequestClose={() => setSelectedDevice(null)}>
          <h2>Configure {selectedDevice.name}</h2>
          <label>Temperature: </label>
          <input
            type="number"
            className="form-control"
            value={selectedDevice.temperature}
            onChange={(e) => setSelectedDevice({ ...selectedDevice, temperature: e.target.value })}
            required
          />
          <button onClick={handleTemperatureChange} className="btn btn-success mt-3">
            Save Changes
          </button>
          <button onClick={() => setSelectedDevice(null)} className="btn btn-secondary mt-3">
            Close
          </button>
        </Modal>
      )}
    </div>
  );
};

export default DeviceDashboard;
