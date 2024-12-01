import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import SignUpPage from "./components/pages/SignUpPage";
import SignInPage from "./components/pages/SignInPage";
import UserListPage from "./components/pages/UserListPage";
import DashboardPage from "./components/pages/DashboardPage";


const App = () => {
  return (
    <Router>
      <Routes>        
        <Route path="/signup" element={<SignUpPage />} /> 
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/userlists" element={<UserListPage />} />
        <Route path="/dashboards" element={<DashboardPage />} />
      </Routes>
    </Router>
  );
};

export default App;
