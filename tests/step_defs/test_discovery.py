import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os
import re

# Load scenarios
scenarios('../features/discovery.feature')

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


