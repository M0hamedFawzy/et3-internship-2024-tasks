from django.test import SimpleTestCase
from django.urls import resolve, reverse
from homePage.views import sign_in, register, logout_user, home_page

#
# class TestUrls(SimpleTestCase):
#
#     def test_home_pg_url(self):
#         url = reverse('home_pg')
#         self.assertEqual(resolve(url).func, home_page)
#
#     def test_home_pg_url_register(self):
#         url = reverse('register')
#         self.assertEqual(resolve(url).func, register)
#
#     def test_home_pg_url_sign_in(self):
#         url = reverse('sign_in')
#         self.assertEqual(resolve(url).func, sign_in)
#
#     def test_home_pg_url_logout(self):
#         url = reverse('logout')
#         self.assertEqual(resolve(url).func, logout_user)
