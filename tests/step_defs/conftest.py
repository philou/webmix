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
        
        content = data.get('content')
        if not content:
            # If 'content' column is missing or empty, check for 'body'
            body = data.get('body')
            
            # Check for title and link columns
            title = data.get('title')
            link_spec = data.get('link')
            
            if body:
                content = f"<html><body>{body}</body></html>"
            else:
                # Generate dummy content
                html_parts = ["<html><head>"]
                if title:
                    html_parts.append(f"<title>{title}</title>")
                html_parts.append("</head><body>")
                
                if title:
                    html_parts.append(f"<h1>{title}</h1>")
                
                # Add enough content for trafilatura to recognize it
                html_parts.append("<p>This is some dummy content that is long enough to be considered as main content by the extraction engine. " * 5 + "</p>")
                
                if link_spec:
                    # Parse link spec: "[link text](target.html)" or just "target.html"
                    import re
                    match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', link_spec)
                    if match:
                        text, href = match.groups()
                    else:
                        href = link_spec
                        text = "link"
                    html_parts.append(f'<p>Here is a <a href="{href}">{text}</a>.</p>')
                
                html_parts.append("</body></html>")
                content = "".join(html_parts)
        
        if path:
            file_path = site_dir / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

@given("a standard sitemap")
def standard_sitemap(context):
    base_dir = context['base_dir']
    # Walk the directory to find all HTML files
    urls = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                # Convert file path to URL path (simplified)
                url_path = rel_path.replace(os.sep, "/")
                # In a real sitemap, we might want full URLs, but for this test, 
                # we just need to match what the code expects or just valid XML.
                # The existing test used http://example.com/
                if url_path == "index.html":
                    url = "http://example.com/"
                elif url_path.endswith("/index.html"):
                    url = f"http://example.com/{url_path[:-11]}" # remove /index.html
                else:
                    url = f"http://example.com/{url_path}"
                urls.append(url)
    
    # Generate XML
    sitemap_content = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sorted(urls):
        sitemap_content += f'   <url><loc>{url}</loc></url>\n'
    sitemap_content += '</urlset>'
    
    with open(os.path.join(base_dir, "sitemap.xml"), "w") as f:
        f.write(sitemap_content)

@when('I aggregate the website content')
def aggregate_content(context):
    base_dir = context['base_dir']
    context['output'] = aggregate_website(base_dir)

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

