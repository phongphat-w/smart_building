import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import SignUpPage from "./components/pages/SignUpPage.js";
import SignInPage from "./components/pages/SignInPage.js";
import UserListPage from "./components/pages/UserListPage.js";
import SignOutPage from "./components/pages/SignOutPage.js";
import DashboardPage from "./components/pages/DashboardPage.js";


const App = () => {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>        
        <Route path="/signup" element={<SignUpPage />} /> 
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/userlists" element={<UserListPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/signout" element={<SignOutPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
