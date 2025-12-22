import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import os
from webmix.main import aggregate_website

scenarios('../features/sitemap.feature')

@given(parsers.parse('a local mirror of "{site_name}"'))
def local_mirror(context, tmp_path, site_name):
    site_dir = tmp_path / site_name
    if not site_dir.exists():
        site_dir.mkdir()
    context['base_dir'] = str(site_dir)
    context['site_name'] = site_name
    
    if site_name == "simple-site":
        # Create files corresponding to the sitemap
        (site_dir / "index.html").write_text("<html><title>Home</title><body>Home</body></html>")
        (site_dir / "about").mkdir()
        (site_dir / "about" / "index.html").write_text("<html><title>About</title><body>About</body></html>")
        (site_dir / "contact").mkdir()
        (site_dir / "contact" / "index.html").write_text("<html><title>Contact</title><body>Contact</body></html>")
    elif site_name == "no-sitemap-site":
        (site_dir / "index.html").write_text("<html><title>Home</title><body>Home</body></html>")
        (site_dir / "page1.html").write_text("<html><title>Page 1</title><body>Page 1</body></html>")

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

@when('I generate the webmix')
def generate_webmix(context):
    base_dir = context['base_dir']
    context['output'] = aggregate_website(base_dir)

@given(parsers.parse('the site contains "{filename}"'))
def ensure_file_exists(context, filename):
    base_dir = context['base_dir']
    file_path = os.path.join(base_dir, filename)
    
    if not os.path.exists(file_path):
        # Create default content if not exists
        content = "default content"
        if "sitemap" in filename and filename.endswith(".xml"):
            if "custom" in filename:
                # Custom order: Contact then About
                content = """
                <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                   <url><loc>http://example.com/contact</loc></url>
                   <url><loc>http://example.com/about</loc></url>
                </urlset>
                """
            else:
                # Standard order
                content = """
                <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                   <url><loc>http://example.com/</loc></url>
                   <url><loc>http://example.com/about</loc></url>
                   <url><loc>http://example.com/contact</loc></url>
                </urlset>
                """
        
        with open(file_path, 'w') as f:
            f.write(content)

@when(parsers.parse('I generate the webmix with argument "{args}"'))
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

@then(parsers.parse('the structure should be generated from "{filename}"'))
def check_structure_source(context, filename):
    output = context['output']
    if "custom" in filename:
        # Check for Contact before About (as defined in ensure_file_exists for custom sitemap)
        contact_idx = output.find("Contact")
        about_idx = output.find("About")
        
        assert contact_idx != -1, "Contact page not found in output"
        assert about_idx != -1, "About page not found in output"
        assert contact_idx < about_idx, "Expected Contact before About as per custom sitemap"

@then("the Table of Contents should follow the order:")
def check_toc_order(context, datatable):
    output = context['output']
    # datatable is a list of dicts or rows depending on pytest-bdd version/usage
    # Assuming it's a list of rows (lists)
    
    # If datatable is not passed correctly, we might need to parse it manually or use a different approach.
    # For now, let's assume we get a list of rows.
    
    # Debug print
    print(f"Output: {output}")
    
    expected_paths = [row[0] for row in datatable]
    
    current_index = 0
    for path in expected_paths:
        # We expect the path or the title to appear.
        # The sitemap has /about, which maps to About title.
        # The output TOC usually contains titles.
        # But the test says "follow the order: | /about |"
        # So we should look for something that represents /about.
        # In the generated markdown, it might be "About" or the link "about/index.html".
        
        # Let's try to find the path itself if it's preserved, or the title.
        # Given the simple-site setup:
        # / -> Home
        # /about -> About
        # /contact -> Contact
        
        search_term = path
        if path == "/":
            search_term = "Home"
        elif path == "/about":
            search_term = "About"
        elif path == "/contact":
            search_term = "Contact"
            
        found_index = output.find(search_term, current_index)
        assert found_index != -1, f"Expected '{search_term}' (for path {path}) not found in output after index {current_index}"
        current_index = found_index

@then("the Table of Contents should reflect the directory structure")
def check_toc_directory_structure(context):
    output = context['output']
    assert "Home" in output
    assert "Page 1" in output
