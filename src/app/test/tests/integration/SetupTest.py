from django.test import TestCase


class SetupTest(TestCase):


    def test_db_setup(self):
        # Issue a GET request.
        from manage import perform_basic_setup
        perform_basic_setup()


