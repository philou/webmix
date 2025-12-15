import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os
from webmix.main import aggregate_website

# Load scenarios
scenarios('../features/aggregation.feature')

@pytest.fixture
def context():
    return {}

@given(parsers.parse('the website "{website_name}" downloaded in local directory "{path}"'))
def website_downloaded(context, website_name, path):
    context['website_name'] = website_name
    context['base_dir'] = os.path.abspath(path)

@when('I aggregate the website content')
def aggregate_content(context):
    base_dir = context['base_dir']
    # We'll need to implement aggregate_website in webmix/main.py or similar
    context['output'] = aggregate_website(base_dir)

@then(parsers.parse('the output should start with "{text}"'))
def check_output_starts_with(context, text):
    assert context['output'].startswith(text)

@then(parsers.parse('the output should contain "{text}"'))
def check_output_contains(context, text):
    assert text in context['output']
