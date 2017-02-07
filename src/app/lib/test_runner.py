
from django.test.simple import DjangoTestSuiteRunner
from django.utils import unittest
from django.utils.importlib import import_module


class MyTestSuiteRunner(DjangoTestSuiteRunner):

    def build_suite(self, test_labels, extra_tests=None, *args, **kwargs):
        if test_labels:
            extra_test_modules = [label.lstrip('module:')
                                  for label in test_labels
                                  if label.startswith('module:')]
            extra_tests = extra_tests or []
            for module_path in extra_test_modules:
                # Better way to load the tests here would probably be to use
                # `django.test.siple.build_suite` as it does some extra stuff like looking for doctests.
                extra_tests += unittest.defaultTestLoader.loadTestsFromModule(import_module(module_path))

            # Remove the 'module:*' labels
            test_labels = [label for label in test_labels if not label.startswith('module:')]

        # Let Django do the rest
        return super(MyTestSuiteRunner, self).build_suite(test_labels, extra_tests, *args, **kwargs)