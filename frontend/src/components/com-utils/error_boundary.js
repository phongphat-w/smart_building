import React, { Component } from 'react';

class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, errorInfo: null };
    }

    // Update state so the next render shows the fallback UI
    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    // Log the error details for debugging
    componentDidCatch(error, errorInfo) {
        console.error("Error caught by ErrorBoundary:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ color: 'red', textAlign: 'center', marginTop: '20px' }}>
                    <h2>Something went wrong.</h2>
                    <p>We're working on fixing this issue.</p>
                </div>
            );
        }

        // Render children components if no error
        return this.props.children;
    }
}

export default ErrorBoundary;
