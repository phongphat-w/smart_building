import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SignOutPage = () => {
  const navigate = useNavigate();

  // SignOut function - used to remove tokens from localStorage
  const signOut = useCallback(() => {
    console.log("DEBUG: signOut() - is working")
    localStorage.removeItem('sb_access_token');  // Remove access token
    localStorage.removeItem('sb_refresh_token');  // Remove refresh token
    localStorage.removeItem('sb_user_info');  // Remove refresh token
    // console.log("DEBUG: 2 tokens are removed")
    navigate('/signin');  // Redirect to Sign In page
  }, [navigate]);


  return (
    <div className="signout-message">
      <h2>Signing out...</h2>
    </div>
  );
};

export default SignOutPage;
