import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import SignUpPage from "./components/pages/SignUpPage";
import SignInPage from "./components/pages/SignInPage";
import UserListPage from "./components/pages/UserListPage";
import SignOutPage from "./components/pages/SignOutPage";
import MainDashboard from "./components/pages/MainDashboard";


const App = () => {
  return (
    <Router>
      <Routes>        
        <Route path="/signup" element={<SignUpPage />} /> 
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/userlists" element={<UserListPage />} />
        <Route path="/dashboard" element={<MainDashboard />} />
        <Route path="/signout" element={<SignOutPage />} />
      </Routes>
    </Router>
  );
};

export default App;
