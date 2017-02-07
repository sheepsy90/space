import re

from django.test import TestCase
from django.test.client import Client

import test.tests.unit.TestSetups as _setup

def content_has_id(content, id):
    return 'id="%s"' % id in content

class IntegrationTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index_page(self):
        # Issue a GET request.
        response = self.client.get('/index/')
        
        # Assert the correct Template is delivered
        self.assertEqual("index.html", response.templates[0].name)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Assert That the Login box is present
        self.assertTrue(content_has_id(response.content, "login_box"))
        
    def test_registration_page(self):
        # Setup the Basic Setups
        _setup.setup_basic_backpack_and_farm_and_forest_location_and_four_basic_fruits()
        _setup.setup_ship_status_history()
            
        # Issue a GET request.
        response = self.client.get('/view_registration_page/')
        
        # Assert the correct Template is delivered
        self.assertEqual("registration.html", response.templates[0].name)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Assert That the Login box is present
        self.assertTrue(content_has_id(response.content, "registration_box"))
        


        # Set the post request for registration
        registration_response = self.client.post('/ajax/send_registration/', {'user': 'testuser', 'password_first': 'qwer2345', 'password_again': 'qwer2345'})
        
        # Assert that the status code is a redirect
        self.assertEquals(302, registration_response.status_code)
        
        # Assert that the Location of Redirection is correct
        redirect_url = self.get_redirect_url(registration_response)
        self.assertEquals("http://testserver/backpackpage", redirect_url)
        
        # Get that page
        response = self.client.get(redirect_url)
        
        # Assert it has the Welcome Dialog       
        content_has_id(response, "welcomedialog")
        content_has_id(response, "backpack")
        content_has_id(response, "container_fuse")
        
    def get_redirect_url(self, response):
        """ Parses 302 response object.
            Returns redirect url, parsed by regex. """
        self.assertEqual(response.status_code, 302)
        return re.search("(?P<url>https?://[^\s]+)", str(response)).group("url")
