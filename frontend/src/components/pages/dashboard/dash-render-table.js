import React, { useState } from 'react';
import { Form, Table, Button, Badge } from 'react-bootstrap';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaUsers, FaWater, FaRecycle, FaBatteryHalf, FaWindows, FaChild, FaTrash, FaTools } from 'react-icons/fa'; // Importing icons

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';
import ConfDeviceInfo from '../../com-utils/conf-device-Info.js';
import getDeviceIcon from './dash-icons.js';

const RECORD_PER_PAGE = process.env.REACT_APP_SB_RECORD_PER_PAGE;

export const RenderDeviceTable = ({ deviceData, handleModalShow }) => {
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

        // Calculate records to display based on current page
        const indexOfLastRecord = currentPage * recordsPerPage;
        const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;
        const currentRecords = filteredData.slice(indexOfFirstRecord, indexOfLastRecord);

        // Pagination Handlers
        const goToFirstPage = () => setCurrentPage(1);
        const goToPreviousPage = () => setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
        const goToNextPage = () => setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));
        const goToLastPage = () => setCurrentPage(totalPages);

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

                {/* Pagination */}
                <div style={{ display: 'flex', justifyContent: 'right', alignItems: 'center', gap: '15px', marginTop: '20px' }}>
                    <Button
                        style={{
                            backgroundColor: '#A8D5BA', // Pastel green
                            border: 'none',
                            color: '#2C6E49', // Darker green for text
                            padding: '8px 16px', // Adjust padding for smaller buttons
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Soft shadow
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === 1}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToFirstPage}
                    >
                        First
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#D4EED1', // Lighter pastel green
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === 1}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToPreviousPage}
                    >
                        Previous
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#A8D5BA',
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={true}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToLastPage}
                    >
                        {currentPage} of {totalPages}
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#D4EED1',
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === totalPages}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToNextPage}
                    >
                        Next
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#A8D5BA',
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === totalPages}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToLastPage}
                    >
                        Last
                    </Button>
                </div>
                
                {/* Device Table */}
                <br/>
                <Table striped bordered hover>
                    <thead>
                        <tr style={{ textAlign: 'center' }}>
                            <th>No.</th>
                            <th></th>
                            <th>Device ID</th>
                            <th>Device Type</th>
                            <th>Device Sub-type</th>
                            <th style={{ width: '20%' }}>Sensors</th>
                            <th>Building ID</th>
                            <th>Floor ID</th>
                            <th>Room ID</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {currentRecords.map((device) => {
                            const originalIndex = deviceData.findIndex((item) => item.iot_device_id === device.iot_device_id);
                            return (
                                <tr key={device.iot_device_id}>
                                    <td style={{ textAlign: 'center' }}>{originalIndex + 1}</td>
                                    <td>{getDeviceIcon(device)}</td>

                                    <td>{device.iot_device_id}</td>
                                    <td>{device.device_type_name}</td>
                                    <td>{device.device_sub_type_name}</td>
                                    
                                    <td className="device-status">
                                        {/* Dynamic status */}

                                        {/*Smart thermostats */}
                                        { device.iot_device_id === ConfDeviceInfo.devIdThermostats && (
                                            <>
                                            <p><FaThermometerHalf /> Temperature: 25°C</p>
                                            <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                            
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
                                            
                                            </>
                                        )}

                                        {/* Smart cameras */}
                                        { device.iot_device_id === ConfDeviceInfo.devIdCameras && (
                                            <>
                                            <p>Human Status: Yes</p>
                                            <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                            
                                            </>
                                        )}

                                        {/* Leak detection sensors */}
                                        { device.iot_device_id === ConfDeviceInfo.devIdWaterLeak && (
                                            <>
                                            <p><FaWater />Water Leak Status: No</p>
                                            <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                            
                                            </>
                                        )}

                                        {/* Smart bins */}
                                        { device.iot_device_id === ConfDeviceInfo.devIdBins && (
                                            <>
                                            <p><FaTrash /> Bins Level: 30%</p>
                                            <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                            
                                            </>
                                        )}

                                        {/* RFID tags and sensors */}
                                        { device.iot_device_id === ConfDeviceInfo.devIdRfidTags && (
                                            <>
                                            <p>Object Position: Move</p>
                                            <p><FaBatteryHalf /> Battery Level: 70%</p> 
                                            
                                            </>
                                        )}

                                    </td>   


                                <td>{device.building_id}</td>
                                <td>{device.floor_id}</td>
                                <td>{device.room_id}</td>
                                {/* <td style={{ textAlign: 'center' }}>
                                    <Button onClick={() => handleModalShow(device)} variant="success"><FaTools></FaTools></Button>
                                </td> */}
                                <td style={{ textAlign: 'center' }}>
                                    <Button
                                        onClick={() => handleModalShow(device)}
                                        style={{
                                            backgroundColor: '#A2CFFF', // Pastel blue
                                            border: 'none',            // Remove border
                                            color: '#FFFFFF',          // White text
                                            padding: '8px 16px',       // Adjust padding
                                            fontWeight: 'bold',        // Bold text
                                            fontSize: '0.85rem', // Smaller font size
                                            borderRadius: '5px',       // Rounded corners
                                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Soft shadow
                                            transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out', // Interaction effects
                                        }}
                                        onMouseEnter={(e) => {
                                            e.target.style.transform = 'scale(1.1)'; // Enlarge on hover
                                            e.target.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)'; // Stronger shadow on hover
                                        }}
                                        onMouseLeave={(e) => {
                                            e.target.style.transform = 'scale(1)'; // Reset size on mouse leave
                                            e.target.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)'; // Reset shadow
                                        }}
                                    >
                                        <FaTools color='blue' />
                                    </Button>
                                </td>
                            </tr>
                            );
                        })}
                    </tbody>
                </Table>

                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '15px', marginTop: '20px' }}>
                    <Button
                        style={{
                            backgroundColor: '#A8D5BA', // Pastel green
                            border: 'none',
                            color: '#2C6E49', // Darker green for text
                            padding: '8px 16px', // Adjust padding for smaller buttons
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Soft shadow
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === 1}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToFirstPage}
                    >
                        First
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#D4EED1', // Lighter pastel green
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === 1}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToPreviousPage}
                    >
                        Previous
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#A8D5BA',
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={true}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToLastPage}
                    >
                        {currentPage} of {totalPages}
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#D4EED1',
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === totalPages}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToNextPage}
                    >
                        Next
                    </Button>

                    <Button
                        style={{
                            backgroundColor: '#A8D5BA',
                            border: 'none',
                            color: '#2C6E49',
                            padding: '8px 16px',
                            borderRadius: '25px',
                            fontWeight: 'bold',
                            fontSize: '0.85rem', // Smaller font size
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transition: 'all 0.2s ease-in-out',
                        }}
                        disabled={currentPage === totalPages}
                        onMouseEnter={(e) => (e.target.style.transform = 'scale(1.1)')}
                        onMouseLeave={(e) => (e.target.style.transform = 'scale(1)')}
                        onClick={goToLastPage}
                    >
                        Last
                    </Button>
                </div>
            </>
        );
    } catch (error) {
        Logger.error(`${RenderDeviceTable.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display device information in table format');
    }
};
