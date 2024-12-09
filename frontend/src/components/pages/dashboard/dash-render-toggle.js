import React, { useState } from 'react';

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../page-utils/message-alert.js';

export const RenderViewToggle = ({ deviceData, setViewMode }) => {
    try {
        const [viewMode, setLocalViewMode] = useState("thumbnails"); // Default view is thumbnails

        const handleChangeView = (event) => {
            const mode = event.target.value;
            setLocalViewMode(mode);
            setViewMode(mode);
        };

        return (
            <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', marginBottom: '20px' }}>
                <label htmlFor="view-select" style={{ marginRight: '10px' }}>View Mode:</label>
                <select
                    id="view-select"
                    value={viewMode}
                    onChange={handleChangeView}
                    style={{ padding: '5px' }}
                >
                    <option value="thumbnails">Thumbnails</option>
                    <option value="table">Table</option>
                </select>
            </div>
        );
    } catch (error){
        Logger.error(`${RenderViewToggle.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display View Toggle');
    }
};
