import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [review, setReview] = useState({
    name: "",
    purchase: false,
    car_make: "",
    car_model: "",
    car_year: "",
    review: "",
    purchase_date: ""
  });
  const [dealer, setDealer] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();
  const { id } = useParams();

  const getDealer = useCallback(async () => {
    try {
      const response = await fetch(`/djangoapp/dealer/${id}`);
      const data = await response.json();
      if (data.status === 200) {
        setDealer(data.dealer[0]);
      }
    } catch (error) {
      setError("Error fetching dealer information");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  const checkAuthAndFetchDealer = useCallback(() => {
    if (!sessionStorage.getItem("username")) {
      navigate("/login");
    } else {
      getDealer();
    }
  }, [navigate, getDealer]);

  useEffect(() => {
    checkAuthAndFetchDealer();
  }, [checkAuthAndFetchDealer]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!review.name || !review.review) {
      setError("Please fill in all required fields");
      return;
    }

    const reviewData = {
      ...review,
      dealership: id,
      purchase_date: review.purchase_date || new Date().toISOString().split('T')[0]
    };

    try {
      const response = await fetch('/djangoapp/add_review', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reviewData),
      });

      const data = await response.json();
      if (data.status === 200) {
        setSubmitted(true);
        setTimeout(() => {
          navigate(`/dealer/${id}`);
        }, 2000);
      } else {
        setError(data.message || "Failed to submit review. Please try again.");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setReview(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  if (loading) {
    return (
      <div className="container">
        <Header />
        <div className="loading">Loading dealer information...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <Header />
      <div className="review-page">
        <h2 className="review-title">Post a Review for {dealer.full_name}</h2>
        {submitted ? (
          <div className="alert alert-success success-message">
            <h3>Review submitted successfully!</h3>
            <p>Redirecting you back to the dealer page...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="review-form">
            {error && <div className="alert alert-danger">{error}</div>}
            
            <div className="form-section">
              <h3>Personal Information</h3>
              <div className="form-group">
                <label>Your Name:</label>
                <input
                  type="text"
                  name="name"
                  value={review.name}
                  onChange={handleChange}
                  className="form-control"
                  placeholder="Enter your name"
                  required
                />
              </div>
            </div>

            <div className="form-section">
              <h3>Car Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Car Make:</label>
                  <input
                    type="text"
                    name="car_make"
                    value={review.car_make}
                    onChange={handleChange}
                    className="form-control"
                    placeholder="e.g., Toyota"
                  />
                </div>

                <div className="form-group">
                  <label>Car Model:</label>
                  <input
                    type="text"
                    name="car_model"
                    value={review.car_model}
                    onChange={handleChange}
                    className="form-control"
                    placeholder="e.g., Camry"
                  />
                </div>

                <div className="form-group">
                  <label>Car Year:</label>
                  <input
                    type="number"
                    name="car_year"
                    value={review.car_year}
                    onChange={handleChange}
                    className="form-control"
                    min="1900"
                    max={new Date().getFullYear()}
                    placeholder="e.g., 2023"
                  />
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3>Purchase Information</h3>
              <div className="form-group">
                <label>Purchase Date:</label>
                <input
                  type="date"
                  name="purchase_date"
                  value={review.purchase_date}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>

              <div className="form-group checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="purchase"
                    checked={review.purchase}
                    onChange={handleChange}
                  />
                  I purchased a car from this dealership
                </label>
              </div>
            </div>

            <div className="form-section">
              <h3>Your Review</h3>
              <div className="form-group">
                <label>Review:</label>
                <textarea
                  name="review"
                  value={review.review}
                  onChange={handleChange}
                  className="form-control"
                  rows="4"
                  placeholder="Share your experience with this dealership..."
                  required
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary submit-button">
                Submit Review
              </button>
              <button 
                type="button" 
                className="btn btn-secondary cancel-button"
                onClick={() => navigate(`/dealer/${id}`)}
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default PostReview; 