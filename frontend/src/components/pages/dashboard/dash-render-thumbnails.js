import React, { useState } from 'react';
import { Form, Button, Card, Row, Col, Badge } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaUsers, FaWater, FaRecycle, FaBatteryHalf, FaWindows, FaChild, FaTrash, FaTools } from 'react-icons/fa'; // Importing icons

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';
import ConfDeviceInfo from '../../com-utils/conf-device-Info.js';
import getDeviceIcon from './dash-icons.js';

const RECORD_PER_PAGE = process.env.REACT_APP_SB_RECORD_PER_PAGE;

export const RenderDeviceThumbnails = ({ deviceData, handleModalShow }) => {
    try {
        // State variables for pagination
        const recordsPerPage = RECORD_PER_PAGE || 10;
        const [currentPage, setCurrentPage] = useState(1);

        // State variables for search
        const [searchTerm, setSearchTerm] = useState('');

        // Filtered Data
        const filteredData = deviceData.filter((device) =>
            device.iot_device_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.device_type_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.device_sub_type_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.building_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.floor_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.room_id.toLowerCase().includes(searchTerm.toLowerCase())
        );

        // Calculate total pages based on filtered data
        const totalPages = Math.ceil(filteredData.length / recordsPerPage);

        // Calculate records to display up to the current page
        const indexOfLastRecord = currentPage * recordsPerPage;
        const currentRecords = filteredData.slice(0, indexOfLastRecord); // Include all records up to the current page

        // Pagination Handlers
        const handleViewMore = () => {
            if (currentPage < totalPages) {
                setCurrentPage((prevPage) => prevPage + 1);
            }
        };

        // Handle search input
        const handleSearch = (e) => {
            setSearchTerm(e.target.value);
            setCurrentPage(1); // Reset to the first page after search
        };

        return (
            <>
                {/* Search box */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                    <label style={{ whiteSpace: 'nowrap', margin: '0' }}>Search:</label>
                    <Form.Control
                        type="text"
                        placeholder="Device ID, Device Type, Device Sub-type, Building, Floor, or Room"
                        value={searchTerm}
                        onChange={handleSearch}
                        style={{ width: '500px' }}
                    />
                </div>
                
                <div className="devices-grid">
                    <Row>
                    {currentRecords.map((device) => {
                            const originalIndex = deviceData.findIndex((item) => item.iot_device_id === device.iot_device_id);
                            return (
                                <Col key={device.iot_device_id} md={4}>
                                    <Card>
                                        <Card.Body>
                                            <div className="device-card">
                                                <div className="device-icon">
                                                    <div>
                                                        {getDeviceIcon(device)}&nbsp;
                                                        <h4>{device.device_type_name}</h4>
                                                    </div>
                                                </div>
                                                <div><h5>{originalIndex + 1}. {device.device_sub_type_name}</h5></div>
                                                <div>
                                                    <strong>Building ID:</strong> {device.building_id}&nbsp;&nbsp;
                                                    <strong>Floor ID:</strong> {device.floor_id}&nbsp;&nbsp;
                                                    <strong>Room ID:</strong> {device.room_id}
                                                </div>
                                                <div>Device ID: {device.iot_device_id}</div>
                                                <br />
                                                <div className="device-status">
                                                    {/* Dynamic status */}

                                                    {/*Smart thermostats */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdThermostats && (
                                                        <>
                                                        <p><FaThermometerHalf /> Temperature: 25°C</p>
                                                        <p><FaLightbulb /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}
                                                    
                                                    {/*Demand-Controlled Ventilation (DCV) */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdDemConVen && (
                                                        <>
                                                        <p><FaLightbulb /> CO<sub>2</sub>: 400.00 Lux</p>
                                                        <p><FaThermometerHalf /> humidity: 50.00 g/m<sup>3</sup></p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        </>
                                                    )}

                                                    {/*Smart bulbs and LED lights */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdBulbs && (
                                                        <>
                                                        <p><FaLightbulb /> Light Level: 401.00 Lux</p>
                                                        <p><FaThermometerHalf /> Temperature: 25°C</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        </>
                                                    )}

                                                    {/*Smart meters */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdElecMeter && (
                                                        <>
                                                        <p>Voltage: 100.00 Volt</p>
                                                        <p>current: 50.00 Ampere</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        </>
                                                    )}

                                                    {/* Presence sensors */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdPresence && (
                                                        <>
                                                        <p><FaChild /> Human status: Yes</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}

                                                    {/* Automated blinds or shades */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdBlinds && (
                                                        <>
                                                        <p><FaLightbulb /> Light Level: 401.00 Lux</p>
                                                        <p><FaThermometerHalf /> Temperature: 25°C</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        </>
                                                    )}

                                                    {/* Air Conditioning */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdAirCon && (
                                                        <>
                                                        <p><FaThermometerHalf /> Temperature: 25°C</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}

                                                    {/* Smart cameras */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdCameras && (
                                                        <>
                                                        <p>Human Status: Yes</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}

                                                    {/* Leak detection sensors */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdWaterLeak && (
                                                        <>
                                                        <p><FaWater />Water Leak Status: No</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}

                                                    {/* Smart bins */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdBins && (
                                                        <>
                                                        <p><FaTrash /> Bins Level: 30%</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}

                                                    {/* RFID tags and sensors */}
                                                    { device.iot_device_id === ConfDeviceInfo.devIdRfidTags && (
                                                        <>
                                                        <p>Object Position: Move</p>
                                                        <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                                        <p>. </p>
                                                        </>
                                                    )}

                                                </div>
                                                <div style={{ textAlign: 'right' }}>
                                                    <Button onClick={() => handleModalShow(device)} variant="success"><FaTools></FaTools></Button>
                                                </div>
                                            </div>
                                        </Card.Body>
                                    </Card>
                                </Col>
                            );
                    })} 
                    </Row>
                </div>

                {/* View more pages */}
                {(indexOfLastRecord < deviceData.length) && (totalPages > 1) && (
                    <div style={{ textAlign: 'center', marginTop: '10px' }}>
                        <Badge
                            bg="secondary"
                            pill
                            style={{
                                cursor: 'pointer', // Hand pointer when hovering
                                padding: '12px 24px',
                                fontSize: '0.9rem',
                                transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                            }}
                            onMouseEnter={(e) => {
                                e.target.style.transform = 'scale(1.1)';
                                e.target.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)';
                            }}
                            onMouseLeave={(e) => {
                                e.target.style.transform = 'scale(1)';
                                e.target.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
                            }}
                            onClick={handleViewMore}
                        >
                            More...
                        </Badge>
                    </div>
                )}

            </>
        );
    } catch (error) {
        Logger.error(`${RenderDeviceThumbnails.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display device information in thumbnails format');
    }
};
