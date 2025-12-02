from django.test import TestCase, Client
from django.utils import timezone
from .models import Users, Club, Permissions, Login, Member, Events, ClubLogin, Announcements
import json


class AppTests(TestCase):

    def setUp(self):
        # Create permissions
        self.user_permission = Permissions.objects.create(permission_level=1, description="user")
        self.club_permission = Permissions.objects.create(permission_level=2, description="club")

        # Create a standard user
        self.user = Users.add_user(
            username="Alice",
            email="alice@ufl.edu",
            ufid="U12345678",
            permissions=self.user_permission
        )
        Login.objects.create(user=self.user, password="hashed_password")

        # Create a club
        self.club = Club.add_club(
            name="Chess Club",
            category="Games",
            permissions=self.club_permission
        )

        # Create club login
        self.club_login = ClubLogin.objects.create(
            club=self.club,
            username="chessclub",
            password="clubpassword",
            permission=self.club_permission
        )

        # Add member
        Member.add_member(
            user=self.user,
            club_name=self.club,
            date_joined=timezone.now().date(),
            permissions_level=1
        )

        # Django test client
        self.client = Client()

    # -------------------- Sign-up tests --------------------
    def test_sign_up_success(self):
        data = {
            "name": "Bob",
            "email": "bob@ufl.edu",
            "ufid": "U87654321",
            "password": "testpass123"
        }
        response = self.client.post("/sign_up/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Users.objects.filter(email="bob@ufl.edu").exists())

    def test_sign_up_invalid_email(self):
        data = {"name": "Bob", "email": "bob@gmail.com", "ufid": "U87654321", "password": "pass"}
        response = self.client.post("/sign_up/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    # -------------------- Login tests --------------------
    def test_user_login_success(self):
        data = {"email": "alice@ufl.edu", "password": "hashed_password"}
        response = self.client.post("/log_in/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Login successful")

    def test_user_login_invalid(self):
        data = {"email": "wrong@ufl.edu", "password": "pass"}
        response = self.client.post("/log_in/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_club_login_redirect(self):
        # Use club username for login
        data = {"email": "chessclub", "password": "clubpassword"}
        # Simulate your login function checking for club login
        response = self.client.post("/log_in/", data=json.dumps(data), content_type="application/json")
        # This should detect a club account and respond differently
        self.assertEqual(response.status_code, 200)
        # Example check: JSON includes 'club' key
        # (You may need to modify your login view to include this)
        # self.assertIn("club", response.json())

    # -------------------- Club search --------------------
    def test_search_clubs(self):
        response = self.client.get("/search_clubs/?q=Chess")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Chess Club", [c["name"] for c in response.json()])

    # -------------------- Display user clubs --------------------
    def test_display_user_clubs(self):
        self.client.force_login(self.user)
        response = self.client.get("/display_user_clubs/")
        self.assertEqual(response.status_code, 200)
        clubs = response.json()["clubs"]
        self.assertEqual(len(clubs), 1)
        self.assertEqual(clubs[0]["name"], "Chess Club")

    # -------------------- Display user events --------------------
    def test_display_user_events(self):
        # Add an event for the club
        Events.add_event(
            title="Chess Tournament",
            description="Annual tournament",
            event_datetime=timezone.now(),
            club=self.club
        )
        self.client.force_login(self.user)
        response = self.client.get("/display_user_events/")
        self.assertEqual(response.status_code, 200)
        events = response.json()["events"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Chess Tournament")

    # -------------------- Post announcement --------------------
    def test_post_announcement_club(self):
        self.client.force_login(self.club_login)
        data = {"title": "Meeting", "content": "Next week"}
        response = self.client.post("/post_announcement/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Announcements.objects.filter(club=self.club, title="Meeting").exists())

    def test_post_announcement_user_forbidden(self):
        self.client.force_login(self.user)
        data = {"title": "Hack", "content": "Test"}
        response = self.client.post("/post_announcement/", data)
        self.assertEqual(response.status_code, 403)

    # -------------------- Create event --------------------
    def test_create_event_club(self):
        self.client.force_login(self.club_login)
        data = {
            "title": "Chess Meetup",
            "description": "Monthly meetup",
            "datetime": timezone.now().isoformat()
        }
        response = self.client.post("/create_event/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Events.objects.filter(club=self.club, title="Chess Meetup").exists())

    def test_create_event_user_forbidden(self):
        self.client.force_login(self.user)
        data = {"title": "Event", "description": "Test", "datetime": timezone.now().isoformat()}
        response = self.client.post("/create_event/", data)
        self.assertEqual(response.status_code, 403)
from django.test import TestCase

# Create your tests here.
