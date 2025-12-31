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
        
        context['path_title_map'] = {
            "/": "Home",
            "/about": "About",
            "/contact": "Contact"
        }
    elif site_name == "no-sitemap-site":
        (site_dir / "index.html").write_text("<html><title>Home</title><body>Home</body></html>")
        (site_dir / "page1.html").write_text("<html><title>Page 1</title><body>Page 1</body></html>")

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
    
    expected_paths = [row[0] for row in datatable]
    path_map = context.get('path_title_map', {})
    
    current_index = 0
    for path in expected_paths:
        # Look up the title from the map, or use the path itself if not found
        search_term = path_map.get(path, path)
            
        found_index = output.find(search_term, current_index)
        assert found_index != -1, f"Expected '{search_term}' (for path {path}) not found in output after index {current_index}"
        current_index = found_index

@then("the Table of Contents should reflect the directory structure")
def check_toc_directory_structure(context):
    output = context['output']
    assert "Home" in output
    assert "Page 1" in output
