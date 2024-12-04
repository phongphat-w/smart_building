import React, { useEffect, useState, useRef  } from 'react';
import axios from 'axios';
import { Modal, Button, Card, Row, Col } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaMapMarkerAlt, 
  FaUsers, FaWater, FaRecycle, FaBatteryHalf, FaWindows, FaChild  } from 'react-icons/fa'; // Importing icons
// import ReactMapGL, { Marker, NavigationControl } from 'react-map-gl';
import mapboxgl from 'mapbox-gl';
import { Line } from 'react-chartjs-2';  // Import the Line chart
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';  // CSS file for Mapbox GL JS
// import 'mapbox-gl/dist/mapbox-gl.js';   // JS file for Mapbox GL JS
import '../../App.css'; // Custom CSS for styling

// Define the default map view center and zoom level
const MAPBOX_API_KEY = 'pk.eyJ1IjoicGhvbmdwaGF0dyIsImEiOiJjbTQ5cXZiNmowZjJuMnFvaDFkc2N0ZjI5In0.oJiVG2scVaRn7R3STL_1LA';
// const MAPBOX_API_KEY = 'pk.eyJ1IjoicGhvbmdwaGF0dyIsImEiOiJjbTQ5c2R2cTUwMDU2Mm1zZzB0MjltaW9tIn0.V80f6FPJi4fya6uJo0dw-A';

const MainDashboard = () => {
  const [deviceData, setDeviceData] = useState([]);
  const [modalShow, setModalShow] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState(null);  
  const [chartData, setChartData] = useState({});

  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);

  const url_acccout = 'http://127.0.0.1:8000/api/adevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/';
  const url_building = 'http://127.0.0.1:8000/api/bdevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/001/';
  const url_floor = 'http://127.0.0.1:8000/api/fdevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/001/0001/';
  const url_room = 'http://127.0.0.1:8000/api/rdevices/defb76a0-7ff4-4bdf-8100-a2edd5183ef6/001/0001/00001';
    
  // Fetch device data from API
  useEffect(() => {    
    axios.get(url_room) // Account 1
      .then((response) => {
        const data = response.data; // Access the data
        if (data && Array.isArray(data.data)) {
          setDeviceData(data.data); // Set the device data

          // Set the map center based on the country name from the first device's country_name
          // const country = data.data[0]?.country_name;
          // getCountryCoordinates(country); // Fetch the country coordinates
        } else {
          console.error('Expected data to be an array but got:', data);
        }
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []); // Empty dependency array for fetching data once on mount

  // Fetch device data from API
  useEffect(() => {
    // Initialize the map once the component is mounted
    mapboxgl.accessToken = MAPBOX_API_KEY;

    // Create a new Map instance
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,  // container reference
      center: [100.5018, 13.7563],  // initial position [lng, lat]
      zoom: 9,  // initial zoom level
      style: 'mapbox://styles/mapbox/streets-v12' // Map style
    });

    // Add NavigationControl (zoom and rotation)
    const nav = new mapboxgl.NavigationControl({
      visualizePitch: true
    });
    mapRef.current.addControl(nav, 'top-right');  // Position it at the top-right corner

    // Add Fullscreen control
    mapRef.current.addControl(new mapboxgl.FullscreenControl(), 'bottom-right');

    // Add a draggable marker
    const marker = new mapboxgl.Marker({ color: "red", draggable: true })
      .setLngLat([100.5018, 13.7563]) // Set the marker's coordinates (long, lat)
      .addTo(mapRef.current);

    // Cleanup: Remove the map instance on unmount
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();  // Properly remove map instance
      }
    };
  }, []); // Run only once on mount

  // Generate chart data (Example: temperature vs time)
  const generateChartData = (deviceId) => {
    // Dummy data generation for chart, replace this with actual data if needed
    const data = {
      labels: ['12:00', '14:00', '16:00', '18:00', '20:00'],
      datasets: [
        {
          label: 'Temperature',
          data: [22, 24, 23, 26, 28], // Replace this with actual data
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
    switch (device.iot_device_id) {
      case '7c84b98d-8f69-4959-ac5b-1b2743077151': //'Smart thermostats':
        return <FaThermometerHalf size={30} color='red' />;
      case '080d460f-e54c-4262-a4ac-a3d42c40cbd5': //'Demand-Controlled Ventilation (DCV)':
        return <FaCloudSun size={30} color='green' />;
      case '3382ead3-4c22-4fac-bc92-d2cc11e94564': //'Air Conditioning':
        return <FaFan size={30} color='green'/>;
      case '2a66e85b-2e08-4a82-9617-f6ba6ab55cca': //'Smart cameras':
        return <FaCamera size={30} />;
      case 'c0ec3c70-b76f-45e0-9297-8b5a4a462a47': //'Smart bulbs and LED lights':
        return <FaLightbulb size={30} color='orange' />;
      case 'f531b9c1-c46a-42c4-989d-1d5be315f6a6': //'Smart meters':
        return <FaBatteryHalf size={30} />;
      case '3e6448c0-eea1-4f8d-bfc1-366685232a83': //'Leak detection sensors':
        return <FaWater size={30} color='blue' />;
      case '2dcc0b13-ff3a-445d-b6c8-a92b05bbba6c': //'Smart bins':
        return <FaRecycle size={30} color='gray' />;
      case '69b29098-c768-423e-ac2e-cc443e18f8a9': //'Automated blinds or shades':
        return <FaWindows size={30} />;
      case '96b38698-d9ad-4355-807f-5580397471a1': //'Presence sensors':
        return <FaChild size={30} color='gray' />;
      default:
        return <FaSearch size={30} />;
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
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col>
          {/* Map container element */}
          <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <div style={{ flex: 1 }}>
              <div
                ref={mapContainerRef}
                style={{ height: '100%', width: '100%' }} // Takes the full height of the parent container
              />
            </div>
          </div>
         
        </Col>
      </Row>

      <br />
      
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
                      <div>{getDeviceIcon(device)}&nbsp;<h4>{device.device_type_name}</h4></div>
                    </div>
                    <div><h5>{device.device_sub_type_name}</h5></div>
                    <div>Device ID: {device.iot_device_id}</div>
                    <div>                      
                      <strong>Building ID:</strong> {device.building_id}&nbsp;&nbsp;
                      <strong>Floor ID:</strong> {device.floor_id}&nbsp;&nbsp;
                      <strong>Room ID:</strong> {device.room_id}
                    </div>
                    <br/>
                    <div className="device-status">
                      {/* Example of dynamic status */}
                      <p><FaThermometerHalf /> Temperature: 25°C</p>
                      <p><FaLightbulb /> Light Level: 80%</p>
                    </div>
                    <div>
                      {/* Show Line Chart below each device */}
                      {/* <Line data={chartData} /> */}
                    </div>
                    <div style={{ textAlign: 'right' }}><Button onClick={() => handleModalShow(device)} variant="primary">Control Device</Button></div>
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
          xxxxxxxxx
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
