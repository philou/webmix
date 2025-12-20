import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os
from webmix.main import aggregate_website

# Load scenarios
scenarios('../features/linking.feature')

@when('I aggregate the website content')
def aggregate_content(context):
    base_dir = context['base_dir']
    context['output'] = aggregate_website(base_dir)

