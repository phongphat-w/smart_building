import React, { useState } from 'react';
import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../page-utils/message-alert.js';

import { RenderViewToggle } from './dash-render-toggle.js';
import { RenderDeviceTable } from './dash-render-table.js';
import { RenderDeviceThumbnails } from './dash-render-thumbnails.js';

export const RenderDevices = ({ deviceData, handleModalShow }) => {
    const [viewMode, setViewMode] = useState('thumbnails'); // Default view is thumbnails

    try {
        return (
            <>
                <RenderViewToggle setViewMode={setViewMode} />
                {viewMode === 'thumbnails' && <RenderDeviceThumbnails deviceData={deviceData} handleModalShow={handleModalShow} />}
                {viewMode === 'table' && <RenderDeviceTable deviceData={deviceData} handleModalShow={handleModalShow} />}
            </>
        );
    } catch (error) {
        Logger.error(`${RenderDevices.name}(): ${error.message}`, error);
        return <MessageAlert alertType="danger" messageAlert="Cannot display device information" />;
    }
};
