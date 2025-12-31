import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os

# Load scenarios
scenarios('../features/linking.feature')


