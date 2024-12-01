import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Modal from 'react-modal';

const DeviceDashboard = () => {
  const [devices, setDevices] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  //const [newLightLevel, setNewLightLevel] = useState('');
  const [newTemperature, setNewTemperature] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // Fetch devices after login
  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/get_user_devices`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
          
        });
        setDevices(response.data.devices);
      } catch (error) {
        setErrorMessage('Error fetching devices');
        console.error('Error fetching devices:', error);
      }
    };
    fetchDevices();
  }, []);

  // Handle device control (e.g., changing temperature)
  const handleDeviceControl = (device) => {
    setSelectedDevice(device);
    if (selectedDevice.id === "c0ec3c70-b76f-45e0-9297-8b5a4a462a47") //Smart bulbs and LED lights
        //setNewLightLevel(device.light_level);
        setNewTemperature(device.temperature);
  };

  const handleTemperatureChange = async () => {
    try {
      const response = await axios.post(`http://127.0.0.1:8000/api/control_device/${selectedDevice.id}/`, {
        //light_level: newLightLevel,
        temperature: newTemperature,
      }, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
      });
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
        {devices.map(device => (
          <div className="col-md-4" key={device.id}>
            <div className="card mb-4">
              <div className="card-body">
                <h5 className="card-title">{device.name}</h5>
                <p>Current Temperature: {device.temperature}°C</p>
                <p>Status: {device.status}</p>
                <button className="btn btn-primary" onClick={() => handleDeviceControl(device)}>Configure</button>
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
            value={newTemperature}
            onChange={(e) => setNewTemperature(e.target.value)}
            required
          />
          <button onClick={handleTemperatureChange} className="btn btn-success mt-3">Save Changes</button>
          <button onClick={() => setSelectedDevice(null)} className="btn btn-secondary mt-3">Close</button>
        </Modal>
      )}
    </div>
  );
};

export default DeviceDashboard;
