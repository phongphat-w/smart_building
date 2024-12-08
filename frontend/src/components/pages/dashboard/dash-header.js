import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUsers } from 'react-icons/fa';
import { Col, Card } from 'react-bootstrap';

import { getUserDetails } from './dash-user.js';
import Logger from '../../com-utils/logger.js';

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
                {`Welcome: ${user_info?.loginDisplay || '-'}`}
                <button
                    className="btn btn-primary btn-sm"
                    onClick={signOut}
                    style={{ position: 'absolute', top: '10px', right: '10px' }}
                >
                    <FaUsers />&nbsp;Sign Out
                </button>
            </div>
        );
    } catch (error) {
        Logger.error(`${DashboardHeader.name}(): ${error.message}`, error);

        // render a fallback UI
        return (
            <Col md={4}>
                <Card>
                    <Card.Body>
                        <div className="device-card-error">
                            <h5 style={{ color: 'red' }}>Error rendering chart</h5>
                        </div>
                    </Card.Body>
                </Card>
            </Col>
        );
    }
};
