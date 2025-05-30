# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

load_dotenv()

backend_url = os.getenv(
    'BACKEND_URL', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'SENTIMENT_ANALYZER_URL',
    default="http://localhost:5050/")

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                              params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of a review text using the sentiment analyzer service
    """
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-sentiment"
    response = requests.post(url, json={"text": text})
    return response.json()

def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                               params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                 full_name=dealer_doc["full_name"],
                                 id=dealer_doc["id"], lat=dealer_doc["lat"],
                                 long=dealer_doc["long"],
                                 short_name=dealer_doc["short_name"],
                                 st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["rows"]
        # For each review object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["doc"]
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"],
                                    name=review_doc["name"],
                                    purchase=review_doc["purchase"],
                                    review=review_doc["review"],
                                    purchase_date=review_doc["purchase_date"],
                                    car_make=review_doc["car_make"],
                                    car_model=review_doc["car_model"],
                                    car_year=review_doc["car_year"],
                                    sentiment=analyze_review_sentiments(review_doc["review"]))
            results.append(review_obj)
    return results
