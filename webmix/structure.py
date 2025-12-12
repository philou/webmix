from typing import List
from urllib.parse import urlparse

def generate_file_summary(pages: List[str]) -> str:
    return f"""# File Summary

This file contains the content of {len(pages)} pages from the website.
"""

def generate_directory_structure(pages: List[str]) -> str:
    # Simple tree view simulation
    # For now, just list the paths relative to the domain
    structure = "# Directory Structure\n\n"
    
    # Group by domain (though we expect single domain)
    paths = []
    for url in pages:
        parsed = urlparse(url)
        path = parsed.path
        if not path or path == '/':
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        paths.append(path)
    
    paths.sort()
    
    for path in paths:
        structure += f"- {path}\n"
        
    return structure

def generate_repomix_output(pages: List[str]) -> str:
    summary = generate_file_summary(pages)
    structure = generate_directory_structure(pages)
    
    return f"{summary}\n{structure}\n"
