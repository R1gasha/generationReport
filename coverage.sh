coverage run -m pytest src/tests/tests.py -v
coverage html
open htmlcov/index.html