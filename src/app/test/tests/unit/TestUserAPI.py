import unittest
import time

from django.test import TestCase

# Custom Imports

import test.tests.unit.TestSetups as _setup
from core.models import UserLocations

import lib.api.user.userAPI as _userAPI

class TestUserAPI(TestCase):      

    def test_basic_user_creation(self):
        """ This method creates a basic user and checks if he is correctly created """
        # Basic Setup of Model Data
        _setup.setup_basic_location()
        # The User API Call
        user = _userAPI.create_new_user_return_object(username="JonDoe" + str(time.time()), password="qwer1234", email=str(time.time()) + "testuser@lootgame.de")
        # Assert that the User is not none
        self.assertNotEquals(None, user)
        # Check the location
        loc = UserLocations.objects.get(user=user)
        self.assertEquals("Farm", loc.current.name)
        
    def test_basic_user_creation_double_email(self):
        """ This method creates a basic user and checks if he is correctly created """
        # Basic Setup of Model Data
        _setup.setup_basic_location()
        same_email = str(time.time()) + "testuser@lootgame.de"
        # The User API Call
        user = _userAPI.create_new_user_return_object(username="JonDoe" + str(time.time()), password="qwer1234", email=same_email)
        # Assert that the User is not none
        self.assertNotEquals(None, user)
        # Second API Call
        with self.assertRaises(Exception) as exp:
            user = _userAPI.create_new_user_return_object(username="JonDoe" + str(time.time()), password="qwer1234", email=same_email)
        self.assertEquals("UserAPI", exp.exception[0])
        self.assertEquals("Multiple Email!", exp.exception[1])
                
    @unittest.expectedFailure
    def test_basic_user_creation_double_username(self):
        """ This method creates a basic user and checks if he is correctly created """
        # Basic Setup of Model Data
        _setup.setup_basic_location()
        same_name = "JonDoe" + str(time.time())
        # The User API Call
        user = _userAPI.create_new_user_return_object(username=same_name, password="qwer1234", email=str(time.time()) + "testuser@lootgame.de")
        # Assert that the User is not none
        self.assertNotEquals(None, user)
        # Second API Call
        user = _userAPI.create_new_user_return_object(username=same_name, password="qwer1234", email=str(time.time()) + "testuser@lootgame.de")
