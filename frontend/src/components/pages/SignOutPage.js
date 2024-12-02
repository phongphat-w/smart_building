import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SignOutPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear the stored tokens from localStorage
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');

    // Redirect to the SignIn page
    navigate('/signin');
  }, [navigate]);

  return (
    <div className="signout-message">
      <h2>Signing out...</h2>
    </div>
  );
};

export default SignOutPage;
