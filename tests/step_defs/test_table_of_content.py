
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os

scenarios('../features/table_of_content.feature')

@then("the output should match the table of content:")
def check_output_multiline(context, docstring):
    text = docstring
    assert context.get('output') is not None
    # Normalize line endings and whitespace for comparison
    expected_lines = [line.strip() for line in text.strip().split('\n')]
    output_lines = [line.strip() for line in context['output'].strip().split('\n')]
    
    # Check if expected lines appear in output in order
    current_idx = 0
    found = True
    for expected in expected_lines:
        try:
            # Find next occurrence
            current_idx = output_lines.index(expected, current_idx) + 1
        except ValueError:
            found = False
            break
            
    if not found:
        print("\n--- EXPECTED STRUCTURE ---")
        print(text)
        print("\n--- ACTUAL OUTPUT ---")
        print(context['output'])
        raise AssertionError("Expected structure not found in output")
