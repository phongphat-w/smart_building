import axios from 'axios';

import Logger from '../../com-utils/logger.js';

const API_URL = process.env.REACT_APP_SB_API_URL;

export const useHandleSubmit = async (data, setLoading, setMessage) => {
    setLoading(true); // Show loading indicator
    setMessage(''); // Clear previous messages

    try {
        const response = await axios.post(`$API_HOST}/device_control/`, data, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.status === 201) {
            // Success
            setLoading(false);
            setMessage('Save successfully!');
        } else {
            // Handle unexpected status codes
            setLoading(false);
            setMessage(response.data?.message || 'Unexpected response from server.');
            Logger.error(response.data?.message || 'Unexpected response from server.');
        }
    } catch (error) {
        setLoading(false); // Hide loading indicator
        if (error.response) { // Server responded with an error
            console.error("Error response:", error.response);
            setMessage(`Error during save: ${error.response.data?.error || 'Unknown server error'}`);
            Logger.error(`${useHandleSubmit.name}(): Error during save: ${error.response.data?.error || 'Unknown server error'}`);
        
        } else if (error.request) { // No response received from server
            console.error("Error request:", error.request);
            setMessage('No response from server. Please try again later.');
            Logger.error(`${useHandleSubmit.name}(): Error - No response from server. Please try again later.`);
        
        } else { // Other errors
            console.error("Error:", error.message);
            setMessage(`Unexpected error: ${error.message}`);
            Logger.error(`${useHandleSubmit.name}(): Error - ${error}`);
        }
    }
};
