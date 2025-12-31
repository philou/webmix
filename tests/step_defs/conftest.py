import pytest
from pytest_bdd import given, when, then, parsers
import os
from webmix.main import aggregate_website

@pytest.fixture
def context():
    return {}

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

@then(parsers.parse('the output should contain "{text}"'))
def check_output_contains(context, text):
    assert context.get('output') is not None
    assert text in context['output']

@when('I aggregate the website content')
def aggregate_content(context):
    base_dir = context['base_dir']
    context['output'] = aggregate_website(base_dir)

