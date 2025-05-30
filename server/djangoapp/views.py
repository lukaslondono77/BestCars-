# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel, Dealer, CarDealerReview
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    logout(request) # Terminate user session
    data = {"userName":""} # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

def get_dealers(request):
    dealers = Dealer.objects.all()
    dealers_list = []
    for dealer in dealers:
        dealers_list.append({
            'id': dealer.id,
            'full_name': dealer.full_name,
            'city': dealer.city,
            'address': dealer.address,
            'zip': dealer.zip,
            'state': dealer.state
        })
    return JsonResponse({'status': 200, 'dealers': dealers_list})

def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        try:
            dealer = Dealer.objects.get(id=dealer_id)
            dealer_data = {
                'id': dealer.id,
                'full_name': dealer.full_name,
                'city': dealer.city,
                'address': dealer.address,
                'zip': dealer.zip,
                'state': dealer.state
            }
            return JsonResponse({"status": 200, "dealer": [dealer_data]})
        except Dealer.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Dealer not found"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            try:
                response = analyze_review_sentiments(review_detail['review'])
                if response and 'sentiment' in response:
                    review_detail['sentiment'] = response['sentiment']
                else:
                    review_detail['sentiment'] = 'neutral'
            except Exception as e:
                print(f"Error analyzing sentiment: {str(e)}")
                review_detail['sentiment'] = 'neutral'
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

@csrf_exempt
def add_review(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            dealer_id = data.get('dealership')
            dealer = Dealer.objects.get(id=dealer_id)
            
            # Handle empty car_year
            car_year = data.get('car_year')
            if car_year == '':
                car_year = None
            
            review = CarDealerReview(
                dealership=dealer,
                name=data.get('name'),
                purchase=data.get('purchase', False),
                review=data.get('review'),
                purchase_date=data.get('purchase_date'),
                car_make=data.get('car_make', ''),
                car_model=data.get('car_model', ''),
                car_year=car_year,
                sentiment='neutral'  # Will be updated by the sentiment analysis
            )
            review.save()
            
            # Analyze sentiment
            try:
                sentiment = analyze_review_sentiments(review.review)
                if sentiment and 'sentiment' in sentiment:
                    review.sentiment = sentiment['sentiment']
                    review.save()
            except Exception as e:
                print(f"Error analyzing sentiment: {str(e)}")
            
            return JsonResponse({"status": 200, "message": "Review added successfully"})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"status": 401, "message": "Error inserting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
