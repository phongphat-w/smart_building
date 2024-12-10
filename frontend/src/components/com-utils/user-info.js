import Logger from './logger.js';

// Functions to retrieve data from localStorage
export const useGetAuthToken = () => localStorage.getItem('sb_access_token');
export const useRefreshToken = () => localStorage.getItem('sb_refresh_token');
const getUserInfo = () => {
    const userInfo = localStorage.getItem('sb_user_info');
    return userInfo ? JSON.parse(userInfo) : null;
};

let loginDisplay = '';

// Function to retrieve user-related info
export function getUserDetails(){
    try {
        const userInfo = getUserInfo();
        if (!userInfo) {
            Logger.error(`${getUserDetails.name}(): Error - There is no user information`);
            return null;
        }        

        // Format login display string
        loginDisplay = `${userInfo[0]?.first_name} ${userInfo[0]?.last_name} (${userInfo[0]?.role_name})`;

        return {
            userInfo,
            loginDisplay
        };

    } catch (error) {
        console.error("Error response: ", error);
        Logger.error("Error: ", error);
        Logger.error(`${getUserDetails.name}(): Error - ${error}`);
    }
   
};
