import React from 'react';
import { Col, Card, Button } from 'react-bootstrap';

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';
import getDeviceIcon from './dash-icons.js';

export const DeviceCard = ({ device, handleModalShow }) => {
    try {
        return (
            <Col key={device.iot_device_id} md={4}>
                <Card>
                    <Card.Body>
                        <div className="device-card">
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
                            <div style={{ textAlign: 'right' }}>
                                <Button onClick={() => handleModalShow(device)} variant="primary">Control &gt;&gt;</Button>
                            </div>
                        </div>
                    </Card.Body>
                </Card>
            </Col>
        );
    } catch (error) {
        Logger.error(`${DeviceCard.name}(): ${error.message}`, error);
        MessageAlert('danger','Cannot display device information');
    }
};
