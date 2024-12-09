import React, { useState } from 'react';
import { Form, Button, Card, Row, Col } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaUsers, FaWater, FaRecycle, FaBatteryHalf, FaWindows, FaChild, FaTrash, FaTools } from 'react-icons/fa'; // Importing icons

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../page-utils/message-alert.js';
import ConfDeviceInfo from '../../com-utils/conf-device-Info.js';
import getDeviceIcon from './dash-icons.js';

export const RenderDeviceThumbnails = ({ deviceData, handleModalShow }) => {
    try {
        const [searchTerm, setSearchTerm] = useState(''); // State to store search term
        const [filteredData, setFilteredData] = useState(deviceData); // State to store filtered device data

        // Handle search
        const handleSearch = (e) => {
            const term = e.target.value.toLowerCase();
            setSearchTerm(term);

            const filtered = deviceData.filter((device) =>
                device.iot_device_id.toLowerCase().includes(term) ||
                device.device_type_name.toLowerCase().includes(term) ||
                device.device_sub_type_name.toLowerCase().includes(term) ||
                device.building_id.toLowerCase().includes(term) ||
                device.floor_id.toLowerCase().includes(term) ||
                device.room_id.toLowerCase().includes(term)
            );

            setFilteredData(filtered);
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
                        {filteredData.map((device, index) => (
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
                                            <div><h5>{index + 1}. {device.device_sub_type_name}</h5></div>
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
                        ))}
                    </Row>
                </div>
            </>
        );
    } catch (error) {
        Logger.error(`${RenderDeviceThumbnails.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display device information in thumbnails format');
    }
};
