import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Modal, Button, Card, Row, Col, Container } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaMapMarkerAlt, FaGlobe, FaUsers } from 'react-icons/fa'; // Importing icons
import ReactMapGL, { Marker } from 'react-map-gl';
import { Line } from 'react-chartjs-2';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import '../../App.css'; // Custom CSS for styling

// Define the default map view center and zoom level
const MAP_CENTER = { lat: 13.7367, lng: 100.5231 }; // Thailand's coordinates

const MainDashboard = () => {
  const [deviceData, setDeviceData] = useState([]);
  const [modalShow, setModalShow] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [viewport, setViewport] = useState({
    latitude: MAP_CENTER.lat,
    longitude: MAP_CENTER.lng,
    zoom: 10,
  });
  const [chartData, setChartData] = useState({});


  // useEffect(() => {
  //   // Fetch data from API
  //   axios.get('http://127.0.0.1:8000/api/adevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/') //Account 1
  //     .then((response) => {
  //       setDeviceData(response.data.data);
  //     })
  //     .catch((error) => console.error("Error fetching data", error));
  // }, []);

  useEffect(() => {
    // Fetch data from the API
    axios.get('http://127.0.0.1:8000/api/adevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/') // Account 1
      .then((response) => {
        const data = response.data; // Access the data

        // Check if data is in the expected format
        if (data && Array.isArray(data.data)) {
          setDeviceData(data.data); // Set the device data
        } else {
          console.error('Expected data to be an array but got:', data);
        }
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

   // Generate chart data (Example: temperature vs time)
  const generateChartData = (deviceId) => {
    // Dummy data generation for chart
    const data = {
      labels: ['12:00', '14:00', '16:00', '18:00', '20:00'],
      datasets: [
        {
          label: 'Temperature',
          data: [22, 24, 23, 26, 28], // You would replace this with actual data
          fill: false,
          borderColor: 'rgba(75,192,192,1)',
          tension: 0.1,
        },
      ],
    };
    setChartData(data);
  };

  // Handle Modal Open
  const handleModalShow = (device) => {
    setSelectedDevice(device);
    setModalShow(true);
    generateChartData(device.iot_device_id);
  };

  // Handle Modal Close
  const handleModalClose = () => {
    setModalShow(false);
  };

  const handleSave = () => {
    // Implement save logic for updating the device settings
    const updatedDevice = {
      ...selectedDevice,
      auto_flag: 0,  // Change the auto_flag to indicate control
    };
    axios.post('/update-device', updatedDevice)  // Update endpoint
      .then(() => {
        alert("Device settings saved!");
        setModalShow(false);
      })
      .catch((error) => {
        console.error('Error updating device', error);
      });
  };

  // Get the MainDashboardropriate icon based on the device sub-type
  const getDeviceIcon = (device) => {
    switch (device.device_sub_type_name) {
      case 'Smart thermostats':
        return <FaThermometerHalf size={40} color='red' />;
      case 'Demand-Controlled Ventilation (DCV)':
        return <FaCloudSun size={40} />;
      case 'Air Conditioning':
        return <FaFan size={40} />;
      case 'Smart cameras':
        return <FaCamera size={40} />;
      case 'Smart bulbs and LED lights':
        return <FaLightbulb size={40} color='orange' />;
      case 'Smart meters':
        return <FaSearch size={40} />;
      case 'Leak detection sensors':
        return <FaSearch size={40} color='blue' />;
      default:
        return <FaSearch size={40} />;
    }
  };

  // Styling for card components
  const cardStyle = {
    backgroundColor: '#f7f7f7',
    borderRadius: '10px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    padding: '20px',
  };

  const iconStyle = {
    fontSize: '30px',
    color: '#007bff',
  };
  

  return (
    <div className="MainDashboard">
      <header>
        <h1>Smart Building Dashboard</h1>
        <p>Client: {deviceData.client_name} | Account: {deviceData.account_name}</p>
        <p>{deviceData.country_name} | {deviceData.continent_name} | {deviceData.time_zone}</p>
      </header>

      {/* Map Component */}
      <ReactMapGL
        {...viewport}
        width="100%"
        height="400px"
        mapboxApiAccessToken="pk.eyJ1IjoicGhvbmdwaGF0dyIsImEiOiJjbTQ5c2R2cTUwMDU2Mm1zZzB0MjltaW9tIn0.V80f6FPJi4fya6uJo0dw-A"
        onViewportChange={setViewport}
      >
        <Marker latitude={viewport.latitude} longitude={viewport.longitude}>
          <div className="marker-icon">🏢</div>
        </Marker>
      </ReactMapGL>

      {/* Devices Display */}
      <div className="devices-grid">
        <Row>
          {deviceData.map((device) => (
            <Col key={device.iot_device_id} md={4}>
              <Card>
                <Card.Body>
                  <div className="device-card">
                    {/* Device Icon */}
                    <div className="device-icon">
                      {getDeviceIcon(device)}
                    </div>
                    <p><h4>{device.device_type_name}</h4></p>
                    <p><h5>{device.device_sub_type_name}</h5></p>
                    <p>ID: {device.iot_device_id}</p>
                    <div className="device-status">
                      {/* Example of dynamic status */}
                      <p><FaThermometerHalf /> Temperature: 25°C</p>
                      <p><FaLightbulb /> Light Level: 80%</p>
                    </div>
                    <Button onClick={() => handleModalShow(device)} variant="primary">Control Device</Button>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* Modal to control device */}
      <Modal show={modalShow} onHide={handleModalClose}>
        <Modal.Header closeButton>
          <Modal.Title>Device Control: {selectedDevice?.device_sub_type_name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            <Line data={chartData} />
          </div>
          {/* Additional form fields for controlling the device */}
          <div className="control-panel">
            <label>Temperature:</label>
            <input type="number" value={selectedDevice?.sensors?.temperature || ''} />
            <label>Battery Level:</label>
            <input type="number" value={selectedDevice?.sensors?.battery_level || ''} />
            <label>Light Level:</label>
            <input type="number" value={selectedDevice?.sensors?.light_level || ''} />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleModalClose}>Cancel</Button>
          <Button variant="primary" onClick={handleSave}>Save</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MainDashboard;
