import React, { createContext, useState, useEffect } from 'react';

// Create a Context for WebSocket data
export const WebSocketContext = createContext();

const WebSocketProvider = ({ children }) => {
  const [data, setData] = useState(null); // Store incoming WebSocket data
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/data');

    // Open WebSocket connection
    socket.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    // Listen for messages from the server
    socket.onmessage = (event) => {
      console.log('WebSocket message received:', event.data);
      try {
        const parsedData = JSON.parse(event.data);
        setData(parsedData); // Update state with parsed data
      } catch (error) {
        console.error('Error parsing WebSocket data:', error);
      }
    };

    // Handle WebSocket errors
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    // Handle WebSocket closure
    socket.onclose = () => {
      console.log('WebSocket closed');
      setIsConnected(false);
    };

    // Cleanup on unmount
    return () => {
      socket.close();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={{ data, isConnected }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export default WebSocketProvider;
