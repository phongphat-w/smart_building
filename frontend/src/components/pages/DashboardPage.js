// ESLint's Import Order Rule

// React imports
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

// Third-party library imports
//--

// Internal or project-specific imports
import { getUserDetails } from '../com-utils/user-info.js';
import { DashboardHeader } from './dashboard/dash-header.js';
import { useFetchDevices } from './dashboard/dash-fetch.js';
import { RenderDevices } from './dashboard/dash-render.js';
import { ModalDevice } from './dashboard/dash-modal.js';

import Logger from '../com-utils/logger.js';
import { MessageAlert } from '../com-utils/message-alert.js';

// Styles and assets imports
//--

const API_HOST = process.env.REACT_APP_SB_API_URL + ":" + process.env.REACT_APP_SB_API_PORT;

const DashboardPage = () => {
    try {
    
        const navigate = useNavigate();

        const [deviceData, setDeviceData] = useState([]);
        const [modalShow, setModalShow] = useState(false);
        const [selectedDevice, setSelectedDevice] = useState(null);  
        // const [chartDataElecFloor, setChartDataElecFloor] = useState(null);
        // const [chartDataElec, setChartDataElec] = useState(null);
        // const [chartDataWater, setChartDataWater] = useState(null);
        const [isAdmin, setIsAdmin] = useState(false);
        const [roleName, setRoleName] = useState('');
        //const [loginDisplay, setLoginDisplay] = useState(false);
        
        const [message, setMessage] = useState('');
        const [errorMessage, setErrorMessage] = useState('');
        const [loading, setLoading] = useState(false);

        const [dashboardHeader, setDashboardHeader] = useState(null);
        const [deviceCards, setDeviceCards] = useState(null);

         // Handle modal show for a specific device
        const handleModalShow = (device) => {
            setSelectedDevice(device);
            setModalShow(true);
        };

        // Handle modal close
        const handleModalClose = () => {
            setModalShow(false);
            setSelectedDevice(null);
        };

        // Fetch device for all roles
        useEffect(() => {
            const loadDevices = async () => {
                try {
                    const data = await useFetchDevices(API_HOST, getUserDetails().userInfo);
                    setDeviceData(data || []); // Fallback to empty array if no data
                } catch (error) {
                    Logger.error(`${DashboardPage.name}(): Error loading devices: ${error}`);
                }
            };
            loadDevices();
        }, []);
        
        return (
            <div style={{ padding: '20px' }}>
                <DashboardHeader setIsAdmin={setIsAdmin} setRoleName={setRoleName} />

                <>
                    {deviceData && deviceData.length > 0 ? (
                        <RenderDevices deviceData={deviceData} handleModalShow={handleModalShow} />
                    ) : (
                        MessageAlert('warning', 'No devices found')
                    )}
                </>
                
                <ModalDevice  modalShow={modalShow}  handleModalClose={handleModalClose}  selectedDevice={selectedDevice} user_id={deviceData?.[0]?.user_id} />
                
            </div> //End of main div
        ); //End of return
    } catch (error){
        console.error(`${DashboardPage.name}(): Error - ' + ${error}`);
        Logger.error(`${DashboardPage.name}(): Error - ' + ${error}`);
        MessageAlert('danger', 'Cannot show dashboard appropriately')
    }
    
};

export default DashboardPage;
