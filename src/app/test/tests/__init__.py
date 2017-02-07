import unittest


def suite():
    return unittest.TestLoader().discover("test.tests", pattern="*.py")