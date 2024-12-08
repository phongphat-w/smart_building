import React, { useEffect, useState } from 'react';
import { Modal, Button, Col, Card } from 'react-bootstrap';
import { useHandleSubmit } from './dash-submit.js';

import Logger from '../../com-utils/logger.js';
import ConfDeviceInfo from '../../com-utils/conf-device-Info.js';

export const ModalDevice = ({ modalShow, handleModalClose, selectedDevice, user_id }) => {
    try {
        const [temperThemostats, setTemperThemostats] = useState("");
        const [batLevelThermostats, setBatLevelThermostats] = useState("");

        const [co2DemConVen, setCo2DemConVen] = useState("");
        const [humidity, setHumidity] = useState("");
        const [batLevelDemConVen, setBatLevelDemConVen] = useState("");
        
        const [lightLevelBulbs, setLightLevelBulbs] = useState("");
        const [temperBulbs, setTemperBulbs] = useState("");
        const [batLevelBulbs, setBatLevelBulbs] = useState("");

        const [voltageElecMeter, setVoltageElecMeter] = useState("");
        const [currentElecMeter, setCurrentElecMeter] = useState("");
        const [batLevelElecMeter, setBatLevelElecMeter] = useState("");

        const [lightLevelBlinds, setLightLevelBlinds] = useState("");
        const [temperBlinds, setTemperBlinds] = useState("");
        const [batLevelBlinds, setBatLevelBlinds] = useState("");

        const [temperAirCon, setTemperAirCon] = useState("");
        const [batLevelAirCon, setBatLevelAirCon] = useState("");

        const [humanStatus, sethumanStatus] = useState("");
        const [batLevelCameras, setBatLevelCameras] = useState("");

        const [waterLeak, setWaterLeak] = useState("");
        const [batLevelWaterLeak, setBatLevelWaterLeak] = useState("");

        const [smartBins, setSmartBins] = useState("");
        const [batLevelSmartBins, setBatLevelSmartBins] = useState("");

        const [rfidTags, setRfidTags] = useState("");
        const [batLevelRfidTags, setBatLevelRfidTags] = useState("");

        const [message, setMessage] = useState("");

        // Update state when `selectedDevice` changes
        useEffect(() => {
            if (selectedDevice) {
                switch (selectedDevice.iot_device_id) {
                    case ConfDeviceInfo.devIdThermostats:
                        setTemperThemostats('25'); // Default value or fetch existing
                        break;
                    case ConfDeviceInfo.devIdDemConVen:
                        //setTemperDemConVen('25');
                        break;
                    case ConfDeviceInfo.devIdBulbs:
                        setLightLevelBulbs('70');
                        setTemperBulbs('25');
                        break;
                    case ConfDeviceInfo.devIdElecMeter:
                        setVoltageElecMeter('100');
                        setCurrentElecMeter('50');
                        break;
                    case ConfDeviceInfo.devIdBlinds:
                        setLightLevelBlinds('xx');
                        setTemperBlinds('xx');
                        break;
                    case ConfDeviceInfo.devIdAirCon:
                        setTemperAirCon('25');
                        break;
                    default:
                        Logger.warning('Unknown device type:', selectedDevice.iot_device_id);
                }
            } else {
                // Clear state when no device is selected
                setTemperThemostats('');
                //setTemperDemConVen('');
                setLightLevelBulbs('');
                setTemperBulbs('');
                setVoltageElecMeter('');
                setCurrentElecMeter('');
                setLightLevelBlinds('');
                setTemperBlinds('');
                setTemperAirCon('');
            }
        }, [selectedDevice]);

        const handleSave = () => {
            if (!selectedDevice) {
                setMessage("No device selected.");
                return;
            }

            const formData = {
                user_id: user_id,
                device_id: selectedDevice.iot_device_id,
                sensors: {},
            };

            // Dynamically set sensor data; based on device type
            switch (selectedDevice.iot_device_id) {
                case ConfDeviceInfo.devIdThermostats: // Smart thermostats
                    formData.sensors.temperature = temperThemostats;
                    break;
                case ConfDeviceInfo.devIdDemConVen: // Demand-Controlled Ventilation (DCV)
                    formData.sensors.temperature = temperDemConVen;
                    break;
                case ConfDeviceInfo.devIdBulbs: // Smart bulbs and LED lights
                    formData.sensors.light_level = lightLevelBulbs;
                    formData.sensors.temperature = temperBulbs;
                    break;
                case ConfDeviceInfo.devIdElecMeter: // Smart electric meters
                    formData.sensors.voltage = voltageElecMeter;
                    formData.sensors.current = currentElecMeter;
                    break;
                case ConfDeviceInfo.devIdBlinds: // Automated blinds or shades
                    formData.sensors.light_level = lightLevelBlinds;
                    formData.sensors.temperature = temperBlinds;
                    break;
                case ConfDeviceInfo.devIdAirCon: // Air Conditioning
                    formData.sensors.temperature = temperAirCon;
                    break;
                default:
                    setMessage("Unsupported device type.");
                    Logger.error("Error saving configuration:", error);
                    return;
            }

            // Call handleSubmit with the collected form data
            // import { handleSubmit } from './dash-submit.js';
            handleSubmit(formData)
                .then(() => {
                    setMessage("Save successful!");
                    handleModalClose();
                })
                .catch((error) => {
                    console.error("Error saving configuration:", error);
                    setMessage("Error saving configuration.");
                    Logger.error("Error saving configuration:", error);
                });
        };

        return (
            <Modal show={modalShow} onHide={handleModalClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Device Configuration</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="container mt-5">
                        <h4>{selectedDevice?.device_sub_type_name}</h4>
                        <div className="form-group">
                            <label>Device ID: </label>&nbsp;{selectedDevice?.iot_device_id}
                            <br/><br/>
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdThermostats && (
                                <>
                                    <label>Temperature:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={temperThemostats}
                                        onChange={(e) => setTemperThemostats(e.target.value)}
                                        required
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelThermostats}
                                        onChange={(e) => setBatLevelThermostats(e.target.value)}
                                        required
                                        readOnly
                                    />
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdDemConVen && (
                                <>
                                    <label>CO<sub>2</sub>:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={co2DemConVen}
                                        onChange={(e) => setCo2DemConVen(e.target.value)}
                                        required
                                        readOnly
                                    />
                                    <label>Humidity:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={humidity}
                                        onChange={(e) => setHumidity(e.target.value)}
                                        required
                                        readOnly
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelDemConVen}
                                        onChange={(e) => setBatLevelDemConVen(e.target.value)}
                                        required
                                        readOnly
                                    />                              
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdBulbs && (
                                <>
                                    <label>Light Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={lightLevelBulbs}
                                        onChange={(e) => setLightLevelBulbs(e.target.value)}
                                        required
                                    />
                                    <label>Temperature:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={temperBulbs}
                                        onChange={(e) => setTemperBulbs(e.target.value)}
                                        required
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelBulbs}
                                        onChange={(e) => setBatLevelBulbs(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdElecMeter && (
                                <>
                                    <label>Voltage:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={voltageElecMeter}
                                        onChange={(e) => setVoltageElecMeter(e.target.value)}
                                        required
                                    />
                                    <label>Current:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={currentElecMeter}
                                        onChange={(e) => setCurrentElecMeter(e.target.value)}
                                        required
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelElecMeter}
                                        onChange={(e) => setBatLevelElecMeter(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdBlinds && (
                                <>
                                    <label>Light Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={lightLevelBlinds}
                                        onChange={(e) => setLightLevelBlinds(e.target.value)}
                                        required
                                    />
                                    <label>Temperature:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={temperBlinds}
                                        onChange={(e) => setTemperBlinds(e.target.value)}
                                        required
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelBlinds}
                                        onChange={(e) => setBatLevelBlinds(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdAirCon && (
                                <>
                                    <label>Temperature:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={temperAirCon}
                                        onChange={(e) => setTemperAirCon(e.target.value)}
                                        required
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelAirCon}
                                        onChange={(e) => setBatLevelAirCon(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdCameras && (
                                <>
                                    <label>Human Status:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={humanStatus}
                                        onChange={(e) => sethumanStatus(e.target.value)}
                                        required
                                        readOnly
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelCameras}
                                        onChange={(e) => setBatLevelCameras(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdWaterLeak && (
                                <>
                                    <label>Water Leakage Status:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={waterLeak}
                                        onChange={(e) => setWaterLeak(e.target.value)}
                                        required
                                        readOnly
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelWaterLeak}
                                        onChange={(e) => setBatLevelWaterLeak(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdBins && (
                                <>
                                    <label>Bins Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={smartBins}
                                        onChange={(e) => setSmartBins(e.target.value)}
                                        required
                                        readOnly
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelSmartBins}
                                        onChange={(e) => setBatLevelSmartBins(e.target.value)}
                                        required
                                        readOnly
                                    /> 
                                </>
                            )}
                            {selectedDevice?.iot_device_id === ConfDeviceInfo.devIdRfidTags && (
                                <>
                                    <label>Object Position:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={rfidTags}
                                        onChange={(e) => setRfidTags(e.target.value)}
                                        required
                                        readOnly
                                    />
                                    <label>Battery Level:</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={batLevelRfidTags}
                                        onChange={(e) => setBatLevelRfidTags(e.target.value)}
                                        required
                                        readOnly                                        
                                    /> 
                                </>
                            )}

                        </div>
                        {message && <p>{message}</p>}
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={handleSave}>
                        Save
                    </Button>
                    <Button variant="secondary" onClick={handleModalClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        );
    } catch (error) {
        Logger.error(`${ModalDevice.name}(): ${error.message}`, error);

        // render a fallback UI
        return (
            <Col md={4}>
                <Card>
                    <Card.Body>
                        <div className="device-card-error">
                            <h5 style={{ color: 'red' }}>Cannot display device information</h5>
                        </div>
                    </Card.Body>
                </Card>
            </Col>
        );
    }    
};
