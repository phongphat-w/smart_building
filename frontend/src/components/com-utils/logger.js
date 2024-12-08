const ENABLE_EXTERNAL_LOGGING = process.env.REACT_APP_SB_ENABLE_LOGGING === 'true';
// const LOGGING_API_URL = process.env.REACT_APP_LOGGING_API_URL;

async function createLog(level, message, optionalParams) {
    if (!ENABLE_EXTERNAL_LOGGING) return;

    try {
        const response = await fetch(LOGGING_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                timestamp: new Date().toISOString(),
                level,
                message,
                details: optionalParams,
            }),
        });

        if (!response.ok) {
            console.error(
                `Failed to log externally. Status: ${response.status}, Message: ${response.statusText}`
            );
        }
    } catch (err) {
        console.error('Failed to log externally:', err);
    }
}

const logLevels = {
    DEBUG: 'DEBUG',
    INFO: 'INFO',
    WARNING: 'WARNING',
    ERROR: 'ERROR',
    CRITICAL: 'CRITICAL',
};

const Logger = {
    debug: async (message, ...optionalParams) => {
        console.debug(`[${logLevels.DEBUG}] [${new Date().toISOString()}]`, message, ...optionalParams);
        await createLog(logLevels.DEBUG, message, optionalParams);
    },
    info: async (message, ...optionalParams) => {
        console.info(`[${logLevels.INFO}] [${new Date().toISOString()}]`, message, ...optionalParams);
        await createLog(logLevels.INFO, message, optionalParams);
    },
    warning: async (message, ...optionalParams) => {
        console.warn(`[${logLevels.WARNING}] [${new Date().toISOString()}]`, message, ...optionalParams);
        await createLog(logLevels.WARNING, message, optionalParams);
    },
    error: async (message, ...optionalParams) => {
        console.error(`[${logLevels.ERROR}] [${new Date().toISOString()}]`, message, ...optionalParams);
        await createLog(logLevels.ERROR, message, optionalParams);
    },
    critical: async (message, ...optionalParams) => {
        console.error(`[${logLevels.CRITICAL}] [${new Date().toISOString()}]`, message, ...optionalParams);
        await createLog(logLevels.CRITICAL, message, optionalParams);
    },
};

export default Logger;
