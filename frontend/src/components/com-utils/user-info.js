import Logger from './logger.js';

// Functions to retrieve data from localStorage
export const useGetAuthToken = () => localStorage.getItem('sb_access_token');
export const useRefreshToken = () => localStorage.getItem('sb_refresh_token');
const getUserInfo = () => {
    const userInfo = localStorage.getItem('sb_user_info');
    return userInfo ? JSON.parse(userInfo) : null;
};

let loginDisplay = '';
let isAdmin = false;
let roleName = '';

// Function to retrieve user-related info
export function getUserDetails(){
    try {
        const userInfo = getUserInfo();
        if (!userInfo) {
            Logger.error(`${getUserDetails.name}(): Error - There is no user information`);
            return null;
        }

        // Determine user role and construct URL
        if (userInfo[0]?.is_admin) {
            isAdmin = true;
            roleName = 'Administrator';
        } else if (userInfo[0]?.is_staff) {
            isAdmin = false;
            roleName = 'Staff';
        } else {
            isAdmin = false;
            roleName = 'Guest';
        }

        // Format login display string
        loginDisplay = `${userInfo[0]?.first_name} ${userInfo[0]?.last_name} (${roleName})`;

        return {
            userInfo,
            isAdmin,
            roleName,
            loginDisplay
        };

    } catch (error) {
        console.error("Error response: ", error);
        Logger.error("Error: ", error);
        Logger.error(`${getUserDetails.name}(): Error - ${error}`);
    }
   
};
