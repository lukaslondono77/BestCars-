import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [postReview, setPostReview] = useState(null);

  const { id } = useParams();

  const getDealer = useCallback(async () => {
    try {
      const response = await fetch(`/djangoapp/dealer/${id}`);
      const data = await response.json();
      if (data.status === 200 && data.dealer && data.dealer.length > 0) {
        setDealer(data.dealer[0]);
      } else {
        setError("Dealer not found");
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
      }
    } catch (error) {
      setError("Error fetching reviews");
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    getDealer();
    getReviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={`/postreview/${id}`}>
          <img src={review_icon} className="review-button" alt="Post Review"/>
        </a>
      );
    }
  }, [id, getDealer, getReviews]);

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return positive_icon;
      case 'negative':
        return negative_icon;
      default:
        return neutral_icon;
    }
  };

  if (error) {
    return (
      <div className="container">
        <Header />
        <div className="error-message">{error}</div>
      </div>
    );
  }

  if (loading || !dealer) {
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
      <div className="dealer-info">
        <h2>{dealer.full_name} {postReview}</h2>
        <p>{dealer.city}, {dealer.address}, {dealer.zip}, {dealer.state}</p>
      </div>
      
      <div className="reviews-section">
        <h3>Reviews</h3>
        {loading ? (
          <div>Loading reviews...</div>
        ) : reviews.length > 0 ? (
          <div className="reviews-list">
            {reviews.map((review, index) => (
              <div key={index} className="review-card">
                <div className="review-header">
                  <img 
                    src={getSentimentIcon(review.sentiment)} 
                    alt={review.sentiment} 
                    className="sentiment-icon"
                  />
                  <h4>{review.name}</h4>
                </div>
                <div className="review-content">
                  <p>{review.review}</p>
                  {review.car_make && (
                    <p className="car-info">
                      {review.car_make} {review.car_model} {review.car_year}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div>No reviews yet</div>
        )}
      </div>
    </div>
  );
};

export default Dealer; 