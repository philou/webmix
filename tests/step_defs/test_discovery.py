import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from webmix.fetcher import LocalFetcher
from webmix.discovery import discover_pages
from webmix.structure import generate_repomix_output
import os

# Load scenarios
scenarios('../features/discovery.feature')

@pytest.fixture
def context():
    return {}

@given(parsers.parse('a website at "{url}"'))
def website_url(context, url):
    context['start_url'] = url

@given(parsers.parse('the website is simulated using local data in "{path}"'))
def simulated_website(context, path):
    # Resolve absolute path relative to project root
    # Assuming tests are run from project root
    abs_path = os.path.abspath(path)
    context['fetcher'] = LocalFetcher(base_dir=abs_path)

@when('I discover the pages')
def discover(context):
    start_url = context['start_url']
    fetcher = context['fetcher']
    context['pages'] = discover_pages(start_url, fetcher)

@when('I generate the site structure')
def generate_structure(context):
    # Ensure pages are discovered first
    if 'pages' not in context:
        discover(context)
    
    context['output'] = generate_repomix_output(context['pages'])

@then(parsers.parse('I should find at least {count:d} pages'))
def check_page_count(context, count):
    assert len(context['pages']) >= count

@then(parsers.parse('the page "{url}" should be in the list'))
def check_page_exists(context, url):
    assert url in context['pages']

@then(parsers.parse('the output should contain "{text}"'))
def check_output_contains(context, text):
    assert text in context['output']
