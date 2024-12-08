import axios from 'axios';

/**
 * Fetch device data based on user info.
 * @param {Function} setDeviceData - State setter for device data.
 * @param {Function} setIsAdmin - State setter for admin status.
 * @param {Function} setLoginDisplay - State setter for login display.
 * @param {Function} getUserInfo - Function to retrieve user info from localStorage.
 * @param {String} API_URL - Base API URL.
 */
export const fetchDeviceAll = async (setDeviceData, setIsAdmin, setLoginDisplay, getUserInfo, API_URL) => {
  const userInfo = JSON.parse(getUserInfo());
  if (!userInfo || !userInfo[0]?.account_id) {
    console.error("Invalid or missing user info:", userInfo);
    return;
  }

  let roleName = '';
  let urlDevices = '';

  if (userInfo[0].is_admin) {
    roleName = 'Administrator';
    urlDevices = `${API_URL}/api/adevices/${userInfo[0].account_id}/`;
  } else if (userInfo[0].is_staff) {
    roleName = 'Staff';
    urlDevices = `${API_URL}/api/fdevices/${userInfo[0].account_id}/${userInfo[0].building_id}/${userInfo[0].floor_id}/`;
  } else {
    roleName = 'Guest';
    urlDevices = `${API_URL}/api/rdevices/${userInfo[0].account_id}/${userInfo[0].building_id}/${userInfo[0].floor_id}/${userInfo[0].room_id}`;
  }

  console.log("DEBUG: Constructed URL:", urlDevices);

  try {
    const response = await axios.get(urlDevices);
    const data = response.data;
    if (data && Array.isArray(data.data)) {
      setDeviceData(data.data);
    } else {
      console.error("Unexpected response format:", data);
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }

  setIsAdmin(String(userInfo[0].is_admin));
  setLoginDisplay(`${userInfo[0].first_name} ${userInfo[0].last_name} (${roleName})`);
};
