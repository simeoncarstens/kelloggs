import unittest

loader = unittest.TestLoader()
tests = loader.discover('.', pattern='*.py')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
