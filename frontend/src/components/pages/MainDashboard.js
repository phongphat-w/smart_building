import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Modal, Button, Card, Row, Col } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaMapMarkerAlt, FaUsers } from 'react-icons/fa'; // Importing icons
import ReactMapGL, { Marker } from 'react-map-gl';
import { Line } from 'react-chartjs-2';  // Import the Line chart
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import '../../App.css'; // Custom CSS for styling

// Define the default map view center and zoom level
const MAP_CENTER = { lat: 13.7367, lng: 100.5231 }; // Thailand's coordinates
const MAPBOX_API_KEY = 'pk.eyJ1IjoicGhvbmdwaGF0dyIsImEiOiJjbTQ5cXZiNmowZjJuMnFvaDFkc2N0ZjI5In0.oJiVG2scVaRn7R3STL_1LA';

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

  // Fetch device data from API
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/adevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/') // Account 1
      .then((response) => {
        const data = response.data; // Access the data
        if (data && Array.isArray(data.data)) {
          setDeviceData(data.data); // Set the device data

          // Set the map center based on the country name from the first device's country_name
          const country = data.data[0]?.country_name;
          getCountryCoordinates(country); // Fetch the country coordinates
        } else {
          console.error('Expected data to be an array but got:', data);
        }
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []); // Empty dependency array for fetching data once on mount

  // Function to get country coordinates using Mapbox Geocoding API
  const getCountryCoordinates = (country) => {
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${country}.json?access_token=${MAPBOX_API_KEY}`;

    axios.get(url)
      .then((response) => {
        const features = response.data.features;
        if (features && features.length > 0) {
          const { center } = features[0]; // Get the center of the country (longitude, latitude)
          const [longitude, latitude] = center;
          
          setViewport((prev) => ({
            ...prev,
            latitude,
            longitude,
            zoom: 5, // You can adjust the zoom level as needed
          }));
        } else {
          console.error('Country not found or invalid:', country);
        }
      })
      .catch((error) => {
        console.error('Error fetching coordinates for the country:', error);
      });
  };

  // Generate chart data (Example: temperature vs time)
  const generateChartData = (deviceId) => {
    // Dummy data generation for chart, replace this with actual data if needed
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

  // Get the appropriate icon based on the device sub-type
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

  return (
    <div className="MainDashboard">
      <header>
        <br />
        <center><h1>Smart Building Dashboard</h1></center>
      </header>

      {/* Show client info */}
      <Row className="justify-content-center">
        <Col md={6} sm={12} xs={14}>
          <Card style={cardStyle}>
            <Card.Body>
              <Card.Title>Client Info</Card.Title>
              <Card.Text>
                <FaUsers style={{ fontSize: '30px', color: '#007bff' }} /> <strong>{deviceData[0]?.client_name}</strong><br />
                <strong>Account ID:</strong> {deviceData[0]?.account_id}<br />
                <strong>Account Name:</strong> {deviceData[0]?.account_name}<br />
                <strong>Country:</strong> {deviceData[0]?.country_name}<br />
                <strong>Continent:</strong> {deviceData[0]?.continent_name}<br />
                <strong>Time Zone:</strong> {deviceData[0]?.time_zone}<br />
                <FaMapMarkerAlt style={{ fontSize: '30px', color: '#007bff' }} /> <strong>Building:</strong> {deviceData[0]?.building_id}<br />
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <br />
      {/* Map Component */}
      <ReactMapGL
        {...viewport}
        width="100%"
        height="400px"
        //mapboxApiAccessToken={MAPBOX_API_KEY}
        mapboxAccessToken={MAPBOX_API_KEY}
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
                    <div><h4>{device.device_type_name}</h4></div>
                    <div><h5>{device.device_sub_type_name}</h5></div>
                    <p>ID: {device.iot_device_id}</p>
                    <div className="device-status">
                      {/* Example of dynamic status */}
                      <p><FaThermometerHalf /> Temperature: 25°C</p>
                      <p><FaLightbulb /> Light Level: 80%</p>
                    </div>
                    <div>
                      {/* Show Line Chart below each device */}
                      {/* <Line data={chartData} /> */}
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
