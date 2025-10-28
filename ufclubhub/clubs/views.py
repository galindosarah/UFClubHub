from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .models import Account, Club
import json

def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body) #stores the input of the user
        name = data.get("name")# class each variable from the input in its category
        email = data.get("email")
        password = make_password(data.get("password"))
        # grad_year = data.get("grad_year")
        #checks if the address e-mail is already registered
        if not email.endswith("@ufl.edu"):
            return JsonResponse({"Unauthorized address"}, status = 400)
        if Account.objects.filter(email=email).exists():
            return JsonResponse({"E-mail already associated with an account"}, status = 400)
        #create an Account object in the database
        account_obj = Account.objects.create(
            username = name,
            email = email,
            # grad_year = grad_year,
            passowrd = password,
        )
        return JsonResponse({"Account successfully created!!!!"}, status = 200)
    return JsonResponse({"Invalid request"}, status = 400)



def log_in(request):
    # every action like log in, sign up have a POST request
    if request.method == 'POST':
        #save the input from the user
        data = json.loads(request.body)
        # separate the data into categories
        email = data.get("email")
        password = data.get("password")
        #if the input is not an e-mail address or a password
        if not email or not password:
            return JsonResponse({"Invalid input"}, status = 400)
        # check if the e-mail is already in the database
        try:
            account = Account.objects.get(email=email)
        except:
            return JsonResponse({"Account not found"}, status = 400)
        #check if the password is the right one associated to the account
        if not check_password(password,account.password):
            return JsonResponse({"Invalid password"}, status = 400)
        return JsonResponse({
            "name": account.username,
            "email": account.email,
            "message": "Login successful",
        }, status=200)
    return JsonResponse({"Invalid request"}, status = 400)

def search_clubs(request): #when you type a club name in the search bar
    query = request.GET.get("q", "") #retrieve the search keyword typed in the search bar
    # also adds the new entry in the search as the query instead of the default search keyword
    if query: #if the search bar content isn't empty
        club = Club.objects.filter(name__icontains=query) #look for the club name that matches the entry
    else: #if empty
        club = Club.objects.all() #display all the club names in alphabetical order

    results = list(club.values("name","bio", "year", "members")) #convert the list of club Model objects into a dictionary list
    return JsonResponse(results, safe=False) #return the result