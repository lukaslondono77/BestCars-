from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import logging
from djangoapp import restapis

logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'djangoapp/about.html')


def contact(request):
    return render(request, 'djangoapp/contact.html')


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return render(request, 'djangoapp/index.html')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except Exception:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    if request.method == "GET":
        url = (
            "https://us-south.functions.appdomain.cloud/api/v1/web/"
            "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-dealership"
        )
        dealerships = restapis.get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return JsonResponse({"status": 200, "dealers": dealer_names})


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = (
            "https://us-south.functions.appdomain.cloud/api/v1/web/"
            "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/get-review"
        )
        reviews = restapis.get_dealer_reviews_from_cf(url, id=dealer_id)
        review_texts = ' '.join([review.review for review in reviews])
        return JsonResponse({"status": 200, "reviews": review_texts})


def add_review(request, dealer_id):
    if request.method == "POST":
        url = (
            "https://us-south.functions.appdomain.cloud/api/v1/web/"
            "5c1c631c-5e4d-4f1b-8f0d-8f0d8f0d8f0d/dealership-package/post-review"
        )
        review = {
            "id": request.POST['id'],
            "name": request.POST['name'],
            "dealership": dealer_id,
            "review": request.POST['review'],
            "purchase": request.POST['purchase'],
            "purchase_date": request.POST['purchase_date'],
            "car_make": request.POST['car_make'],
            "car_model": request.POST['car_model'],
            "car_year": request.POST['car_year']
        }
        json_payload = {"review": review}
        restapis.post_review(url, json_payload)
        return JsonResponse({"status": 200})
