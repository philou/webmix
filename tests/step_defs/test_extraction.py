import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from webmix.extraction import extract_content
import os

# Load scenarios
scenarios('../features/extraction.feature')

@when(parsers.parse('I extract the content from "{filename}"'))
def extract_file_content(context, filename):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    context['output'] = extract_content(file_path)

@then(parsers.parse('the output should not contain "{text}"'))
def check_output_not_contains(context, text):
    assert context['output'] is not None
    assert text not in context['output']

