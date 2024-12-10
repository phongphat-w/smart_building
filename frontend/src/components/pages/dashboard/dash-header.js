import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUsers } from 'react-icons/fa';
import { Button } from 'react-bootstrap';

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';
import { getUserDetails } from '../../com-utils/user-info.js';

const roleIdString = process.env.REACT_APP_SB_ROLE_ID;
const roleId = JSON.parse(roleIdString);

// it's not a custom hook but a React component.
export const DashboardHeader = ({ setIsAdmin, setRoleName }) => {
    try {
        const navigate = useNavigate();
        const user_info = getUserDetails();

        // Redirect to Sign In page
        const signOut = () => {
            navigate('/signout');
        };

        // Update parent states
        React.useEffect(() => {
            setIsAdmin(user_info?.role_id === roleId.SB_ROLE_ID_ADMIN);
            setRoleName(user_info?.role_name);
        }, [user_info, setIsAdmin, setRoleName]);

        return (
            <div>
                <center><h1>Smart Building Dashboard</h1></center>
                <h5>{`Welcome: ${user_info?.loginDisplay || '-'}`}</h5> 
                {/* <button className="btn btn-primary btn-sm" onClick={signOut} style={{ position: 'absolute', top: '10px', right: '10px' }}>
                    <FaUsers></FaUsers>&nbsp;Sign Out
                </button> */}
                <Button variant="light" onClick={signOut} style={{ position: 'absolute', top: '10px', right: '10px' }}> <FaUsers></FaUsers>&nbsp;Sign Out </Button>
            </div>
        );
    } catch (error) {
        Logger.error(`${DashboardHeader.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display user information')
    }
};
