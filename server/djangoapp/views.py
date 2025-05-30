# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import restapis


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                          password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-review"
        # Get reviews from the URL
        reviews = restapis.get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        review_text = ' '.join([review.review for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(review_text)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/post-review"
        # Get reviews from the URL
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": request.POST['name'],
            "dealership": dealer_id,
            "review": request.POST['content'],
            "purchase": request.POST.get('purchasecheck') == 'on',
            "purchase_date": request.POST['purchasedate'],
            "car_make": request.POST['carmake'],
            "car_model": request.POST['carmodel'],
            "car_year": request.POST['caryear']
        }
        json_payload = {"review": review}
        # Call the post_review method
        response = restapis.post_review(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
