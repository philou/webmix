import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os

# Load scenarios
scenarios('../features/aggregation.feature')

@then(parsers.parse('the output should start with "{text}"'))
def check_output_starts_with(context, text):
    assert context['output'].startswith(text)


