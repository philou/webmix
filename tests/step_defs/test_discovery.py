import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os
import re

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

@then(parsers.parse('I should find at least {count:d} files'))
def check_file_count(context, count):
    output = context['output']
    match = re.search(r"This file contains the content of (\d+) pages", output)
    assert match, "Could not find file count in output summary"
    found_count = int(match.group(1))
    assert found_count >= count

@then(parsers.parse('the file "{path}" should be in the list'))
def check_file_exists(context, path):
    # The path should appear in the directory structure or file headers
    assert path in context['output']


