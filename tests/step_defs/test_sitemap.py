import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os
from webmix.main import aggregate_website

scenarios('../features/sitemap.feature')

@when(parsers.parse('I aggregate the website content with argument "{args}"'))
def generate_webmix_with_args(context, args):
    base_dir = context['base_dir']
    import shlex
    arg_list = shlex.split(args)
    
    sitemap_arg = None
    if "--sitemap" in arg_list:
        idx = arg_list.index("--sitemap")
        if idx + 1 < len(arg_list):
            sitemap_arg = arg_list[idx+1]
            
    context['output'] = aggregate_website(base_dir, sitemap_path=sitemap_arg)

@then("the Table of Contents should follow the order:")
def check_toc_order(context, datatable):
    output = context['output']
    # datatable is a list of dicts or rows depending on pytest-bdd version/usage
    # Assuming it's a list of rows (lists)
    
    # Debug print
    print(f"Output: {output}")
    
    expected_items = [row[0] for row in datatable]
    
    current_index = 0
    for item in expected_items:
        found_index = output.find(item, current_index)
        assert found_index != -1, f"Expected '{item}' not found in output after index {current_index}"
        current_index = found_index

