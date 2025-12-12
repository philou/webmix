import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from webmix.extraction import extract_content
import os

# Load scenarios
scenarios('../features/extraction.feature')

@pytest.fixture
def context():
    return {}

# Reuse steps from test_discovery.py if possible, but for now redefine or import
# To avoid duplication, we could move common steps to a conftest.py or shared module.
# For simplicity in this step, I'll redefine the necessary ones.

@given(parsers.parse('the website "{website_name}" downloaded in local directory "{path}"'))
def website_downloaded(context, website_name, path):
    context['website_name'] = website_name
    context['base_dir'] = os.path.abspath(path)

@given(parsers.parse('the file "{filename}" contains "{content}"'))
def file_contains_content(context, filename, content):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    if not os.path.exists(file_path):
        raise AssertionError(f"Input file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = f.read()
        
    assert content in file_content, f"File {filename} does not contain expected content: {content}"

@when(parsers.parse('I extract the content from "{filename}"'))
def extract_file_content(context, filename):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    context['output'] = extract_content(file_path)

@then(parsers.parse('the output should contain "{text}"'))
def check_output_contains(context, text):
    assert context['output'] is not None
    assert text in context['output']

@then(parsers.parse('the output should not contain "{text}"'))
def check_output_not_contains(context, text):
    assert context['output'] is not None
    assert text not in context['output']
