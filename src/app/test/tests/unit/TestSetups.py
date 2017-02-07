"""
This module is used to setup data used in the test scenarios - mainly for data that is used often 
"""
from core.content import Planets


def setup_basic_location():
    Planets(name="Planet A", description="Planet A - ").save()
    Planets(name="Planet B", description="Planet B - ").save()
