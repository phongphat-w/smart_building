import React, { useState } from 'react';
import { ButtonGroup, Button } from 'react-bootstrap';

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';

export const RenderViewToggle = ({ setViewMode }) => {
    try {
        const [viewMode, setLocalViewMode] = useState('thumbnails'); // Default view is thumbnails

        const handleChangeView = (mode) => {
            setLocalViewMode(mode);
            setViewMode(mode);
        };

        return (
            <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', marginBottom: '20px' }}>
                <label htmlFor='view-select' style={{ marginRight: '10px', fontWeight: 'normal' }}>View Mode:</label>
                <ButtonGroup>
                    <Button
                        variant={viewMode === 'thumbnails' ? 'primary' : 'outline-primary'}
                        onClick={() => handleChangeView('thumbnails')}
                        style={{
                            padding: '8px 16px',
                            fontWeight: viewMode === 'thumbnails' ? 'bold' : 'normal',
                        }}
                    >
                        Thumbnails
                    </Button>
                    <Button
                        variant={viewMode === 'table' ? 'primary' : 'outline-primary'}
                        onClick={() => handleChangeView('table')}
                        style={{
                            padding: '8px 16px',
                            fontWeight: viewMode === 'table' ? 'bold' : 'normal',
                        }}
                    >
                        Table
                    </Button>
                </ButtonGroup>
            </div>
        );
    } catch (error) {
        Logger.error(`${RenderViewToggle.name}(): ${error.message}`, error);
        MessageAlert('danger', 'Cannot display View Toggle');
    }
};
