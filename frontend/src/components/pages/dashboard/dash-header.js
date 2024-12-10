import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUsers } from 'react-icons/fa';
import { Button } from 'react-bootstrap';

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';
import { getUserDetails } from '../../com-utils/user-info.js';


// it's not a custom hook but a React component.
export const DashboardHeader = ({ setIsAdmin, setRoleName }) => {
    try {
        const navigate = useNavigate();
        const user_info = getUserDetails();

        // Redirect to Sign In page
        const signOut = useCallback(() => {
            navigate('/signout');
        }, [navigate]);

        // Update parent states
        React.useEffect(() => {
            setIsAdmin(user_info?.isAdmin);
            setRoleName(user_info?.roleName);
        }, [user_info, setIsAdmin, setRoleName]);

        return (
            <div>
                <center><h1>Smart Building Dashboard</h1></center>
                <h5>{`Welcome: ${user_info?.loginDisplay || '-'}`}</h5> 
                {/* <button className="btn btn-primary btn-sm" onClick={signOut} style={{ position: 'absolute', top: '10px', right: '10px' }}>
                    <FaUsers></FaUsers>&nbsp;Sign Out
                </button> */}
                <Button variant="light" onclick={signOut} style={{ position: 'absolute', top: '10px', right: '10px' }}> <FaUsers></FaUsers>&nbsp;Sign Out </Button>
            </div>
        );
    } catch (error) {
        Logger.error(`${DashboardHeader.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display user information')
    }
};
