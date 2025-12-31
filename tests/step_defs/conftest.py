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

@given(parsers.parse('the site contains a "{filename}" with:'))
def create_file_with_content(context, filename, docstring):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(docstring)

@given(parsers.parse('the site does not contain "{filename}"'))
def ensure_file_not_exists(context, filename):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

@given("a site with pages:")
def site_with_pages(context, tmp_path, datatable):
    site_dir = tmp_path / "site"
    if not site_dir.exists():
        site_dir.mkdir()
    context['base_dir'] = str(site_dir)
    
    # datatable is a list of rows, where the first row is the header
    headers = datatable[0]
    rows = datatable[1:]
    
    for row in rows:
        data = dict(zip(headers, row))
        path = data.get('path') or data.get('url')
        content = data.get('content') or "<html><body>Default Content</body></html>"
        
        if path:
            file_path = site_dir / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

@when('I aggregate the website content')
def aggregate_content(context):
    base_dir = context['base_dir']
    context['output'] = aggregate_website(base_dir)

