import { Pie, Line } from 'react-chartjs-2';

import Logger from '../../com-utils/logger.js';
import { MessageAlert } from '../../com-utils/message-alert.js';

function ElectricityUsageChart(chartDataElecFloor){
    try {
        return (
            <div id='chartDataElecFloor' style={{ height: '200px', width: '100%' }}>
                {chartDataElecFloor ? <Pie data={chartDataElecFloor} /> : <p>Loading chart data...</p>}
            </div>
        );
    } catch (error) {
        Logger.error(`${genElectricityUsageChart.name}(): ${error.message}`, error);
        MessageAlert('danger','Error rendering chart');
    }

};

function ElectricityBillChart(chartDataElec){
    try {
        return (
            <div id='chartDataElec' style={{ height: '200px', width: '100%' }}>
                {chartDataElec ? <Line data={chartDataElec} /> : <p>Loading chart data...</p>}
            </div>
        );
    } catch (error) {
        Logger.error(`${genElectricityBillChart.name}(): ${error.message}`, error);
        MessageAlert('danger','Error rendering chart');
    }
};

function WaterConsumptionChart(chartDataWater){
    try {
        return (
            <div id='chartDataWater' style={{ height: '200px', width: '100%' }}>
                {chartDataWater ? <Line data={chartDataWater} /> : <p>Loading chart data...</p>}
            </div>
        );
    } catch (error) {
        Logger.error(`${genWaterConsumptionChart.name}(): ${error.message}`, error);
        MessageAlert('danger','Cannot display chart');        
    }
};
