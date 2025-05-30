import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const navigate = useNavigate();

  const getDealers = useCallback(async () => {
    try {
      const response = await fetch('/djangoapp/get_dealers');
      const data = await response.json();
      if (data.status === 200) {
        const allDealers = Array.from(data.dealers);
        const uniqueStates = [...new Set(allDealers.map(dealer => dealer.state))];
        setStates(uniqueStates);
        setDealersList(allDealers);
      }
    } catch (error) {
      console.error("Error fetching dealers:", error);
    }
  }, []);

  const filterDealers = useCallback(async (state) => {
    try {
      const response = await fetch(`/djangoapp/get_dealers/${state}`);
      const data = await response.json();
      if (data.status === 200) {
        setDealersList(Array.from(data.dealers));
      }
    } catch (error) {
      console.error("Error filtering dealers:", error);
    }
  }, []);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    getDealers();
  }, [getDealers]);

  const isLoggedIn = sessionStorage.getItem("username") != null;

  return (
    <div className="container">
      <Header />
      <h2>Dealers</h2>
      {dealersList.length > 0 ? (
        <div className="dealers-table">
          <div className="filter-section">
            <select 
              onChange={(e) => filterDealers(e.target.value)}
              className="form-control"
            >
              <option value="">Select State</option>
              <option value="All">All States</option>
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Dealer Name</th>
                <th>City</th>
                <th>Address</th>
                <th>Zip</th>
                <th>State</th>
                {isLoggedIn && <th>Review Dealer</th>}
              </tr>
            </thead>
            <tbody>
              {dealersList.map(dealer => (
                <tr key={dealer.id}>
                  <td>{dealer.id}</td>
                  <td>
                    <a href={`/dealer/${dealer.id}`} className="dealer-link">
                      {dealer.full_name}
                    </a>
                  </td>
                  <td>{dealer.city}</td>
                  <td>{dealer.address}</td>
                  <td>{dealer.zip}</td>
                  <td>{dealer.state}</td>
                  {isLoggedIn && (
                    <td>
                      <a href={`/postreview/${dealer.id}`}>
                        <img src={review_icon} className="review-icon" alt="Post Review"/>
                      </a>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div>Loading dealers...</div>
      )}
    </div>
  );
};

export default Dealers; 