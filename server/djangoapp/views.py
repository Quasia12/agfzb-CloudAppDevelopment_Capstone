from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview, ReviewPost
from .restapis import get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)


def get_dealerships(request):
    context = {}
    url = "https://jahsha.us-south.cf.appdomain.cloud/api/dealerships"
    dealerships = get_dealers_from_cf(url)  
    context["dealership_list"] = dealerships
    if request.method == "GET":
        return render(request, 'djangoapp/dealer_details.html', context)


def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, "Login successfully!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")


def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `get_dealer_details` view to render the reviews of a dealer


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealer_url = "https://jahsha.us-south.cf.appdomain.cloud/api/dealerships"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer

    review_url = "https://jahsha.us-south.cf.appdomain.cloud/api/review"
    reviews = get_dealer_reviews_from_cf(review_url, id=id)
    print(reviews)
    context["reviews"] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review


def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/sbarksdale.bridgespointeinc.nc%40gmail.com_djangoserver-SCB/actions/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer

        review_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/sbarksdale.bridgespointeinc.nc%40gmail.com_djangoserver-SCB/actions/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['lastname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{}is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(
                username == username, first_name=first_name, last_name=last_name, password=password,)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)
