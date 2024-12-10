import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import Logger from '../../components/com-utils/logger.js'
import { MessageAlert } from '../com-utils/message-alert.js';

const API_URL = process.env.REACT_APP_SB_API_URL_PORT

const GuestSignupForm = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [checkInDate, setCheckInDate] = useState('');
  const [checkOutDate, setCheckOutDate] = useState('');
  const [buildingId, setBuildingId] = useState('');
  const [floorId, setFloorId] = useState('');
  const [roomId, setRoomId] = useState('');
  
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');
  
    const data = {
        first_name: firstName,
        last_name: lastName,
        password,
        email,
        checkin_date: checkInDate,
        checkout_date: checkOutDate,
        building_id: buildingId,
        floor_id: floorId,
        room_id: roomId,
    };
  
    try {
      console.log(`DEBUG: URL = ${API_URL}/api/register_guest/`)
      const response = await axios.post(`${API_URL}/api/register_guest/`, data, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 201) {
        setLoading(false);
        MessageAlert('success', 'Registration successful!');
        setMessage(
          <>
            <p>Register successfully! Welcome to our Smart Building. 
              <Link to='/signin' className='btn btn-link'>SignIn</Link>
            </p>
          </>
        );
      }
      else {
        setMessage(response.data.message);
        MessageAlert('danger', 'Error during registration');
      }

    } catch (error) {
      setLoading(false); // Hide loading indicator
      MessageAlert('danger', 'Error during registration');

      if (error.response) {
        // Server responded with an error
        console.error('Error response:', error.response);
        Logger.error(`${GuestSignupForm.name}(): Error response - ' + ${error.response}`);
        setMessage('Error during registration');
        
      } else if (error.request) {
        // No response received from server
        console.error('Error request:', error.request);
        Logger.error(`${GuestSignupForm.name}(): Error request - ' + ${error.request}`);
        setMessage('No response from server');

      } else {
        // Something else went wrong
        console.error('Error:', error.message);
        Logger.error(`${GuestSignupForm.name}(): Error - ' + ${error.message}`);
        setMessage('Error during registration: ' + error.message);
      }
    }
  };

  return (
    <div className='container mt-5'>
      <h2>Guest Registration</h2>
      <form onSubmit={handleSubmit}>        
        <div className='form-group'>
          <label>First Name</label>
          <input type='text' className='form-control' value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Last Name</label>
          <input type='text' className='form-control' value={lastName} onChange={(e) => setLastName(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Password</label>
          <input type='password' className='form-control' value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Email (email will be a user name for sign in)</label>
          <input type='email' className='form-control' value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Check-in Date</label>
          <input type='datetime-local' className='form-control' value={checkInDate} onChange={(e) => setCheckInDate(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Check-out Date</label>
          <input type='datetime-local' className='form-control' value={checkOutDate} onChange={(e) => setCheckOutDate(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Building ID (3 Digits, i.e., 001)</label>
          <input type='text' className='form-control' value={buildingId} onChange={(e) => setBuildingId(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Floor ID (4 Digits, i.e., 0001)</label>
          <input type='text' className='form-control' value={floorId} onChange={(e) => setFloorId(e.target.value)} required />
        </div>
        <div className='form-group'>
          <label>Room ID (5 Digits, i.e., 00001)</label>
          <input type='text' className='form-control' value={roomId} onChange={(e) => setRoomId(e.target.value)} required />
        </div>
        <button type='submit' className='btn btn-primary mt-3'>Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default GuestSignupForm;
