import React, { useState, useEffect } from 'react';
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

  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    if (!sessionStorage.getItem("username")) {
      navigate("/login");
    }
    getDealer();
  }, [id]);

  const getDealer = async () => {
    const response = await fetch(`/djangoapp/dealer/${id}`);
    const data = await response.json();
    if (data.status === 200) {
      setDealer(data.dealer[0]);
    }
  };

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

      if (response.ok) {
        setSubmitted(true);
        setTimeout(() => {
          navigate(`/dealer/${id}`);
        }, 2000);
      } else {
        setError("Failed to submit review. Please try again.");
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

  if (submitted) {
    return (
      <div className="container mt-5">
        <div className="alert alert-success">
          Review submitted successfully! Redirecting...
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <Header />
      <h2 className="mb-4">Add Review for {dealer.full_name}</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit} className="review-form">
        <div className="form-group mb-3">
          <label htmlFor="name">Your Name *</label>
          <input
            type="text"
            className="form-control"
            id="name"
            name="name"
            value={review.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group mb-3">
          <div className="form-check">
            <input
              type="checkbox"
              className="form-check-input"
              id="purchase"
              name="purchase"
              checked={review.purchase}
              onChange={handleChange}
            />
            <label className="form-check-label" htmlFor="purchase">
              Did you purchase a car from this dealership?
            </label>
          </div>
        </div>

        {review.purchase && (
          <>
            <div className="form-group mb-3">
              <label htmlFor="car_make">Car Make</label>
              <input
                type="text"
                className="form-control"
                id="car_make"
                name="car_make"
                value={review.car_make}
                onChange={handleChange}
              />
            </div>

            <div className="form-group mb-3">
              <label htmlFor="car_model">Car Model</label>
              <input
                type="text"
                className="form-control"
                id="car_model"
                name="car_model"
                value={review.car_model}
                onChange={handleChange}
              />
            </div>

            <div className="form-group mb-3">
              <label htmlFor="car_year">Car Year</label>
              <input
                type="text"
                className="form-control"
                id="car_year"
                name="car_year"
                value={review.car_year}
                onChange={handleChange}
              />
            </div>

            <div className="form-group mb-3">
              <label htmlFor="purchase_date">Purchase Date</label>
              <input
                type="date"
                className="form-control"
                id="purchase_date"
                name="purchase_date"
                value={review.purchase_date}
                onChange={handleChange}
              />
            </div>
          </>
        )}

        <div className="form-group mb-3">
          <label htmlFor="review">Your Review *</label>
          <textarea
            className="form-control"
            id="review"
            name="review"
            rows="4"
            value={review.review}
            onChange={handleChange}
            required
          ></textarea>
        </div>

        <button type="submit" className="btn btn-primary">Submit Review</button>
      </form>
    </div>
  );
};

export default PostReview;
