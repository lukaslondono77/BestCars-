import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png"
import neutral_icon from "../assets/neutral.png"
import negative_icon from "../assets/negative.png"
import review_icon from "../assets/reviewbutton.png"
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { id } = useParams();
  const navigate = useNavigate();
  const isLoggedIn = sessionStorage.getItem("username") != null;

  const getDealer = useCallback(async () => {
    try {
      const response = await fetch(`/djangoapp/dealer/${id}`);
      const data = await response.json();
      
      if (data.status === 200) {
        setDealer(data.dealer[0]);
      } else {
        setError("Failed to fetch dealer information");
      }
    } catch (error) {
      setError("Error fetching dealer information");
      console.error("Error:", error);
    }
  }, [id]);

  const getReviews = useCallback(async () => {
    try {
      const response = await fetch(`/djangoapp/reviews/dealer/${id}`);
      const data = await response.json();
      
      if (data.status === 200) {
        setReviews(data.reviews || []);
      } else {
        setError("Failed to fetch reviews");
      }
    } catch (error) {
      setError("Error fetching reviews");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    const fetchData = async () => {
      await Promise.all([getDealer(), getReviews()]);
    };
    fetchData();
  }, [getDealer, getReviews]);

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return positive_icon;
      case "negative":
        return negative_icon;
      default:
        return neutral_icon;
    }
  };

  const handlePostReview = (e) => {
    e.preventDefault();
    navigate(`/postreview/${id}`);
  };

  return (
    <div className="container">
      <Header />
      <div className="dealer-container">
        {error && <div className="alert alert-danger">{error}</div>}
        
        <div className="dealer-header">
          <h1 className="dealer-name">{dealer.full_name}</h1>
          {isLoggedIn && (
            <button 
              onClick={handlePostReview}
              className="post-review-button"
              title="Post a Review"
            >
              <img src={review_icon} alt="Post Review" className="review-icon" />
              Post Review
            </button>
          )}
        </div>

        <div className="dealer-info">
          <p className="dealer-address">
            {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
          </p>
        </div>

        <div className="reviews-section">
          <h2 className="reviews-title">Customer Reviews</h2>
          
          {loading ? (
            <div className="loading">Loading reviews...</div>
          ) : reviews.length === 0 ? (
            <div className="no-reviews">No reviews yet!</div>
          ) : (
            <div className="reviews-grid">
              {reviews.map((review, index) => (
                <div key={index} className="review-card">
                  <div className="review-header">
                    <img 
                      src={getSentimentIcon(review.sentiment)} 
                      className="sentiment-icon" 
                      alt={`${review.sentiment} sentiment`}
                    />
                    <h3 className="reviewer-name">{review.name}</h3>
                  </div>
                  
                  <div className="review-content">
                    <p className="review-text">{review.review}</p>
                    <div className="car-info">
                      {review.car_make} {review.car_model} ({review.car_year})
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dealer
