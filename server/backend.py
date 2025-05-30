from flask import Flask, request, jsonify
from flask_cors import CORS
from djangoapp.models import CarModel, CarMake, CarDealer, DealerReview
from djangoapp.restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
import json


app = Flask(__name__)
CORS(app)


@app.route("/api/dealership", methods=["GET"])
def get_dealerships():
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c8c2e4c-5c8c-2e4c-5c8c-2e4c5c8c2e4c/dealership-package/get-dealership"
    dealerships = get_dealers_from_cf(url)
    return jsonify(dealerships)


@app.route("/api/review/<int:dealer_id>", methods=["GET"])
def get_dealer_reviews(dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c8c2e4c-5c8c-2e4c-5c8c-2e4c5c8c2e4c/dealership-package/get-review"
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    return jsonify(reviews)


@app.route("/api/review", methods=["POST"])
def add_review():
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400

    review = request.json
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c8c2e4c-5c8c-2e4c-5c8c-2e4c5c8c2e4c/dealership-package/post-review"
    response = post_request(url, review)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True) 