import React from 'react';
import { FaThermometerHalf, FaLightbulb, FaCloudSun, FaFan, FaCamera, FaSearch, FaUsers, FaWater, FaRecycle, FaBatteryHalf, FaWindows, FaChild, FaTrash } from 'react-icons/fa';

import ConfDeviceInfo from '../../com-utils/conf-device-Info.js';
import Logger from '../../com-utils/logger.js';

export function getDeviceIcon(device){
    try {
        switch (device.iot_device_id) {
            case ConfDeviceInfo.devIdThermostats: return <FaThermometerHalf size={30} color='red' />;
            case ConfDeviceInfo.devIdDemConVen: return <FaCloudSun size={30} color='green' />;
            case ConfDeviceInfo.devIdAirCon: return <FaFan size={30} color='green' />;
            case ConfDeviceInfo.devIdCameras: return <FaCamera size={30} color='gray' />;
            case ConfDeviceInfo.devIdBulbs: return <FaLightbulb size={30} color='orange' />;
            case ConfDeviceInfo.devIdElecMeter: return <FaBatteryHalf size={30} />;
            case ConfDeviceInfo.devIdWaterLeak: return <FaWater size={30} color='blue' />;
            case ConfDeviceInfo.devIdBins: return <FaRecycle size={30} color='brown' />;
            case ConfDeviceInfo.devIdBlinds: return <FaWindows size={30} color='pink' />;
            case ConfDeviceInfo.devIdPresence: return <FaChild size={30} color='blue' />;
            default: return <FaSearch size={30} />;
        }
    } catch (error) {
        Logger.error(`${getDeviceIcon.name}(): ${error}`);
        return <FaSearch size={30} />;
    }   
};