import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from webmix.discovery import discover_files
from webmix.structure import generate_webmix_output
import os

# Load scenarios
scenarios('../features/discovery.feature')

@given(parsers.parse('the website contains an "{filename}" file'))
def website_contains_file(context, filename):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    if not os.path.exists(file_path):
        raise AssertionError(f"Input file not found: {file_path}")

@given(parsers.parse('the website contains at least {count:d} files'))
def website_contains_files(context, count):
    base_dir = context['base_dir']
    found = 0
    for _, _, files in os.walk(base_dir):
        found += len(files)
    
    if found < count:
        raise AssertionError(f"Input directory has fewer files than expected: found {found}, expected >= {count}")

@when('I aggregate the website content')
def discover(context):
    base_dir = context['base_dir']
    context['files'] = discover_files(base_dir)
    # Also generate output for the second scenario
    context['output'] = generate_webmix_output(context['files'])

@then(parsers.parse('I should find at least {count:d} files'))
def check_file_count(context, count):
    assert len(context['files']) >= count

@then(parsers.parse('the file "{path}" should be in the list'))
def check_file_exists(context, path):
    assert path in context['files']

