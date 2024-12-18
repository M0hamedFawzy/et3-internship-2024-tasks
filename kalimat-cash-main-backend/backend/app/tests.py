import datetime

from django.test import TestCase
from django.utils import timezone


class DummyTest(TestCase):
    def test_dummy_case(self):

        self.assertIs(True, True)