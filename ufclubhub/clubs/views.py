from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from .models import Users, Club, Permissions, Login, Member, Events, ClubLogin, Announcements
import json

def sign_up(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)

    name = data.get("name")
    email = data.get("email")
    raw_password = data.get("password")
    password = make_password(raw_password)

    if not email:
        return JsonResponse({"error": "Email required"}, status=400)

    # Validate UF email
    if not email.endswith("@ufl.edu"):
        return JsonResponse({"error": "Unauthorized email address"}, status=400)

    # Check duplicates
    if Users.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already associated with an account"}, status=400)

    # You MUST generate or collect UFID — currently missing in your view
    ufid = data.get("ufid")
    if not ufid:
        return JsonResponse({"error": "UFID is required"}, status=400)

    # Default permissions (nullable foreign key)
    default_permissions = Permissions.objects.filter(level='user').first()

    # Create the user using refactored class method
    Users.add_user(
        email=email,
        name=name,
        ufid=ufid,
        permissions=default_permissions
    )

    Login.objects.create(
        user=ufid,
        password=password
    )

    return JsonResponse({"success": "Account successfully created!"}, status=200)




def log_in(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=400)

    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    name_or_email = data.get("email")  # could be email or club username
    password = data.get("password")
    if not name_or_email or not password:
        return JsonResponse({"error": "Email/username and password are required"}, status=400)

    # -------------------- Try standard user login --------------------
    try:
        user = Users.objects.get(email=name_or_email)
        login_record = Login.objects.get(user=user)
        if check_password(password, login_record.password):
            return JsonResponse({
                "type": "user",
                "ufid": user.ufid,
                "name": user.name,
                "email": user.email,
                "message": "User login successful"
            }, status=200)
        else:
            return JsonResponse({"error": "Invalid password"}, status=400)
    except Users.DoesNotExist:
        pass  # Continue to try club login
    except Login.DoesNotExist:
        return JsonResponse({"error": "Login record not found"}, status=400)

    # -------------------- Try club login --------------------
    try:
        club_login = ClubLogin.objects.get(club_name=name_or_email)
        if club_login.password != password:  # assuming plaintext; if hashed, use check_password
            return JsonResponse({"error": "Invalid password"}, status=400)

        club = club_login.club
        return JsonResponse({
            "type": "club",
            "club_name": club.name,
            "category": club.category,
            "permission_level": club_login.permission.permission_level,
            "message": "Club login successful"
        }, status=200)

    except ClubLogin.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=400)

def search_clubs(request): #when you type a club name in the search bar
    query = request.GET.get("q", "") #retrieve the search keyword typed in the search bar
    print("Search query recieved:", query)  # Debugging statement to check the received query
    # also adds the new entry in the search as the query instead of the default search keyword
    if query: #if the search bar content isn't empty
        club = Club.objects.filter(club_name__icontains=query) #look for the club name that matches the entry
    else: #if empty
        club = Club.objects.all() #display all the club names in alphabetical order

    print("Clubs returned:", club)  # Debugging statement to check the retrieved clubs

    results = list(club.values("club_name","category")) #convert the list of club Model objects into a dictionary list
    return JsonResponse(results, safe=False)

#returns the list of clubs for a single member
def display_user_clubs(request):
    # get logged-in user’s Member object
    clubs = Member.retrieve_user_clubs(request.user)

    data = [{"name": c.name} for c in clubs]

    return JsonResponse({"clubs": data})


def display_user_events(request):
    user = request.user

    clubs = Member.retrieve_user_clubs(user)

    if not clubs:
        return JsonResponse({"events": []})

    events = Events.retrieve_events_for_clubs(clubs)

    events_list = []
    for event in events:
        events_list.append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_datetime": event.event_datetime.isoformat(),
            "club": event.club.name,
        })

    return JsonResponse({"events": events_list})


def post_announcement(request):
    club_login = ClubLogin.objects.filter(username=request.user.username).first()
    if not club_login:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    club = club_login.club
    required = club.permissions.permission_level
    actual = club_login.permission.permission_level
    if actual != required:
        return JsonResponse({"error": "Insufficient permissions"}, status=403)

    body = json.loads(request.body.decode()) if request.body else {}
    title = body.get("title") or request.POST.get("title")
    content = body.get("content") or request.POST.get("content")

    if not title or not content:
        return JsonResponse({"error": "Title and content are required"}, status=400)

    announcement = Announcements.add_announcement(
        title=title,
        content=content,
        posted_at=timezone.now().time(),
        club=club
    )

    return JsonResponse({
        "success": True,
        "announcement_id": announcement.id,
        "club": club.club_name,
        "title": title
    })

def create_event(request):
    club_login = ClubLogin.objects.filter(username=request.user.username).first()
    if not club_login:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    club = club_login.club
    required = club.permissions.permission_level
    actual = club_login.permission.permission_level
    if actual != required:
        return JsonResponse({"error": "Insufficient permissions"}, status=403)

    title = request.POST.get("title")
    description = request.POST.get("description")
    datetime_str = request.POST.get("datetime")
    if not title or not description or not datetime_str:
        return JsonResponse({"error": "Title, description, and event date/time are required"}, status=400)

    try:
        from datetime import datetime
        event_datetime = datetime.fromisoformat(datetime_str)
    except ValueError:
        return JsonResponse({"error": "Invalid date/time format"}, status=400)

    event = Events.add_event(
        title=title,
        description=description,
        event_datetime=event_datetime,
        club=club
    )

    return JsonResponse({
        "success": True,
        "event_id": event.id,
        "title": event.title,
        "club": club.club_name,
        "datetime": event.event_datetime.isformat()
    })


def test_connection(request):
    return JsonResponse({"status": "Backend is connected!"})
