import React, { useEffect, useState, useRef, useCallback  } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';
import { Modal, Button, Card, Row, Col } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, 
  FaUsers, FaWater, FaRecycle, FaBatteryHalf, FaWindows, FaChild } from 'react-icons/fa'; // Importing icons

  // import ReactMapGL, { Marker, NavigationControl } from 'react-map-gl';
import mapboxgl from 'mapbox-gl';

//Chart
import { Line, Pie, Bar } from 'react-chartjs-2';  // Import the Line chart
import { Chart as ChartJS, CategoryScale, LinearScale, ArcElement, PointElement, LineElement, Title, 
  Tooltip, Legend } from "chart.js";

import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';  // CSS file for Mapbox GL JS
// import 'mapbox-gl/dist/mapbox-gl.js';   // JS file for Mapbox GL JS

import '../../App.css'; // Custom CSS for styling

ChartJS.register(CategoryScale, LinearScale, ArcElement, PointElement, LineElement, Title, Tooltip, Legend);

// Access your environment variables
const API_URL = process.env.REACT_APP_SB__API_URL + ":" + process.env.REACT_APP_SB__API_PORT;
const MAPBOX_API_KEY = process.env.REACT_APP_SB__MAP_TOKEN;
//const MAPBOX_API_KEY = "--";

console.log('DEBUG: API_URL = ' + API_URL);
console.log('DEBUG: MAPBOX_API_KEY = ' + MAPBOX_API_KEY);

// Function to get the token from localStorage
const getAuthToken = () => localStorage.getItem('sb_access_token');
const getRefreshToken = () => localStorage.getItem('sb_refresh_token');
const getUserInfo = () => localStorage.getItem('sb_user_info');

const MainDashboard = () => {
  const [deviceData, setDeviceData] = useState([]);
  const [modalShow, setModalShow] = useState(false);
  const [selectedDevice, setSelectedDevice] = useState(null);  
  const [chartDataElecFloor, setChartDataElecFloor] = useState(null);
  const [chartDataElec, setChartDataElec] = useState(null);
  const [chartDataWater, setChartDataWater] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loginDisplay, setLoginDisplay] = useState(false);
  
  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const [temperature, setTemperature] = useState("");
  const navigate = useNavigate();

  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);

  const token = getAuthToken();
  const decodedToken = jwtDecode(token); // jwtDecode is a function use from the 'jwt-decode' library
  console.log("DEBUG: Dashbaord - Token expiry: ", new Date(decodedToken.exp * 1000)); // Convert from seconds to milliseconds

  // SignOut function - used to remove tokens from localStorage
  const signOut = useCallback(() => {
    console.log("DEBUG: signOut() - is working")
    localStorage.removeItem('sb_access_token');  // Remove access token
    localStorage.removeItem('sb_refresh_token');  // Remove refresh token
    localStorage.removeItem('sb_user_info');  // Remove refresh token
    // console.log("DEBUG: 2 tokens are removed")
    navigate('/signin');  // Redirect to Sign In page
  }, [navigate]);

  
  //========================================
  // Fetch device for all roles
  //========================================
  useEffect(() => {
    const userInfo = JSON.parse(getUserInfo());
    if (!userInfo || !userInfo[0]?.account_id) {
      console.error("Invalid or missing user info:", userInfo);
      return;
    }
    
    let roleName = '';
    let urlDevices = "";
    const url_account = `/api/adevices/${userInfo[0].account_id}/`;
  
    if (userInfo[0].is_admin) {
      roleName = 'Administrator';
      urlDevices = `${API_URL}${url_account}`;
    } else if (userInfo[0].is_staff) {
      roleName = 'Staff';
      urlDevices = `${API_URL}/api/fdevices/${userInfo[0].account_id}/${userInfo[0].building_id}/${userInfo[0].floor_id}/`;
    } else {
      roleName = 'Guest';
      urlDevices = `${API_URL}/api/rdevices/${userInfo[0].account_id}/${userInfo[0].building_id}/${userInfo[0].floor_id}/${userInfo[0].room_id}`;
    }
    
    console.log("DEBUG: Constructed URL:", urlDevices); 

    axios.get(urlDevices)
      .then((response) => {
        const data = response.data;
        if (data && Array.isArray(data.data)) {
          setDeviceData(data.data);
        } else {
          console.error("Unexpected response format:", data);
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
    
    setIsAdmin(String(userInfo[0].is_admin));
    setLoginDisplay(userInfo[0].first_name + ' ' + userInfo[0].first_name + ' (' + roleName + ')' );

  }, []);
  
  //========================================
  // Fetch data for overview
  //========================================
  useEffect(() => {
    const userInfo = JSON.parse(getUserInfo());
  
    if (!userInfo || !userInfo[0]?.account_id) {
      console.error("Invalid or missing user info:", userInfo);
      return;
    }
  
    let urlDevices = '';
  
    console.log("DEBUG: useEffect1() - is working");
    const token = getAuthToken();
  
    console.log("DEBUG: useEffect() - token =", token);
  
    if (!token) {
      navigate('/signin'); // Redirect if no token
      console.log("DEBUG: useEffect1() - check token =", token);
      return; // Prevent further execution
    }
  
    // API URL
    const url_account = `/api/adevices/${userInfo[0].account_id}/`;
  
    if (String(userInfo[0].is_admin) === 'true') {
      // Admin logic
      urlDevices = `${API_URL}${url_account}`;
      console.log("DEBUG: Admin login");
  
      axios
        .get(urlDevices)
        .then((response) => {
          const data = response.data; // Access the data
          if (data && Array.isArray(data.data)) {
            setDeviceData(data.data); // Set the device data
  
            // Generate chart data after fetching device data
            genDataElecFloor();
            genDataElec();
            genDataWater();
          } else {
            console.error("Expected data to be an array but got:", data);
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    } else {
      console.log("DEBUG: User or staff login");
    }
  }, [selectedDevice, navigate]); // Add selectedDevice and navigate as dependencies
  


  //========================================
  //Fetch data for overview - map
  //========================================
  useEffect(() => {
    // Initialize the map once the component is mounted
    if (!mapContainerRef.current){
      console.log('Map container ref is not available');
    }else{
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
    } //End of 'else'
  }, []); // Run only once on mount


  // Generate chart data
  const genDataElecFloor = (deviceId) => {
    const data = {
      labels: ["Building 1", "Building 2", "Building 3"], // Labels for the chart
      datasets: [
        {
          label: "Energy Usage (2023)",
          data: [80, 53, 90], // Data for each slice
          backgroundColor: [
            "rgba(255, 159, 64, 0.7)", // Pastel orange
            "rgba(144, 238, 144, 0.7)", // Pastel green
            "rgba(135, 206, 235, 0.7)", // Pastel sky
          ],
          borderColor: [
            "rgba(255, 159, 64, 1)", // Solid pastel orange
            "rgba(144, 238, 144, 1)", // Solid pastel green
            "rgba(135, 206, 235, 1)", // Solid pastel sky
          ],
          borderWidth: 1, // Border width for chart slices
        },
      ],
    };

    const options = {
      plugins: {
        legend: {
          position: "right", // Move legend to the right-hand side
          labels: {
            usePointStyle: true, // Optional: Use circle markers in legend
            padding: 20, // Add space between labels
          },
        },
      },
    };

    setChartDataElecFloor(data, options); // Ensure options are applied
  };
 

  const genDataElec = (deviceId) => {    
    const data = {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [
        {
          label: "2023",
          data: [4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00, 7.50, 8.50, 8.00, 9.00, 12.00],
          fill: true,
          backgroundColor: "rgba(255, 182, 193, 0.5)", // Pastel pink
          borderColor: "rgba(255, 182, 193, 1)", // Border pastel pink
          borderWidth: 1.5, // Slightly thicker border for better visibility
        },
        {
          label: "2024",
          data: [3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00, 7.50, 8.50],
          fill: true,
          backgroundColor: "rgba(173, 216, 230, 0.5)", // Pastel blue
          borderColor: "rgba(173, 216, 230, 1)", // Border pastel blue
          borderWidth: 1.5,
        }
      ]
    };
    setChartDataElec(data);
  };
  
  const genDataWater = (deviceId) => {    
    const data = {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [
        {
          label: "2022",
          data: [100.00, 150.00, 200.00, 250.50, 300.50, 350.00, 360.00, 380.00, 400.35, 450.00, 460.50, 470.00],
          fill: true,
          backgroundColor: "rgba(255, 223, 186, 0.5)", // Pastel orange
          borderColor: "rgba(255, 223, 186, 1)", // Solid pastel orange
          borderWidth: 1.5,
        },
        {
          label: "2023",
          data: [90.00, 140.00, 160.00, 180.00, 200.50, 250.00, 270.00, 280.00, 300.00, 290.00, 295.50, 320.00],
          fill: true,
          backgroundColor: "rgba(173, 216, 230, 0.5)", // Pastel blue
          borderColor: "rgba(173, 216, 230, 1)", // Solid pastel blue
          borderWidth: 1.5,
        },
        {
          label: "2024",
          data: [110.00, 160.00, 220.00, 260.50, 320.50, 360.00, 370.00, 400.00, 430.35, 450.00, 500.00],
          fill: false, // Transparent background
          borderColor: "rgba(144, 238, 144, 1)", // Pastel green
          borderWidth: 2, // Slightly thicker border for distinction
        }
      ]
    };
    setChartDataWater(data);
  };
  

  //========================================
  // Fetch device data
  //========================================
  




  // Handle Modal Open
  const handleModalShow = (device) => {
    setSelectedDevice(device);
    setModalShow(true);
    // genDataElecity(device.iot_device_id);
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
        return <FaCamera size={30} color='gray' />;
      case 'c0ec3c70-b76f-45e0-9297-8b5a4a462a47': //'Smart bulbs and LED lights':
        return <FaLightbulb size={30} color='orange' />;
      case 'f531b9c1-c46a-42c4-989d-1d5be315f6a6': //'Smart meters':
        return <FaBatteryHalf size={30} />;
      case '3e6448c0-eea1-4f8d-bfc1-366685232a83': //'Leak detection sensors':
        return <FaWater size={30} color='blue' />;
      case '2dcc0b13-ff3a-445d-b6c8-a92b05bbba6c': //'Smart bins':
        return <FaRecycle size={30} color='brown' />;
      case '69b29098-c768-423e-ac2e-cc443e18f8a9': //'Automated blinds or shades':
        return <FaWindows size={30} color='rgba(255, 182, 193, 1)' />;// Border pastel pink
      case '96b38698-d9ad-4355-807f-5580397471a1': //'Presence sensors':
        return <FaChild size={30} color='rgba(173, 216, 230, 1)' />; // Solid pastel blue
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

  //=============================================
  //Submit form
  //=============================================
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');
  
    const data = {
        device_id: '7c84b98d-8f69-4959-ac5b-1b2743077151', //'Smart thermostats'
        temperature: '25.00', //'Smart thermostats'
        update_by: '32ab3f31-01bf-4ea3-b27e-135497b10a46'
    };
  
    try {
      const response = await axios.post(`${API_URL}}/api/device_control/`, data, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.status === 201) {

        setLoading(false);

        setMessage(
          <>
            <p>Save successfully</p>
          </>
        );
      }
      else {
        setMessage(response.data.message);
      }

    } catch (error) {
      setLoading(false); // Hide loading indicator
      if (error.response) {
        // Server responded with an error
        console.error("Error response:", error.response);
        setMessage("Error during save data: " + error.response.data.error);
      } else if (error.request) {
        // No response received from server
        console.error("Error request:", error.request);
        setMessage("No response from server");
      } else {
        // Something else went wrong
        console.error("Error:", error.message);
        setMessage("Error during save data: " + error.message);
      }
    }
  };

  return (
    <div className="MainDashboard" style={{ padding: '20px' }}>
        <div>
          <center><h1>Smart Building Dashboard</h1></center>
        
          {`Welcome: ${loginDisplay}`}
          <button className="btn btn-primary btn-sm" onClick={signOut} style={{ position: 'absolute', top: '10px', right: '10px' }}>
            <span class="glyphicon glyphicon-log-out"></span> Sign Out
          </button>
        </div>
      

        {isAdmin === 'true' ? (
        <div id='overview'>
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

          <br/>
          <Row className="justify-content-center">
            <Col md={4} sm={6} xs={8}>
              <Card>
                <Card.Body>
                  <Card.Title>Electricity Usage (kWh/m<sup>2</sup>)</Card.Title>
                  <Card.Text>
                    <div id='chartDataElecFloor' style={{ height: '200px', width: '100%' }}>
                        {chartDataElecFloor ? (
                          <Pie data={chartDataElecFloor} />
                        ) : (
                          <p>Loading chart data...</p>
                        )}
                    </div>
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col> 

            <Col md={4} sm={6} xs={8}>
              <Card>
                <Card.Body>
                  <Card.Title>Electricity Bill (Million THB)</Card.Title>
                  <Card.Text>
                    <div id='chartDataElec' style={{ height: '200px', width: '100%' }}>
                        {chartDataElec ? (
                          <Line data={chartDataElec} />
                        ) : (
                          <p>Loading chart data...</p>
                        )}
                    </div>
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col> 

            <Col md={4} sm={6} xs={8}>
              <Card>
                <Card.Body>
                  <Card.Title>Water Consumption (m<sup>3</sup>)</Card.Title>
                  <Card.Text>
                    <div id='chartDataWater' style={{ height: '200px', width: '100%' }}>
                        {chartDataWater ? (
                          <Line data={chartDataWater} />
                        ) : (
                          <p>Loading chart data...</p>
                        )}
                    </div>
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col> 

          </Row>
        </div>  
        ) : (
          console.log('User is not Administrator')
        )}

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
                    
                    <div>                      
                      <strong>Building ID:</strong> {device.building_id}&nbsp;&nbsp;
                      <strong>Floor ID:</strong> {device.floor_id}&nbsp;&nbsp;
                      <strong>Room ID:</strong> {device.room_id}
                    </div>

                    <div>Device ID: {device.iot_device_id}</div>
                    <br/>
                    <div className="device-status">
                        {/* Dynamic status */}

                        {/*Smart thermostats */}
                        { device.iot_device_id === '7c84b98d-8f69-4959-ac5b-1b2743077151' ? (
                            <>
                              <p><FaThermometerHalf /> Temperature: 25°C</p>
                              <p><FaLightbulb /> Light Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}
                        
                        {/*Demand-Controlled Ventilation (DCV) */}
                        { device.iot_device_id === '080d460f-e54c-4262-a4ac-a3d42c40cbd5' ? (
                            <>
                              <p><FaLightbulb /> CO<sub>2</sub>: 400.00 Lux</p>
                              <p><FaThermometerHalf /> humidity: 50.00 g/m<sup>3</sup></p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                            </>
                          ) : (
                            <></>
                        )}

                        {/*Smart bulbs and LED lights */}
                        { device.iot_device_id === 'c0ec3c70-b76f-45e0-9297-8b5a4a462a47' ? (
                            <>
                              <p><FaLightbulb /> Light Level: 401.00 Lux</p>
                              <p><FaThermometerHalf /> Temperature: 25°C</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                            </>
                          ) : (
                            <></>
                        )}

                        {/*Smart meters */}
                        { device.iot_device_id === 'f531b9c1-c46a-42c4-989d-1d5be315f6a6' ? (
                            <>
                              <p>Voltage: 100.00 Volt</p>
                              <p>current: 50.00 Ampere</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                            </>
                          ) : (
                            <></>
                        )}

                        {/* Presence sensors */}
                        { device.iot_device_id === '96b38698-d9ad-4355-807f-5580397471a1' ? (
                            <>
                              <p><FaChild /> Human status: Yes</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}

                        {/* Automated blinds or shades */}
                        { device.iot_device_id === '69b29098-c768-423e-ac2e-cc443e18f8a9' ? (
                            <>
                              <p><FaLightbulb /> Light Level: 401.00 Lux</p>
                              <p><FaThermometerHalf /> Temperature: 25°C</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                            </>
                          ) : (
                            <></>
                        )}

                        {/* Air Conditioning */}
                        { device.iot_device_id === '3382ead3-4c22-4fac-bc92-d2cc11e94564' ? (
                            <>
                              <p><FaThermometerHalf /> Temperature: 25°C</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}

                        {/* Smart cameras */}
                        { device.iot_device_id === '2a66e85b-2e08-4a82-9617-f6ba6ab55cca' ? (
                            <>
                              <p>Human Status: Yes</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}

                        {/* Leak detection sensors */}
                        { device.iot_device_id === '3e6448c0-eea1-4f8d-bfc1-366685232a83' ? (
                            <>
                              <p><FaWater />Water Leak Status: No</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}

                        {/* Smart bins */}
                        { device.iot_device_id === '2dcc0b13-ff3a-445d-b6c8-a92b05bbba6c' ? (
                            <>
                              <p><FaThermometerHalf /> Bins Level: 30%</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}


                        {/* RFID tags and sensors */}
                        { device.iot_device_id === '21a0a6de-88a5-4a42-8734-1fa27483e138' ? (
                            <>
                              <p>Object Position: Move</p>
                              <p><FaBatteryHalf /> Battery Level: 70%</p> 
                              <p>. </p>
                            </>
                          ) : (
                            <></>
                        )}

                        

                    </div>

                    <div>
                      {/* Show Line Chart below each device */}
                      {/* <Line data={chartData} /> */}
                    </div>

                    <div style={{ textAlign: 'right' }}><Button onClick={() => handleModalShow(device)} variant="primary">Control >></Button></div>
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
          <Modal.Title>Device Configuration</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="container mt-5">
            <h3>{selectedDevice?.device_sub_type_name}</h3>
            <form onSubmit={handleSubmit}>        
              <div className="form-group">
                <label>Device ID: </label>
                <input type='text' className="form-control" value={selectedDevice?.iot_device_id} required />

                <label>Temperature:</label>
                <input type="text" className="form-control" value="25" onChange={(e) => setTemperature(e.target.value)} required />
              </div>              
              <center><button type="submit" className="btn btn-primary mt-3">Save</button></center>
            </form>
            {message && <p>{message}</p>}
          </div>
        </Modal.Body>
        <Modal.Footer>
          {/* <Button variant="secondary" onClick={handleModalClose}>Cancel</Button> */}
          {/* <Button variant="primary" onClick={handleSave}>Save</Button> */}
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MainDashboard;
