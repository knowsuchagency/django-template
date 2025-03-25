from django.test import TestCase, override_settings, Client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.urls import path
from django.contrib.auth import get_user_model
from datetime import date
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
        get_redis_connection("default").flushall()

    def test_landing_page(self):
        """Test that landing page is accessible"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing.html")

    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        # Test without login
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Test with login
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")


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
        get_redis_connection("default").flushall()

    def test_csrf_token_endpoint(self):
        """Test CSRF token endpoint"""
        response = self.client.get("/api/v1/csrf-token")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_add_endpoint(self):
        """Test add numbers endpoint"""
        response = self.client.post("/api/v1/add?a=5&b=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], 8)

    def test_greet_endpoint_authenticated(self):
        """Test greet endpoint with authentication"""
        # Login required
        self.client.login(username="testuser", password="testpass123")

        # Test default greeting
        response = self.client.post("/api/v1/greet")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello, world!")

        # Test custom greeting
        response = self.client.post("/api/v1/greet?name=Alice")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello, Alice!")

    def test_stocks_endpoint(self):
        """Test stocks endpoint"""
        self.client.login(username="testuser", password="testpass123")

        # Test getting all stocks
        response = self.client.get("/api/v1/stocks")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

        # Test getting specific stock
        response = self.client.get("/api/v1/stocks?symbol=AAPL")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["symbol"], "AAPL")

    def test_sentry_debug_endpoint(self):
        """Test sentry debug endpoint raises exception"""
        self.client.login(username="testuser", password="testpass123")
        with self.assertRaises(Exception) as context:
            self.client.get("/api/v1/sentry-debug")
        self.assertEqual(str(context.exception), "This is a test exception for Sentry")
