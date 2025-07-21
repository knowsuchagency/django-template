from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from django_redis import get_redis_connection

from core.models import StockTicker

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",  # Required for custom User model
        )

    def tearDown(self):
        # Only flush Redis if it's configured and available
        if "redis" in settings.CACHES and settings.CACHES["redis"]["LOCATION"] != "redis://localhost:6379":
            try:
                get_redis_connection("redis").flushall()
            except:
                pass

    def test_root_redirect(self):
        """Test that root redirects to app"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/app/", fetch_redirect_response=False)

    def test_app_page(self):
        """Test that app page is accessible"""
        response = self.client.get("/app/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",  # Required for custom User model
        )
        # Delete any existing stock data
        StockTicker.objects.all().delete()

        # Create some test stock data
        StockTicker.objects.create(
            symbol="AAPL",
            company_name="Apple Inc.",
            price=150.00,
            change=2.15,
            percent_change=1.18,
            volume=45750000,
            market_cap=2950000000000,
            date=date.today(),
        )
        StockTicker.objects.create(
            symbol="GOOGL",
            company_name="Alphabet Inc.",
            price=2500.00,
            change=-3.25,
            percent_change=-0.78,
            volume=28300000,
            market_cap=3120000000000,
            date=date.today(),
        )

    def tearDown(self):
        # Only flush Redis if it's configured and available
        if "redis" in settings.CACHES and settings.CACHES["redis"]["LOCATION"] != "redis://localhost:6379":
            try:
                get_redis_connection("redis").flushall()
            except:
                pass

    def test_csrf_token_endpoint(self):
        """Test CSRF token endpoint"""
        response = self.client.get("/api/v1/csrf-token")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_add_endpoint(self):
        """Test add numbers endpoint"""
        response = self.client.post("/api/v1/example/add?a=5&b=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], 8)

    def test_greet_endpoint_authenticated(self):
        """Test greet endpoint with authentication"""
        # Login required
        self.client.login(username="testuser", password="testpass123")

        # Test default greeting
        response = self.client.post("/api/v1/example/greet")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello, world!")

        # Test custom greeting
        response = self.client.post("/api/v1/example/greet?name=Alice")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello, Alice!")

    def test_stocks_endpoint(self):
        """Test stocks endpoint"""
        self.client.login(username="testuser", password="testpass123")

        # Test getting all stocks
        response = self.client.get("/api/v1/example/stocks")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

        # Test getting specific stock
        response = self.client.get("/api/v1/example/stocks?symbol=AAPL")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["symbol"], "AAPL")

    def test_sentry_debug_endpoint(self):
        """Test sentry debug endpoint raises exception"""
        self.client.login(username="testuser", password="testpass123")
        # The test client re-raises exceptions in DEBUG mode, so we expect the exception
        with self.assertRaisesMessage(Exception, "This is a test exception for Sentry"):
            self.client.get("/api/v1/sentry-debug")
