import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Modal from 'react-modal';  // Import Modal component

const DeviceDashboard = () => {
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  // Function to get the token from localStorage
  const getAuthToken = () => localStorage.getItem('auth_token');
  const getRefreshToken = () => localStorage.getItem('refresh_token');

  // Memoized function to refresh the token
  const refreshAuthToken = useCallback(async () => {
    try {
      const refreshToken = getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', { refresh: refreshToken });
      const { access } = response.data;
      localStorage.setItem('auth_token', access);
      return access;
    } catch (error) {
      console.error('Error refreshing token:', error);
      throw new Error('Unable to refresh token');
    }
  }, []);  // Empty dependency array to ensure this function is stable

  // Memoized function to fetch devices with token expiration handling
  const fetchDevices = useCallback(async () => {
    try {
      const token = getAuthToken();
      if (!token) {
        setErrorMessage('No authorization token found');
        return;
      }

      try {
        const response = await axios.get('http://127.0.0.1:8000/api/get_user_devices', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDevices(response.data.data);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token expired, try refreshing
          const newToken = await refreshAuthToken();
          const response = await axios.get('http://127.0.0.1:8000/api/get_user_devices', {
            headers: { Authorization: `Bearer ${newToken}` },
          });
          setDevices(response.data.data);
        } else {
          setErrorMessage('Error fetching devices');
          console.error('Error fetching devices:', error);
        }
      }
    } catch (error) {
      setErrorMessage('Error fetching devices');
      console.error('Error fetching devices:', error);
    }
  }, [refreshAuthToken]);  // Add refreshAuthToken as a dependency

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
        { temperature: selectedDevice.temperature },
        { headers: { Authorization: `Bearer ${token}` } }
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
