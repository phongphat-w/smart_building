import axios from 'axios';
import Logger from '../../com-utils/logger.js';

const roleIdString = process.env.REACT_APP_SB_ROLE_ID;
const roleId = JSON.parse(roleIdString);

export const useFetchDevices = async (API_HOST, userInfo) => {
    try {
        if (!userInfo || !userInfo[0]){
            Logger.error('Invalid user info');
            return [];
        } 

        let urlDevices = "";

        if (userInfo[0]?.role_id === roleId.SB_ROLE_ID_ADMIN) {
            urlDevices = `${API_HOST}/api/adevices/${userInfo[0]?.account_id}/`;
        } else if (userInfo[0]?.role_id === roleId.SB_ROLE_ID_STAFF) {
            urlDevices = `${API_HOST}/api/fdevices/${userInfo[0]?.account_id}/${userInfo[0]?.building_id}/${userInfo[0]?.floor_id}/`;
        } else {
            urlDevices = `${API_HOST}/api/rdevices/${userInfo[0]?.account_id}/${userInfo[0]?.building_id}/${userInfo[0]?.floor_id}/${userInfo[0]?.room_id}`;
        }

        const response = await axios.get(urlDevices);
        if (response.data && Array.isArray(response.data.data)) {
            return response.data.data; // Return the data
        } else {
            Logger.error('Unexpected response format:', response.data);
            Logger.error(`${fetchDevices.name}(): Unexpected response format: - ${response.data}`);
            return [];
        }
    } catch (error) {
        Logger.error(`${useFetchDevices.name}(): ${error}`);
        return [];
    }
};