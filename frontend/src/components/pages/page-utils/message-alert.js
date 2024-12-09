import { Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Logger from '../../com-utils/logger.js';

export const MessageAlert = ({ alertType, messageAlert }) => {
    try {
        const variantTypes = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'];

        // Check if the provided alertType is valid
        const isValidType = variantTypes.includes(alertType);

        return (
            <Alert variant={isValidType ? alertType : 'info'}>{messageAlert}</Alert>
        );
    } catch (error){
        Logger.error(`${MessageAlert.name}(): ${error.message}`, error);
        return <Alert variant="danger">An error occurred while displaying the alert.</Alert>;
    }
};