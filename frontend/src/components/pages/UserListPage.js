import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const UserListPage = () => {
  const [users, setUsers] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [expanded, setExpanded] = useState({});

  // Fetch users data from the API
  const fetchUsers = useCallback(async (page = 1) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/get_users/?search=${searchQuery}&page=${page}`);
      
      // Check the data returned
      console.log("API Response:", response.data);
  
      setUsers(response.data.results);
      setTotalPages(Math.ceil(response.data.count / 10));  // Adjust for pagination
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  }, [searchQuery]);  // Make sure searchQuery is a dependency here

  // Handle page change
  const handlePageChange = (page) => {
    setCurrentPage(page);
    fetchUsers(page);
  };

  // Handle search
  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
    fetchUsers(1); // Fetch results for page 1 when search query changes
  };

  // Toggle the expand/collapse for a user
  const toggleExpand = (userId) => {
    setExpanded((prevExpanded) => ({
      ...prevExpanded,
      [userId]: !prevExpanded[userId]
    }));
  };

  useEffect(() => {
    fetchUsers(currentPage);  // Fetch users on page load
  }, [currentPage, fetchUsers]);  // Now using 'fetchUsers' as a dependency

  return (
    <div className="container mt-5">
      <h2>User Management</h2>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Search by name or email"
          value={searchQuery}
          onChange={handleSearchChange}
        />
      </div>
      <table className="table table-bordered table-striped">
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Check-in Date</th>
            <th>Check-out Date</th>
            <th>Status</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          {users.length > 0 ? users.map(user => (
            <tr key={user.email}>
              <td>{user.first_name}</td>
              <td>{user.last_name}</td>
              <td>{user.email}</td>
              <td>{user.checkin_date}</td>
              <td>{user.checkout_date}</td>
              <td>{user.is_active ? 'Active' : 'Inactive'}</td>
              <td>
                <button className="btn btn-info" onClick={() => toggleExpand(user.email)}>
                  {expanded[user.email] ? 'Hide Details' : 'Show Details'}
                </button>
                {expanded[user.email] && (
                  <div className="mt-3">
                    <strong>Booking ID:</strong> N/A <br />
                    <strong>Building ID:</strong> {user.building_id}<br />
                    <strong>Floor ID:</strong> {user.floor_id}<br />
                    <strong>Room ID:</strong> {user.room_id}
                  </div>
                )}
              </td>
            </tr>
          )) : <tr><td colSpan="7">No users found</td></tr>}
        </tbody>
      </table>

      {/* Pagination */}
      <nav>
        <ul className="pagination">
          {Array.from({ length: totalPages }).map((_, index) => (
            <li key={index} className={`page-item ${currentPage === index + 1 ? 'active' : ''}`}>
              <button className="page-link" onClick={() => handlePageChange(index + 1)}>
                {index + 1}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default UserListPage;
