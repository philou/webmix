import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from webmix.discovery import discover_files
from webmix.structure import generate_repomix_output
import os

# Load scenarios
scenarios('../features/discovery.feature')

@pytest.fixture
def context():
    return {}

@given(parsers.parse('a local directory "{path}"'))
def local_directory(context, path):
    # Resolve absolute path relative to project root
    context['base_dir'] = os.path.abspath(path)

@when('I discover the files')
def discover(context):
    base_dir = context['base_dir']
    context['files'] = discover_files(base_dir)

@when('I generate the site structure')
def generate_structure(context):
    # Ensure files are discovered first
    if 'files' not in context:
        discover(context)
    
    context['output'] = generate_repomix_output(context['files'])

@then(parsers.parse('I should find at least {count:d} files'))
def check_file_count(context, count):
    assert len(context['files']) >= count

@then(parsers.parse('the file "{path}" should be in the list'))
def check_file_exists(context, path):
    assert path in context['files']

@then(parsers.parse('the output should contain "{text}"'))
def check_output_contains(context, text):
    assert text in context['output']
