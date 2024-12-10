import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SignOutPage = () => {
  const navigate = useNavigate();

  // SignOut function - used to remove tokens from localStorage
  const signOut = () => {
    console.log("DEBUG: signOut() - is working");

    // Remove the items
    localStorage.removeItem('sb_access_token');
    localStorage.removeItem('sb_refresh_token');
    localStorage.removeItem('sb_user_info');

    // Confirm the removal
    console.log("DEBUG: After removal");
    console.log("DEBUG: sb_access_token", localStorage.getItem('sb_access_token'));
    console.log("DEBUG: sb_refresh_token", localStorage.getItem('sb_refresh_token'));
    console.log("DEBUG: sb_user_info", localStorage.getItem('sb_user_info'));
  };

  useEffect(() => {
    console.log("DEBUG: useEffect triggered");
    signOut();

    // Adding a slight delay before navigating
    setTimeout(() => {
      navigate('/signin');
    }, 1000);  // Delay for 1 second to ensure signOut happens
  }, [navigate]);

  return (
    <div className="signout-message">
      <h2>Signing out...</h2>
    </div>
  );
};

export default SignOutPage;
