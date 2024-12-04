import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import SignUpPage from "./components/pages/SignUpPage";
import SignInPage from "./components/pages/SignInPage";
import UserListPage from "./components/pages/UserListPage";
// import DashboardPage from "./components/pages/DashboardPage";
import SignOutPage from "./components/pages/SignOutPage";
import MainDashboard from "./components/pages/MainDashboard";
import TestMap from "./components/pages/TestMap.js";
import TestMap2 from "./components/pages/TestMap2.js";


const App = () => {
  return (
    <Router>
      <Routes>        
        <Route path="/signup" element={<SignUpPage />} /> 
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/userlists" element={<UserListPage />} />
        {/* <Route path="/dashboards" element={<DashboardPage />} /> */}
        <Route path="/dashboard" element={<MainDashboard />} />
        <Route path="/testmap" element={<TestMap />} />
        <Route path="/testmap2" element={<TestMap2 />} />
        <Route path="/signout" element={<SignOutPage />} />
      </Routes>
    </Router>
  );
};

export default App;
