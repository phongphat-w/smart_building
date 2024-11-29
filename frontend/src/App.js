import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
//import GenDataPage from "./pages/GenDataPage";  // Import the page
import GuestSignupForm from "./pages/GuestSignupForm";
import UserListPage from "./pages/UserListPage";
import DeviceDashboard from "./pages/DeviceDashboard";
import LoginPage from "./pages/LoginPage";

const App = () => {
  return (
    <Router>
      <Routes>        
        <Route path="/signup" element={<GuestSignupForm />} /> 
        <Route path="/get_users" element={<UserListPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DeviceDashboard />} />
      </Routes>
    </Router>
  );
};

export default App;
