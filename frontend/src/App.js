import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import SignUpPage from "./pages/SignUpPage";
import SignInPage from "./pages/SignInPage";
import UserListPage from "./pages/UserListPage";
import DashboardPage from "./pages/DashboardPage";


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
