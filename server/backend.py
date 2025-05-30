from flask import Flask, request, jsonify
from flask_cors import CORS
from . import restapis

app = Flask(__name__)
CORS(app)

@app.route('/api/dealership', methods=['GET'])
def get_dealerships():
    url = ("https://us-south.functions.appdomain.cloud/api/v1/web/"
           "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-dealership")
    dealerships = restapis.get_dealers_from_cf(url)
    return jsonify([dealer.to_dict() for dealer in dealerships])

@app.route('/api/dealership/<int:dealer_id>', methods=['GET'])
def get_dealership(dealer_id):
    url = ("https://us-south.functions.appdomain.cloud/api/v1/web/"
           "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-dealership")
    dealerships = restapis.get_dealers_from_cf(url, dealerId=dealer_id)
    return jsonify([dealer.to_dict() for dealer in dealerships])

@app.route('/api/review', methods=['GET'])
def get_reviews():
    url = ("https://us-south.functions.appdomain.cloud/api/v1/web/"
           "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-review")
    reviews = restapis.get_dealer_reviews_from_cf(url)
    return jsonify([review.to_dict() for review in reviews])

@app.route('/api/review/<int:dealer_id>', methods=['GET'])
def get_dealer_reviews(dealer_id):
    url = ("https://us-south.functions.appdomain.cloud/api/v1/web/"
           "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-review")
    reviews = restapis.get_dealer_reviews_from_cf(url, dealer_id)
    return jsonify([review.to_dict() for review in reviews])

@app.route('/api/review', methods=['POST'])
def add_review():
    url = ("https://us-south.functions.appdomain.cloud/api/v1/web/"
           "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/post-review")
    review = request.json
    response = restapis.post_review(url, review)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 