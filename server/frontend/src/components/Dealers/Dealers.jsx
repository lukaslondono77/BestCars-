import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedState, setSelectedState] = useState("");
  const navigate = useNavigate();

  const dealer_url = "/djangoapp/get_dealers";
  const dealer_url_by_state = "/djangoapp/get_dealers/";

  const filterDealers = useCallback(async (state) => {
    setLoading(true);
    setError("");
    try {
      const url = state === "All" ? dealer_url : `${dealer_url_by_state}${state}`;
      const res = await fetch(url, {
        method: "GET"
      });
      const retobj = await res.json();
      if (retobj.status === 200) {
        const state_dealers = Array.from(retobj.dealers);
        setDealersList(state_dealers);
      } else {
        setError("Failed to fetch dealers");
      }
    } catch (error) {
      setError("Error fetching dealers");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const getDealers = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(dealer_url, {
        method: "GET"
      });
      const retobj = await res.json();
      if (retobj.status === 200) {
        const all_dealers = Array.from(retobj.dealers);
        const uniqueStates = Array.from(new Set(all_dealers.map(dealer => dealer.state)));
        setStates(uniqueStates);
        setDealersList(all_dealers);
      } else {
        setError("Failed to fetch dealers");
      }
    } catch (error) {
      setError("Error fetching dealers");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    getDealers();
  }, [getDealers]);

  const isLoggedIn = sessionStorage.getItem("username") != null;

  const handleStateChange = (e) => {
    const state = e.target.value;
    setSelectedState(state);
    filterDealers(state);
  };

  const handleDealerClick = (dealerId) => {
    navigate(`/dealer/${dealerId}`);
  };

  const handleReviewClick = (e, dealerId) => {
    e.preventDefault();
    navigate(`/postreview/${dealerId}`);
  };

  return (
    <div className="container">
      <Header />
      <div className="dealers-container">
        <h2 className="dealers-title">Dealerships</h2>
        
        <div className="filter-section">
          <select 
            name="state" 
            id="state" 
            value={selectedState}
            onChange={handleStateChange}
            className="state-select"
          >
            <option value="" disabled>Select State</option>
            <option value="All">All States</option>
            {states.map(state => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        {loading ? (
          <div className="loading">Loading dealers...</div>
        ) : dealersList.length > 0 ? (
          <div className="table-responsive">
            <table className="table dealers-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Dealer Name</th>
                  <th>City</th>
                  <th>Address</th>
                  <th>Zip</th>
                  <th>State</th>
                  {isLoggedIn && <th>Review</th>}
                </tr>
              </thead>
              <tbody>
                {dealersList.map(dealer => (
                  <tr key={dealer.id}>
                    <td>{dealer.id}</td>
                    <td>
                      <a 
                        href={`/dealer/${dealer.id}`}
                        onClick={(e) => {
                          e.preventDefault();
                          handleDealerClick(dealer.id);
                        }}
                        className="dealer-link"
                      >
                        {dealer.full_name}
                      </a>
                    </td>
                    <td>{dealer.city}</td>
                    <td>{dealer.address}</td>
                    <td>{dealer.zip}</td>
                    <td>{dealer.state}</td>
                    {isLoggedIn && (
                      <td>
                        <a 
                          href={`/postreview/${dealer.id}`}
                          onClick={(e) => handleReviewClick(e, dealer.id)}
                          className="review-link"
                        >
                          <img 
                            src={review_icon} 
                            className="review-icon" 
                            alt="Post Review"
                            title="Post a Review"
                          />
                        </a>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-dealers">No dealers found</div>
        )}
      </div>
    </div>
  );
};

export default Dealers
