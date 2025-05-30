import os
import json
import requests
from dotenv import load_dotenv
from .models import CarDealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


load_dotenv()

backend_url = os.getenv(
    "BACKEND_URL",
    default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    "SENTIMENT_ANALYZER_URL",
    default="http://localhost:5050/"
)


def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    try:
        response = requests.get(
            url,
            headers={"Content-Type": "application/json"},
            params=kwargs
        )
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None

    print(f"With status {response.status_code}")
    return response.json()


def analyze_review_sentiments(text):
    url = (
        "https://api.us-south.natural-language-understanding."
        "watson.cloud.ibm.com/instances/"
        "4f4f4f4f-4f4f-4f1b-8f0d-8f0d8f0d8f0d"
    )
    api_key = "your-api-key"
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version="2021-08-01",
        authenticator=authenticator
    )
    nlu.set_service_url(url)
    response = nlu.analyze(
        text=text,
        features=Features(
            sentiment=SentimentOptions(targets=[text])
        )
    ).get_result()
    return response["sentiment"]["document"]["label"]


def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    try:
        resp = requests.post(request_url, json=data_dict)
        print(resp.json())
        return resp.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None


def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(f"POST to {url}")
    try:
        response = requests.post(
            url,
            params=kwargs,
            json=json_payload,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None

    print(f"With status {response.status_code}")
    return response.json()


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        for dealer in json_result.get("rows", []):
            doc = dealer.get("doc", {})
            results.append(
                CarDealer(
                    address=doc.get("address"),
                    city=doc.get("city"),
                    full_name=doc.get("full_name"),
                    id=doc.get("id"),
                    lat=doc.get("lat"),
                    long=doc.get("long"),
                    short_name=doc.get("short_name"),
                    st=doc.get("st"),
                    zip=doc.get("zip")
                )
            )
    return results


def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, dealerId=dealer_id)
    if json_result and json_result.get("rows"):
        doc = json_result["rows"][0].get("doc", {})
        return CarDealer(
            address=doc.get("address"),
            city=doc.get("city"),
            full_name=doc.get("full_name"),
            id=doc.get("id"),
            lat=doc.get("lat"),
            long=doc.get("long"),
            short_name=doc.get("short_name"),
            st=doc.get("st"),
            zip=doc.get("zip")
        )
    return None


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        docs = (
            json_result.get("body", {})
                       .get("data", {})
                       .get("docs", [])
        )
        for rev in docs:
            review = DealerReview(
                dealership=rev.get("dealership"),
                name=rev.get("name"),
                purchase=rev.get("purchase"),
                review=rev.get("review")
            )
            for attr in (
                "id",
                "purchase_date",
                "car_make",
                "car_model",
                "car_year"
            ):
                if attr in rev:
                    setattr(review, attr, rev[attr])

            review.sentiment = analyze_review_sentiments(review.review)
            print(review.sentiment)
            results.append(review)
    return results
