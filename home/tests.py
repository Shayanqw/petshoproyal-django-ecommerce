from django.test import TestCase
from django.urls import reverse


class BasicSmokeTests(TestCase):
    def test_homepage_returns_200(self):
        resp = self.client.get(reverse("home:home"))
        self.assertEqual(resp.status_code, 200)

    def test_product_list_returns_200(self):
        resp = self.client.get(reverse("home:product"))
        self.assertEqual(resp.status_code, 200)

    def test_sitemap_returns_200(self):
        resp = self.client.get("/sitemaps.xml")
        self.assertEqual(resp.status_code, 200)
